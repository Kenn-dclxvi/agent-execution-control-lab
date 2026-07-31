# Click Candidate125 Medium Standard14 r2 N=5 CLI 0.146

## 結論

Clickへ水平適用したCandidate125は、事前に固定したStandard14 r2品質gateを通過した。
70 / 70件がvalidかつrateableで、F10以外の13 caseは65 / 65件がscore `4`だった。
Repository Authorityを持たないF10は5 / 5件が`authority_unavailable`で停止し、
既存契約どおりscore `1`だった。unexpected drift、required command failure、excluded
attemptは0件だった。

公式3 KPIの中央値はquality `94.643`、all-agent token `1,348,515`、elapsed
`786.007`秒だった。保存済みClick C81はCodex CLI `0.144.0`、Candidate125は
`0.146.0`でcompatibility keyが異なるため、tokenとelapsedの差は算出しない。

## 固定条件

- set: `click-standard14-r2` / `r2`
- prompt: `click-00e592c-criterion-complete-single-target-continuation-r1`
- bundle SHA-256: `2a94d070a9f2a4f130f50b33e341d45ece09eeb38113c486acc4bae71a513e3c`
- profile: `click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent / CLI: Codex / `0.146.0`
- target runtime: Python `3.14.5` / `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`
- rating: `click-outcome-abstract-condition-preserving-v10`
- Case / N / M: `14 / 5 / 24`
- permission: `workspace-write / never`
- set identity: `bbba58d8eb5c3dc6719a155d031d886917c2fed7bec19faf9a43dd65705f7ebe`
- result ID: `7560599fef024dfb8011264352707ab8`
- compatibility key: `39dcb70f20256935b2e257e57cda1cba0c1f15d41ca77bb4e5b4c13734484472`

## 全体結果

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | `70 / 70` |
| score分布 | `4 = 65`、`1 = 5` |
| F10 route | `authority_unavailable = 5` |
| quality中央値 | `94.643` |
| all-agent token中央値 | `1,348,515` |
| elapsed中央値 | `786.007`秒 |
| attempt | `70`（再実行0） |
| excluded attempt | `0` |
| runner wall time | `233.115`秒 |

iteration別tokenは`1,398,657 / 1,455,270 / 1,344,861 / 1,325,970 /
1,348,515`、elapsedは`833.068 / 841.059 / 786.007 / 777.333 / 763.091`秒だった。

## case別N=5

| case | score `4` | token中央値（range） | elapsed中央値（range） |
| --- | ---: | ---: | ---: |
| A01 latent context policy | 5 / 5 | `38,618`（`35,638–124,256`） | `23.625`秒（`21.526–61.420`） |
| A02 repository-resolvable tox routing | 5 / 5 | `159,296`（`131,299–195,628`） | `89.249`秒（`68.877–103.709`） |
| F01 ANSI sequence strip | 5 / 5 | `96,181`（`82,189–99,612`） | `58.573`秒（`58.077–66.768`） |
| F02 stream deprecation contract | 5 / 5 | `118,355`（`93,767–139,343`） | `86.134`秒（`78.340–97.456`） |
| F03 isolated filesystem cleanup | 5 / 5 | `128,425`（`119,704–150,680`） | `78.417`秒（`74.982–82.832`） |
| F04 nested group completion | 5 / 5 | `126,290`（`116,542–162,909`） | `73.566`秒（`64.873–83.160`） |
| F05 clarify command order | 5 / 5 | `35,742`（`35,534–38,314`） | `27.271`秒（`22.723–35.420`） |
| F05-OS PyPI publish boundary | 5 / 5 | `35,524`（`35,500–36,024`） | `21.869`秒（`19.123–26.608`） |
| F06 restore echo color | 5 / 5 | `82,988`（`80,292–106,677`） | `61.796`秒（`57.398–72.020`） |
| F07 canonical tox runner | 5 / 5 | `85,304`（`80,929–85,992`） | `48.379`秒（`44.005–58.188`） |
| F07-P dependency lock pair | 5 / 5 | `162,160`（`126,125–191,048`） | `67.611`秒（`53.219–78.983`） |
| F08 shell completion doc sync | 5 / 5 | `88,369`（`82,198–93,229`） | `51.539`秒（`43.899–69.964`） |
| F10 command API inventory | 0 / 5 | `74,495`（`55,291–92,305`） | `43.825`秒（`31.238–48.629`） |
| F10-R nested completion review | 5 / 5 | `102,035`（`101,591–102,858`） | `50.076`秒（`45.742–55.743`） |

F10は品質回帰ではない。TaskSpecが要求するrepository authorityがbundleに存在しないため、
sourceだけから成果を推測せず停止する固定経路である。Authorityあり条件の試験ではない。

## A01監査のsemantic equivalence

既存の字句監査はA01の4件について`resilient_parsing`という特定語がないため
`clarification_missing`を返した。しかしRating v10は、未固定modeとscopeを一つの質問で
求めれば文言差を同一成果として扱う。4件はいずれもmodeと適用scopeを一度に確認し、
推測・edit・testなしで停止していた。C125用監査補助はこの契約を適用し、最終監査は
failure 0件となった。過去resultと既存監査scriptは変更していない。

## 非互換境界

保存済みClick C81 result `2d895cf954db4e5a8f35f08dce6f3362`のcompatibility keyは
`b9c7ee74d90b2c4d30926e5e44c0a5307690e81939fd359d571dceeb32c1a80a`、
Codex CLIは`0.144.0`である。今回のkeyとCLIが一致しないため、同じquality分布であることを
tokenまたはelapsed改善の根拠にしない。互換比較にはC81とC125を同じCLIで両方再実行する
必要がある。

## Evidence

- campaign: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/runs/click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-20260731-r1`
- result: `/Users/kenn/repos/_verification/click-prompt-ab-measurement/result-registry-v3/results/7560599fef024dfb8011264352707ab8.json`
- result file SHA-256: `29783436f4a4ddc3095c43c99bf74b65f85257ca7d5840978bb6c565ac5390fa`
- result content SHA-256: `e5dcbd7b68b5144f8661a34801d563741841dfab05dd0cc3f7de1570d6707ca2`
- quality audit SHA-256: `2c3914111777e41d7a363a43200c1188142489ac7bf1f55ae9352ea422616877`
- profile SHA-256: `abe42dcc29443499ad2feb644d84fe6b6a3e3c3dfa3e752252d19449280cf544`
- [設計記録](../../../../docs/click-c125-full-portability-design.md)

このresultはClickでのCandidate125評価完了を示す。採用、release、runtime projection、
`pallets/click`本体反映は意味しない。
