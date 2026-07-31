# Candidate118 / Candidate121 evidence request scope closure結果

## 結論

Candidate121は20 / 20件がvalidかつscore `4`だった。A02のimplementation bind後・最初のartifact変更前のcommand再入は0 / 5件で、token中央値は直接親Candidate119の`149,154`から`143,419`へ`5,735`（`3.85%`）減った。

一方、A02の変更後・最初のvalidation前method探索は1 / 5件再発した。F02では、location bind前に4 targetを横断してcode contentを返すlocatorが3 / 5件あり、F02 token中央値は`209,379`だった。これはCandidate118の`256,931`より`47,552`（`18.51%`）低いが、事前目標`173,000`を`36,379`（`21.03%`）上回る。

したがってquality gateは通過したが、mechanism gateとF02 cost gateは不通過である。A02 / F02拡張試験、Standard14、採用、release、runtime projection、本体反映へ進めず、Candidate121を`stopped`とする。

## Identityと互換条件

- candidate: `the-caption-3ce91a4-evidence-request-scope-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`（Candidate119）
- non-parent: `the-caption-3ce91a4-implementation-edit-ticket-closure-r1`（Candidate120）
- bundle SHA-256: `7895e458bde78bee4fa560420d09b87482b4af6d6963ae77406337d03be33aa1`
- Evaluation set: `the-caption-standard14-r1` / `r1`からA01 r2、A02 r2、F01 r3、F02 r1を選択
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- case別N: 5
- profile上のM: 24
- atomic comparison key: `65301eae7c45c0d30af09c6e0659c92d698cdeb603edfdefd2d6dcbea5cb0d4a`
- result compatibility key: `5fd07842276b862329d72268b59256341c4869c85ccec19c7a534aa669a7a083`

Candidate121はCandidate119のroot `AGENTS.md`にある`EVIDENCE_GATE`だけを置換した。evidence invocationの発行前に、未解決predicateまたはterminal disposition、admission済みtarget、decision-relevant result scope、result受領後に確定する判断をbindする`evidence_request_ready`を追加した。location未特定時のlocator resultはpath / line / symbol identityへ限定し、その後はbind済みspanだけを読む。TaskSpec、case、fixture、rating、executorは変更していない。

比較preflightでは、既存Candidate118 Standard14 resultの14-case coverageと今回の4-case coverageが一致しなかったため、slot発行前に停止した。Candidate118の既存atomic poolからA01 / A02 / F01 / F02各5件だけを選び、新規runなしで4-case基準result `9e97af352b104addbd1b67e06bebad46`として登録した。そのresultへbindしたpreflightが20 slotを認可した後にCandidate121だけを発行した。

## 実行と品質

- 新規発行: Candidate121の不足20 runだけ
- execution: 20 / 20 valid、excluded 0、external failure 0
- parallel execution wall time: `116.091`秒
- quality: score `4` × 20
- A01: required value待ち5 / 5、変更0 / 5、test 0 / 5
- A02: canonical成果5 / 5、successful test evidence 5 / 5
- F01: required command evidence完備5 / 5、command protocol違反0件
- F02: focused / full required validation完備5 / 5
- pool key: `2cb4e28c05733c8e3006fd05fb275377ec96936b3a7b47533712fb77c4742566`
- selection ID: `265543fe7f9a4875ad4ae1a80174d406`
- analysis ID: `b73009a2eba04b649867882ce3f752eb`
- result ID: `555784ace7a64451939012731d6b0a29`

## KPI

4 caseのCandidate118基準は、同じatomic run poolから選んだ既存20 runである。

| 4-case集約中央値 | Candidate118 | Candidate121 | 差 |
| --- | ---: | ---: | ---: |
| quality | `100.000` | `100.000` | `0.000` |
| all-agent token | `642,176` | `527,739` | `-114,437`（`-17.82%`） |
| elapsed | `250.667`秒 | `292.691`秒 | `+42.024`秒（`+16.76%`） |

case別token中央値は次のとおりである。

| case | Candidate118 | Candidate121 | 差 |
| --- | ---: | ---: | ---: |
| A01 | `18,431` | `18,157` | `-274` |
| A02 | `226,321` | `143,419` | `-82,902` |
| F01 | `120,050` | `139,940` | `+19,890` |
| F02 | `256,931` | `209,379` | `-47,552` |

