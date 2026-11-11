#!/usr/bin/env python3
"""固定入力から試験を準備し、保存・復元照合・後片付けまで完了させる。"""
from __future__ import annotations

import argparse
from contextlib import contextmanager, ExitStack
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import shutil
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from layer2.extensions.long_run_storage.batch_archive import archive_homes, tree_snapshot, require_usage
from layer2.extensions.long_run_storage.minimal_archive import archive_minimal, read_manifest, open_archive
from layer2.extensions.long_run_storage.long_run_storage import capacity_guard, LongRunStorageError


class TrialError(Exception):
    pass


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_once(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, mode="w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
        os.link(stream.name, path)



def call(script, *arguments):
    result = subprocess.run(
        [sys.executable, str(ROOT / script), *map(str, arguments)],
        capture_output=True, text=True, cwd=ROOT,
        env={**os.environ, "THE_CAPTION_EVAL_COPY_MODE": "clonefile"},
    )
    if result.returncode:
        raise TrialError(f"{script}: {result.stderr or result.stdout}")
    return json.loads(result.stdout)


@contextmanager
def locked(trial):
    trial = Path(trial).absolute()
    if trial.resolve() != trial or trial.is_relative_to(ROOT):
        raise TrialError("試験はリポジトリ外の、リンクを経由しない場所へ置いてください")
    trial.mkdir(parents=True, exist_ok=True)
    with (trial / ".lock").open("a+") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise TrialError("同じ試験の処理が実行中です") from exc
        yield trial


def snapshot(path):
    path = Path(path)
    return tree_snapshot(path, exclude_compact=False) if path.exists() else {}


def check_protected(config):
    for item in config["protected"]:
        current = snapshot(item["path"])
        expected = item["entries"]
        if item["append_only"]:
            for name, original in expected.items():
                actual = current.get(name)
                if actual is None:
                    raise TrialError(f"保護対象が削除されました: {item['path']}/{name}")
                original, actual = dict(original), dict(actual)
                # 登録の追記による親ディレクトリの時刻変化だけを許す。
                if original.get("type") == stat.S_IFDIR:
                    original.pop("mtime_ns", None)
                    actual.pop("mtime_ns", None)
                if original != actual:
                    raise TrialError(f"保護対象が変更されました: {item['path']}/{name}")
        elif expected != current:
            raise TrialError(f"保護対象が変更されました: {item['path']}")
    for path, digest in config["inputs"].items():
        if sha(path) != digest:
            raise TrialError(f"固定入力が変更されました: {path}")


def initialize(trial, args):
    required = ("profile", "store", "registry", "price_table", "resource_class", "archive_store", "archive_root")
    if any(not getattr(args, name, None) for name in required) or not args.template:
        raise TrialError("最初のprepareにはprofile、store、registry、price-table、resource-class、template、archive-store、archive-rootが必要です")
    paths = {name: str(Path(getattr(args, name)).resolve()) for name in required}
    templates = [str(Path(p).resolve()) for p in args.template]
    if Path(paths["archive_root"]).exists() and any(Path(paths["archive_root"]).iterdir()):
        raise TrialError("archive-rootにはこの試験専用の空の保存先を指定してください")
    profile = load(paths["profile"])
    if profile["execution"]["max_workers"] != 24 or profile["comparison_conditions"]["executor_parameters"]["max_workers"] != 24:
        raise TrialError("標準実行の並列上限は24です")
    if profile["iterations"] != profile["comparison_conditions"]["repetition_condition"]["iterations"]:
        raise TrialError("反復数が一致しません")
    protected = {paths["store"]}
    protected.update(str(Path(p).resolve()) for p in (args.protect or []))
    homes = [str(Path(p).absolute()) for p in (args.homes or [])]
    for p in homes:
        if (not Path(p).is_relative_to(trial) or Path(p).resolve() != Path(p)
                or Path(p).name != "codex-homes"
                or any(Path(p).is_relative_to(trial / name) for name in ("rounds", "inputs", "receipts"))):
            raise TrialError("実行別ホームは試験内のcodex-homesへ置いてください")
    for p in templates:
        for link in load(p).get("parameters", {}).get("runtime_links", []):
            protected.add(str(Path(link["source"]).resolve()))
    for name in ("archive_store", "archive_root", "registry", "store"):
        path = Path(paths[name])
        if path.is_relative_to(trial) or trial.is_relative_to(path):
            raise TrialError(f"{name}と試験ディレクトリを分離してください")
    destinations = [Path(paths[k]) for k in ("archive_store", "archive_root", "registry")]
    if any(a.is_relative_to(b) or b.is_relative_to(a) for i, a in enumerate(destinations) for b in destinations[i + 1:]):
        raise TrialError("保存先・共有保管場所・registryを分離してください")
    for p in protected:
        if not Path(p).is_dir():
            raise TrialError(f"保護対象がありません: {p}")
        if any(d.is_relative_to(p) or Path(p).is_relative_to(d) for d in [trial, *destinations]):
            raise TrialError("保存先・作業領域と保護対象が重なっています")
    inputs = {p: sha(p) for p in [paths["profile"], paths["price_table"], paths["resource_class"], *templates]}
    frozen = trial / "inputs"
    frozen.mkdir(parents=True, exist_ok=True)
    for name in ("profile", "price_table", "resource_class"):
        destination = frozen / f"{name}.json"
        source = Path(paths[name]).read_bytes()
        if destination.exists() and destination.read_bytes() != source:
            raise TrialError("準備を再開する固定入力が一致しません")
        if not destination.exists():
            destination.write_bytes(source)
        inputs[str(frozen / f"{name}.json")] = sha(frozen / f"{name}.json")
    config = {"schema_version": "the-caption-prompt.evaluation-trial/v1", **paths,
              "templates": templates, "homes": homes, "inputs": inputs,
              "protected": [{"path": p, "append_only": False, "entries": snapshot(p)} for p in sorted(protected)],
              "iterations": profile["iterations"]}
    for name in ("registry", "archive_store"):
        config["protected"].append({"path": paths[name], "append_only": True, "entries": snapshot(paths[name])})
    write_once(trial / "trial.json", config)
    return config


def rounds(trial):
    return sorted((trial / "rounds").glob("[0-9][0-9][0-9][0-9]"))


def remaining(config, pool_key):
    with tempfile.TemporaryDirectory(prefix="trial-missing-") as tmp:
        return call("scripts/atomic_run_registry.py", "plan-missing", "--registry", config["registry"],
                    "--pool-key", pool_key, "--desired-count", config["iterations"], "--output", Path(tmp) / "missing.json")


def pool_for(config, cycle, profile):
    with tempfile.TemporaryDirectory(prefix="trial-pool-") as tmp:
        fresh = call("scripts/atomic_run_registry.py", "create-pool", "--registry", tmp,
                     "--profile", profile, "--cycle", cycle, "--compatibility-rule", "effective-v1")
        document = load(Path(tmp) / "pools" / f"{fresh['pool_key']}.json")
    existing = Path(config["registry"]) / "pools" / f"{fresh['pool_key']}.json"
    if existing.exists():
        ignored = {"created_at", "created_from_profile_sha256", "pool_content_sha256"}
        if {k: v for k, v in document.items() if k not in ignored} != {k: v for k, v in load(existing).items() if k not in ignored}:
            raise TrialError("保存済みpoolと固定条件が一致しません")
        return fresh["pool_key"]
    return call("scripts/atomic_run_registry.py", "create-pool", "--registry", config["registry"],
                "--profile", profile, "--cycle", cycle, "--compatibility-rule", "effective-v1")["pool_key"]


def prepare(trial, args):
    config = load(trial / "trial.json") if (trial / "trial.json").exists() else initialize(trial, args)
    check_protected(config)
    existing = rounds(trial)
    if (trial / "complete.json").exists():
        raise TrialError("この試験は保存・後片付けまで完了しています")
    if existing and not (trial / "receipts" / f"{existing[-1].name}-saved.json").exists():
        last = existing[-1]
        if (trial / "receipts" / f"{last.name}-prepared.json").exists():
            raise TrialError("前回の採点・登録・保存をfinishで終えてから不足分を準備してください")
        # 発行許可前に失敗した準備だけを作り直す。証拠があれば自動削除しない。
        ensure_quiet(trial)
        if (last / "cycle/layer2").exists() or (last / "runner.log").exists():
            raise TrialError("準備未完了の領域に実行証拠があります")
        shutil.rmtree(last)
        existing = existing[:-1]
    if not capacity_guard(trial, trial / "capacity.jsonl")["dispatch_allowed"]:
        raise TrialError("試験準備の空き容量が不足しています")
    directory = trial / "rounds" / f"{len(existing) + 1:04d}"
    directory.mkdir(parents=True)
    cycle = directory / "cycle"
    profile = trial / "inputs/profile.json"
    call("scripts/evaluation_loop.py", "install-layer1", "--store", config["store"], "--profile", profile, "--cycle", cycle)
    pool_key = pool_for(config, cycle, profile)
    dispatch = call("scripts/atomic_run_registry.py", "plan-missing", "--registry", config["registry"],
                    "--pool-key", pool_key, "--desired-count", config["iterations"], "--output", directory / "dispatch.json")
    receipt = {"round": directory.name, "pool_key": pool_key, "missing_slot_count": dispatch["missing_slot_count"]}
    if dispatch["missing_slot_count"]:
        argv = []
        for template in config["templates"]:
            argv += ["--template", template]
        p = load(profile)
        plan = call("layer2/extensions/parallel_execution/prepare_atomic_plan.py", *argv,
                    "--dispatch-plan", directory / "dispatch.json", "--registry", config["registry"],
                    "--cycle", cycle, "--evaluation-loop", ROOT / "scripts/evaluation_loop.py",
                    "--duration-hints", profile, "--resource-class", trial / "inputs/resource_class.json",
                    "--output", directory / "plan", "--max-workers", 24,
                    "--max-attempts", p["execution"].get("max_attempts", 3),
                    "--monitor-interval-seconds", p["execution"].get("monitor_interval_seconds", 5))
        preflight = call("scripts/evaluation_loop.py", "preflight-execution", "--cycle", cycle,
                         "--profile", profile, "--global-plan", plan["plan"])
        receipt.update(plan=plan["plan"], plan_sha256=sha(plan["plan"]), authorized_slot_count=preflight["authorized_slot_count"])
    receipt["layer1_snapshot"] = snapshot(cycle / "layer1")
    write_once(trial / "receipts" / f"{directory.name}-prepared.json", receipt)
    check_protected(config)
    return {"status": "prepared", "round": directory.name, "missing_slots": dispatch["missing_slot_count"]}


def latest(trial):
    directories = rounds(trial)
    if not directories:
        raise TrialError("prepareが完了していません")
    directory = directories[-1]
    return directory, load(trial / "receipts" / f"{directory.name}-prepared.json")


def run(trial):
    config = load(trial / "trial.json")
    check_protected(config)
    directory, prepared = latest(trial)
    receipt = trial / "receipts" / f"{directory.name}-executed.json"
    if receipt.exists():
        raise TrialError("発行済みです。採点後にfinishし、不足分だけprepareしてください")
    if snapshot(directory / "cycle/layer1") != prepared["layer1_snapshot"]:
        raise TrialError("複製したLayer 1が変更されています")
    if not capacity_guard(trial, trial / "capacity.jsonl")["dispatch_allowed"]:
        raise TrialError("発行前の空き容量が不足しています")
    code = 0
    if prepared["missing_slot_count"]:
        if sha(prepared["plan"]) != prepared["plan_sha256"]:
            raise TrialError("発行計画が変更されています")
        call("scripts/evaluation_loop.py", "verify-execution-preflight", "--cycle", directory / "cycle")
        command = [sys.executable, str(ROOT / "layer2/extensions/parallel_execution/campaign_runner.py"),
                   "--plan", prepared["plan"], "--runner-output", str(directory / "parallel-run"),
                   "--campaign-output", str(directory / "campaign"), "--max-workers", "24"]
        with (directory / "runner.log").open("x") as log:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True, env={**os.environ, "THE_CAPTION_EVAL_COPY_MODE": "clonefile"})
            try:
                code = process.wait()
            except KeyboardInterrupt:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                code = 130
    write_once(receipt, {"return_code": code, "status": "executed" if code == 0 else "interrupted"})
    check_protected(config)
    return {"status": "awaiting_ratings", "runner_return_code": code, "cycle": str(directory / "cycle")}


