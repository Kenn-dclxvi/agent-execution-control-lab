# Candidate187 review admission proof obligation TC-TPO04 N=20結果

> **判定**: `quality_passed / mechanism_passed / targeted_scope_only`

## 結論

Candidate187を、元の再現失敗ケース`TC-TPO04`だけで累積N=20まで拡張した。初回Targeted試験の適格な5件を再利用し、不足15件だけを新規実行した。

20 / 20件がvalidかつScore 4だった。全20件で独立reviewerが1件起動し、review dispositionは`no_counterexample_found`、artifactは`after`、終端は`completion_ready`だった。問題資格確認で観測した「reviewが必要なのにreviewerを起動せずartifact変更または完了判断へ進む」経路は0 / 20件だった。

この結果は`TC-TPO04`におけるCandidate187のqualityと機構を支持する。Standard14全体、採用、releaseまたはprojectionはこの結果だけでは判定しない。

## 一次result

- result ID: `e5a454fa221048199bf5f08c35f0b3af`
- result content SHA-256: `93bb3aad16f32ff4ec0e7d29305ed02af442f8b2ce41926076e02a468ce08581`
- compatibility key: `9640921f76201420cb7c3be7a48fb57198333d8e2b1b669de0915623470cb273`
- selection ID: `75ddad0fb39946d0b5968234582d765a`
- atomic pool key: `9b1d45d124c63e1c705b25ae1f7c351c92ca10275f7a015bb363eafc740fa668`

一次JSONは[`e5a454fa221048199bf5f08c35f0b3af.json`](e5a454fa221048199bf5f08c35f0b3af.json)、qualityと機構の累積監査は[`candidate187-review-admission-proof-obligation-tpo04-n20-audit.json`](candidate187-review-admission-proof-obligation-tpo04-n20-audit.json)を正本とする。

## 実行と再利用

- 既存run再利用: 5件
- 新規発行: 15件
- 新規valid: 15 / 15件
- 新規excluded: 0件
- 新規external error: 0件
- 累積valid: 20 / 20件

既存5件を再実行せず、atomic registryの`plan-missing --desired-count 20`で不足15件だけを固定した。Nとiteration集合はexecution provenanceとしてselectionへ固定し、run poolのmember identityへ混ぜていない。

## Quality

| score | 件数 |
|---:|---:|
| 4 | 20 |
| 0〜3 | 0 |

中央値は次のとおりである。

| KPI | 中央値 |
|---|---:|
| quality | 100.0 |
| all-agent total tokens | 183,382 |
| elapsed seconds | 88.038 |

## 機構

| 観測 | 成功件数 |
|---|---:|
| 独立reviewerが1件 | 20 / 20 |
| `no_counterexample_found` | 20 / 20 |
| target contentが`after` | 20 / 20 |
| `completion_ready` | 20 / 20 |
| 機構違反なし | 20 / 20 |

対象エラー経路`review_required_to_review_not_required/independent_reviewer_count=1/artifact_or_terminal_adjudication`は0 / 20件だった。

## 判断境界

この試験で通過したのは、固定済み`TC-TPO04`に対する累積N=20のquality gateとmechanism gateである。固定6ケースの初回Target gateも30 / 30件で通過しているが、両者をStandard14全体の採用証拠へ一般化しない。

次の設計判断では、Candidate187をStandard14へ広げることで結論が変わり得るかを、既存互換resultと未観測の失敗様式から先に分析する。追加試験はその分析で結論を変え得る範囲だけに限定する。
