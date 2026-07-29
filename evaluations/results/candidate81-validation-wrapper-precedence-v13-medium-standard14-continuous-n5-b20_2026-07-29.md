# Candidate81 validation wrapper precedence Rating v13 Medium 標準14項目 N=5 B20

## 結論

Candidate81の標準14項目B20は、20 / 20 batch、1,400 / 1,400件をvalidかつrateableとして完了した。20 resultは独立登録し、全batchでexecution sealとfinal compactまで完了した。excluded attemptと再試行は0件だった。

公式score分布は`4 / 1 = 1,399 / 1`、公式score合算率は`99.946429%`だった。score `1`のA01は「既定値を`strict`に変更する、という理解でよいでしょうか」と質問し、編集とtestを開始せず停止していた。Candidate82 B20のA01と同じく、Rating v13が「よいでしょうか」を確認要求として認識しない機械判定偽陰性である。一次resultは変更しない。

保存済みall-agent usageを全1,400件で再監査すると、全件がroot-onlyかつsession count 1だった。Candidate82 B20は1,398件がroot-onlyで、F02とF04の各1件がchildを起動した。したがって、今回のC81ではC82で停止理由となった低頻度route非安定性を観測しなかった。

ただしC81とC82のevaluation-set identityは一致しない。fixtureのfile内容とtarget commit / treeは同一だが、C82は通常file / directory modeが`0644 / 0755`、C81は`0600 / 0700`で固定された。このmode差によりfixture digest、evaluation-set identity、compatibility keyが変わった。以下のC82差は記述的比較であり、互換Layer 4 comparison、winner、採用判断には使わない。

Candidate81の今回の評価状態を`standard14_b20_evaluated / descriptive_comparison_only`とする。Candidate82の`standard14_b20_evaluated / stopped`履歴は変更しない。このB20から新しい採用、release、runtime projection、本体反映判断は行わない。既存のCandidate81 releaseは別stateで`approved / projected`のままである。

## 固定条件

