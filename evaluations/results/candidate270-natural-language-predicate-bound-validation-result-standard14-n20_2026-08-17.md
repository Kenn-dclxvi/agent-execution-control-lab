# Candidate270 Standard14 N=20 評価

## 結論

Candidate270（`the-caption-3ce91a4-natural-language-predicate-bound-validation-result-r1`）のStandard14を、14項目各N=20へ拡張した。登録済みN=5の70件を再利用し、不足15件×14項目、合計210件だけを新規発行した。追加210 / 210件はvalidかつScore `4`で、excluded、再試行、controller errorは0件だった。累積280 / 280件もすべてScore `4`である。

Candidate147の保存済みN=100 poolから各20件を同じ選定規則で固定した同数比較では、品質中央値は同値だった。一方、Candidate270はtoken中央値`1,643,302`、elapsed中央値`893.875`秒で、Candidate147よりtoken `+259,464`（`+18.75%`）、elapsed `+62.945`秒（`+7.58%`）だった。

required validationを持つ7項目140件のpersisted rollout監査では、134件で一つの外側callとterminal result一件のvalidation carrierが成立した。残る6件はrequired command群が2〜3個の別outer callへ分離しており、単一carrierを確認できなかった。したがって現在状態は`standard14_n20_completed / valid_280_of_280 / score4_280_of_280 / c147_n20_matched_comparison_completed / aggregate_cost_both_higher / validation_carrier_passed_134_of_140 / split_outer_calls_observed_6 / validation_carrier_mechanism_gate_failed / candidate270_not_adopted / release_not_created / projection_not_performed`とする。

## 固定条件と実行

- profile: `candidate270-natural-language-predicate-bound-validation-result-v14-reasoning-medium-standard14-global-m24-n20-cli0146-r1`
- bundle SHA-256: `481a035966f1cc6ad8faba7fd05b07baf357d29e0a75dccc563963878547c439`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI: `0.146.0`
- 外側並列上限: `M=24`
- C270 N=5基準result: `3658861abc824d52b2fd49dbba6900d3`
- comparison compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- C270 N=20登録result: [`4d2971b66f0e4754b893abd7be672aad.json`](4d2971b66f0e4754b893abd7be672aad.json)

N延長のpreflightには保存済みN=5 resultとN=5 profileを使い、N=20 profileは最終selectionのcoverageへだけ使用した。全210件を一括発行せず、容量停止線を守るため2項目×15件の30件batchを7回実行した。各batchはfull Standard14 Layer 1とN=5 resultへbindし、`ready / authorized 30 / issued 0`を確認した後、3.75 GiB見積りの容量guardが`dispatch_allowed`の場合だけ発行した。

各batchは実行後に事前観測、execution seal、Rating v14採点、atomic登録の順で閉じた。7 batchの実行時間は`108.492 / 94.170 / 127.714 / 134.850 / 105.321 / 121.574 / 157.309`秒だった。新規210件は全件valid、Score `4`である。full poolへの最終`plan-missing --desired-count 20`は14項目すべて`existing=20 / missing=0`を返した。

最初のLayer 1複製は、参照元の旧write-once receiptを新cycleへ複製したため、`comparison-generation.json`の上書き拒否でslot発行前に停止した。保存済み`reference-layer1-clean`へ切り替え、set、coverage、fixture identityを変えずにpreflightを再実行した。また第1batchの最初のowner-producer evidence生成は`--output`省略により標準出力へ返っただけで、採点はScore書込み前に停止した。出力先を固定して同じrunを採点しており、評価runの再実行は0件である。

## 品質

14項目すべて20 / 20件がScore `4`だった。成果不成立、必須command違反、許可外path変更およびcommand protocol違反は0件である。owner-producer evidenceはRating v14の`diagnostic_only`規則に従い品質点へ混ぜていない。

N=5時点の集約中央値と比べると、N=20のtoken中央値は`-3.93%`、elapsed中央値は`-3.88%`だった。これは追加15件による分布の更新であり、prompt改善として扱わない。

## validation carrier機序

[`candidate270-natural-language-predicate-bound-validation-result-standard14-n20-validation-carrier-audit-r1.json`](candidate270-natural-language-predicate-bound-validation-result-standard14-n20-validation-carrier-audit-r1.json)は、required validationを持つ7項目140件をlocal persisted rolloutの`response_item`で監査した。

