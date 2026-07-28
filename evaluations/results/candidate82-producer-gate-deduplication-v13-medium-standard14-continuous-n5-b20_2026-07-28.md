# Candidate82 producer gate重複削除 Rating v13 Medium 標準14項目 N=5 B20

## 結論

Candidate82の標準14項目B20は、20 / 20 batch、1,400 / 1,400件をvalidかつrateableとして完了した。20 resultはすべて独立登録し、execution sealとfinal compactまで完了した。excluded attemptと再試行は0件だった。

公式score分布は`4 / 1 = 1,399 / 1`、公式score合算率は`99.946429%`だった。score `1`のA01は、実応答が「`strict`でよいでしょうか」と質問し、編集と試験を開始せず停止していた。Rating v13の機械判定がこの質問表現を確認要求として認識しなかった偽陰性である。追記専用resultは変更せず、現在解釈だけを分離して保存する。

保存済みall-agent usageを全1,400件で再監査すると、root-onlyは1,398件、child sessionを1件起動したrunは2件だった。2件はF02の`independent contract check`とF04の`independent source check`を独立producer指定へ変換していた。どちらも成果品質はscore `4`だったが、標準14 TaskSpecは独立producer executionを明示していない。これはCandidate82設計の「不要workerが1件でもあれば停止する」に該当する。

