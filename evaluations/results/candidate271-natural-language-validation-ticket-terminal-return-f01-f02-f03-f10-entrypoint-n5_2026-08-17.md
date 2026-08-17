# Candidate271 natural-language validation ticket terminal return F01・F02・F03・F10 entrypoint N=5

## 結論

Candidate271は20 / 20件がvalidかつScore `4`だった。しかし、設計した「validation開始前の実行票bindingとticket terminal時だけのmodel-visible result返却」はF01・F02の0 / 10件で、一回の外側validation wrapperも0 / 10件だった。10 / 10件すべてがfocused validation resultをAIへ返してからfull validationを別発行し、さらにdiffまたはstatusを別の外側callで取得した。

したがってC269型の過大全output carrierを正しく修正したのではなく、C270と同じvalidation間model再入へ再び迂回した。四ケース合算tokenはCandidate269比`-0.06%`で実質同水準、F02は`+3.03%`へ悪化した。F03共同発行もC147基準5 / 5に対して2 / 5だったため、N=20へ進めず`mechanism_failed / no_n20_extension / stopped`とする。

## ケース別KPI

| ケース | C147 N=5 token | C269 N=5 token | C270 N=5 token | C271 N=5 token | C269比 | C147比 | C271秒 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,202 | 163,264 | 121,788 | 147,496 | `-9.66%` | `+37.59%` | 65.249 |
| F02 | 128,236 | 166,758 | 138,017 | 171,806 | `+3.03%` | `+33.98%` | 78.554 |
| F03 | 104,320 | 133,527 | 128,806 | 134,431 | `+0.68%` | `+28.86%` | 66.821 |
| F10 | 87,934 | 115,122 | 114,084 | 114,860 | `-0.23%` | `+30.63%` | 72.664 |

F10のC147中央値87,934 tokenには、現目的のinstruction result dependencyを満たさない安いrouteが含まれる。C147の目的達成済み5応答route 108,454 tokenと比べたC271は`+5.91%`である。

同じiterationの四ケース合算中央値はCandidate147 494,706 token、Candidate269 569,253 token、Candidate270 532,952 token、Candidate271 568,890 tokenだった。Candidate271はCandidate269比`-363` token（`-0.06%`）、Candidate147比`+74,184` token（`+14.99%`）である。経過時間はCandidate269比`-17.49%`、Candidate147比`+0.28%`だった。

token KPIは改善していない。F01の低下をF02・F03の上昇で相殺した合算値だけを改善とは扱わず、ケース別原因を保持する。Candidate270よりtokenが`+6.74%`なのも、正しいticket routeへ戻った費用ではない。両Candidateとも対象wrapperを0 / 10件しか実行していないため、別の迂回route同士の差である。

## 機序

| 観測 | C271 | C147基準 | 判定 |
| --- | ---: | ---: | --- |
| F01・F02で一回の外側validation wrapperを保持 | 0 / 10 | ケース別保存観測 | 不成立 |
| 実行票未完了時にchild validation resultをAIへ返さない | 0 / 10 | F01 5 / 5、F02 4 / 5以上 | 不成立 |
| 実行前bindingとticket terminal返却を一体で実行 | 0 / 10 | 対象route | 観測不能ではなく、route未実行 |
| required validation間にresultをAIへ返却 | 10 / 10 | 誤経路 | C270型迂回が再発 |
| validation後のdiff / statusを別の外側callで取得 | 10 / 10 | 診断 | 再入を追加 |
| F03開始identityと影響を受けないreadを共同発行 | 2 / 5 | 5 / 5 | 不成立 |
| F10 `src/AGENTS.md` result後に配下read | 5 / 5 | 2 / 5以上 | 保持 |
| F10 result後の必要read完遂 | 5 / 5 | 5 / 5 | 保持 |

Candidate271本文は、ticket未完了時のchild result返却を明示的に禁止した。しかし評価runでは、個別validationをトップレベルcommandとして発行し、そのresult受領後に残りを発行する経路が全件で選ばれた。禁止文が存在することと、その外側invocationが実行不能になったことは同じではない。このCandidateはpermission edgeを実行上閉じた証拠にならない。

C269型の`発行済みの全result` carrierは0 / 10件だったが、これはcarrier返却対象を改善した結果ではない。wrapperそのものを0 / 10件で迂回したためである。よってC269とC270の二つの高費用routeを同時に閉じる目的は未達である。

## 登録状態

- 比較可能な登録result: [`baf01e47d8d8432bbe2dc92a961287cb.json`](baf01e47d8d8432bbe2dc92a961287cb.json)
- 品質監査: [`candidate271-natural-language-validation-ticket-terminal-return-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json`](candidate271-natural-language-validation-ticket-terminal-return-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json)
- 機序監査: [`candidate271-natural-language-validation-ticket-terminal-return-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json`](candidate271-natural-language-validation-ticket-terminal-return-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)
- 直接基準: Candidate269 N=5 result `2398d22125bd4e658fe5b653679167b5`
- Candidate269、Candidate270、Candidate147再実行: 0
- 現在状態: `quality_passed / token_not_improved / target_route_not_exercised / c270_bypass_route_recurred / f03_regressed / mechanism_failed / no_n20_extension / stopped`

最初のselection登録`3c28d737d2ff475b8119b8bd2a717d93`はreference resultとcycle receiptをbindしていないため直接比較には使わない。同じ20件を再実行せず、Candidate269 resultと比較receiptへbindした`baf01e47d8d8432bbe2dc92a961287cb`だけを比較に用いる。

Candidate272は作成しない。次に進む前に、明示禁止を全runで越えた理由を、C81およびC243〜C246で成立した境界との差として再分析する。
