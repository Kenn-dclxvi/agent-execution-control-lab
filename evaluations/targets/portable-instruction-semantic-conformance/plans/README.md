# Dispatch plans

[`portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json`](portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json)は、control-free資格確認の`PIC-H01`から`PIC-H14`までを各1回だけ許可するwrite-once計画である。計画上の発行数は0件であり、計画の存在は実行済みまたは評価済みを意味しない。

[`portable-semantic-control-free-heldout-r1-n1-preflight-r1.json`](portable-semantic-control-free-heldout-r1-n1-preflight-r1.json)は、この計画、Profile、target、Codex CLI 0.146.0、共通アダプターおよび資格確認入口の同一性を固定する実行機固有の事前確認票である。入口は、この確認票に一度だけ現れるスロットで、かつ出力先がまだ存在しない場合だけ発行を許可する。

r1は14件すべてが`uniqueItems`非対応で推論前に外部失敗となった。r2は一件先行発行で型を伴わない`const`の非対応を確認し、残り13件を発行しなかった。r3は一件でschema適合応答まで得たが、exec JSONLに一次`total_tokens`がないため固定token contractを満たさず、残り13件を発行しなかった。各外部失敗は`attempt-r1`、`attempt-r2`、`attempt-r3`のsummaryへhash固定した。

r4は公式Structured Outputs subsetへの意味保存投影、canonical事後検証およびthread-bound永続一次tokenを固定した。最初の一件で測定成立を確認後、残り13件を発行し、`authorized_slot_count=14 / issued_slot_count=14 / valid_result_count=14`となった。生の応答、イベント、標準エラー、token証跡および実行観測は公開領域へ保存しない。
