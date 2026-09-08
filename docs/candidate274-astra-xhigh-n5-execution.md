# C274 Astra xhighの比較計測

利用者の「もう一つ上も試験して」に基づき、rootが推論レベルhighの次のxhighで、Standard14全14ケース各N=5（70件）を実行する。直前のhigh結果`9630aa4cdb514bc3bc5e89aaead56ce1`を基準にし、medium結果`d2a5c2dbe2bd405c835a05afd2ddccae`も併記する。両基準は再実行しない。

C274 bundle、Astra、CLI 0.153.3、Python 3.14.5、固定Layer 1・fixture・TaskSpec・採点・時間記録コード・全エージェントトークン集計・並列上限24・N=5を保持し、推論レベルだけを変える。実行前にCLI実体hash、コードhash、fixtureとset identityを照合し、全14テンプレートの差が推論設定だけであることを確認した。不一致では発行しない。新しい条件プールへ登録し、各反復の14ケース合算後の中央値で比較する。

実行証跡は`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-astra-xhigh-standard14-n5-cli0153-20260908-r1`の`preparation.json`、`reasoning-only-receipt.json`、Layer 1の`model-runtime-axis-preflight.json`。正式な作業時間の欠測を推定で補完しない。追加Nや本体設定の変更は行わない。既存の外部失敗方針（同じスロット最大3試行）を保持する。

## 実行完了

[3段階の結果](../evaluations/results/candidate274-astra-medium-high-xhigh-standard14-n5_2026-09-08.md)に新規xhigh70件と保存済みhigh・medium各70件の比較を記録した。
