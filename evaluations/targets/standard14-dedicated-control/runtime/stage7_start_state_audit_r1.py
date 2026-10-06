"""保存済み開始状態の契約照合。モデルや測定対象の操作は発行しない。"""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

TARGET = Path(__file__).resolve().parents[1]
REPO = TARGET.parents[2]
ROOT = Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs')
REG = TARGET / 'registrations'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt_issues(receipt, contract):
    fields = contract['receipt_fields']
    issues = []
    for field in sorted(set(fields) - set(receipt)):
        issues.append('missing:' + field)
    for field in sorted(set(receipt) - set(fields)):
        issues.append('extra:' + field)
    types = {'str': str, 'dict': dict, 'int': int}
    for field in sorted(set(fields) & set(receipt)):
        if type(receipt[field]) is not types[fields[field]]:
            issues.append('type:' + field)
    return issues


def exact_pair_issues(old, new, contract):
    return ['different:' + field for field in contract['exact_pair_fields']
            if old.get(field) != new.get(field)]


def git(workspace, *args):
    return subprocess.check_output(['git', '-C', str(workspace), *args])


def history(workspace, start):
    base, seed, free = [start[x] for x in ['base_commit', 'seed_commit', 'free_commit']]
    for commit in [base, seed, free]:
        git(workspace, 'cat-file', '-e', commit + '^{commit}')
    subprocess.run(['git', '-C', str(workspace), 'merge-base', '--is-ancestor', base, seed], check=True)
    subprocess.run(['git', '-C', str(workspace), 'merge-base', '--is-ancestor', seed, free], check=True)
    changes = git(workspace, 'diff', '--numstat', seed, free).decode()
    log = git(workspace, 'log', '--format=%s', seed + '..' + free).decode().splitlines()
    return {'base_seed_free_ancestry_valid': True,
            'seed_to_free_changes': changes,
            'seed_to_free_commit_subjects': log,
            'root_at_seed_bytes': len(git(workspace, 'show', seed + ':AGENTS.md')),
            'root_at_free_bytes': len(git(workspace, 'show', free + ':AGENTS.md')),
            'current_postexecution_head_not_used_as_start_proof': True}


def rejection_checks(contract, example):
    checks = []
    original = copy.deepcopy(example)
    original['git_objects_logical_bytes'] = 0
    original['git_objects_allocated_bytes'] = 0
    assert receipt_issues(original, contract) == []
    for name, change, expected in [
        ('容量2項目がない旧宣言を拒否', lambda d: (d.pop('git_objects_logical_bytes'), d.pop('git_objects_allocated_bytes')), ['missing:git_objects_allocated_bytes', 'missing:git_objects_logical_bytes']),
        ('構築用情報の追加を拒否', lambda d: d.update(fixture_receipt={}), ['extra:fixture_receipt']),
        ('容量の真偽値を整数として受理しない', lambda d: d.update(git_objects_logical_bytes=True), ['type:git_objects_logical_bytes']),
    ]:
        changed = copy.deepcopy(original)
        change(changed)
        observed = receipt_issues(changed, contract)
        assert observed == expected, (name, observed)
        checks.append({'check': name, 'passed': True})
    changed = copy.deepcopy(original)
    changed['authority']['AGENTS.md'] = 'changed'
    assert exact_pair_issues(original, changed, contract) == ['different:authority']
    checks.append({'check': '正本の内容差を拒否', 'passed': True})
    changed = copy.deepcopy(original)
    changed['git_objects_logical_bytes'] += 10
    assert receipt_issues(changed, contract) == [] and exact_pair_issues(original, changed, contract) == []
    checks.append({'check': '同じ型の素材容量の差を比較条件の不一致へ誤分類しない', 'passed': True})
    return checks


def main():
    contract_path = REG / 'stage7-start-state-contract-r1.json'
    contract = read(contract_path)
    accepted_path = REG / 'stage3-verdict-r4.json'
    mapping = read(accepted_path)['cases']
    evidence = {str(contract_path): sha(contract_path), str(accepted_path): sha(accepted_path)}
    rows, declarations = [], []
    for reason in ['low', 'medium', 'high']:
        old_root = ROOT / 'standard14-old-new-paired-n2-20261004-r2' / reason
        new_root = ROOT / f'standard14-dedicated-{reason}-n2-20261004-r1'
        pre = old_root / 'preflight.json'
        declared = read(pre)
        evidence[str(pre)] = sha(pre)
        declarations.append({'reasoning_effort': reason,
                             'historical_start_receipt_keys_match_dedicated': declared['start_receipt_keys_match_dedicated'],
                             'actual_keyset_equal': False,
                             'declaration_contradicted': True})
        for case in mapping:
            cid = case['case_id']
            for iteration in [1, 2]:
                label = f'{reason}-{iteration:02}'
                runs = {side: root / 'cases' / cid / 'runs' / label
                        for side, root in [('old', old_root), ('dedicated', new_root)]}
                starts, histories, identities = {}, {}, {}
                for side, run in runs.items():
                    p = run / 'start.json'
                    starts[side] = read(p)
                    launch = read(run / 'launch.json')
                    for source in [p, run / 'launch.json']:
                        evidence[str(source)] = sha(source)
                    expected = case['source_case'] if side == 'old' else cid
                    identities[side] = {
                        'case_binding_valid': starts[side]['case_id'] == launch['case_id'] == expected,
                        'run_binding_valid': starts[side]['run_id'] == launch['label'] == label,
                        'launch_task_binding_valid': starts[side]['task_sha256'] == launch['task_sha256']}
                    assert all(identities[side].values())
                    histories[side] = history(run / 'workspace', starts[side])
                rows.append({'case_id': cid, 'reasoning_effort': reason, 'iteration': iteration,
                             'receipt_issues': {side: receipt_issues(start, contract) for side, start in starts.items()},
                             'exact_pair_issues': exact_pair_issues(starts['old'], starts['dedicated'], contract),
                             'identity_checks': identities,
                             'history': histories,
                             'history_correspondence_status': 'unresolved',
                             'pre_dispatch_clean_proof': 'not_certified_by_this_offline_audit',
                             'comparison_admitted': False})
    assert len(rows) == 84 and len({r['case_id'] for r in rows}) == 14
    assert all(r['receipt_issues']['old'] == ['missing:git_objects_allocated_bytes', 'missing:git_objects_logical_bytes'] for r in rows)
    assert all(not r['receipt_issues']['dedicated'] and not r['exact_pair_issues'] for r in rows)
    result = {'schema_version': 'standard14-stage7-start-state-audit/r1', 'case_count': 14,
              'pair_count': len(rows), 'identity_bound_pairs': 84,
              'receipt_schema_rejected_pairs': 84, 'history_correspondence_unresolved_pairs': 84,
              'declaration_contradictions': declarations, 'rows': rows,
              'rejection_checks': rejection_checks(contract, starts['old']),
              'source_sha256': evidence, 'model_slots': 0,
              'historical_preflight_retroactively_certified': False,
              'difficulty_certified': False, 'full_comparison_admitted': False}
    output = REG / 'stage7-start-state-audit-r1.json'
    if output.exists():
        raise FileExistsError('既存の診断記録へ上書きしない')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['case_count', 'pair_count', 'identity_bound_pairs', 'receipt_schema_rejected_pairs', 'model_slots', 'full_comparison_admitted']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
