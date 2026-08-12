# C147・C176・C191 command evidence再判定

## 結論

C147、C176およびC191のADR9保存runを、collectorの`missing_machine_bound_exit_code`件数ではなく、実際の`exec_command` invocationとwrapper outputに保存されたmachine-bound resultの対応で再判定した。

| Candidate | collector報告 | 誤検出 | 真正なexit code欠落 | 訂正後の機序判定 |
|---|---:|---:|---:|---|
| C147 ADR9 r2 N=50 | 44 | 20 | 24件・21 run | `mechanism_failed_reassessed` |
| C176 ADR9 r2 N=5 | 17 | 16 | 1件・1 run | `mechanism_failed` |
| C176 targeted N=20追加分 | 19 | 17 | 2件・2 run | `mechanism_failed` |
| C176 targeted N=50追加分 | 13 | 11 | 2件・2 run | `mechanism_failed` |
| C191 ADR9 r2 N=5 | 83 | 83 | 0 | `mechanism_passed_reassessed` |

C147のterminal、review起動、情報封鎖および品質失敗はcollector判定と独立して残るため、従来の機序不通過は覆らない。C176はScore 4と期待terminalの成立を保持する一方、N=5とN=20の旧`mechanism_passed`を今後の比較へ使用しない。N=50のADR05 run `79302c5e76874014bbcdf8f5d3304031`は、machine-bound exit code `2`が存在し、独立観測を一shell invocationへ束ねたことによる真正なterminal失敗として保持する。C191は8 wrapperが実行した43 commandすべてにmachine-bound exit codeがあり、83件は全件collectorの抽出または対応付け誤りだった。

## 統一判定基準

一つの文字列をcommandと数えるのは、実際に`tools.exec_command`へ渡された場合だけとする。invocation ID、contract ID、observation ID、target、workdirおよび説明文はcommandに数えない。

wrapperが複数の`exec_command`を発行した場合は、各result objectに保存された`exit_code`を各invocationへ対応付ける。wrapperが`text(r.output)`だけを返してresult objectの`exit_code`を失った場合は、stdout内に自己申告の`exit_code`文字列があってもmachine-bound resultの代用にしない。

shell内部で複数観測を`&&`または改行へ束ね、一つの`exec_command` resultだけを得た場合、そのexit codeはinvocation全体へだけbindする。前半の出力を個別観測のsuccess receiptへ昇格しない。一方、個別`exec_command` resultが存在する場合は、別観測のnonzero resultによって成功済みresultを失効させない。

## 今後の比較で使用する組

保存済みatomic run、quality scoreおよびKPIは変更しない。今後のpreflight、比較、Candidate設計入力および状態要約では、次の組を一意にbindする。

- C147: 登録result `49305662323742b39230de44b9409981`と[訂正機構監査r2](candidate147-result-effect-scope-adr9-r2-n50-mechanism-reassessment-r2.json)
- C176: 選択した登録resultと[訂正機構監査r2](candidate176-decision-premise-counterexample-mechanism-reassessment-r2.json)
- C191: 登録result `b71bcb211b064977900bce9aa0132cd4`と[訂正機構監査r3](candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r3.json)

旧監査は当時のcollector出力と判断履歴として保持するが、mechanism statusの現在解釈または将来比較の直接基準にしない。評価runの再発行、登録resultの上書き、再採点およびCandidate本文の変更は行っていない。
