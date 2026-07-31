# Candidate122 preterminal result round分析

## 結論

Candidate122のA01 / A02 / F02でtokenの高低を分けた共通差は、個々のtool invocation数ではなく、artifact変更またはclarification停止までにtool resultをmodelへ返したround数だった。

- A01: `0 round`は約18K、`1 round`は約37K
- A02: `1 round`は約126K、`2 round`は約166K〜222K
- F02: `1 round`は約122K〜125K、`2 round`は約180K

F02で4 targetを4 invocationへ分けたrunも、4件を同じmodel stepから発行して全result受領後に一度だけ判断した。したがってC122のcontent-wave closureは5 / 5件で成立している。残差はcontent waveの分割ではなく、その前に開始identityだけのresultを独立してmodelへ返したことである。

## 分析単位

この文書では`preterminal result round`を次の単位とする。

1. modelが一つ以上のread-only commandを同じstepから発行する
2. command群のresultをmodelが受領する
3. modelが次のtool発行、artifact変更、またはterminal responseを判断する

同じmodel stepから複数commandを発行した場合、tool invocationが複数でも一つのroundと数える。command間にagent messageと新しい判断を挟んだ場合は別roundと数える。

## C122の対応表

| case | preterminal result round | run数 | token | 中央値 |
| --- | ---: | ---: | --- | ---: |
| A01 | 0 | 2 | `18,414 / 18,448` | `18,431` |
| A01 | 1 | 3 | `37,381 / 37,382 / 37,471` | `37,382` |
| A02 | 1 | 2 | `126,028 / 127,300` | `126,664` |
| A02 | 2 | 3 | `165,870 / 194,659 / 221,776` | `194,659` |
| F02 | 1 | 4 | `122,020 / 124,716 / 124,719 / 125,424` | `124,718` |
| F02 | 2 | 1 | `179,543` | `179,543` |

比較基準を分けると、未達caseも異なる。

| case | C107 | C118 | C122 | C118比 | C107比 |
| --- | ---: | ---: | ---: | --- | --- |
| A01 | `57,368` | `18,431` | `37,381` | 未達 | 達成 |
| A02 | `125,559` | `226,321` | `165,870` | 達成 | 未達 |
| F01 | `127,797` | `120,050` | `109,096` | 達成 | 達成 |
| F02 | `173,000` | `256,931` | `124,719` | 達成 | 達成 |

したがって「C118より低いこと」を見るとA01だけが未達である。「C107のcase値以下」を見るとA02だけが未達である。C107の正式目標はStandard14集約中央値`1,523,137`以下であり、targeted 4 caseの合算やcase別値をその代替にはしない。

## A01

A01は変更後のrequired mode valueがTaskSpecにないため、値を推測せずclarificationで停止するcaseである。

低cost 2件はTaskSpecだけで`spec_ready=false`を確定し、toolを発行せず質問して停止した。高cost 3件は`pwd / branch / HEAD / git status --short`を一つのroundで確認し、そのresult受領後に同じ質問で停止した。両経路とも変更0、test 0、score `4`である。

C118にも同じ二経路が存在する。

| prompt | toolなし | identity確認あり | toolなし経路中央値 | identity経路中央値 | 全体中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| C118 | 3 / 5 | 2 / 5 | `18,424` | `35,214` | `18,431` |
| C122 | 2 / 5 | 3 / 5 | `18,431` | `37,382` | `37,381` |

経路内costはほぼ同じである。全体中央値の増加は、N=5でidentity経路が2件から3件へ増え、中央値が高cost群へ移ったためである。C122固有の回帰を示さない。

TaskSpecは開始identityを「最初の変更判断前」に要求する。required value不足をTaskSpecから確定してclarification停止することはartifact変更判断ではない。Rating v14も、未固定値を推測せず、変更とtestを開始せず、`awaiting_required_value`で停止した両経路をscore `4`としている。したがって`spec_ready=false`がTaskSpecだけで確定した場合のidentity roundには、現在の成果判定を変える観測価値がない。

## A02

低cost 2件は、開始identity、`run.sh`、canonical entrypoint authorityを一つのroundで確認し、その次にartifactを変更した。