| 項目 | 単一carrier成立 | 別outer callへ分離 |
|---|---:|---:|
| F01 duplicate asset key | 19 / 20 | 1 |
| F02 history date bound | 18 / 20 | 2 |
| F03 atomic cleanup | 20 / 20 | 0 |
| F04 web audit column | 18 / 20 | 2 |
| F06 empty snapshot | 19 / 20 | 1 |
| F07 canonical runner | 20 / 20 | 0 |
| F07 dependency provenance | 20 / 20 | 0 |
| 合計 | 134 / 140 | 6 |

6件の内訳はF01 iteration 9、F02 iteration 13 / 18、F04 iteration 8 / 10、F06 iteration 20である。いずれもrequired command group自体はrollout内に存在するが、各groupが異なるouter call IDへ属していた。監査schemaは単一outer resultを観測できないこれらを`unobserved`へ分類するため、source集計は`passed 134 / failed 0 / unobserved 6`である。しかし、単一carrierの成立predicateは6件でfalseであり、N=5の35 / 35成立を累積N=20で再現できなかった。

この結果から、成功時のcommand順またはwait手順を新しいprompt義務へ転記しない。6件で別outer callへ分かれることを許したpermissionまたはdependencyの辺は、この評価だけでは一意にbindできていない。Candidate270を採用せず、次Candidateも自動作成しない。

## Candidate147との3 KPI比較

Candidate147は保存済みatomic runから14項目×20件のselectionを新規作成し、Candidate270と同じ集計器で再集計した。両selectionは同じexecution stratumに属する。

| 指標 | Candidate147 | Candidate270 | 差分 |
|---|---:|---:|---:|
| quality中央値 | 100.00 | 100.00 | 0.00 |
| token中央値 | 1,383,838 | 1,643,302 | +259,464（+18.75%） |
| elapsed中央値 | 830.930秒 | 893.875秒 | +62.945秒（+7.58%） |

| 項目 | C147 token | C270 token | token差 | C147 elapsed | C270 elapsed | elapsed差 |
|---|---:|---:|---:|---:|---:|---:|
| A01 | 36,209.5 | 20,054.5 | -44.62% | 17.527秒 | 13.258秒 | -24.36% |
| A02 | 128,030.5 | 159,068.0 | +24.24% | 76.422秒 | 74.218秒 | -2.88% |
| F01 | 107,010.5 | 118,954.0 | +11.16% | 62.107秒 | 73.229秒 | +17.91% |
| F02 | 134,960.0 | 167,380.5 | +24.02% | 79.763秒 | 80.648秒 | +1.11% |
| F03 | 98,746.0 | 127,358.0 | +28.98% | 70.780秒 | 70.114秒 | -0.94% |
| F04 | 157,347.0 | 194,677.5 | +23.72% | 82.421秒 | 101.859秒 | +23.58% |
| F05 clarify | 37,401.0 | 41,644.0 | +11.34% | 22.318秒 | 26.903秒 | +20.54% |
| F05 out-of-scope | 37,321.5 | 41,871.5 | +12.19% | 22.880秒 | 27.072秒 | +18.32% |
| F06 | 105,044.5 | 134,864.0 | +28.39% | 76.694秒 | 78.876秒 | +2.85% |
| F07 canonical | 101,060.0 | 135,501.5 | +34.08% | 63.941秒 | 85.583秒 | +33.85% |
| F07 dependency | 83,585.0 | 87,004.5 | +4.09% | 58.006秒 | 53.988秒 | -6.93% |
| F08 | 100,884.5 | 135,335.5 | +34.15% | 59.709秒 | 76.283秒 | +27.76% |
| F10 entrypoint | 102,345.0 | 114,129.5 | +11.51% | 66.849秒 | 64.165秒 | -4.01% |
| F10 monthly | 93,526.0 | 137,989.0 | +47.54% | 53.743秒 | 58.127秒 | +8.16% |

tokenはA01を除く13項目で増え、elapsedは9項目で増えた。N=5とN=20のどちらでも集約tokenとelapsedがともにCandidate147より高く、N=20ではvalidation carrierの非再現も確認した。したがって、必要処理のcostかどうかを人間のtradeoffだけへ残す状態ではなく、Candidate270の採用は承認しない。

## 保存先

raw試験rootは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate270-natural-language-predicate-bound-validation-result-v14-medium-standard14-n20-cli0146-20260817-b01`から`b07`までである。各rootにpreflight、実行証拠、quality auditおよびexecution sealを保持する。最終selection、Candidate147 fresh selection、両analysis、比較viewおよびLayer 4登録receiptは`b07`へ保存した。

この結果はCandidate270 Standard14 N=20の評価完了と不採用判断を示す。release作成、THE-CAPTION本体へのprojectionおよび次Candidate作成は実施していない。
