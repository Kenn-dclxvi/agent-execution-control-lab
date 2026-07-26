# click control-free F01-only P1-c N=5 B=3

## 結論

P1-cは、同じBundle A identityと`N=5` profileを固定した独立3 result、計15 / 15件がvalid・rateableで、全件score `4`だった。batch中央値の中央値はall-agent token `189,033`、elapsed `80.590`秒である。

batch中央値のrangeはtoken `26,878`（中央値比`14.22%`）、elapsed `1.501`秒（中央値比`1.86%`）だった。これは1 caseにおける同一Bundle Aのbatch間基準線である。標準14項目、Bundle間の差、採用、release、本体反映を示さない。

## 固定identity

| 項目 | 値 |
| --- | --- |
| profile | `click-control-free-f01-only-global-m24-n5-r1` |
| prompt identity | `click-00e592c-control-free-r1` |
| bundle SHA-256 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` |
| evaluation set | `click-f01-only-r1` |
| set identity SHA-256 | `cc0582d2327088f6790bd4bf2b5e84e9ef5f288b64c35660d0cff4ebf08b0a38` |
| case | `CLICK-F01-ANSI-SEQUENCE-STRIP` r1 |
| model / reasoning | `gpt-5.6-sol` / `high` |
| compatibility key | `bc44567542c938534cbdc2dc7520228514e3cdd55c476182b90a549f5fc0a79a` |

3 resultは同じcompatibility keyを持つ。P1-c用の別profileやcontent-identicalなBundle Bは作成していない。

## batch中央値

| batch | result ID | result content SHA-256 | quality | token | elapsed秒 |
| ---: | --- | --- | ---: | ---: | ---: |
| 1（P1-b） | `d83aab21064c4425b690a922ba0e2877` | `6bd06cac99c9b8a184e469113705c98e9bfac60c8aeba660790bc49d16748178` | 100.000 | 189,977 | 80.475 |
| 2 | `80a0c99d81d14092aa66868e6476341c` | `8586b5761060f52cfb39c6e10146a9751d2d158fb676b0d95bd2b21ffdd40e50` | 100.000 | 189,033 | 80.590 |
| 3 | `3e9a62c6eb99423299d9d00a1174e1e3` | `5e70d6b65e5d6a33c4f1147902d6f9018232764cf125b163ea7be414e258a8b5` | 100.000 | 163,099 | 81.976 |

| KPI | batch中央値の中央値 | 最小 | 最大 | range | range / 中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `quality_score` | `100.000` | `100.000` | `100.000` | `0.000` | `0.00%` |
| all-agent `total_tokens` | `189,033` | `163,099` | `189,977` | `26,878` | `14.22%` |
| `elapsed_seconds` | `80.590` | `80.475` | `81.976` | `1.501` | `1.86%` |

## 15 runの観測値

| batch | iteration | run ID | raw score | all-agent token | elapsed秒 |
| ---: | ---: | --- | ---: | ---: | ---: |
| 1 | 1 | `16835a154ce44f2694746ddc81edca62` | 4 | 202,176 | 80.475 |
| 1 | 2 | `fa4eee3918a9457e81419deec1bb6b2e` | 4 | 170,228 | 79.569 |
| 1 | 3 | `102607e7939e4c919c36a2adbce145b9` | 4 | 198,376 | 79.323 |
| 1 | 4 | `aadf7b4104dc47a4ab206ad53c8165fd` | 4 | 189,977 | 85.443 |
| 1 | 5 | `4de6eb40979e46418d87e1f14678d87e` | 4 | 174,959 | 85.349 |
| 2 | 1 | `416f23c87e71428baa8af36b42a03b7f` | 4 | 208,321 | 87.873 |
| 2 | 2 | `2c28540f93f141ddab2ba94512d99183` | 4 | 180,096 | 67.226 |
| 2 | 3 | `a4bfe7db314d4a0b9879782ced93c417` | 4 | 169,693 | 68.966 |
| 2 | 4 | `0e35419d9f0c4c2099ffb6e450fde4a2` | 4 | 207,299 | 106.572 |
| 2 | 5 | `bad832b6744c4caba4c7db6c31ee5cd0` | 4 | 189,033 | 80.590 |
| 3 | 1 | `250b6aec7fd24ba688c32afd6f580842` | 4 | 185,915 | 81.976 |
| 3 | 2 | `9adebf1c1b1c4dafbe1e7f9ebaff66d7` | 4 | 144,401 | 67.119 |
| 3 | 3 | `512f68b89b8e423ab547ca63ac1c4c25` | 4 | 163,099 | 86.299 |
| 3 | 4 | `855cd40082b048b28313091de7c7f1b9` | 4 | 144,037 | 70.248 |
| 3 | 5 | `72ffacf9c95c48e499ea59989d4eccea` | 4 | 178,482 | 86.171 |

15 run全体の中央値はtoken `180,096`、elapsed `80.590`秒だった。run単位の最小 / 最大はtoken `144,037` / `208,321`、elapsed `67.119` / `106.572`秒である。P1-cの主目的はbatch間の基準線なので、比較値には上表のbatch中央値を使う。

## 成果とgate

15 runすべてで最終changed pathは`src/click/_compat.py`だけだった。CSI除去用の正規表現は固定rating contractが求めるparameter byte、intermediate byte、final byteの範囲を満たした。

- focused gateとfull gateは全runでexit `0`
- required command evidenceは各runで2 / 2 successful
- protocol違反、許可外drift、adapter-owned cleanup試行、外部失敗は0件
- child sessionは全runで0件、excluded attemptも0件

## 次の境界

Bundle Aの1 caseにおける成立確認とbatch内・batch間基準線は確立した。次は残り13項目を1 caseずつqualificationし、追加caseだけ各`N=3`でBundle Aの成立を確認する。その後に14項目setを固定し、Bundle AでClick Std14 `14 × N=5 = 70`を実行する。

Bundle BはClick Std14 baseline確立後に、1軸だけを変更した実Candidateとして作成する。

## 保存境界

3件のregistry resultとraw execution evidenceはverification environmentへappend-onlyで保存した。repositoryにはこの公開要約を置き、raw run log、session file、fixture workspaceはcommitしない。