def run_group(trials):
    """事前照合済みの試験を一つの待ち行列へ入れ、合計24件以内で実行する。"""
    if len(trials) < 2 or len(set(trials)) != len(trials):
        raise TrialError("異なる試験を二つ以上指定してください")
    entries = []
    for trial in trials:
        config = load(trial / "trial.json")
        check_protected(config)
        directory, prepared = latest(trial)
        receipt = trial / "receipts" / f"{directory.name}-executed.json"
        if receipt.exists():
            raise TrialError("発行済みの試験が含まれています")
        if snapshot(directory / "cycle/layer1") != prepared["layer1_snapshot"]:
            raise TrialError("複製したLayer 1が変更されています")
        if not capacity_guard(trial, trial / "capacity.jsonl")["dispatch_allowed"]:
            raise TrialError("発行前の空き容量が不足しています")
        if prepared["missing_slot_count"]:
            if sha(prepared["plan"]) != prepared["plan_sha256"]:
                raise TrialError("発行計画が変更されています")
            call("scripts/evaluation_loop.py", "verify-execution-preflight", "--cycle", directory / "cycle")
        entries.append((trial, config, directory, prepared, receipt))
    if not any(entry[3]["missing_slot_count"] for entry in entries):
        for _, config, _, _, receipt in entries:
            write_once(receipt, {"return_code": 0, "status": "executed", "campaign": None})
            check_protected(config)
        return {"status": "awaiting_ratings", "runner_return_code": 0,
                "cycles": [str(entry[2] / "cycle") for entry in entries]}
    first = entries[0][2]
    command = [sys.executable, str(ROOT / "layer2/extensions/parallel_execution/campaign_runner.py")]
    for _, _, directory, prepared, _ in entries:
        if prepared["missing_slot_count"]:
            command += ["--plan", prepared["plan"], "--runner-output", str(directory / "parallel-run")]
    command += ["--campaign-output", str(first / "campaign"), "--max-workers", "24"]
    with (first / "runner.log").open("x") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True, env={**os.environ, "THE_CAPTION_EVAL_COPY_MODE": "clonefile"})
        try:
            code = process.wait()
        except KeyboardInterrupt:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 130
    for trial, config, directory, _, receipt in entries:
        write_once(receipt, {"return_code": code, "status": "executed" if code == 0 else "interrupted",
                             "campaign": str(first / "campaign")})
        check_protected(config)
    return {"status": "awaiting_ratings", "runner_return_code": code,
            "cycles": [str(entry[2] / "cycle") for entry in entries]}


