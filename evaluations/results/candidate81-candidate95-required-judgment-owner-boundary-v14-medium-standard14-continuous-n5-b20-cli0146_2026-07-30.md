# Candidate81 / Candidate95 Rating v14 Medium標準14 N=5 B20比較

## 結論

Candidate81とCandidate95を、同じStandard14、Rating v14、Medium、Codex CLI `0.146.0`で各20 batch、各1,400件新規実行した。全2,800件がvalid・rateableで、excluded attemptは0件だった。

品質はCandidate81が1,400 / 1,400件でscore `4`、Candidate95がscore `4 / 2 / 1 = 1,398 / 1 / 1`だった。Candidate95のscore `1`はA02で不要なowner clarificationを返して未実行停止した。score `2`はF06でownerの具体的主体を質問し、必須変更とtestを実行しなかった。いずれもRating偽陰性ではなく、Candidate95の狙った境界に残った実route failureである。

Candidate95の20 batch中央値はCandidate81比で、all-agent tokenが`+90,356`（`+4.49%`）、elapsedが`+52.701秒`（`+5.53%`）だった。対応batchの二側正確Wilcoxon符号付順位検定を行い、2 KPIをHolm補正した。tokenは補正後`p=0.002325`、elapsedは補正後`p=0.000019`で、両方ともCandidate95の有意な悪化だった。

現在状態を`standard14_b20_evaluated / quality_gate_failed / route_stability_gate_failed / cost_both_significantly_higher / stopped`とする。Candidate95の採用、release、本体反映は行わない。Candidate81を採用・投影済みbaselineとして維持する。

## 固定条件

| 条件 | 値 |
| --- | --- |
| C81 prompt | `the-caption-3ce91a4-validation-wrapper-precedence-r1`、bundle SHA-256 `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` |
| C95 prompt | `the-caption-3ce91a4-required-judgment-owner-boundary-r1`、bundle SHA-256 `8c845f18bd6ed86d6f2f19281ba1257f0f1a213fa1c3466c76ede402451ee190` |
| C81 profile | `candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2` |
| C95 profile | `candidate95-required-judgment-owner-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1` |
| evaluation set | `the-caption-standard14-r1` r1、identity SHA-256 `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db` |
| repetition | 各prompt 14 case × `N=5` × 20 batch、各1,400件 |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| execution | global queue、`M=24` |
| Codex CLI | `0.146.0` |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| compatibility key | `c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c` |
| execution order | 奇数batchはC81→C95、偶数batchはC95→C81 |

両profileの差はprofile IDとprompt identityだけである。TaskSpec、14 case、fixture、rating、model、reasoning、CLI、permission、M / Nは同一である。時刻順の偏りを一方へ固定しないため、promptの実行順をbatchごとに交互にした。

## 品質とroute

| 指標 | Candidate81 | Candidate95 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 1,400 / 1,400 | 1,400 / 1,400 | 同数 |
| score `4` | 1,400 | 1,398 | C95で2件不足 |
| score `2` | 0 | 1 | F06未実行停止 |
| score `1` | 0 | 1 | A02未実行停止 |
| excluded attempt | 0 | 0 | 同数 |
| command protocol violation | 0件 / 0 run | 19件 / 10 run | C95のみ観測 |

score `4`か否かを対応slotで比較すると、Candidate81のみscore `4`が2件、Candidate95のみscore `4`は0件だった。二側正確McNemar検定は`p=0.5`であり、2件だけでは統計的有意差にならない。ただし、Candidate95の事前品質gateはscore `4`未満を1件も許容しない。したがってgateは不通過である。「有意差なし」を品質同等または採用可能とは解釈しない。

command protocol violationは10対応slotでCandidate95だけに観測され、対応するCandidate81側は0件だった。run単位の二側正確McNemar検定は`p=0.001953`である。10 runは最終成果と必須commandを満たしたためscore `4`のままだが、実行規律のdiagnostic regressionとして記録する。

