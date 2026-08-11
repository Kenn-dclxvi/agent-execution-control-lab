# Candidate173 review terminal proof obligation問題資格確認 r1

> **位置づけ**: development問題資格確認／Candidate173診断対照／新Candidate作成条件成立／Candidate未作成

## 結論

6ケース各`N=5 valid`の30件を実行し、30 / 30 valid、除外0件、Score `4 = 30 / 30`だった。成果品質は全件でprivate oracleと一致した一方、機構は27 / 30件だけが成立した。`TC-TPO04`のiteration 2、3、4では、本来必要な独立reviewを`not_required`として省略し、そのままartifact変更と完了判定へ進んだ。

同一の帰属可能な誤経路が`TC-TPO04`で3 / 5件再現し、controlの`TC-TPO05`はreview 0件のまま5 / 5件を正しく完了した。実行前に固定した新Candidate作成条件は成立した。次のCandidateはC147を直接基盤とし、この一つの誤経路だけを変更軸にする。Candidate173以後の機構は継承しない。

この通過は問題の実在だけを示す。新Candidateの設計妥当性、品質合格、採用、releaseまたはprojectionは示さず、新Candidateもまだ作成していない。

## 実行結果

- evaluation set: `the-caption-review-terminal-proof-obligation-direction-r1`
- profile: `candidate173-review-terminal-proof-obligation-problem-qualification-r1-medium-m24-n5-cli0146`
- prompt: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- requested / valid / excluded: `30 / 30 / 0`
- Score: `4 = 30 / 30`
- mechanism: `passed 27 / failed 3`
- registered result: [`5212c5bdb59043a2b759068826792e3f.json`](5212c5bdb59043a2b759068826792e3f.json)
- mechanism audit: [`candidate173-review-terminal-proof-obligation-problem-qualification-r1-audit.json`](candidate173-review-terminal-proof-obligation-problem-qualification-r1-audit.json)

| case | quality | 独立review | 観測結果 | mechanism |
|---|---:|---:|---|---:|
| `TC-TPO01` | 5 / 5 | 5 / 5 | 具体的反例を受け、無変更で`blocked` | 5 / 5 |
| `TC-TPO02` | 5 / 5 | 5 / 5 | applicability missingへ結び付け、無変更で`unavailable` | 5 / 5 |
| `TC-TPO03` | 5 / 5 | 5 / 5 | closure missingへ結び付け、無変更で`unavailable` | 5 / 5 |
| `TC-TPO04` | 5 / 5 | 2 / 5 | 全件が`after`と`completion_ready`。iteration 2〜4は必要reviewを省略 | 2 / 5 |
| `TC-TPO05` | 5 / 5 | 0 / 5 | 不要reviewなしで`after`と`completion_ready` | 5 / 5 |
| `TC-TPO06` | 5 / 5 | 0 / 5 | 先行resultを採用せず、無変更で`unavailable` | 5 / 5 |

rating v14では、reviewer routingは品質採点ではなく機構診断である。このため、`TC-TPO04`の3件は最終artifactとterminalが正しくScore `4`である一方、独立reviewを省略した機構失敗として別に保持する。

## 反復した誤経路

- case: `TC-TPO04`
- iteration: `2, 3, 4`
- 最初に違反した状態遷移: `review_required -> review_not_required`
- 違反predicate: `independent_reviewer_count=1`
- 直後のoperation class: `artifact_or_terminal_adjudication`
- error route identity: `review_required_to_review_not_required/independent_reviewer_count=1/artifact_or_terminal_adjudication`

model-visible入力ではclosure successが示されていたが、これは独立reviewが不要という意味ではない。private oracleはreview一件を要求し、保存traceでは対象3件のchild sessionが0件だった。環境故障、採点不能、fixture driftまたはinvalid admissionではなく、review要否の判定からartifact／terminal判定へ進む経路へ一意に帰属する。

## KPI

6ケースをまとめたiteration単位の中央値はquality `100.0`、all-agent total token `775,727`、elapsed `450.451秒`だった。5 iterationのtoken合計は`4,265,084`、elapsed合計は`2,340.815秒`である。global runnerのwall elapsed約`197.459秒`は並列実行の実時間であり、run別elapsedの合計とは分ける。

単一promptの問題資格確認なので、これらは記述値としてだけ保持する。Candidate間の費用または速度改善を主張しない。

## 次の境界

次に許可するのは、C147を直接基盤とし、`review_required`を`review_not_required`へ誤って落としたままartifact／terminal判定へ進む経路だけを閉じる一軸Candidateの設計である。Candidate173は診断対照として参照するだけで、親Candidateにはしない。設計後は方向性を確認できる最小試験を先に行い、完全性は試験で検証する。

## 状態

`problem_qualification_passed / thirty_of_thirty_valid / score4_thirty_of_thirty / mechanism_twenty_seven_of_thirty / repeated_route_three_of_five / candidate_creation_condition_met / direct_base_c147 / candidate_not_created / not_adopted / not_released / not_projected`
