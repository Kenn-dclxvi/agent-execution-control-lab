# Portable instruction control-free資格確認 r4

> [!IMPORTANT]
> **結果**: `measurement_gate_passed / valid_14_of_14 / schema_valid_14 / score4_5 / mechanism_passed_5 / quality_descriptive_only / adoption_not_decided / release_not_decided / runtime_projection_not_authorized`

## 結論

Codex CLI 0.146.0、GPT-5.6 Sol、reasoning `medium`、control-free 0 byte、held-out r1全14 Case、N=1で、応答、all-agent一次tokenおよび単調時計elapsedを14件すべて欠落なく取得できた。新しいsemantic protocol targetの測定成立gateは通過した。

品質はscore 4が5/14、機序通過も5/14である。これはcontrol-freeの記述値であり、資格確認の合否条件、portable kernelの効果、採用、releaseまたは他runtimeへの一般化ではない。

## 測定値

| 指標 | 結果 |
| --- | ---: |
| 有効result | 14/14 |
| schema適合 | 14/14 |
| score 4 | 5/14 |
| score 3 | 0/14 |
| score 2 | 6/14 |
| score 1 | 3/14 |
| 機序通過 | 5/14 |
| all-agent token中央値 | 12,673.5 |
| all-agent token範囲 | 12,424–13,140 |
| elapsed中央値 | 10.431秒 |
| elapsed範囲 | 7.421–14.997秒 |

Case別のscore、診断、tokenおよびelapsedは[`qualification result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-control-free-heldout-r1-n1-qualification-r4.json)を正本とする。生応答、Codex JSONL、stderr、永続sessionおよび実行観測はrepository外の非公開領域へ保持する。

## 実行基盤の切り分け

| Profile | 発行 | 有効result | 観測 | 処置 |
| --- | ---: | ---: | --- | --- |
| r1 | 14 | 0 | APIがcanonical schemaの`uniqueItems`を推論前に拒否 | 全件を外部失敗として保持 |
| r2 | 1 | 0 | `uniqueItems`除去後、型を伴わない`const`を推論前に拒否 | 残り13件を発行せず停止 |
| r3 | 1 | 0 | schema適合応答は取得したが、固定token contractがexec JSONLの一次`total_tokens`欠落で拒否 | 残り13件を発行せず停止 |
| r4 | 14 | 14 | 公式Structured Outputs subsetへの意味保存投影とthread-bound永続一次tokenで成立 | 資格確認resultへ登録 |

r3からr4ではtoken内訳を加算していない。execの`thread.started.thread_id`を同じworkspaceの永続sessionへbindし、保存済み`event_msg.token_count.info.total_token_usage.total_tokens`だけを採用した。schemaはcanonical bytesを採点正本として維持し、API向けには未対応制約を外すか、文字列`const`を型付き単一`enum`へ意味同値変換した。保存応答はcanonical schemaで再検証した。

Structured OutputsがJSON Schemaのsubsetだけを支え、全fieldの`required`、objectの`additionalProperties: false`および対応制約を要求する根拠は[OpenAI Structured Outputs公式資料](https://developers.openai.com/api/docs/guides/structured-outputs)を参照する。

## 効率上の判断

r1ではtransport互換性を14件同時発行前に確認できず、推論前失敗を14件発行した。r2以降は一件を先行確認し、成立前に残り13件を発行しないfrontierへ修正した。この結果、r2とr3の不成立で追加発行したのは各1件だけである。

正式r4のall-agent token合計は177,790である。r1とr2は推論前拒否、r3の一件だけがschema適合応答まで生成したが、r3 Profileのtoken contractを満たさないため正式値へ混ぜない。

## 次のgate

次は同じtarget、Case、oracle、TaskSpec、runtime、schema transport、token accountingおよび実行条件を固定し、prompt identityだけをportable kernelへ変更する比較設計である。control-freeの5/14を上げるためにCase、oracleまたは採点を変更しない。まずroot-onlyまたは一枚化kernelのどちらを直接比較対象にするかを、現在の一枚化設計上の直接親とallowed deltaへ固定する。
