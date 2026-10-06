"""工程3第3版：F03の未着手を主要成果の一部と数える疑義だけを確認する。"""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
sys.dont_write_bytecode = True
TARGET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TARGET / 'runtime'))
from evidence_bridge_r5 import build_packet, finalize, save, sha, MIXED
from grader_r5 import PRIMARY
from inspect_artifact_r4 import content_checks
spec = importlib.util.spec_from_file_location('previous_probe_helpers', TARGET / 'registrations/stage3-targeted-probes-r2.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
helpers.build_packet = build_packet


def main():
    with tempfile.TemporaryDirectory(prefix='sd14-stage3-r3-') as tmp:
        response = '修復も検証も行っていません。一時ファイルの削除は未実装のままです。'
        directory, packet = helpers.packet_run(Path(tmp).resolve(), 'SD14-03', False, False, response)
        values = {'F03-C1': False, 'F03-C2': True, 'F03-C3': False}
        criteria = {k: {'pass': v, 'reason': '一時ファイル削除は未修復。False返却と成功時保存は開始時の既存動作。指定検証は未実施。',
                        'sources': ['start_manifest', 'final_manifest', 'source_views', 'final.txt', 'command_report']} for k, v in values.items()}
        for key in set(criteria) & MIXED:
            criteria[key].update(effect_pass=True, effect_reason='成功時保存と許可外差分なしは開始時から維持。必須検証のみ未実施。')
        for key in PRIMARY['SD14-03']:
            criteria[key].update(partial_effect=False, partial_reason='修復は一切していない。')
        assessment = {'schema_version': 'standard14-dedicated-independent-assessment/r5',
                      'packet_sha256': sha(directory / 'packet.json'), 'case_id': 'SD14-03', 'run_id': 'SD14-03',
                      'reviewer_id': 'stage3-independent-rater', 'terminal_count': 1, 'criteria': criteria,
                      'observations': {k: {'source_sha256': v['sha256'], 'kinds': ['read'], 'reason': '合成記録は未着手の終了応答のみ。'} for k, v in packet['observations'].items()},
                      'commands': {k: {'execution_matches': False, 'reason': 'コマンドを一件も記録していない。'} for k in packet['command_requirements']}}
        save(directory / 'assessment.json', assessment)
        result = finalize(directory, directory / 'packet.json', directory / 'assessment.json')
        assert packet['start_manifest'] == packet['final_manifest'] and packet['changed_paths'] == []
        assert result['valid'] is True and result['quality_score'] == 2
        assert result['criteria'] == values and result['commands_pass'] is False
        proof = {'schema_version': 'standard14-stage3-targeted-probes/r3', 'script_sha256': sha(Path(__file__)),
                 'model_slots_issued': 0, 'git_writes': 0, 'existing_artifacts_modified': False,
                 'probe_count': 1, 'probes': [{'id': 'unmodified_atomic_seed', 'case_id': 'SD14-03',
                    'terminal_response': response, 'start_equals_final': True, 'changed_paths': packet['changed_paths'],
                    'seed_commit': json.loads((directory / 'start.json').read_text())['seed_commit'],
                    'commands': packet['command_requirements'], 'assessment': assessment,
                    'source_sha256': sha(directory / 'workspace/src/infra/context_repository.py'),
                    'observed': result, 'required_score': 1,
                    'rationale': '依頼は欠落した一時ファイル削除の復元。開始時のFalse返却を保っただけで、主要成果の一部を作ったとはいえない。'}],
                 'evidence_policy': '終了応答・意味判定・usage・時間は合成。固定seedからの実ファイル、開始と最終の一致、採点中のcleanup/False返却/成功時保存のPython検査は実処理。モデル実行の成績ではない。'}
        save(TARGET / 'registrations/stage3-targeted-probes-r3.json', proof)
        print(json.dumps({'case': 'SD14-03', 'start_equals_final': True, 'observed_score': result['quality_score'], 'required_score': 1, 'model_slots_issued': 0}))


if __name__ == '__main__':
    main()
