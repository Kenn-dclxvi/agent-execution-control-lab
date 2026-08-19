# P006 THE-CAPTION投影 Standard14 N=5評価

## 結論

P006のroot `AGENTS.md`をTHE-CAPTIONへ投影し、P005の非root 18 targetをbyte一致で保持した条件で、Standard14の14項目を各5件評価した。70 / 70件が`valid`かつScore `4`だった。

P005との互換比較では、5回の14項目集約中央値がtoken `-10.57%`、elapsed `-3.90%`だった。品質を維持したまま3 KPI上のcostは両方減った。一方、Candidate147比ではtoken `+21.75%`、elapsed `+13.86%`が残る。

trace診断では、raw traceが三者で揃う11 Caseについて、P006のmodel responseはP005の240件から224件へ減った。しかし、P006が直接閉じる対象としたF08では5 / 5件とも、開始identityとclean statusのresultをmodelへ返した後に対象readを別model responseから発行した。F08のmodel response中央値もP005と同じ5件である。したがって、aggregate cost改善は観測されたが、`FRONTIER_CARRIER_CODEX`によるC147 frontier移植の機序成立は確認できない。

現在状態は`standard14_n5_completed / quality_gate_passed / p005_cost_both_lower / c147_cost_regression_persists / frontier_nonconformance_observed / p006_delta_causal_attribution_not_established / independent_mechanism_gate_retracted / n20_eligible_not_started / p006_canonical_unchanged / adoption_not_decided / release_not_created / runtime_projection_not_authorized`とする。N=5の差を安定傾向とは扱わず、N=20へ自動拡張しない。

## identityと互換条件

