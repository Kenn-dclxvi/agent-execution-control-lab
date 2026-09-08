# C274 Astra maxの比較計測

利用者の「最大も記録して」に基づき、rootがC274・Astraの推論設定maxでStandard14全14ケースを各N=5（70件）実行する。品質採点、全エージェントのトークンと総所要時間の集計、直近mediumおよび保存済みlow・high・xhighとの比較を成果とする。ケースや採点規則、本体設定は変更しない。

基準は直近のmedium再計測結果`0dfec297f0fe4d5f9d2d38fb2fff154e`。その固定Layer 1を複製し、全14テンプレートの差が推論設定だけであることを実行前に機械照合した。Astraの保存済み対応設定にもmaxが存在することを確認した。C274 bundle、CLI 0.153.3の実体とハッシュ、Python 3.14.5、fixture・TaskSpec・採点・全エージェントトークン集計・時間記録コード・並列上限24を維持する。推論設定を実験変数とする別の評価条件であり、プロンプト変更の効果として扱わない。

実行前照合の不一致があれば発行しない。発行後の無効試行は既存方針の同一スロット最大3試行までとし、それ以上の追加試験は行わない。品質を採点してからKPIを比較し、失敗があればそのまま記録する。各反復の14ケース合計を求め、5反復の中央値を指標ごとに算出する。並列試験全体の壁時計時間は別記し、正式な作業時間の欠測は推定しない。

実行証跡は`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-astra-max-standard14-n5-cli0153-20260908-r1`。実行前の`preparation.json`、`reasoning-only-receipt.json`、Layer 1の`model-runtime-axis-preflight.json`に基準結果、環境、互換条件、発行範囲を固定した。

## 実行完了

[max・low・medium・high・xhighの比較](../evaluations/results/candidate274-astra-max-low-medium-high-xhigh-standard14-n5_2026-09-08.md)に、今回max70件と保存済み4条件の結果を記録した。
