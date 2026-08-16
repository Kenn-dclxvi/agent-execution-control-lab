# Candidate265 instruction result read permission復元 F01・F02・F03・F10 entrypoint N=5

> **位置づけの訂正（2026-08-16）**: Candidate265は、作成前に禁止されているモデル自己判定をpermission条件へ含めていた。本来は`candidate_not_created`として棄却すべき案であり、以下のN=5は正式なCandidate評価または次案の親ではない。自己判定では誤経路を閉じられないことを示す診断反例としてのみ保持する。

## 結論

Candidate265 `the-caption-3ce91a4-instruction-result-read-permission-restoration-r1`をF01、F02、F03、F10 entrypointで各N=5実行した。20 / 20件がvalidかつ採点可能で、すべてScore `4`だった。

Candidate264で成立していたF01、F02、F03の開始確認と影響を受けない必要readの共同発行は各5 / 5件で保持した。F10では、`src/AGENTS.md`のterminal result受領前に配下listingまたは本文を発行しない経路がCandidate264の2 / 5件からCandidate265の4 / 5件へ改善した。しかし残る1件はinstruction result前に配下listingと`v4_daily_main.py`本文を発行した。未解決dependencyを持つ配下read permissionを閉じ切れず、固定済み停止条件へ該当した。

四ケースを一組とする5標本の中央値は、Candidate265が品質100、all-agent総token `536,176`、経過時間`320.269`秒だった。Candidate264比でtokenは`52,055`、`10.75%`増え、経過時間は`12.558`秒、`4.08%`増えた。F10のケースtoken中央値は`+0.95%`、経過時間は`-16.66%`だった一方、変更対象外のF02ではvalidation完了待ちの追加モデル再入がCandidate264の0 / 5件からCandidate265の5 / 5件へ増え、ケースtoken中央値が`24.63%`増えた。この頻度差をF10のinstruction dependency制御へ因果帰属しないが、増加分を必要なF10依存へ対応づけられないため、設計済みcost gateでは正当化できない退行となる。

したがってCandidate265は`design_gate_violation / candidate_should_not_have_been_created / prompt_control_not_demonstrated / diagnostic_only`とし、追加N、Standard14、採用、releaseおよびprojectionへ進めない。Score、成立率およびKPIは、作成前gate違反を事後的に正当化しない。この結果は、instruction依存の有無をモデルの自己判定へ残すだけではpermission edgeを閉じ切れない反例としてのみ保持する。

## 実行と登録

- 直接の比較元および基準result: Candidate264 `1a64c1b2429c4e89aff3aedd6836944e`。
- cases: `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3、`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1、`TC-F03-ATOMIC-CONTEXT-CLEANUP` r2、`TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1。
- 各N=5、合計20件。
- valid / rateable: 20 / 20。
- excluded / execution error: 0 / 0。
- Score: `4 = 20`。
- Candidate265 selection: `84ffe31b1c9443bebfdf3b754a657ef5`。
- Candidate265 analysis: `2e653c61085c4ae6872cdd266b3a7132`。
- Candidate264 reference analysis: `5ba90c6c103546c1a9f33729aeb680c2`。
- Candidate265登録result: [`cd29f61f140d400c821e9b1900b40f8a`](cd29f61f140d400c821e9b1900b40f8a.json)。
- compatibility key: `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`。
- comparison key: `29ca0f436d0cc06df4b37f4b8943e998c10276ee024d38ab0c9cb42f81fc1ee4`。
- Candidate264再実行: 0件。

## ケース別KPI

| ケース | Candidate264 token | Candidate265 token | 差 | Candidate264秒 | Candidate265秒 | 差 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| F01 domain duplicate asset key | 145,447 | 145,346 | `-0.07%` | 72.577 | 84.852 | `+16.91%` |
| F02 cross-layer history date bound | 133,018 | 165,775 | `+24.63%` | 80.972 | 89.466 | `+10.49%` |
| F03 atomic context cleanup | 133,285 | 135,147 | `+1.40%` | 77.404 | 84.965 | `+9.77%` |
| F10 entrypoint inventory | 90,323 | 91,178 | `+0.95%` | 71.026 | 59.194 | `-16.66%` |
| 四ケース合算中央値 | 484,121 | 536,176 | `+10.75%` | 307.710 | 320.269 | `+4.08%` |

ケース別中央値の合計と、同じselection iterationで四ケースを一組にした合算中央値は集計方法が異なるため一致しない。合算行を主KPI、ケース別値を経路診断に使う。

## 機序監査

### F01・F02・F03

三ケースとも、開始identityの確認と、開始結果でtarget、permissionまたはstop conditionが変わらない必要readを5 / 5件で同じAI判断から発行した。Candidate264で有効だった共同発行を一般的な逐次実行へ戻す過剰遮断は観測されなかった。

### F10 entrypoint

Candidate265は4 / 5件で`src/AGENTS.md`のterminal result受領後にだけ配下listingとentrypoint本文を発行し、必要なinventory reviewを完遂した。失敗したselection iteration 2、run `3e110cb347584b1196b37b4a0e3ef7ed`では、`src/AGENTS.md`のcommand result受領前に`find src/app/entrypoints`と`v4_daily_main.py`本文readを発行した。

成功率はCandidate264の2 / 5件から4 / 5件へ上がったが、この改善を機序成立とはしない。追加したpredicateは「そのinstruction resultがtarget、permissionまたはstop conditionを変え得るか」の判定をモデルへ残しており、誤って`authorized_read`と分類すれば配下readを合法に発行できる。このpermission edgeが残っているためである。

### validation完了待ち

保存root rolloutで、validation wrapperがcell ID付きnonterminal resultを返した後の`wait`を数えた。`wait`発生runはCandidate264の6 / 20件に対しCandidate265は12 / 20件だった。特にF02は0 / 5件から5 / 5件へ増えた。Candidate265ではF01 iteration 1に5回の`wait`があり、全20件の`wait` invocationは16回だった。

この差はtoken増加経路を説明するが、Candidate265の対象機序が生んだ効果とは扱わない。Candidate264とCandidate265で`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、wrapperおよびwait制御は同一byteであり、F10用のinstruction dependency predicateだけが異なるからである。validation完了境界は次の一案として別に扱う。

## 判断

Candidate265は必要なF10経路を2 / 5件から4 / 5件へ改善し、F01からF03の有効な共同発行も保った。しかし、一件の誤経路がprompt準拠のまま到達可能であり、制御の成立条件である実行不能性を満たさない。品質Score `4`と改善率を、permission edgeの残存を無視する採用根拠にはしない。

次案では、成功runのtool順を実行義務へ転記せず、「instruction resultが影響し得るか」という自己判定をread側へ置かない構造へ分解し直す。Candidate265へ条件を継ぎ足さず、この案はここで停止する。

一次証拠は[品質監査](candidate265-instruction-result-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json)、[機序・再入監査](candidate265-instruction-result-read-permission-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)、登録result、Candidate264登録result、および各atomic runの保存rolloutである。

現在状態は`design_gate_violation_confirmed / candidate_should_not_have_been_created / prompt_control_not_demonstrated / diagnostic_only / valid_20_of_20_historical_observation / score4_20_of_20_historical_observation / f10_forbidden_route_1_of_5 / token_regressed_10_75_percent / elapsed_regressed_4_08_percent / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。
