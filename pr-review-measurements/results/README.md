# PRレビュー測定result

登録済みresultはまだない。Core Review workflowが生成する`run-result.json`はGitHub Actions artifactとして保持し、pilotの互換条件とquality gateを確認した後に、別変更でこの配下へappend-only登録する。

- 生のAction出力を登録しない。
- `result_id`とcontent SHA-256を固定する。
- 同じ`case / variant / repetition / attempt`を上書きしない。
- `pass`以外のterminal resultも削除せず、成功runとは分けて保持する。
- pilot result、N=5 result、Integration resultを同一状態として混ぜない。