### A02 score 1

- batch: 4
- iteration: 5
- run ID: `1d1e209856e04482b1c37d00f68b0913`
- failure: `a02_canonical_route_mismatch`、`a02_changed_paths_mismatch`、`a02_abstract_test_evidence_missing`
- final response: `non_machine_risk=canonical entrypoint selection`を、具体的なcriterion ownerが必要なnon-machine judgment resultと解釈した。`criterion owner=root`または担当者名を質問し、repository read、編集、testを開始しなかった。

Candidate95は「別のnon-machine judgment resultをrequiredとしないcriterionには`owner=none`」としたが、何をもってjudgment resultがrequiredかを機械的に判別するpredicateを持たない。このため、risk記載だけからowner要求へ戻る旧経路が低頻度で残った。Candidate95のA02限定B20 100件では再現しなかったが、今回の別100件で1件再現した。

### F06 score 2

- batch: 17
- iteration: 4
- run ID: `6c4c78d0c055447e8602e962f010a3d0`
- failure: `empty_snapshot_regression_missing`、許可test pathの変更欠落、focused / full pytest未実行
- final response: TaskSpecの`owner=independent contract check`を役割名にすぎないと解釈し、具体的な判断主体を質問した。checkout確認、編集、testを開始しなかった。

Candidate95はcriterion ownerを明示user inputまたはjudgment authorityを直接指定するrepository authorityへbindする。しかし、TaskSpecに明示されたowner語列を「bind済みowner identity」とするか「未具体化の役割」とするかが未定義である。この曖昧さがF06の未実行停止を生んだ。

## cost比較

| 指標 | Candidate81 | Candidate95 | C95 − C81 | 対応batch | raw p | Holm p |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| token中央値の中央値 | 2,010,298 | 2,100,654 | +90,356（+4.49%） | C95低5 / 高15 | 0.002325 | 0.002325 |
| elapsed中央値の中央値 | 952.881秒 | 1,005.581秒 | +52.701秒（+5.53%） | C95短1 / 長19 | 0.000010 | 0.000019 |
| token合計 | 202,075,433 | 208,649,337 | +6,573,904（+3.25%） | — | — | — |
| run elapsed合計 | 95,500.776秒 | 100,340.195秒 | +4,839.419秒（+5.07%） | — | — | — |

検定は対応するbatch 1〜20の中央値をpairとする二側正確Wilcoxon符号付順位検定である。二つのKPIを一つのfamilyとしてHolm補正し、`alpha=0.05`とした。対応差中央値はtoken `+51,366.5`、elapsed `+52.472秒`である。

## 各batch