したがってCandidate82を`standard14_b20_evaluated / stopped`とする。単発N=5の`quality_gate_passed`履歴は上書きしないが、現在の採用gateは不通過である。採用、release、runtime projection、THE-CAPTION本体反映は実施しない。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-producer-gate-deduplication-r1` |
| bundle SHA-256 | `a5a8dad8d615f4075bd399938bd621f9906d9b71c9de59425815be63027201cd` |
| evaluation set | `the-caption-standard14-r1` revision `r1` |
| repetition | 14項目 × 各`N=5` × 20 batch、計1,400 slot |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| schedule | global queue、`M=24` |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| evaluation set identity SHA-256 | `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| comparison conditions SHA-256 | `f76bf65fef7dbedd26cc7afaa66e7a4fe1af60f968d37eb88e72091dd91fcbbb` |
| compatibility key | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` |

既存Candidate82 N=5は参考resultとして保持するが、B20の20 batchには数えていない。Candidate81の同条件B20は存在しないため、B20集計をCandidate81の単発N=5と効率比較しない。

## 集計

- valid / rateable: `1,400 / 1,400`
- score `4 / 1`: `1,399 / 1`
- score `0 / 2 / 3`: `0 / 0 / 0`
- 公式score合算率: `99.946429%`
- excluded attempt / 再試行: `0 / 0`
- 20 resultのquality中央値の中央値: `100.000`
- 20 resultのall-agent token中央値の中央値: `1,913,586.5`
- 20 resultのelapsed中央値の中央値: `949.569秒`
- 1,400件all-agent token合計: `192,704,115`
- 1,400件run elapsed合計: `94,933.624秒`
- controller実行時間合計: `4,838.266秒`
- campaign開始から全保存完了まで: `5,249.646秒`、1時間27分29.646秒
- command protocol違反: `7` observation、`2` run
- F10 Monthly numeric location: `exact 98 / mismatch 2 / absent 0`

並列`M=24`のcontroller時間とrun elapsed合計は別の量である。前者はcampaign進行時間、後者は70 runの個別elapsedを各result内で合算した値であり、相互に置き換えない。

## 各batch

| batch | result ID | quality中央値 | token中央値 | elapsed中央値 | score 4 / 1 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `583afd95124d42ac839cafa466ce01ca` | 100.000 | 1,979,590 | 986.323秒 | 70 / 0 |
| 2 | `55eead30d8b244aebfe97675cd31668f` | 100.000 | 1,866,526 | 939.760秒 | 70 / 0 |
| 3 | `88025aea286547e489cc61dbc950eb85` | 100.000 | 1,956,353 | 959.771秒 | 69 / 1 |
| 4 | `59f50490eb0743aa879f557755e385d7` | 100.000 | 1,995,447 | 956.330秒 | 70 / 0 |
| 5 | `f7d86d0164ad41e386db42ebe54d13a1` | 100.000 | 1,834,954 | 924.535秒 | 70 / 0 |
| 6 | `b2419291e8b3466eaae92133f79ff1cd` | 100.000 | 1,914,188 | 970.211秒 | 70 / 0 |
| 7 | `d158bba0c2fc45ac9b0ba20aabd448d4` | 100.000 | 1,899,587 | 931.583秒 | 70 / 0 |
| 8 | `29e60e36ed5b490099ef21bbdedf7c13` | 100.000 | 1,912,985 | 905.858秒 | 70 / 0 |
| 9 | `a4c353fd3ced4c49b686483b8685b827` | 100.000 | 1,984,668 | 930.084秒 | 70 / 0 |
| 10 | `7b03e5969e694d869ca01c02736114ae` | 100.000 | 1,894,514 | 942.817秒 | 70 / 0 |
| 11 | `983fba47a7bb49d3b3c4b2c718237eb9` | 100.000 | 1,988,370 | 958.591秒 | 70 / 0 |
| 12 | `105eb1cf5f614bce99d4262376eb3ea0` | 100.000 | 1,923,592 | 955.869秒 | 70 / 0 |
| 13 | `acc43871cec04c7b8eb70747f9790629` | 100.000 | 1,928,194 | 950.589秒 | 70 / 0 |
| 14 | `0b15fcfb9fb74ca583b46d13a6a8492f` | 100.000 | 1,980,131 | 938.118秒 | 70 / 0 |
| 15 | `caabf0d515024e08bc442e6910adebdc` | 100.000 | 1,873,054 | 947.929秒 | 70 / 0 |
| 16 | `ef4392a01e854fedb9cd597bd489c389` | 100.000 | 1,982,579 | 986.766秒 | 70 / 0 |
| 17 | `490551b722754112948292eead364808` | 100.000 | 1,847,557 | 1,008.969秒 | 70 / 0 |
| 18 | `056ca70a1eb14969a06ed1d7549fe477` | 100.000 | 1,853,915 | 912.653秒 | 70 / 0 |
| 19 | `09b1ef9a1d6b4374ba3ebb641ef0ae4e` | 100.000 | 1,869,201 | 948.548秒 | 70 / 0 |
| 20 | `b3671cc3214444e68bf8d339060d49b4` | 100.000 | 1,874,515 | 978.683秒 | 70 / 0 |
| 20 result中央値 | — | 100.000 | 1,913,586.5 | 949.569秒 | 1,399 / 1（合計） |

最終行は20個の登録resultに対する記述的集計であり、新しい一次resultではない。

## score 1の現在解釈

| batch / iteration | run ID | case | 公式score | 公式failure |
| --- | --- | --- | ---: | --- |
| 3 / 2 | `beaa2744ab6f4293a49d3dad10459cf1` | A01 | 1 | `a01_clarification_disposition_missing` |

実応答は現在値`daily`と未固定条件を示した後、「変更後の`units_mode`は`strict`でよいでしょうか」と確認し、「値が確定するまで、編集とtestは開始していません」と停止した。final changed pathは0、試験・変更commandも0だった。

Rating v13の契約は未固定値を一度確認して停止することを要求する。このrunの意味は契約を満たす。一方、v13実装の機械判定は疑問符、特定の質問語、または「明示してください」系だけを確認要求として認識し、「よいでしょうか」を認識しない。したがって公式resultはscore `1`のまま保持し、prompt品質の低下とは解釈しない。rating修正または保存resultの再採点はこの判断単位で行わない。

後続のRating v14では、A01を応答文面ではなく`terminal-state-evidence/v1`で判定する。未固定値が残り、terminal responseがあり、final changed pathが0件で、試験・変更operationが未開始なら`awaiting_required_value`とする。このrunのv13公式scoreは変更せず、v14 resultとして再採点もしない。v14の新規実行結果はまだない。

## route診断

| route | 件数 |
| --- | ---: |
| root-only、session count 1 | 1,398 |
| child session 1件あり | 2 |

childを起動した2件は次のとおりである。

| batch / iteration | run ID | case | child task | score |
| --- | --- | --- | --- | ---: |
| 3 / 5 | `f20dec5176e6492988cd291c3460bb41` | F02 | `/root/independent_contract_check` | 4 |
| 15 / 2 | `324b1da118324dc78503b9f7e058e1ff` | F04 | `/root/independent_source_check` | 4 |

2件ともchildは変更・試験を行わず、rootの成果を独立確認してterminal resultを返した。成果品質は満たしたが、TaskSpecのcriterion ownerをproducer execution指定へ変換した点がCandidate82のroute条件に反する。発生率は全runで`2 / 1,400 = 0.142857%`、F02とF04の合計200件では`2 / 200 = 1.0%`だった。

command protocol違反7 observationはこの2 runだけに対応する。diagnosticでありscoreを変更しないが、不要workerの直接証拠として停止判断へ使用する。

## 判定境界

- 事実: 1,400 / 1,400件がvalid・rateableで、公式score `4 / 1 = 1,399 / 1`だった。
- 事実: 公式score `1`のrunは意味として正しく確認停止しており、Rating v13の機械判定偽陰性だった。
- 事実: 標準14で明示producer指定がないにもかかわらず、2 runがcriterion ownerをchild execution指定へ変換した。
- 判断: B20はCandidate82の低頻度route非安定性を観測したため、Candidate82を`standard14_b20_evaluated / stopped`とする。
- 未実施: 採用、release、runtime projection、THE-CAPTION本体反映。

Candidate82へ意味を補う文を追加しない。次のCandidateまたはrating変更をこのresultへ混ぜず、別の判断単位として扱う。

## 保存artifact

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate82-producer-gate-deduplication-v13-reasoning-medium-standard14-global-m24-n5-b20-20260728-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- 保存archive合計: `1,071,323,259 bytes`
- capacity sample最小free: `37,868,318,720 bytes`
- capacity sample最小projected free: `35,183,964,160 bytes`

全20 batchに`execution-seal.json`、`execution-evidence.tar.zst`、`result-registration.json`、`final-compact-receipt.json`、`final-evidence.tar.zst`が存在する。archive SHA-256とmember hashは各batchのwrite-once manifestを正本とする。
