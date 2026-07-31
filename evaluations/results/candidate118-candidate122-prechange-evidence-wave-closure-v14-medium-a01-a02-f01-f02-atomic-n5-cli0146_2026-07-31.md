# Candidate118 / Candidate122 prechange evidence wave closure結果

## 結論

Candidate122は20 / 20件がvalidかつscore `4`だった。F02の変更前content evidenceを途中のmodel判断なしの一waveへ閉じる経路は5 / 5件で成立し、F02 token中央値はCandidate118の`256,931`から`124,719`へ`132,212`（`51.46%`）減った。Candidate107実績に基づく事前目標`173,000`も`48,281`（`27.91%`）下回った。

F02の1件は4 targetを4個のcontent invocationへ分けたが、4件を同じmodel stepから発行して全result受領後に一度だけ変更を判断した。したがってliteralな単一invocation条件は4 / 5件、調査仮説である単一content waveは5 / 5件である。このrunのtokenが`179,543`まで増えた直接の分離要因は、content前に開始identityだけのresult roundを一度modelへ返したことである。

A02ではimplementation bind後・最初のartifact変更前のcommand再入が1 / 5件あり、token中央値`165,870`は直接親Candidate119の`149,154`を`16,716`（`11.21%`）上回った。ただしC122 fast pathはTaskSpecがexact evidence target setを列挙した場合だけ適用され、A02は非適用である。C119自体にも変更前再入1 / 5件があるため、このN=5差をC122中核制御の失敗または停止根拠へbindできない。

したがってC122は`stopped`ではない。quality、F02 content-wave mechanism、F02 cost targetを通過した`targeted_evaluated / adoption_not_decided`とする。A01 / A02 / F02に残るcost分散は、変更または停止前にresultをmodelへ返したround数の差として別分析する。Standard14、採用、release、runtime projection、本体反映は未判断・未実施である。

## Identityと互換条件

