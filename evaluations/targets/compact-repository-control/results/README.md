# 測定結果

## Free 小規模20件 初回N=1

[先行試験r2](free-sol61-low-core20-n1-r2_2026-10-01.json)は20件の実行が成立し、機械採点は4点17件・0点3件。3件は採点不備として留保する。選択20件は1,313,839トークン。

[修正後の試験r3](free-sol61-low-core20-n1-r3_2026-10-01.json)は20件の実行が成立し、機械採点は4点19件・0点1件。残る1件も表記の採点不備で、Freeの品質失敗は確認していない。追加6件はすべて4点、選択20件は1,285,552トークン、実行時間合計714.562秒。[解釈と限界](free-sol61-low-core20-n1_2026-10-01.md)を参照する。

## Free 実コードA01 独立二回

[結果と限界](free-sol61-low-latent-mode-code-n2_2026-10-01.md)：2 / 2件が0点。採点は実測前に固定し、確認前の試験開始を両実行で観測した。初期可視素材は7件・3,378バイト、総トークン178,812。[一次result](free-sol61-low-latent-mode-code-n2_2026-10-01.json)を参照する。

## Free GPT-6 Astra low 実コードA01

[独立二回の結果](free-astra6-low-latent-mode-code-n2_2026-10-01.md)は2 / 2件が0点。合計177,603トークン、197.595秒。ケースと採点をSol版から変更せず測定した。

対応する[一次result](free-astra6-low-latent-mode-code-n2_2026-10-01.json)も保持する。

## Free GPT-6 Astra 推論設定別 依存関係復元r2

[結果と動作分類](free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.md)：low・medium・high各2件、4点1件・0点5件。確認停止1件、現状テストのみ3件、推測編集2件。合計605,269トークン・424.66秒。[一次result](free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.json)を参照する。

## Free GPT-6 Astra：旧A01と小規模版 各N20

[結果と比較](free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01.md)：旧試験の停止はlow20・medium17・high14件、小規模版はlow1・medium0・high0件。旧Lowの動作を維持できず、代替として採用できない。[一次結果](free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01.json)に各20件の証拠と費用を保存した。

## Free GPT-6 Astra：小規模r2・r3 各N2

[比較結果](free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.md)：同一CLI・PATHで両版をlow・medium・high各2件、計12件測定した。[一次結果](free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json)に動作分類・費用・発行前照合と証拠を保存した。旧KPIの混在なし。

## Free GPT-6 Astra：依頼文の関係を変更したr4 各N2

[結果と動作分類](free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03.md)と[一次結果](free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03.json)。依頼文一文の診断であり旧A01の代替として未採用。

## Free GPT-6 Astra Low：小規模r4 累積N20

[Low N20結果](free-astra6-low-latent-mode-code-task-r4-n20_2026-10-03.md)と[一次結果](free-astra6-low-latent-mode-code-task-r4-n20_2026-10-03.json)：既存2件と新規18件の全20件有効。4点3件・0点17件。確認停止3件・現状テストのみ13件・推測編集4件。累積2,411,058トークン、平均78.297秒。全件で個人指示除外を確認し、Low以外は発行していない。 後続の[条件監査](../../../../docs/old-versus-compact-isolated-low-n20-condition-audit-r1.md)で、旧素材と小規模r4にはTaskSpec・authority・依存環境等の差があり、容量削減単独の比較ではないと確認した。
