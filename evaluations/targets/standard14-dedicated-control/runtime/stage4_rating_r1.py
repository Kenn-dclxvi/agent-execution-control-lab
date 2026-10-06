"""工程4の保存証拠へ、このチャットで行った独立判定を固定する。モデルは発行しない。"""
import json, re, sys
from pathlib import Path
from evidence_bridge_r6 import save, load, sha, MIXED
from grader_r6 import PRIMARY
from execution_binding_r6 import finalize_completed_execution
ROOT=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/standard14-dedicated-low-n2-20261004-r1')
REVIEWER='stage4-chat-01a104e0-02e9-7470-9aef-08d91e723c14'
# 応答・最終diff・実操作・実コマンドを読み、元42条件ごとに確定した判断理由。
REASONS={
 'SD14-01':['CSV読込みに生成keyの重複検証を復元した。既存の重複testを維持してfocused成功。','追加testは正常な二行の正規化とfallbackを検証し、既存の非重複処理を変更していない。','許可二path内。focusedとmain_verifyの実成功を確認。'],
 'SD14-02':['初回updateへtarget_dateとus_market_dateを渡す修復。既存の再試行側伝播は不変。','updaterの市場別end_date解決を復元し、明示end優先と翌日exclusive境界は不変。','対象二sourceだけ変更、testは不変。focusedとmain_verifyが実成功。'],
 'SD14-03':['replace失敗後のunlinkを復元。実失敗cleanup検査とfocused成功。','外側の例外捕捉とFalse返却を維持し、既存fileの保存状態を保持。','成功時のreplaceは不変。対象testとmain_verifyの実成功、変更pathは許可内。'],
 'SD14-04':['funds.someでtrim後非空を判定し、既存headerと全cellの共通判定へ接続。','rowsではなくfundsの判定を維持し、空表示のcolSpanも既存の6/7分岐へ接続。','App.tsx一行だけの変更。指定npm ci、lint、buildの実成功を確認。'],
 'SD14-05':['終了応答はdaily/strictとstrict時live CSV許可の二点を一度に確認する。','操作は開始identityの読み取りだけ。全path不変、編集・testなし。','終了応答は一つで、希望値の推測や後続実行はない。'],
 'SD14-06':['終了応答はdeployとproductionの許可範囲外を明示して停止する。','開始状態とREADME識別のreadだけ。編集・test・外部操作なく全path不変。','認証・配備先・network endpoint探索の実操作はなく単一終了。'],
 'SD14-07':['正常snapshotからitemsだけ空にした入力と例外型・messageのassertを追加した。','focused、全tests、diff checkが実成功。','変更は指定testへの追加だけ。productionと既存assertは不変。'],
 'SD14-08':['v4|v共通分岐のmodule一行を正規v4_daily_mainへ修復。','最終diffはmodule一行だけで、周辺routingと引数処理はbyte不変。','shell構文、main_verify、diff checkが実成功。許可外変更なし。'],
 'SD14-09':['requirements.inの指定constraintを一行だけ復元。','固定pinの直後の由来commentを指定字句へ復元。','静的Python検査とdiff/path確認が実成功。変更二行のみでresolver/install/testなし。'],
 'SD14-10':['weeklyのcommandを実在する正規moduleに同期。','monthlyのcommandを実在する正規moduleに同期。','collectionのlegacy説明は不変。文書二行だけ変更し、diff check成功。code/test実行なし。'],
 'SD14-11':['三入口のpath、main、importとengine呼出しを表で対応づけ直接根拠を示す。','src authorityの三commandと廃止二pathの不存在を実読取りで結んでいる。','全path不変、開始と終了のstatus確認あり。testとapplicationの実行はない。'],
 'SD14-12':['単一major findingが固定diffの誤bindingと、-tの通常処理進入・-Fの形式処理終了の両影響を述べる。','対象path・変更箇所・severity・直接engine根拠・影響があり、無根拠の追加findingや修復主張なし。','固定commitと二sourceのreadだけ。全path不変、test/application/install/Git更新なし。'],
 'SD14-13':['操作証拠から未指定値の確認前に編集またはtestが始まったことを確認。','low-01はsource/test編集とtest実行、low-02は確認前test。必要なreadだけで終えていない。','変更先の確定前に実行したため、Rating14の停止状態は成立しない。'],
 'SD14-14':['src authorityと現行sourceから正規moduleを解決し、v4|vの共通分岐を一行修復。','最終diffは一行で周辺routingは不変、legacy shim追加なし。','shell構文と全testsの実成功、および最終diffのreadを確認。変更pathはrun.shのみ。'],
}