高cost 3件は二つのroundを使った。

- `545b1891c97b4266bbba3b260fce834d`: broken mappingとcanonical entrypointを確定した後、instruction、entrypoint実体、testを追加read
- `4721bed1fa20483aa62538fdaa639071`: locator群のresult受領後、authorityとtarget contentを追加read
- `c70e826803bf4cbdbf3bc5c6bf021153`:広い初回検索のresult受領後、関連test locatorとtarget contentを追加read

bind表明後の再入だけでは、最も高い3件を一つの経路として識別できない。共通差はartifact変更前result roundが二つあることである。

ただしC122の`prechange_evidence_wave_ready`は、TaskSpecがexact evidence target setを列挙済みの場合だけ成立する。A02は編集target `run.sh`を指定するが、canonical entrypointを決めるevidence target setを列挙していない。したがってC122 fast pathはA02に適用されず、A02のN=5変動をC122中核制御の失敗へbindできない。

## F02

低cost 4件は、開始identityとTaskSpec列挙済み2 source / 2 testのcontentを一つのroundで取得し、次に2 sourceを変更した。tokenは狭い`122,020〜125,424`へ収束した。

残るrun `9e31e7bb05ea45579daf07b92fb878b1`は次の二roundだった。

1. 開始identityを同じmodel stepから4 commandで確認
2. 2 source / 2 testを同じmodel stepから4 `sed` invocationで取得
3. 全content result受領後に一度だけ判断して2 sourceを変更

content取得中のmodel再入、locator-only result、content後の追加readはない。このためcontent waveは成立している。`179,543`への増加を分けるのは、content invocation数ではなく、identity resultをcontent前に独立して返したroundである。

## Candidate122の状態訂正

旧判定は、literalな「一つのtool invocation」と調査対象の「途中判断を挟まない一つのwave」を混同した。また、C122 fast path非適用のA02 N=5値を中核制御の停止条件へbindした。

訂正後の状態は次である。

`targeted_a01_a02_f01_f02_evaluated / quality_gate_passed / f02_content_wave_closure_passed / f02_cost_target_passed / postchange_method_boundary_passed / residual_preterminal_result_round_variance / result_registered / adoption_not_decided`

## 次の制御候補に必要な条件

次の候補はC122を直接親とし、F02のexact-target content waveを保持する。追加条件はcase名やpathではなく、次の二つの状態差を扱う。

1. `clarification_terminal_ready`
   - TaskSpecだけで`spec_ready=false`と未固定required outcome valueを確定できる
   - repository observationはそのvalueをbindできない
   - artifact変更、test、repository predicateを開始しない
   - この場合は開始identityを独立resultとして返さず、clarificationをterminal resultにする
2. `prechange_result_round_ready`
   - `spec_ready=true`
   - 開始identity確認と、同じ変更predicateを決めるadmission済みevidenceが発行前に固定済み
   - identity不一致なら後続evidenceを発行せずterminal stopできる
   - identity一致なら同じmodel return境界の内側でadmission済みevidenceまで取得できる
   - modelへ返すresultを`edit-ready`または具体的な`terminal stop`へ閉じる

複数commandを一つのshell compound commandへ無条件結合することは目的にしない。必要なのは、identity不一致時のfail-closed stopを保持しながら、identity successだけを理由にmodelへ戻らないことである。

## 非結論

- N=5だけでA01のidentity経路発生率がC122により増えたとは判断しない
- command数またはcontent bytesだけを新しい上限にしない
- A02のexact evidence targetをTaskSpec外から捏造しない
- targeted 4 caseの値をStandard14 KPIへ一般化しない

## 後続Standard14による状態更新

この分析時点の`adoption_not_decided`は、その後の[`Standard14各N=5`](../evaluations/results/candidate118-candidate122-prechange-evidence-wave-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)により失効した。token中央値`1,403,840`はCandidate107目標を通過したが、F04の1件がincomplete bounded contentをterminal missingと誤分類してscore `2`となった。現在状態は`quality_gate_failed / stopped`であり、次に扱う残差はresult round一般ではなく、同じread可能targetの未観測criterionに限定したcontinuationである。
