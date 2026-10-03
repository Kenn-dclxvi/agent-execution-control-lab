#!/usr/bin/env python3
"""r2とr3の小規模素材を共通の固定環境でN2測定する。"""
from pathlib import Path
from types import SimpleNamespace
import importlib.util
import os
import sys

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[2]
spec = importlib.util.spec_from_file_location('latent_paired_r2', BASE / 'runtime/run_latent_mode_code_r2.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
runner = module.runner


def main():
    campaign = Path(sys.argv[1]).resolve()
    receipt = runner.load(campaign / 'comparison-preflight.json')
    if not receipt['ready'] or receipt['slots'] != 12:
        raise ValueError('実行前照合が未成立')
    if os.environ['PATH'] != receipt['inherited_path'] or sys.version != receipt['python_version'] or sys.executable != receipt['python_executable']:
        raise ValueError('PythonまたはPATHが実行前照合から変化した')
    for rel, digest in receipt['module_sha256'].items():
        if runner.sha(REPO / rel) != digest:
            raise ValueError('実行器の固定内容が変化した: ' + rel)
    for revision, paths in receipt['fixture'].items():
        visible = BASE / f'cases/latent-mode-code/{revision}/visible'
        actual = {str(p.relative_to(visible)) for p in visible.rglob('*') if p.is_file()}
        if actual != set(paths):
            raise ValueError('fixtureのファイル集合が変化した')
        for rel, value in paths.items():
            path = visible / rel
            if runner.sha(path) != value['sha256'] or oct(path.stat().st_mode & 0o777) != value['mode']:
                raise ValueError('fixtureの内容またはmodeが変化した')
    profiles = {}
    for key, value in receipt['profiles'].items():
        path = Path(value['path'])
        if runner.sha(path) != value['sha256']:
            raise ValueError('profileが変化した')
        profiles[key] = runner.load(path)
        for ref in ['evaluation_set_ref', 'rating_ref', 'prompt_ref']:
            identity = profiles[key][ref]
            if runner.sha(REPO / identity['path']) != identity['sha256']:
                raise ValueError('参照アーティファクトが変化した')
    if runner.sha(Path(receipt['runtime_binding']['executable'])) != receipt['runtime_binding']['entrypoint_sha256']:
        raise ValueError('CLIが変化した')
    runner.write(campaign / 'controller-preflight.json', {'ready': True, 'comparison_preflight_sha256': runner.sha(campaign / 'comparison-preflight.json'), 'controller_sha256': runner.sha(Path(__file__).resolve()), 'max_workers': 24, 'actual_concurrency': 1, 'new_slots': 12})
    runner.fixture = SimpleNamespace(prepare=module.old.prepare, grade=module.old.grade)
    try:
        for level in ['low', 'medium', 'high']:
            for n in [1, 2]:
                for revision in ['r2', 'r3']:
                    module.old.CASE = BASE / f'cases/latent-mode-code/{revision}'
                    result = runner.execute(campaign / revision, profiles[revision + '-' + level], 'CRC-A01-CODE', f'{level}-{n:02}')
                    if not result['valid']:
                        raise ValueError('無効runで追加発行停止: ' + revision + '-' + result['label'])
    finally:
        for revision in ['r2', 'r3']:
            (campaign / revision / 'authentication-source/auth.json').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
