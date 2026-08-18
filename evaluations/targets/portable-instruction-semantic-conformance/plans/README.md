# Dispatch plans

[`portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json`](portable-semantic-control-free-heldout-r1-n1-dispatch-r1.json)は、control-free資格確認の`PIC-H01`から`PIC-H14`までを各1回だけ許可するwrite-once計画である。計画上の発行数は0件であり、計画の存在は実行済みまたは評価済みを意味しない。

[`portable-semantic-control-free-heldout-r1-n1-preflight-r1.json`](portable-semantic-control-free-heldout-r1-n1-preflight-r1.json)は、この計画、Profile、target、Codex CLI 0.146.0、共通アダプターおよび資格確認入口の同一性を固定する実行機固有の事前確認票である。入口は、この確認票に一度だけ現れるスロットで、かつ出力先がまだ存在しない場合だけ発行を許可する。

r1は14件すべてが`uniqueItems`非対応で推論前に外部失敗となった。r2は一件先行発行で型を伴わない`const`の非対応を確認し、残り13件を発行しなかった。r3は一件でschema適合応答まで得たが、exec JSONLに一次`total_tokens`がないため固定token contractを満たさず、残り13件を発行しなかった。各外部失敗は`attempt-r1`、`attempt-r2`、`attempt-r3`のsummaryへhash固定した。

r4は公式Structured Outputs subsetへの意味保存投影、canonical事後検証およびthread-bound永続一次tokenを固定した。最初の一件で測定成立を確認後、残り13件を発行し、`authorized_slot_count=14 / issued_slot_count=14 / valid_result_count=14`となった。生の応答、イベント、標準エラー、token証跡および実行観測は公開領域へ保存しない。

portable full-agent CandidateのN=1は[`dispatch-r1`](portable-semantic-c147-portable-full-agent-heldout-r1-n1-dispatch-r1.json)と[`preflight-r1`](portable-semantic-c147-portable-full-agent-heldout-r1-n1-preflight-r1.json)へ14スロットを固定した。発行数は0であり、Candidate quality gateをC147 referenceより先に実行する。reference planとProfileはまだ作成していない。

Candidateの14スロットは全件発行・採点し、7 / 14 score 4でquality gate不通過となった。計画とpreflightの`issued_slot_count=0`は発行前のwrite-once状態を保持する履歴値であり、実発行数は[`正式result`](../results/portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json)の14件を正とする。C147 reference planとProfileは作成していない。

後続の順序監査により、新semantic setはportable Candidateより先にC147自身を資格確認する必要があると判定した。[`C147 reference dispatch r1`](portable-semantic-c147-full-agent-reference-heldout-r1-n1-dispatch-r1.json)と[`preflight r1`](portable-semantic-c147-full-agent-reference-heldout-r1-n1-preflight-r1.json)は、既存held-out r1を変更せず、C147 reference一枚についてPIC-H01〜PIC-H14を各一回だけ許可した。14件は全件有効だったがScore 4は6 / 14となり、正式resultでsemantic setをreference不適格として停止した。

TaskSpec r2のreference calibrationは、[`dispatch`](portable-semantic-c147-reference-transition-calibration-r2-n1-dispatch-r1.json)と[`preflight`](portable-semantic-c147-reference-transition-calibration-r2-n1-preflight-r1.json)へ同じ14 Case各一回だけを固定した。promptはC147 referenceのまま、TaskSpecとset identityだけをr2 calibrationへ変更し、portable promptは発行対象へ含めない。

契約矛盾をrevisionで分離した後続校正は、[`r3 dispatch`](portable-semantic-c147-reference-transition-calibration-r3-n1-dispatch-r1.json)／[`preflight`](portable-semantic-c147-reference-transition-calibration-r3-n1-preflight-r1.json)と[`r4 dispatch`](portable-semantic-c147-reference-transition-calibration-r4-n1-dispatch-r1.json)／[`preflight`](portable-semantic-c147-reference-transition-calibration-r4-n1-preflight-r1.json)に固定した。全revisionでC147だけを発行し、portable promptは未発行である。

独立heldoutは、[`r2 C147 dispatch`](portable-semantic-c147-reference-heldout-r2-n1-dispatch-r1.json)／[`preflight`](portable-semantic-c147-reference-heldout-r2-n1-preflight-r1.json)をLayer 1不適格の履歴として保持する。修正版[`r3 C147 dispatch`](portable-semantic-c147-reference-heldout-r3-n1-dispatch-r1.json)／[`preflight`](portable-semantic-c147-reference-heldout-r3-n1-preflight-r1.json)が14 / 14を通過した後、同条件の[`portable dispatch`](portable-semantic-c147-portable-full-agent-heldout-r3-n1-dispatch-r1.json)／[`preflight`](portable-semantic-c147-portable-full-agent-heldout-r3-n1-preflight-r1.json)を発行した。

N=5拡張は[`C147 dispatch`](portable-semantic-c147-reference-heldout-r3-n5-dispatch-r1.json)／[`preflight`](portable-semantic-c147-reference-heldout-r3-n5-preflight-r1.json)と[`portable dispatch`](portable-semantic-c147-portable-full-agent-heldout-r3-n5-dispatch-r1.json)／[`preflight`](portable-semantic-c147-portable-full-agent-heldout-r3-n5-preflight-r1.json)へ固定した。各preflightは対応するN=1 resultをhashでbindし、i001を再利用してi002〜i005の56 slotだけを許可する。

N=20拡張は[`C147 dispatch`](portable-semantic-c147-reference-heldout-r3-n20-dispatch-r1.json)／[`preflight`](portable-semantic-c147-reference-heldout-r3-n20-preflight-r1.json)と[`portable dispatch`](portable-semantic-c147-portable-full-agent-heldout-r3-n20-dispatch-r1.json)／[`preflight`](portable-semantic-c147-portable-full-agent-heldout-r3-n20-preflight-r1.json)へ固定した。各preflightは対応するN=5 resultをhashでbindし、i001〜i005を再利用してi006〜i020の210 slotだけを許可する。
