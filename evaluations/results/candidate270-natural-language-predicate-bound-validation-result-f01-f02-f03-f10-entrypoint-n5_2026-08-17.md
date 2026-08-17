# Candidate270 natural-language predicate-bound validation result F01・F02・F03・F10 entrypoint N=5

## 結論

Candidate270は20 / 20件がvalidかつScore `4`で、Candidate269比の四ケース合算中央値もtoken `-6.38%`、経過時間`-22.27%`となった。しかし、削減経路は設計したpredicate-bound carrierではない。F01・F02の10 / 10件が一回の外側validation wrapperを使わず、focused test、full test、diff / statusを別々のtool resultとmodel再入へ分割した。

したがって、Candidate269の過大carrier原因を正しく直したとは判定しない。過大carrierを閉じた代わりにC69・C71までに閉じていたvalidation途中のmodel再入を再び開いた反例である。さらにF03の開始identityと影響を受けないreadの共同発行は0 / 5で、Candidate269の4 / 5から後退した。N=20へ拡張せず`mechanism_failed / stopped`とする。

## ケース別KPI

| ケース | C147 N=5 token中央値 | C269 N=5 token中央値 | C270 N=5 token中央値 | C269比token | C269秒中央値 | C270秒中央値 | C269比秒 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,202 | 163,264 | 121,788 | `-25.40%` | 93.850 | 67.465 | `-28.11%` |
| F02 | 128,236 | 166,758 | 138,017 | `-17.24%` | 90.846 | 76.976 | `-15.27%` |
| F03 | 104,320 | 133,527 | 128,806 | `-3.54%` | 85.141 | 70.554 | `-17.13%` |
| F10 | 87,934 | 115,122 | 114,084 | `-0.90%` | 73.307 | 64.034 | `-12.65%` |

C270のC147比はF01 `+13.61%`、F02 `+7.63%`、F03 `+23.47%`、F10 `+29.74%`である。ただしF10のC147中央値には現目的のinstruction result dependencyを満たさない安いrouteが含まれるため、同目的の費用差としては扱わない。

KPIは改善方向に見えるが、F01・F02では10件すべてが別機序である。このため、N=5中央値の低下を「predicate-bound resultへ戻した効果」としてN=20へ外挿しない。

## 機序

| 観測 | C270 | 判定 |
| --- | ---: | --- |
| F01・F02で一回の外側validation wrapperを保持 | 0 / 10 | 不成立 |
| F01・F02でrequired validation間にresultをAIへ返さず完了 | 0 / 10 | 不成立 |
| F01・F02でvalidation後のdiff / statusを同じ実行票へ保持 | 0 / 10 | 不成立 |
| 保持したwrapper内でpredicate-bound resultを構成 | 0 / 10 | wrapperを迂回したため対象機序として観測不能 |
| F03で開始identityと影響を受けないreadを共同発行 | 0 / 5 | Candidate269の4 / 5から後退 |
| F10で`src/AGENTS.md`結果後に配下read | 5 / 5 | 保持 |

Candidate270本文は「対応づけ済みの確定result」を強めた一方で、外側wrapperを使う経路を実行不能にはしていないし、wrapperを迂回して個別tool resultを順次受け取る経路も閉じていない。モデルは後者を全runで選び、raw outputを一つの巨大carrierへ再配送するC269経路は消えた。しかし、それはC147のresult binding復元ではなく、validation closure全体の回避である。

## 登録状態

- 比較可能な登録result: `e34f3b5820d745f5912e5af82fede6aa`
- 直接基準: Candidate269 N=5 result `2398d22125bd4e658fe5b653679167b5`
- quality: 20 / 20 Score `4`
- excluded: 0
- Candidate269再実行: 0
- C147再実行: 0
- 現在状態: `quality_passed / kpi_decreased_by_bypass_route / target_mechanism_not_exercised / f03_regressed / mechanism_failed / no_n20_extension / stopped`

最初に作成したselection result `1c8953e487f844638925e52696dd69a3`はreference resultをbindしておらず、四ケースfixtureだけのcompatibilityになったため比較resultには使わない。保存済みCandidate269 resultをbindし直した`e34f3b5820d745f5912e5af82fede6aa`だけを直接比較に用いる。

失敗routeの因果分解と次に閉じるpermission・dependencyは[`Candidate270失敗後の次自然語route閉鎖分析`](../../docs/candidate270-failure-next-natural-language-route-closure-analysis.md)を参照する。

## 後続再判定

上記はN=5直後の判定として保持するが、現在判定には使わない。`codex-events.jsonl`の個別`command_execution`はwrapper内部でも生じるため、それだけでは外側tool callやmodel-visible result配送を判定できなかった。persisted rolloutの`response_item`を使った[validation carrier再監査](candidate147-candidate270-validation-carrier-rollout-reassessment-r1.json)では、Candidate270のF01、F02、F03は15 / 15件で単一outer call、wait-only継続、途中validation output 0 bytes、terminal output一件だった。

経路、model step、共同発行およびmechanism成立率は3 KPI差を説明する診断情報であり、それらだけでKPI比較または追加Nを停止しない。後続の[Standard14 N=5](candidate270-natural-language-predicate-bound-validation-result-standard14-n5_2026-08-17.md)は70 / 70件がScore `4`、Candidate147比token `+18.16%`、elapsed `+9.09%`だった。現在状態は`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`である。