| 条件 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-validation-wrapper-precedence-r1` |
| bundle SHA-256 | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` |
| evaluation set | `the-caption-standard14-r1` revision `r1` |
| repetition | 14項目 × 各`N=5` × 20 batch、計1,400 slot |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-abstract-condition-preserving-owner-diagnostic-v13` |
| schedule | global queue、`M=24` |
| token accounting | all-agent v1 |
| target commit / tree | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` / `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| evaluation set identity SHA-256 | `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33` |
| comparison conditions SHA-256 | `f76bf65fef7dbedd26cc7afaa66e7a4fe1af60f968d37eb88e72091dd91fcbbb` |
| compatibility key | `bd9e4d98750e9472d024b0de07442b5f257c2fbaf3b03aad20d76d2edc791438` |

## C81集計

- valid / rateable: `1,400 / 1,400`
- score `4 / 1`: `1,399 / 1`
- score `0 / 2 / 3`: `0 / 0 / 0`
- 公式score合算率: `99.946429%`
- excluded attempt / 再試行: `0 / 0`
- 20 resultのquality中央値の中央値: `100.000`
- 20 resultのall-agent token中央値の中央値: `2,367,907`
- 20 resultのelapsed中央値の中央値: `936.670秒`
- 1,400件all-agent token合計: `236,855,792`
- 1,400件run elapsed合計: `94,034.242秒`
- controller実行時間合計: `4,680.542秒`
- campaign開始から全保存完了まで: `5,051.934秒`、1時間24分11.934秒
- command protocol違反: `0`
- F10 Monthly numeric location: `exact 93 / mismatch 7 / absent 0`
- route: root-only `1,400 / 1,400`、child session `0`

## Candidate82との差（記述的比較）

差分方向は`C81 - C82`である。fixture mode差によりcompatibility keyが異なるため、差を改善・悪化またはwinnerへ読み替えない。

| 指標 | C81 | C82 | 差 |
| --- | ---: | ---: | ---: |
| valid / rateable | 1,400 / 1,400 | 1,400 / 1,400 | 0 |
| score `4 / 1` | 1,399 / 1 | 1,399 / 1 | 0 / 0 |
| 20 result token中央値の中央値 | 2,367,907 | 1,913,586.5 | `+454,320.5`、`+23.74%` |
| 1,400件token合計 | 236,855,792 | 192,704,115 | `+44,151,677`、`+22.91%` |
| 20 result elapsed中央値の中央値 | 936.670秒 | 949.569秒 | `-12.898秒`、`-1.36%` |
| 1,400件run elapsed合計 | 94,034.242秒 | 94,933.624秒 | `-899.382秒`、`-0.95%` |
| controller実行時間合計 | 4,680.542秒 | 4,838.266秒 | `-157.723秒`、`-3.26%` |
| campaign全保存時間 | 5,051.934秒 | 5,249.632秒 | `-197.698秒`、`-3.77%` |
| root-only | 1,400 | 1,398 | `+2` |
| childありrun | 0 | 2 | `-2` |
| command protocol違反 | 0 | 7 | `-7` |
| F10 numeric location mismatch | 7 | 2 | `+5` |

品質分布は同じだった。C81はC82よりtokenが大きく、elapsedは小さい方向だった。routeはC81が全件root-onlyで、C82だけが2件の不要childを起動した。token、elapsed、routeの方向が分かれ、かつfixture identityも一致しないため、C81またはC82の採用結論は出さない。

## 各batch

| batch | result ID | quality中央値 | token中央値 | elapsed中央値 | score 4 / 1 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | `e0aca2c6f08b4a07adac77237f96cdb0` | 100.000 | 2,252,462 | 989.329秒 | 70 / 0 |
| 2 | `031b7ac712554da8a16d46d756f6de0a` | 100.000 | 2,473,409 | 1,007.824秒 | 70 / 0 |
| 3 | `985817768b144ff1ac5cde39c3641897` | 100.000 | 2,284,407 | 948.315秒 | 70 / 0 |
| 4 | `57eed5c75e5e4fa9aa84981e240519a9` | 100.000 | 2,296,518 | 912.873秒 | 70 / 0 |
| 5 | `b3a32f3d78b945f5acdb1c4d13e48c51` | 100.000 | 2,677,704 | 983.432秒 | 69 / 1 |
| 6 | `0afd6ed900e046d7870da39f1ee0d9e5` | 100.000 | 2,292,293 | 914.232秒 | 70 / 0 |
| 7 | `5ab22456c91541b4a99ad54bbf466123` | 100.000 | 2,484,426 | 989.486秒 | 70 / 0 |
| 8 | `826cdcdce3934945804f5e9fa63c7f25` | 100.000 | 2,399,276 | 936.844秒 | 70 / 0 |
| 9 | `cbcdce2f1ae44cb0bb0ebac66c5a0ab7` | 100.000 | 2,429,936 | 942.109秒 | 70 / 0 |
| 10 | `41769588804d4c5c82a39cc872f8d067` | 100.000 | 2,396,493 | 920.849秒 | 70 / 0 |
| 11 | `b7544304b70f4a09be8455d98a27522c` | 100.000 | 2,365,139 | 895.293秒 | 70 / 0 |
| 12 | `109b72d9db7a40dd9000b2e1d68ea0ed` | 100.000 | 2,265,411 | 917.403秒 | 70 / 0 |
| 13 | `fb0910ff779349658660a23b17d839e6` | 100.000 | 2,269,413 | 965.336秒 | 70 / 0 |
| 14 | `6b28876a831f4227847e9e70f88cb1ce` | 100.000 | 2,405,091 | 948.695秒 | 70 / 0 |
| 15 | `87d04c5a8d1048179fc6fc2dc66ffc37` | 100.000 | 2,321,647 | 957.264秒 | 70 / 0 |
| 16 | `f60c9a5def6349b4828428139e699feb` | 100.000 | 2,351,690 | 908.672秒 | 70 / 0 |
| 17 | `a4db2f9ee8d747028e9cde43870d25c5` | 100.000 | 2,183,839 | 930.921秒 | 70 / 0 |
| 18 | `cacf339cdcdf463b8d9db4d17982b170` | 100.000 | 2,370,675 | 936.128秒 | 70 / 0 |
| 19 | `8b9edca596264e9495f5339ee9f409b0` | 100.000 | 2,466,175 | 936.497秒 | 70 / 0 |
| 20 | `5e8b47d1943b47dd89b85e4023eace61` | 100.000 | 2,417,917 | 921.840秒 | 70 / 0 |

## 保存artifact

- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate81-validation-wrapper-precedence-v13-reasoning-medium-standard14-global-m24-n5-b20-20260729-r1`
- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- 保存archive合計: `1,141,992,674 bytes`

全20 batchに`execution-seal.json`、`execution-evidence.tar.zst`、`result-registration.json`、`final-compact-receipt.json`、`final-evidence.tar.zst`が存在する。archive SHA-256とmember hashは各batchのwrite-once manifestを正本とする。
