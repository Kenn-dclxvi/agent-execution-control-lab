"""固定実行器のprepare/採点後処理に結ぶ。dispatch入口は持たない。"""
import importlib.util, json, sys
from pathlib import Path
from fixture import TARGET,SHARED,materialize,task,sha
from evidence_bridge_r2 import save,load,build_packet,finalize
REPO=TARGET.parents[2]
FIXED_RUNNER=REPO/'evaluations/targets/the-caption/runtime/run_old_a01_current_environment_n2_r1.py'
MATERIALIZER=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/astra-a01-old-and-compact-n20-20261001-r1/frozen-lab/scripts/run_codex_evaluation.py')
EXPECTED_RUNNER='565e94ac8adf190871f419ae32a59986df1c39cb39cd7f3cc08e12b52009d058'
EXPECTED_MATERIALIZER='28728c2284550f227a5c24f40f4751e2654bc7598b8d9cf68ddef9eae162d80c'

def bind_sources():
    if sha(FIXED_RUNNER)!=EXPECTED_RUNNER or sha(MATERIALIZER)!=EXPECTED_MATERIALIZER:
        raise ValueError('fixed executor or shared Python materializer mismatch')
    return {'executor':{'path':str(FIXED_RUNNER),'sha256':sha(FIXED_RUNNER)},
            'materializer':{'path':str(MATERIALIZER),'sha256':sha(MATERIALIZER)}}

def prepare(case_id,workspace):
    workspace=Path(workspace); directory=workspace.parent
    binding=bind_sources(); identity=materialize(case_id,workspace)
    # 元の共有Python接続実装をそのまま再利用する。
    (workspace/'.venv').unlink()
    spec=importlib.util.spec_from_file_location('sd14_shared_python_materializer',MATERIALIZER)
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module)
    module.materialize_shared_venv(SHARED,workspace/'.venv',workspace)
    if (directory/'task.json').exists() or (directory/'start.json').exists(): raise ValueError('start evidence already exists')
    raw=task(case_id,identity['seed_commit']); (directory/'task.json').write_bytes(raw)
    identity.update({'case_id':case_id,'run_id':directory.name,'authority':{p:sha(workspace/p) for p in ['AGENTS.md','src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']},'task_sha256':sha(directory/'task.json'),'executor_binding':binding})
    save(directory/'start.json',identity)
    return identity

def capture_completed_execution(run):
    run=Path(run); binding=bind_sources(); completed=load(run/'run.json'); launch=load(run/'launch.json'); start=load(run/'start.json')
    if completed['case_id']!=start['case_id'] or completed['label']!=start['run_id'] or launch['label']!=start['run_id']:
        raise ValueError('fixed execution identity mismatch')
    if launch['task_sha256']!=sha(run/'task.json'): raise ValueError('delivered task mismatch')
    if completed.get('exit_code')!=0: raise ValueError('execution did not complete successfully')
    usage=load(run/'usage.json')
    origin='local_synthetic_no_model' if any(s.get('source')=='local_synthetic_no_model' for s in usage['sessions']) else 'measured'
    save(run/'execution.json',{'run_id':start['run_id'],'case_id':start['case_id'],
         'elapsed_seconds':completed['elapsed_seconds'],'elapsed_boundary':'cli_subprocess_start_to_return_monotonic',
         'executor_binding':binding,'run_source_sha256':sha(run/'run.json'),'launch_source_sha256':sha(run/'launch.json'),
         'evidence_origin':origin,'quality_not_yet_finalized':True})
    packet=build_packet(run,start['case_id']); save(run/'rating-packet.json',packet)
    return packet

def finalize_completed_execution(run,assessment_path):
    run=Path(run); result=finalize(run,run/'rating-packet.json',assessment_path)
    save(run/'quality-result-r2.json',result)
    return result


def load_bound_executor():
    """元executeのバイトを維持し、専用fixtureの入口だけを結ぶ。呼出しは行わない。"""
    from types import SimpleNamespace
    bind_sources()
    spec=importlib.util.spec_from_file_location('sd14_fixed_codex_executor',FIXED_RUNNER)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    def bound_prepare(case_id, workspace):
        identity=prepare(case_id,workspace)
        campaign=Path(workspace).parent.parent.parent
        if not (campaign/'task.txt').exists() or (campaign/'task.txt').read_bytes()!=task(case_id,identity['seed_commit']):
            raise ValueError('case campaign TaskSpec must be fixed before dispatch')
    def pending_rating(case_id,workspace,evidence):
        return {'case_id':case_id,'valid':False,'execution_valid':True,'quality_score':None,'reason':'awaiting_independent_rating','model_dispatch_admitted':False}
    module.fixture=SimpleNamespace(prepare=bound_prepare,grade=pending_rating)
    return module
