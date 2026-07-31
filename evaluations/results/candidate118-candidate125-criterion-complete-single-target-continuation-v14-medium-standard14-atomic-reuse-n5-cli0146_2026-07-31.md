# Candidate118 / Candidate125 criterion-complete single-target continuation Rating v14 Medium Standard14 atomic reuse N=5

## 結論

Candidate125はStandard14のquality gateと正式token目標を同時に通過した。

14 case × 5件は70 / 70件がvalidかつscore `4`だった。token中央値は`1,401,225`で、Candidate107目標`1,523,137`を`121,912`（`8.00%`）下回った。elapsed中央値も`846.377秒`でCandidate107を`99.119秒`（`10.48%`）下回った。

C122との比較では、token中央値を`2,615`（`0.19%`）下げながら、score `2`だったF04の1件を含め全70件をscore `4`へ戻した。elapsedはC122より`23.357秒`（`2.84%`）長い。したがって「全KPIがC122より改善」とは主張しない。

後続のA02 `N=20`も20 / 20件がscore `4`で、implementation bind後・最初のartifact変更前のcommand再入は0 / 20件だった。これによりCandidate118のA02 terminal closureをCandidate125でも維持した。

現在状態は`targeted_evaluated / a02_n20_evaluated / standard14_evaluated / quality_gate_passed / targeted_mechanism_passed / a02_terminal_closure_passed / candidate107_token_target_passed / candidate107_elapsed_below / result_registered / adoption_not_decided`とする。採用、release、runtime projection、本体反映はまだ実施しない。

## Identityとreuse

- Candidate125 prompt: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- bundle SHA-256: `60e95bfe7f9e09a0cbb2fb980c54f1cd1bd671c37509976e7e88574adf911435`
- profile: `candidate125-criterion-complete-single-target-continuation-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- reference Candidate118 result: `ed8862d5b6af472da4247d39ef80075f`
- Candidate125 pool: `9437d24c1a536cd10f61a17badac01537045862554dec8f43f5477f394d6f830`
- reused Candidate125 atomic runs: A01 / A02 / F01 / F02 / F04各5件、計25件
- newly executed atomic runs: 残る9 case各5件、計45件
- new execution: 45 / 45 valid、excluded 0、profile上の`M=24`
- Candidate125 selection: `33722b96e0ef4127a299d28982d308bb`
- Candidate125 analysis: `1d6b1f6559d9433e87a1e24d86644a10`
- Candidate125 result: `96fb571308de4c08a7aeed0faefb7d72`
- execution archive SHA-256: `8766a93c27ff672a7305f45f4515f8a2ffa0b8b33828f961f3f95f9a8d459899`
- final compact archive SHA-256: `25a35671f0c577df47bdb2d5b5331f7e458dcba9c18d068bd474044a159056a3`

## KPI比較

| 比較 | quality分布 | token中央値差 | elapsed中央値差 |
|---|---|---:|---:|
| Candidate125 - Candidate107 | 両方70 / 70 score `4` | `-121,912`（`-8.00%`） | `-99.119秒`（`-10.48%`） |
| Candidate125 - Candidate118 | 両方70 / 70 score `4` | `-317,500`（`-18.47%`） | `+4.729秒`（`+0.56%`） |
| Candidate125 - Candidate122 | C125 70 / 70、C122 69 / 70 score `4` | `-2,615`（`-0.19%`） | `+23.357秒`（`+2.84%`） |

Candidate107のouter deadline gate失敗は、Candidate107を採用可能にしない。一方、同じ固定executor条件でprompt差分だけにより到達したtoken目標は比較目標として有効である。Candidate125はC107制御を継承せず、C122のF02 cost経路とF04 quality closureを両立してその目標を通過した。

## Targeted mechanismの保持

登録済みtargeted 25 runでは次を確認した。

- F04: 5 / 5 score `4`、false stop 0 / 5
- F04: 一つのeditable targetが全変更criterionを所有する経路で、同一targetへのcriterion-complete continuationを変更前に一度だけ使用
- F02: 5 / 5 score `4`、initial content後の追加read 0 / 5、content wave 5 / 5
- F02 token中央値: `124,094`、目標`173,000`以下
- A01 / A02 / F01: quality 15 / 15 score `4`

Standard14の追加45 runも45 / 45 score `4`であり、targeted以外の9 caseへ品質回帰は観測されなかった。

## A02 N=20 terminal closure

Standard14後に、登録済みA02 5 runを再利用し、不足15 runだけを追加した。

- A02 selection: `ea47d7ea7f124f928d61ba4f0eacb506`
- A02 analysis: `1d0be47ece82433d821de2f7a62fdff8`
- A02 result: `7741f85dad2a4e7dac2fcc7c00a78522`
- quality: 20 / 20 score `4`
- implementation bind後・最初のartifact変更前command再入: 0 / 20件、0 command
- token中央値: `121,164`
- elapsed中央値: `71.798秒`
- execution / final archive SHA-256: `dfd0d613d95440bece677871bb7b161bc01d61d05d39f61dcce70bdb7a0b89af` / `8cf313a7b1c6dd62ffbfe776ed46a9f79d896997022253626ca520f2214436a7`

このdiagnosticはC125がC118のA02 terminal closureを維持したことを示す。Standard14 KPI result自体は変更しない。

## 判断境界

このresultはCandidate125の評価成功とA02 terminal closureの維持を示す。採用済み、release済み、本体反映済みを意味しない。validation制御本文は親系列から変更しておらず、Standard14 70 / 70の品質は維持したが、これは新しいB20 route-stability試験の実施を意味しない。追加の長期stability確認を採用前gateにするかは別判断である。