def ensure_quiet(trial):
    processes = {}
    for line in subprocess.check_output(["ps", "-axo", "pid=,ppid=,args="], text=True).splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) == 3:
            processes[int(parts[0])] = (int(parts[1]), parts[2])
    ancestors = {os.getpid()}
    pid = os.getpid()
    while pid in processes and processes[pid][0] not in ancestors:
        pid = processes[pid][0]
        ancestors.add(pid)
    for pid, (_, command) in processes.items():
        if pid not in ancestors and str(trial) in command:
            raise TrialError("試験ディレクトリを使うプロセスが残っています")


def save_round(trial, config, directory, complete):
    saved = trial / "receipts" / f"{directory.name}-saved.json"
    archive = Path(config["archive_root"]) / directory.name
    if saved.exists():
        record = load(saved)
        manifest = read_manifest(archive)
        verification = load(archive / "verification.json")
        prune = load(archive / "prune-receipt.json")
        if (record["manifest"] != manifest["content_sha256"]
                or verification.get("manifest") != record["manifest"]
                or prune.get("manifest") != record["manifest"]
                or verification.get("status") != "verified" or prune.get("status") != "complete"
                or any((directory / p).exists() for p in manifest["workspaces"])):
            raise TrialError("保存・復元照合・削除の完了記録が一致しません")
        with open_archive(archive, Path(config["archive_store"]), archive.parent):
            pass
        return record
    cycle = directory / "cycle"
    prepared = load(trial / "receipts" / f"{directory.name}-prepared.json")
    if snapshot(cycle / "layer1") != prepared["layer1_snapshot"]:
        raise TrialError("固定済みLayer 1が変化しています")
    check_protected(config)
    # 復元後にも準備条件・選択・集計を追跡できるよう、回の保存単位へ含める。
    records = {"trial.json": trial / "trial.json"}
    records.update({f"inputs/{p.name}": p for p in (trial / "inputs").glob("*.json")})
    for index, path in enumerate(config["templates"]):
        records[f"templates/{index:04d}.json"] = Path(path)
    if complete:
        records.update({name: trial / name for name in ("selection.json", "analysis.json")})
    if not (archive / "manifest.json.zst").exists():
        for name, source in records.items():
            target = directory / "lifecycle" / name
            if target.exists():
                if target.read_bytes() != source.read_bytes():
                    raise TrialError("保存する試験記録が変化しています")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    result = archive_minimal(directory, Path(config["archive_store"]), archive,
                             preserve_existing=not complete, prune_workspaces=True)
    verification = load(archive / "verification.json")
    prune = load(archive / "prune-receipt.json")
    if verification.get("status") != "verified" or prune.get("status") != "complete" or verification["manifest"] != prune["manifest"]:
        raise TrialError("保存・復元照合・削除の完了記録が揃っていません")
    if list((cycle / "layer2/evidence").glob("*/workspace")):
        raise TrialError("作業コピーが残っています")
    check_protected(config)
    write_once(saved, {"archive": str(archive), "manifest": verification["manifest"], "status": result["status"]})
    return load(saved)