- candidate: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`（Candidate119）
- non-parent: `the-caption-3ce91a4-implementation-edit-ticket-closure-r1`（Candidate120） / `the-caption-3ce91a4-evidence-request-scope-closure-r1`（Candidate121）
- bundle SHA-256: `5b7525ec265ea10f207a3b23f0bbf749f677554aad1c2fa0c5beae0c41e0d2d3`
- Evaluation set: `the-caption-standard14-r1` / `r1`からA01 r2、A02 r2、F01 r3、F02 r1を選択
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- case別N: 5
- profile上のM: 24
- atomic comparison key: `65301eae7c45c0d30af09c6e0659c92d698cdeb603edfdefd2d6dcbea5cb0d4a`
- result compatibility key: `5fd07842276b862329d72268b59256341c4869c85ccec19c7a534aa669a7a083`

Candidate122はCandidate119のroot `AGENTS.md`にある`EVIDENCE_GATE`だけを置換した。TaskSpecが同じ未解決predicateを共同で決めるexact target setを列挙済みで、全targetがadmission済みの場合だけ、変更前content evidenceを一つのinvocationへ閉じる`prechange_evidence_wave_ready`を追加した。result後は`edit-ready`または具体的理由を伴う`terminal stop`へ限定した。TaskSpec、case、fixture、rating、executorは変更していない。

保存済みCandidate118 Standard14 poolからA01 / A02 / F01 / F02各5件だけを選んだ4-case result `9e97af352b104addbd1b67e06bebad46`へbindしたcomparison preflightが`ready`になった後、Candidate122の不足20 slotだけを発行した。

## 実行と品質

- 新規発行: Candidate122の不足20 runだけ
- execution: 20 / 20 valid、excluded 0、external failure 0
- parallel execution wall time: `113.812`秒
- quality: score `4` × 20
- A01: required value待ち5 / 5、変更0 / 5、test 0 / 5
- A02: canonical成果5 / 5、successful test evidence 5 / 5
- F01: required command evidence完備5 / 5、command protocol違反0件
- F02: focused / full required validation完備5 / 5
- pool key: `884d3c76475c8c3f9efef05cb59722dd35a8cf692ee2443865e18a1c8f3b91ca`
- selection ID: `fe4924c78ab2424db3a31aa322a3a1e6`
- analysis ID: `4a981b643bcd461c8217c50b748814ba`
- result ID: `c68a9fe2beee47d38865653706f9c87e`

owner / producer evidence diagnosticはexit `1`だった。Rating v14では`diagnostic_only`であり、成果品質とmodel-visible required command evidenceを満たした20件のscoreを変更しない。

## KPI

4 caseのCandidate118基準は、同じatomic run poolから選んだ既存20 runである。

| 4-case集約中央値 | Candidate118 | Candidate122 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `642,176` | `473,550` | `-168,626`（`-26.26%`） |
| elapsed | `250.667`秒 | `244.693`秒 | `-5.974`秒（`-2.38%`） |

case別token中央値は次のとおりである。

| case | Candidate118 | Candidate122 | 差 |
| --- | ---: | ---: | ---: |
| A01 | `18,431` | `37,381` | `+18,950` |
| A02 | `226,321` | `165,870` | `-60,451` |
| F01 | `120,050` | `109,096` | `-10,954` |
| F02 | `256,931` | `124,719` | `-132,212` |

直接親Candidate119とのA02比較は`149,154 → 165,870`、差`+16,716`（`+11.21%`）である。F02は事前目標`173,000`以下を達成した。4-case集約値または少数caseの値をStandard14へ一般化しない。

A01はC118 / C122の両方で二経路に分かれた。TaskSpecだけで未固定値を判定してtoolなしで停止したrunは、C118が3件、C122が2件だった。開始identityを確認し、そのresult受領後に停止したrunは、C118が2件、C122が3件だった。toolなし経路のtoken中央値は`18,424 / 18,431`、identity確認経路は`35,214 / 37,382`である。経路内costはほぼ同じで、N=5の構成比が反転して全体中央値が高cost群へ移った。C122固有のA01回帰とは判定しない。

## Mechanism監査

| 判定項目 | Candidate122 | gate |
| --- | ---: | --- |
| A02 implementation bind後・変更前command再入 | `1 / 5` | non-applicable route diagnostic |
| A02変更後・最初のvalidation前method探索 | `0 / 5` | pass |
| F02 exact target setを同一predicateへbind | `5 / 5` | pass |
| F02変更前content evidence invocation 1件以下 | `4 / 5` | literal condition diagnostic |
| F02変更前content evidenceの単一model-step wave | `5 / 5` | pass |
| F02 locator-only result後の別content invocation | `0 / 5` | pass |
| F02 content evidence terminal result後の追加read | `0 / 5` | pass |
| F02 focused / full required validation | `5 / 5` | pass |

F02の4件は、開始identity、2 source、2 testのcontentを一つのcommand invocationで取得し、次のtoolで2 sourceを変更した。tokenは`122,020 / 124,716 / 125,424 / 124,719`だった。

run `9e31e7bb05ea45579daf07b92fb878b1`は、開始identityを一つのmodel stepから4 commandで確認し、そのresult受領後、2 sourceと2 testを次の一つのmodel stepから4個の`sed` invocationとして発行した。4 content resultの途中にmodel判断はなく、その後に変更した。tokenは`179,543`だった。これはcontent wave分割ではなく、開始identityとcontent evidenceを二つのpreterminal result roundへ分けた事象である。

A02の再入run `545b1891c97b4266bbba3b260fce834d`は、`run.sh`の`v4`分岐だけが旧entrypointを参照し、既定値・日付・option経路は正規entrypointを参照していると確定した後、`src/AGENTS.md`、entrypoint実体、testを追加で読んでから変更した。Candidate119で成立した変更後method境界は5 / 5件で保持したが、変更前terminal closureは保持しなかった。

## 判定と次の調査境界

Candidate122は、C121で分離できなかったF02 costを大きく下げた。bytes、target数、invocation数を単独で一般制約する案ではなく、TaskSpec列挙済みexact target setと同一predicateを条件にした一括content waveが、5 / 5件で目的event sequenceを成立させた事実を残す。

残差はcontent invocation数ではなく、変更または停止前にresultをmodelへ返すround数である。C122ではA01が`0 round: 2件 / 1 round: 3件`、A02が`1 round: 2件 / 2 round: 3件`、F02が`1 round: 4件 / 2 round: 1件`へ分かれ、各caseでroundが多い群のtokenが高かった。この共通構造を独立分析し、C122のF02成功を維持する次の変更条件を検討する。

## 状態

`targeted_a01_a02_f01_f02_evaluated / quality_gate_passed / f02_content_wave_closure_passed / f02_cost_target_passed / postchange_method_boundary_passed / residual_preterminal_result_round_variance / result_registered / adoption_not_decided`

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate122-prechange-evidence-wave-closure-v14-medium-a01-a02-f01-f02-atomic-n5-cli0146-20260731-r1`
- execution archive SHA-256: `4238ef7e5a7968860e0885cb65c508c7eb7b7d3b13bc92ebd8b2f838d544d234`
- final archive SHA-256: `c3128e8a25ffadca207858367ccbe0842ac322020ec8dd082d677d054433615f`
- quality audit: `batch-001/quality-audit.json`
- reference selection / analysis: `reference-4case-selection.json` / `reference-4case-analysis.json`
- candidate selection / analysis: `candidate-selection.json` / `candidate-analysis.json`
- comparison: `comparison-analysis.json`
