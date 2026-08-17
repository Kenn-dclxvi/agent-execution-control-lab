# Candidate272 natural-language issued result permission removal F01・F02・F03・F10 entrypoint N=5

## 結論

Candidate272は20 / 20件がvalidかつScore `4`だった。required validation間のAI再入はF01が5 / 5、F02が4 / 5で、F10 instruction dependencyも5 / 5だった。一方、raw rolloutでcustom exec境界を確認すると、F03共同発行は3 / 5でC147基準5 / 5を満たさなかった。

しかし、除去対象だった`発行済みの全result` permissionは実行上閉じなかった。F01・F02の10 / 10件でfull gateのinner raw output `158,870`文字がwrapper carrierへ入り、outer resultにもraw stdoutが残った。outer custom tool側で切り詰められる場合はあるため、158,870文字すべてがmodel-visibleだったとは扱わない。F01の1件はそのcarrierに埋もれたdiff / statusを同じ理由で再取得した。F01中央値はCandidate269比`+18.04%`、F02は`+32.15%`、四ケース合算は`+18.71%`へ悪化した。

つまり、明示permissionを消しただけでdefault denyにはならず、`wrapperが終了した時に一度だけ結果を返す`という残存文が全command resultを返す既定経路を合法なまま残した。加えて、user-visible messageを挟まないことを同一model stepと誤って数えると、変更前の分割再入を見落とす。目的のpermission closure、F03共同発行およびKPI改善は未達である。N=20へ進めず`f03_mechanism_failed / target_permission_mechanism_failed / major_case_kpi_regression / stopped`とする。

## ケース別KPI

| ケース | C147 N=5 token | C269 N=5 token | C272 N=5 token | C269比 | C147比 | C272秒 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,202 | 163,264 | 192,719 | `+18.04%` | `+79.77%` | 82.462 |
| F02 | 128,236 | 166,758 | 220,371 | `+32.15%` | `+71.85%` | 89.704 |
| F03 | 104,320 | 133,527 | 134,981 | `+1.09%` | `+29.39%` | 77.397 |
| F10 | 87,934 | 115,122 | 114,335 | `-0.68%` | `+30.02%` | 68.404 |

F10のC147中央値87,934 tokenには、現目的のinstruction result dependencyを満たさない安いrouteが含まれる。C147の目的達成済み5応答route 108,454 tokenと比べるとCandidate272は`+5.42%`である。

同じiterationの四ケース合算中央値はCandidate147 494,706 token、Candidate269 569,253 token、Candidate272 675,767 tokenだった。Candidate272はCandidate269比`+106,514` token（`+18.71%`）、Candidate147比`+181,061` token（`+36.60%`）である。経過時間はCandidate269比`-15.82%`、Candidate147比`+2.32%`だった。

N=5のため安定した分布差とは断定しない。ただし、F01とF02がともに大幅悪化し、除去対象のraw carrierが10 / 10件で残り、F01再取得も1 / 5件で残ったため、追加Nで同じ未成立機序の精度だけを上げない。

## 機序

| 観測 | C272 | 合格基準 | 判定 |
| --- | ---: | ---: | --- |
| F01 required validation間のAI再入なし | 5 / 5 | C147 5 / 5 | 成立 |
| F02 required validation間のAI再入なし | 4 / 5 | C147 19 / 20に対応する初回4 / 5以上 | 成立 |
| F01同理由の検証後result再取得なし | 4 / 5 | C147 5 / 5 | 不成立 |
| F03開始identityと影響を受けないreadの共同発行 | 3 / 5 | C147 5 / 5 | 不成立 |
| F10 instruction result先行 | 5 / 5 | C269 5 / 5 | 成立 |
| F10 instruction result後の必要read完遂 | 5 / 5 | C147 5 / 5 | 成立 |
| nonterminal後の同一cell待機 | 17 / 17 | C147 6 / 6 | 成立 |
| F01・F02でfull gate raw outputをwrapper carrierへ収容 | 10 / 10 | 診断 | permission closure不成立 |

F02 iteration 3だけはfocused resultを受領してからfull gateを別発行した。これは事前基準内の1 / 5であり、C270・C271の10 / 10迂回は再発していない。

F03 iterations 1と3は、開始確認のcustom exec resultをmodelが受領してからsource / test readのcustom execを別発行した。codex eventの`agent_message`だけを見ると間に表示メッセージがないため共同発行に見えるが、raw rolloutには別々の`custom_tool_call`とtoken-count更新がある。機序判定は後者を正とする。

nonterminal resultはF01 4件、F02 3件、F03 4件の合計11件で発生し、外部`wait`は17回だった。17 / 17回は同じcellだけを待っておりdependency違反はない。ただしC147 N=5の4件・6回より再入回数が多く、token上振れの使用先として分離して扱う。

問題はrouteの外形だけでなく、完了時に何をwrapper carrierへ入れられるかである。Candidate272は`発行済み`を十分条件とする明示語を削ったが、返却対象を必要な完了resultへ限定するpermission boundaryは作っていない。ただし、後続のraw rollout比較では、carrierが小さいC272 runでもC147よりtokenが高く、主差は変更前の余分なmodel再入だった。したがってraw carrierを単独原因にはしない。Candidate272本文はCandidate269より短いため、prompt長増加も原因にはできない。

## 登録状態

- 登録result: [`8048e02d1765434fa93155a256550ce7.json`](8048e02d1765434fa93155a256550ce7.json)
- 品質監査: [`candidate272-natural-language-issued-result-permission-removal-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json`](candidate272-natural-language-issued-result-permission-removal-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json)
- 機序監査: [`candidate272-natural-language-issued-result-permission-removal-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json`](candidate272-natural-language-issued-result-permission-removal-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)
- 直接基準: Candidate269 N=5 result `2398d22125bd4e658fe5b653679167b5`
- Candidate269、Candidate147再実行: 0
- 現在状態: `quality_passed / validation_route_shape_passed / f03_mechanism_failed / target_permission_mechanism_failed / f01_reacquisition_failed / major_case_kpi_regression / no_n20_extension / stopped`

後続の[`Candidate272とCandidate147のmodel再入原因分析`](../../docs/candidate272-c147-model-reentry-causal-analysis.md)では、raw carrier単独原因を棄却した。C272はvalidation outputがC147と同等以下のrunでも、変更前の開始確認と必要readを別の外側custom execへ分け、F01で3回、F02で2回多くmodelへ戻っていた。次に閉じる一辺は、共同発行対象の個別resultが外側evidence operationのterminal前にAIへ越境できるpermissionである。Candidate273 bundleはまだ作成していない。
