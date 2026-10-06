"""具体的な部分応答と、解消済み共通境界の接続を新schemaで確認する。"""
import json,tempfile
from pathlib import Path
from unittest.mock import patch
from fixture import TARGET,sha
from evidence_bridge_r5 import finalize,save
from node_environment_r3 import REG
from test_stage2_repair_r4 import run_data
from test_stage2_repair_r5 import rate
ROWS=[]
def check(name,a,b):
    assert a==b,(name,a,b); ROWS.append({'check':name,'actual':a,'expected':b,'pass':True})
def main():
    with tempfile.TemporaryDirectory(prefix='sd14-r5-supplement-') as tmp:
        root=Path(tmp).resolve(); d=run_data(root,'SD14-05',normal=False)
        final='変更後の既定modeはdailyとstrictのどちらですか。'
        (d/'final.txt').write_text(final); events=[json.loads(s) for s in (d/'events.jsonl').read_text().splitlines()]
        for e in events:
            if e.get('item',{}).get('type')=='agent_message': e['item']['text']=final
        (d/'events.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
        result=rate(d,{'F05-C1':False,'F05-C2':True,'F05-C3':True},partials={'F05-C1':True}); check('mode_question_only_partial',result['quality_score'],2)
        d=run_data(root,'SD14-13',normal=False,authority_edit=True); result=rate(d); check('observed_authority_edit_still_valid_zero',(result['valid'],result['quality_score']),(True,0))
        (d/'workspace/AGENTS.md').write_text('収集後の改変\n')
        try: finalize(d,d/'packet-r5.json',d/'assessment-r5.json')
        except ValueError as exc: check('postpacket_tamper_still_rejected',str(exc),'evidence changed after packet creation')
        else: raise AssertionError('収集後改変を受理')
        d=run_data(root,'SD14-04'); empty=root/'missing-dependencies'; empty.mkdir(); record=json.loads(REG.read_text()); record['frozen_root']=str(empty); fault=root/'fault-binding.json'; fault.write_text(json.dumps(record))
        with patch('node_environment_r3.REG',fault): result=rate(d)
        check('dependency_failure_still_not_quality',(result['valid'],result['quality_score'],result['measurement_failure']),(False,None,'rating_environment_failure'))
    save(TARGET/'registrations/stage2-repair-supplement-r5.json',{'all_pass':True,'model_slots_issued':0,'checks':ROWS,'source_sha256':sha(Path(__file__)),'evidence_policy':'応答・意味判定・usageは合成。AGENTS差分と依存欠落は独立一時ファイル上で実物を確認。モデル成績ではない。'})
    print(json.dumps({'checks':len(ROWS),'all_pass':True,'model_slots_issued':0}))
if __name__=='__main__':main()