- P006正本: `p006-portable-full-agent-codex-frontier-carrier-r1`
- P006 root SHA-256: `669a66d8350e250260922eb25706a11f0e75b5aeb1064ca323a62a9be26c5c91`
- Standard14投影bundle: `p006-the-caption-standard14-projection-r1`
- 投影bundle SHA-256: `8ef34227c5affaa099bc7e25700829f017794d289f480c2d2a161b537e6d204b`
- profile: `p006-the-caption-standard14-projection-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- permission: `workspace-write / never`
- 設定上の並列上限: `M=24`
- token accounting: all-agent v1
- 直接比較基準: P005 result `28082254ecc6447f8d76d63e85062299`
- 副比較基準: Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- P006投影result: [`684cb3c380bc4b28a65680f415ecb8e6.json`](684cb3c380bc4b28a65680f415ecb8e6.json)

投影bundleはP005 bundleと同じ19 targetを持ち、root `AGENTS.md`だけをP006 bytesへ置換した。P005との差は`FRONTIER_CARRIER_CODEX` 1,763 bytesだけである。preflightはprompt identity以外の条件を照合し、14項目×5件の70 slot、発行済み0件、status `ready`を固定した。

新規70件は232.317秒の外側実行で完了し、valid 70、excluded 0、再試行0、controller error 0だった。

## 品質

Rating v14では70 / 70件がScore `4`で、成果不成立、必須command失敗、許可外path変更および採点failureは0件だった。

owner-producer evidence不成立54件を診断情報として記録した。command protocol violationは0件で、F10 monthlyのnumeric locationは5 / 5件がexactだった。Rating v14では診断情報を成果品質へ混ぜていない。

## 3 KPI比較

Candidate147とP005は、同じcompatibility keyを持つ保存済みatomic runから14項目×5件を選択し、P006と同じ集計器で再集計した。

| 指標 | Candidate147 | P005投影 | P006投影 | P006-C147 | P006-P005 |
| --- | ---: | ---: | ---: | ---: | ---: |
| quality中央値 | 100.00 | 100.00 | 100.00 | 0.00 | 0.00 |
| token中央値 | 1,447,626 | 1,970,857 | 1,762,521 | +314,895（+21.75%） | -208,336（-10.57%） |
| elapsed中央値 | 852.543秒 | 1,010.082秒 | 970.730秒 | +118.187秒（+13.86%） | -39.352秒（-3.90%） |

## 項目別KPI

各値は同一項目5件の中央値である。差分率はP006を左記の比較対象に対して計算した。

| Case | C147 token | P005 token | P006 token | 対C147 | 対P005 | C147秒 | P005秒 | P006秒 | 対C147 | 対P005 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 19,195 | 36,580 | 19,127 | -0.4% | -47.7% | 12.148 | 17.054 | 11.871 | -2.3% | -30.4% |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 129,085 | 203,624 | 143,446 | +11.1% | -29.6% | 73.379 | 97.754 | 90.071 | +22.7% | -7.9% |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 107,202 | 144,610 | 159,835 | +49.1% | +10.5% | 66.424 | 74.229 | 88.278 | +32.9% | +18.9% |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 128,236 | 250,072 | 228,495 | +78.2% | -8.6% | 100.607 | 111.245 | 108.041 | +7.4% | -2.9% |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 104,320 | 164,494 | 145,414 | +39.4% | -11.6% | 70.866 | 100.423 | 98.302 | +38.7% | -2.1% |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 151,170 | 196,763 | 168,015 | +11.1% | -14.6% | 91.431 | 124.681 | 91.226 | -0.2% | -26.8% |
| `TC-F05-CLARIFY-UNITS-MODE` | 37,242 | 39,618 | 42,162 | +13.2% | +6.4% | 26.725 | 17.728 | 20.575 | -23.0% | +16.1% |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 37,366 | 39,797 | 42,154 | +12.8% | +5.9% | 25.291 | 20.419 | 21.027 | -16.9% | +3.0% |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 151,542 | 151,513 | 156,596 | +3.3% | +3.4% | 79.393 | 80.465 | 71.736 | -9.6% | -10.8% |
| `TC-F07-CANONICAL-V4-RUNNER` | 102,504 | 151,826 | 144,437 | +40.9% | -4.9% | 72.547 | 88.799 | 88.879 | +22.5% | +0.1% |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 87,284 | 100,259 | 112,029 | +28.3% | +11.7% | 54.324 | 54.703 | 57.905 | +6.6% | +5.9% |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 113,067 | 119,932 | 127,099 | +12.4% | +6.0% | 56.343 | 79.126 | 83.577 | +48.3% | +5.6% |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 87,934 | 110,600 | 115,847 | +31.7% | +4.7% | 61.546 | 64.905 | 71.358 | +15.9% | +9.9% |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 93,096 | 98,857 | 104,704 | +12.5% | +5.9% | 51.796 | 47.159 | 51.471 | -0.6% | +9.1% |

P005比ではtokenが7 / 14項目、elapsedが7 / 14項目で減った。改善は全項目一様ではなく、A01、A02、F04の寄与が大きい。直接の狙いに挙げたF07 dependency、F08、F10 entrypointはいずれもP005比でtokenとelapsedが増えた。N=5の項目別中央値だけを各条文の固定効果へ一般化しない。

## frontier機序診断

P005監査と同じく、C147の選択済みN=5 archiveにraw traceがないF01、F02、F03を除き、11 Case各55 runの`codex-events.jsonl`を診断に使った。model-visibleな`agent_message`の総数はP005の240件からP006の224件へ16件減った。A02の中央値は7件から5件へ減った一方、F07 canonical、F07 dependency、F08、F10 entrypointは中央値が変わっていない。

F08では5 / 5件とも、第一model responseから開始identityとclean statusだけを発行し、そのterminal result受領後の第二model responseからauthority、対象文書、weekly / monthly entrypointを発行した。`FRONTIER_CARRIER_CODEX`が閉じるとした「frontier全memberのcommit前に個別resultをmodel-visible inputへ返す経路」が、このCaseでは残っている。

これは品質failureではない。またP006のaggregate cost改善を否定しない。N=5直後は、P006の追加blockと狙ったroute closureの対応を示せないことを`quality_gate_passed / mechanism_gate_failed`として分けた。後続再監査では、この機序判定を独立gateとして扱わないよう修正した。

## 後続再監査による判定修正

F08のTaskSpecはdriftまたはdirty stateで編集を禁止するが、指定文書、authorityおよびentrypointのreadを禁止していない。P005から保持した共通`FRONTIER`も、drift時にobservationが禁止されずtargetとpermissionが変わらない場合、identity observationと許可済みobservationを同じfrontierへ入れるよう明示している。したがって、F08の5件はP006が合法に残したrouteではなく、既存条項へのnonconformanceである。

P006の追加blockは、共通`FRONTIER`が正しい複数member集合を構成済みであることを前提にした再記述であり、P005から新たに削除したprompt準拠permission edgeを示せない。F08の全件はScore `4`で、機序nonconformanceと品質不成立の100%対応もないため、`frontier_mechanism_gate_failed`を独立した合否状態から撤回する。登録result、Score、3 KPI、traceおよび当初判定は変更しない。

現在解釈、P007を作成しない理由、およびN=20の不足slotは[`P006 frontier carrier結果後因果再監査`](../../docs/p006-frontier-carrier-post-result-causal-reassessment.md)を正とする。

## 保存先と境界

raw試験rootは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/p006-the-caption-standard14-projection-v14-medium-standard14-n5-cli0146-20260819-r1`である。preflight、70件の実行証拠、quality audit、P006・P005・C147のselection・analysis・comparison、execution seal、result登録およびfinal compactを保持する。execution archive SHA-256は`0bea2bd4ce4a9edc39ad25aa3079015ea6ce0f9277285d3316719d359126ef24`、final compact archive SHA-256は`b89013c705020cf250ffed547c3d29d78a9861dff0d062d8cbf3f70a6153081a`である。

execution seal後のCodex project config cleanupは、明示した`cycle-p005-reference`配下のpruned workspace pathをcleanup側が想定外としたwarningを1件記録した。archiveのhash検証、workspace prune、result登録およびfinal compactは成功しており、このwarningをexecution validityまたはqualityへ混ぜていない。

この結果はTHE-CAPTION Standard14上のP006投影評価だけを示す。P006正本、採用、release、他platformへの配置およびruntime projectionは変更していない。