直接親Candidate119との互換A02比較では`149,154 → 143,419`、差`-5,735`（`-3.85%`）である。F02の事前cost gateはCandidate107実績`173,000`以下であり、Candidate121は`36,379`（`21.03%`）上回った。4-case集約値または少数caseの値をStandard14へ一般化しない。

## Mechanism監査

| 判定項目 | Candidate121 | gate |
| --- | ---: | --- |
| A02 implementation bind後・変更前command再入 | `0 / 5` | pass |
| A02変更後・最初のvalidation前method探索 | `1 / 5` | fail |
| F02 location bind前の複数target content locator | `3 / 5` | fail |
| F02 locator後のcontent readがbind済みspanだけ | `5 / 5` | pass |
| F02 focused / full required validation | `5 / 5` | pass |

A02の再発runは`e6a4d68f3d8a450983c00d02c3910d71`である。canonical entrypointと変更1行を確定して`run.sh`を変更した後、最初のvalidation前に、test file locator、`tests/AGENTS.md`、test symbolを3 commandで追加探索した。最終成果とrequired validationは成功し、tokenは`242,584`だった。これはquality失敗ではなく、Candidate119で成立した変更後method境界の非保持である。

F02の`748f28d315a546f4b132474055170b76`、`d777cb47eaa44889aeec568aa94d030f`、`e31a84e02c894747a73d4127e5b7d7d6`は、locationをbindする最初のinvocationで2 sourceと2 testを同時に検索し、約16〜19KBのcode contentを返した。Candidate118の高cost 3件で観測した`rg -C`型の約81〜92KB resultは再発しなかったが、path / line / symbol identityだけへ閉じるCandidate121の発行前境界は成立していない。

残るF02 2件は、1件が4 targetのfunction / class symbol locator、1件がtargetごとのlocatorを使った。その後は5 / 5件とも、明示したcriterionに対応するsource / test spanだけを読んで実装へ進んだ。したがってCandidate121は巨大な周辺context取得を縮小したが、location bind前のcontent scopeを安定してidentityだけへ限定できなかった。

## 判定と次の調査境界

Candidate121の一変更軸は、A02の変更前terminal closureとA02 costを改善した。一方で、同じ`EVIDENCE_GATE`内にlocator identity、content scope、変更後validation methodの保持条件を含めても、全経路を閉じなかった。

後続の[`F02 evidence route分析`](../../docs/candidate121-f02-evidence-route-analysis.md)で、C121 / C118 / C107各5 traceを対応付けた。C121は変更前evidence bytes中央値をC118の`110,667`から`41,410`へ減らし、C107の`53,938`も下回ったが、tokenはC107水準へ届かなかった。bytes、最初のtarget数、evidence invocation数、validation再入のどれか一つでは高低を分離できない。

次の変更軸候補は、TaskSpecが同一predicateへ使うexact target setを列挙済みの場合だけ、locatorを独立resultにせず一つのcontent evidence waveへまとめ、そのterminal resultを`edit-ready`または`stop`にする`prechange evidence wave closure`である。Candidate50の一般read batchingとは適用条件が異なる。Candidateを作る場合はCandidate119を直接親とし、C121のlocator-identity必須条件は継承しない。

## 状態

`targeted_a01_a02_f01_f02_evaluated / quality_gate_passed / a02_prechange_terminal_closure_passed / postchange_method_boundary_failed / f02_locator_scope_failed / a02_cost_target_passed / f02_cost_target_failed / result_registered / stopped`

## 証跡

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate121-evidence-request-scope-closure-v14-medium-a01-a02-f01-f02-atomic-n5-cli0146-20260731-r1`
- execution archive SHA-256: `ed286b4d76db7f254c2ca8d527e2417375f3d3865befd2703de4807d8911d819`
- final archive SHA-256: `e8a7105e68f71f001fcdac69516754de6c19542807a8e7b7013f610cd2436787`
- quality audit: `batch-001/quality-audit.json`
- reference selection / analysis: `reference-selection.json` / `reference-analysis.json`
- candidate selection / analysis: `candidate-selection.json` / `candidate-analysis.json`
- comparison: `comparison-analysis.json`
