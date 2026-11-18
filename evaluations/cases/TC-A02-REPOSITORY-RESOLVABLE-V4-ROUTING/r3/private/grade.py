"""A02 r3 の保存済み実行証拠から三項目を独立判定する。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex

CONTRACT = json.loads(Path(__file__).with_name("case-data.json").read_text())
ARM = re.compile(rb'(?m)^  v4\|v\)\n    module=([^\n]*)$')
CANONICAL = b'src.app.entrypoints.v4_daily_main'


def command_body(command):
    words = shlex.split(command)
    if len(words) == 3 and words[0] in ('/bin/zsh', '/bin/bash', '/bin/sh') and words[1] in ('-c', '-lc'):
        return words[2]
    return command


def grade(cycle, run_id):
    evidence = cycle / 'layer2/evidence' / run_id
    case = json.loads((evidence / 'case.json').read_text())
    if (case['id'], case['case_revision']) != (CONTRACT['case_id'], 'r3'):
        raise ValueError('A02 r3 の実行記録が必要です')
    seed = (cycle / 'layer1/fixtures' / case['id'] / 'run.sh').read_bytes()
    expected = CONTRACT['seed']['expected_post_seed_files'][0]['raw_sha256']
    if hashlib.sha256(seed).hexdigest() != expected:
        raise ValueError('開始ファイルの識別値が一致しません')
    workspace = evidence / 'workspace'
    if not workspace.is_dir():
        raise ValueError('採点には実行後ワークスペースの保存または復元が必要です')
    path = workspace / 'run.sh'
    regular = not path.is_symlink() and path.is_file()
    final = path.read_bytes() if regular else b''
    matches = ARM.findall(final)
    literals = {CANONICAL, b'"' + CANONICAL + b'"', b"'" + CANONICAL + b"'"}
    route = len(matches) == 1 and matches[0].rstrip() in literals
    rhs = matches[0] if len(matches) == 1 else b""
    module_name = rb"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*"
    simple_rhs = re.fullmatch(rb"([\"']?)" + module_name + rb"\1", rhs) is not None
    view = json.loads((evidence / 'rating-view/validation.json').read_text())
    if view['run_id'] != run_id:
        raise ValueError('最終差分の実行IDが一致しません')
    scope = (regular and simple_rhs and
             (path.stat().st_mode & 0o7777) == 0o755 and
             ARM.sub(b'  v4|v)\n    module=', final) == ARM.sub(b'  v4|v)\n    module=', seed) and
             not view['unexpected_changed_paths'] and set(view['result_paths']) <= {'run.sh'})
    commands = CONTRACT['grader']['commands']
    results = {cmd: '証拠なし' for cmd in commands}
    receipt = cycle / 'layer2/extensions' / run_id / 'all-agent-command-evidence/evidence.json'
    if receipt.exists():
        data = json.loads(receipt.read_text())
        if data['run_id'] != run_id:
            raise ValueError('コマンド記録の実行IDが一致しません')
        for field, state in [('attempted_commands', '終了未確認'), ('failed_commands', '失敗'), ('successful_commands', '成功')]:
            for entry in data[field]:
                try:
                    body = command_body(entry['command'])
                except ValueError:
                    continue
                if body in results and (state != '成功' or entry.get('exit_code') == 0):
                    results[body] = state
    verified = all(state == '成功' for state in results.values())
    return {'case_revision': 'r3', 'run_id': run_id, '起動先': route,
            '変更範囲': scope, '検証結果': verified, '検証内訳': results,
            '完全達成': route and scope and verified}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycle', type=Path, required=True)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    print(json.dumps(grade(args.cycle, args.run_id), ensure_ascii=False, indent=2))
