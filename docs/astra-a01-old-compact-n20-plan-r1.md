# 旧A01と小規模復元版の累積N20確認

2026年10月1日の利用者依頼により、旧A01と小規模復元版r2について、Free・GPT-6 Astraのlow・medium・highをそれぞれ累積N20まで測定する。対象はこの一件の動作分岐であり、Standard14の残り13ケースは発行しない。目的は旧lowの停止と小規模版の分岐の再現を、同条件の実績を増やして確認することである。

## 再利用と追加件数

| 試験 | 推論設定 | 互換する既存件数 | 追加件数 | 累積上限 |
| --- | --- | ---: | ---: | ---: |
| 旧A01 | low | 5 | 15 | 20 |
| 旧A01 | medium | 5 | 15 | 20 |
| 旧A01 | high | 5 | 15 | 20 |
| 小規模r2 | low | 2 | 18 | 20 |
| 小規模r2 | medium | 2 | 18 | 20 |
| 小規模r2 | high | 2 | 18 | 20 |

旧mediumは過去二系列計10件だが、9月5日系列には9月8日系列のexecution-time-recording/r1が固定されていなかった。同じCLI・モデルでも完全互換ではないため、今回の累積Nには9月8日系列の5件だけを用いる。過去10件の発生実績は削除せず、別条件の記録として保持する。

追加する有効スロットは計99件。旧A01は各条件の固定上限M24と旧外部失敗時の最大3試行を保持し、low・medium・highの条件別キューを順に実行する。小規模版は同時1件の順次実行と自動再試行なしを保持し、無効runで追加発行停止。両経路の実際の同時実行数を合わせても上限24を超えない。条件別の開始時刻と実行順を保存する。

## 保持する条件と発行前照合

旧A01は各条件の保存済みLayer 1と固定CLI 0.153.3を再利用する。作業中のevaluation_loop.pyは旧測定のhashと異なったため、同じhashを持つHEAD版をリポジトリ外の専用保存場所へ復元した。他作業のdirtyファイルは変更しない。fixtureはpath・type・mode・contentを照合し、元fixtureと元結果は書き換えない。復元コードと固定Python環境のhashも旧条件と一致することを確認した。

旧経路ではatomic registryの既存runを数え、plan-missingの出力からA01だけを発行対象として固定した。残り13件は発行対象に含めない。prepare-comparison-layer1、prepare_atomic_plan、preflight-comparisonで元result・profile・fixture・capsule・CLI・Mを照合し、各15件のreceiptが通ってから起動した。Nはexecution provenanceであり、旧profileの実効条件を別条件へ変更しない。

小規模版はr2の固定素材・採点・CLI 0.159.0・モデルカタログ・個人指示除外・全担当usageを保持する。既存6件の一次resultを一意にbindし、内容固定に含まれる全ファイル、fixtureの各ファイル属性、固定CLIとカタログを照合した。新profileは反復数と追加予算を固定し、実効条件は既存profileと共通とする。旧A01との品質差をprompt効果とするLayer 4登録は行わない。

発行前に外部保存場所で固定したprofileの同一内容を、[low](../evaluations/targets/compact-repository-control/profiles/free-astra6-low-latent-mode-code-n20-r2.json)、[medium](../evaluations/targets/compact-repository-control/profiles/free-astra6-medium-latent-mode-code-n20-r2.json)、[high](../evaluations/targets/compact-repository-control/profiles/free-astra6-high-latent-mode-code-n20-r2.json)へ保存する。

## 採点と診断

採点契約は試験ごとに保持し、過去を再採点しない。0点の内訳として現状テストのみと推測編集を分け、質問表示後の続行も記録する。bytecode生成や不存在pythonコマンドの失敗だけを仕様編集や有効な試験成功へ変換しない。意味確認待ちのnullは実際の終了文と全担当操作を照合してから採点し、採点不能を0点にしない。

累積N20で終了し、N50へ自動延長しない。低得点を捨てず、旧lowの全件停止に対して有効な反例が出ればその場で不成立の事実を記録する。ユーザーが今回求めたN20の頻度確認は、その事実と分けて上限まで継続する。

## 所在

専用保存場所はSN7100の`_verification/THE-CAPTION-prompt-ab-measurement/runs/astra-a01-old-and-compact-n20-20261001-r1`。旧3条件のreceiptは各`old-*/cycle-valid/layer1/comparison-preflight.json`、小規模版のreceiptは`compact-r2/comparison-preflight.json`へ保存する。生ログと認証はリポジトリへ追加しない。

- [旧履歴調査](compact-latent-mode-historical-free-audit-r1.md)
- [小規模r2の初回結果](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.md)
- [累積Nの判断基準](reproducibility-decision-policy.md)