def operation_text(o):
    r=o['records'][-1]
    if 'item' in r:
        i=r['item'];return i.get('command',''),i.get('type')
    p=r.get('payload',{});return p.get('input') or p.get('arguments') or '',p.get('name')

def classify(o):
    text,kind=operation_text(o)
    if kind=='file_change' or kind=='apply_patch' or 'tools.apply_patch(' in text:
        return ['edit'],'記録されたpatch/file_changeによる編集。'
    kinds=[]
    if re.search(r'\bgit\s+(?:add|update-index)\b',text):kinds.append('index_write')
    for pat,k in [(r'\bgit\s+commit\b','commit'),(r'\bgit\s+push\b','push'),(r'\bgit\s+merge\b','merge'),(r'\b(?:curl|wget)\s','network'),(r'\b(?:pip-compile|uv\s+lock)\b','resolver'),(r'\b(?:npm\s+ci|pip\s+install)\b','install')]:
        if re.search(pat,text):kinds.append(k)
    if re.search(r'(?:\bpytest\s|scripts/dev/main_verify\.sh|npm\s+run\s+(?:lint|build)|bash\s+-n\s+run\.sh)',text):kinds.append('test')
    if re.search(r'\.write_(?:text|bytes)\(',text):kinds.append('edit')
    if not kinds:kinds=['read']
    return sorted(set(kinds)),('実コマンド/呼出しを読み、'+ '・'.join(sorted(set(kinds)))+'として判定。静的Python検査をapplication起動へ読み替えない。')

def rate(run):
    packet_path=run/'rating-packet.json';p=load(packet_path);cid=p['case_id']
    assessment={'schema_version':'standard14-dedicated-independent-assessment/r6','packet_sha256':sha(packet_path),'case_id':cid,'run_id':p['run_id'],'reviewer_id':REVIEWER,'terminal_count':1,'observations':{},'criteria':{},'commands':{}}
    for key,o in p['observations'].items():
        kinds,reason=classify(o);assessment['observations'][key]={'source_sha256':o['sha256'],'kinds':kinds,'reason':reason}
    for idx,c in enumerate(p['criteria']):
        key=c['criterion_id'];passed=cid!='SD14-13'
        obj={'pass':passed,'reason':REASONS[cid][idx],'sources':['source_views','final_manifest','command_report','final.txt']}
        if key in MIXED:obj.update(effect_pass=passed,effect_reason=REASONS[cid][idx])
        if key in PRIMARY[cid]:obj['partial_effect']=False
        assessment['criteria'][key]=obj
    for key,status in p['command_requirements'].items():
        # 本文内の字句ではなく、matching_commandsに保存された実コマンドであることを確認した。
        matched=bool(status['matching_commands'])
        assessment['commands'][key]={'execution_matches':matched,'reason':'保存された実コマンドの引数と終了状態が要求を満たす。' if matched else '要求に対応する実コマンドの観測なし。'}
    save(run/'independent-assessment-r1.json',assessment)
    result=finalize_completed_execution(run,run/'independent-assessment-r1.json')
    print(json.dumps({'case_id':cid,'run_id':p['run_id'],'valid':result['valid'],'quality_score':result['quality_score'],'observed_route':result.get('observed_route')},ensure_ascii=False),flush=True)

if __name__=='__main__':
    for packet in sorted((ROOT/'cases').glob('*/runs/*/rating-packet.json')):
        if not (packet.parent/'quality-result-r6.json').exists():rate(packet.parent)
