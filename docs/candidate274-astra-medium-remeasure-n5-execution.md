# C274 Astra mediumの再計測

利用者の「medium も改めて実施して。」に基づき、rootがmedium・Standard14全14ケース各N=5（70件）を新規実行する。前回mediumの70件は保持し、新しい同条件の反復として別resultへ記録する。前回と今回をN=10へ集約せず、実行時期の異なる2回のN=5として扱う。

前回medium結果`d2a5c2dbe2bd405c835a05afd2ddccae`と全14テンプレートが完全一致し、profileの差は識別子だけである。high結果`9630aa4cdb514bc3bc5e89aaead56ce1`とは推論設定だけが異なることを実行前に照合した。CLI 0.153.3実体hash、C274 bundle、Python 3.14.5、fixture・Layer 1、TaskSpec、採点、時間記録コード、並列上限24、全エージェントトークン集計を保持する。xhigh結果`e162237faf0c415a8e7c39c1e63e7f4d`も比較へ併記する。

再計測は利用者による明示指定であり、不足スロットとして旧結果を再利用する操作とは区別する。記録は既存resultを上書きせず追加する。各反復の14ケース合計を求めた後の5反復中央値で比較し、時間の欠測は推定しない。無効試行は既存方針の同一スロット最大3試行で扱い、それ以外の追加Nや本体設定変更は行わない。

実行証跡は`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-astra-medium-remeasure-standard14-n5-cli0153-20260908-r1`。`preparation.json`、`reasoning-only-receipt.json`、Layer 1の`model-runtime-axis-preflight.json`へ照合を記録した。

## 実行完了

[再計測mediumとhigh・xhighの比較](../evaluations/results/candidate274-astra-medium-remeasure-high-xhigh-standard14-n5_2026-09-08.md)に、新規medium70件と前回3条件の結果を保存した。