| batch | C81 result ID | C95 result ID | C81 token | C95 token | C81 elapsed | C95 elapsed | C95 score |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `ed624ace311e489cb8ee7eb0c1736111` | `5d4f3decb7e14179bbd300cb0bf980b5` | 2,017,922 | 2,228,513 | 958.748秒 | 1,007.291秒 | 4×70 |
| 2 | `c14dbbabbb654572905e09588a72b662` | `8e11aa54261a4ba09d66c50b78e714dd` | 1,933,280 | 1,971,765 | 964.083秒 | 1,047.877秒 | 4×70 |
| 3 | `24ddc007998a4525ae70eaadb89cf41d` | `eb1eac9cebf64ab88e052efc7896e3b6` | 2,033,202 | 1,980,858 | 975.499秒 | 1,009.256秒 | 4×70 |
| 4 | `c3345a873c9b45d99b73e4dbb5a8a1a2` | `93b6fffaf01742eaa5bcd078cf6ba3e6` | 1,968,311 | 2,099,129 | 932.660秒 | 940.581秒 | 4×69、1×1 |
| 5 | `930521c85ac94543ad6d35f40f658aa9` | `fcf7f222c1534e95be6e39f9bcad5500` | 2,015,443 | 2,112,539 | 934.071秒 | 1,018.974秒 | 4×70 |
| 6 | `c2f2d57ec2474dad8fc903ef772e279c` | `8530bd4f08b44e71931d2e108fcb029f` | 1,911,285 | 2,168,571 | 932.004秒 | 993.404秒 | 4×70 |
| 7 | `6bef21ea92844548a7f88a4970defa55` | `44dc56fc464d4fa39b516f4e57be83a7` | 2,028,146 | 2,180,319 | 950.058秒 | 1,011.078秒 | 4×70 |
| 8 | `8e82849fd87e4c5cb18f770df9f07a45` | `3a91d10383164d3a97ea4c14361c6eec` | 1,919,897 | 2,102,179 | 926.624秒 | 1,006.442秒 | 4×70 |
| 9 | `c7e5cfd5a30247839fefa52bff19e137` | `8700e593acf444cf9be6d339ab49da2f` | 2,004,689 | 2,052,219 | 929.772秒 | 982.512秒 | 4×70 |
| 10 | `3f7a48de5537426282f1e96f6f843e87` | `ea4e54ca2c94466db8daf3c2d3f79ae0` | 2,048,073 | 2,103,276 | 972.983秒 | 986.948秒 | 4×70 |
| 11 | `1282d4c2ba6543a1ace4556e264e1c0d` | `3221b25d7cb242eea9ef165b0a80fd62` | 2,076,410 | 2,070,226 | 905.449秒 | 978.361秒 | 4×70 |
| 12 | `9be7a6f07ac44c869d8ec337f5581038` | `eaa62cefb2674875b24acd5085e27921` | 2,017,381 | 2,073,200 | 951.770秒 | 985.810秒 | 4×70 |
| 13 | `d46321749120486cb62945afe19d3e13` | `5517667b844f43bca71074ef357439d5` | 1,944,198 | 2,197,589 | 969.595秒 | 1,030.805秒 | 4×70 |
| 14 | `e20173565b3e4bc194839264b0aa7ecd` | `ee08ef35bc2d4ba78e04ce35adc0881b` | 1,974,718 | 2,012,568 | 953.992秒 | 1,006.651秒 | 4×70 |
| 15 | `d413e141067c4fb4af11cd5922d2242b` | `2d992a427b494d4886d588235034defa` | 2,075,347 | 2,012,888 | 994.562秒 | 1,041.025秒 | 4×70 |
| 16 | `b0497aebeff64442bee74e5cb6273eff` | `da698f19f76c45adb1b5f23bf7573886` | 1,989,715 | 2,034,565 | 1,008.387秒 | 994.764秒 | 4×70 |
| 17 | `aaf531fb813344a6988d65f3880639fa` | `8a69bfe003154515adc72e0744300a01` | 2,005,153 | 2,162,275 | 974.133秒 | 1,004.721秒 | 4×69、2×1 |
| 18 | `2b04fbab6b88422dbcf77992ba1fba41` | `a63a0734e5564fc1bb204a1bd922f52a` | 2,156,758 | 2,147,314 | 938.956秒 | 1,026.750秒 | 4×70 |
| 19 | `87860ab2310d4058aa6c9c3f06340164` | `64d208158c1e4ae29eb6307d9e59d8dd` | 2,107,402 | 2,123,805 | 985.880秒 | 996.478秒 | 4×70 |
| 20 | `76124c8b958a4020bb3eb5e4480b8502` | `cce4097e2e614d8b86d36301389b0951` | 1,982,533 | 1,974,842 | 932.816秒 | 985.100秒 | 4×70 |

## 保存場所

- C81 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate81-validation-wrapper-precedence-v14-medium-standard14-continuous-n5-b20-cli0146-20260730-r1`
- C95 campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146-20260730-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`

各campaignは20 result registration、execution seal、final compact receipt、execution / final evidence archiveを持つ。非公開raw evidenceはverification checkoutに保持し、このrepositoryへcommitしない。
