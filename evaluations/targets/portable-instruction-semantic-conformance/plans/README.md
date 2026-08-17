# Dispatch plans

[`portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json`](portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json)は、control-free資格確認の`PIC-H01`から`PIC-H14`までを各1回だけ許可するwrite-once計画である。計画上の発行数は0件であり、計画の存在は実行済みまたは評価済みを意味しない。

[`portable-semantic-control-free-heldout-r1-n1-preflight-r1.json`](portable-semantic-control-free-heldout-r1-n1-preflight-r1.json)は、この計画、Profile、target、Codex CLI 0.146.0、共通アダプターおよび資格確認入口の同一性を固定する実行機固有の事前確認票である。入口は、この確認票に一度だけ現れるスロットで、かつ出力先がまだ存在しない場合だけ発行を許可する。

現在は`authorized_slot_count=14 / issued_slot_count=0 / qualification_not_started`である。生の応答、イベント、標準エラー、token証跡および実行観測は公開領域へ保存しない。