def check_result(receipt):
    from scripts.evaluation_loop import identity_sha256
    result = load(receipt["result_path"])
    content = dict(result)
    digest = content.pop("result_content_sha256", None)
    if (digest != identity_sha256(content) or digest != receipt["result_content_sha256"]
            or result["result_id"] != receipt["result_id"]):
        raise TrialError("登録結果と登録記録が一致しません")


def finish(trial):
    config = load(trial / "trial.json")
    check_protected(config)
    ensure_quiet(trial)
    if (trial / "complete.json").exists():
        for directory in rounds(trial):
            save_round(trial, config, directory, True)
        result = load(trial / "complete.json")
        check_result(result["result"])
        for receipt in result["home_receipts"]:
            if load(receipt).get("status") != "complete" or Path(receipt).parent.with_name("codex-homes").exists():
                raise TrialError("実行別ホームの完了記録が一致しません")
        return result
    directory, prepared = latest(trial)
    executed = trial / "receipts" / f"{directory.name}-executed.json"
    if not executed.exists():
        if not (directory / "runner.log").exists():
            raise TrialError("runの終了記録がありません")
        # 親プロセスが強制終了しても、静止確認後に証拠を保存して不足分へ進める。
        write_once(executed, {"return_code": 130, "status": "interrupted"})
    cycle = directory / "cycle"
    for path in sorted((cycle / "layer2/bindings").glob("*.json")):
        binding = load(path)
        if binding["status"] != "valid":
            continue
        run_id = binding["run_id"]
        require_usage(cycle, run_id)
        rating = cycle / "layer3/ratings" / f"{run_id}.json"
        if not rating.is_file():
            raise TrialError(f"未採点の実行があります: {run_id}")
        for name in ("result.diff", "validation.json", "final-response.txt"):
            if not (cycle / "layer2/evidence" / run_id / "rating-view" / name).is_file():
                raise TrialError(f"採点証拠がありません: {run_id}/{name}")
        call("scripts/atomic_run_registry.py", "register-run", "--registry", config["registry"],
             "--pool-key", prepared["pool_key"], "--cycle", cycle, "--run-id", run_id)
    # 使用したホームを申告から落としたまま完了しない。
    declared = {Path(p) for p in config["homes"]}
    if any(p not in declared for p in trial.rglob("codex-homes") if p.is_dir()):
        raise TrialError("未登録の実行別ホームがあります。最初のprepareで--homesへ指定してください")
    pending = remaining(config, prepared["pool_key"])
    complete = not pending["missing_slot_count"]
    if complete:
        selection = trial / "selection.json"
        if not selection.exists():
            call("scripts/atomic_run_registry.py", "select-runs", "--registry", config["registry"],
                 "--pool-key", prepared["pool_key"], "--count", config["iterations"], "--output", selection)
        analysis = trial / "analysis.json"
        if not analysis.exists():
            call("scripts/atomic_run_registry.py", "aggregate-selection", "--registry", config["registry"],
                 "--selection", selection, "--price-table", trial / "inputs/price_table.json", "--output", analysis)
        registration = cycle / "layer4/result-registration.json"
        if not registration.exists():
            call("scripts/atomic_run_registry.py", "register-selection-result", "--registry", config["registry"],
                 "--selection", selection, "--profile", trial / "inputs/profile.json",
                 "--price-table", trial / "inputs/price_table.json", "--cycle", cycle)
    archives = [save_round(trial, config, q, complete and q == directory) for q in rounds(trial)]
    if not complete:
        return {"status": "incomplete_saved", "missing_slots": pending["missing_slot_count"], "archives": archives}
    home_receipts = []
    for path in config["homes"]:
        home = Path(path)
        receipt = home.with_name("codex-homes.archive") / "prune-receipt.json"
        if not receipt.exists():
            archive_homes(home)
        record = load(receipt)
        if record.get("status") != "complete" or home.exists():
            raise TrialError("実行別ホームの保存・後片付けが完了していません")
        home_receipts.append(str(receipt))
    check_protected(config)
    registration = load(cycle / "layer4/result-registration.json")
    check_result(registration)
    result = {"status": "complete", "result": registration,
              "archives": archives, "home_receipts": home_receipts, "protected_inputs_unchanged": True}
    write_once(trial / "complete.json", result)
    return result


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare", help="固定入力から不足分だけを準備する")
    p.add_argument("--trial", required=True, type=Path)
    for flag in ("profile", "store", "registry", "price-table", "resource-class", "archive-store", "archive-root"):
        p.add_argument("--" + flag, type=Path)
    for flag in ("template", "protect", "homes"):
        p.add_argument("--" + flag, action="append", type=Path)
    for name in ("run", "finish"):
        p = commands.add_parser(name)
        p.add_argument("--trial", required=True, type=Path)
    p = commands.add_parser("run-group", help="複数試験を一つの待ち行列で実行する")
    p.add_argument("--trial", required=True, type=Path, action="append")
    return result


def main():
    args = parser().parse_args()
    try:
        if args.command == "run-group":
            with ExitStack() as stack:
                trials = [stack.enter_context(locked(path)) for path in sorted(args.trial)]
                value = run_group(trials)
        else:
            with locked(args.trial) as trial:
                value = prepare(trial, args) if args.command == "prepare" else run(trial) if args.command == "run" else finish(trial)
        print(json.dumps(value, ensure_ascii=False))
        return value.get("runner_return_code", 0)
    except (TrialError, LongRunStorageError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
