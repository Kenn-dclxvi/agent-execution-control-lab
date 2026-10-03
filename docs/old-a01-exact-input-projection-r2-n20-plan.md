# PNG投影r2のAstra Low累積N20

利用者が2026年10月3日に「削減版N20まで実施して」と依頼したため、既存Low2件の有効証拠を再利用し、同一の画像投影r2条件で18件だけ追加する。旧素材・小規模r4・画像削除r1の実行は合算しない。

元の投影r2 Layer1・JSON TaskSpec・257ファイル・Git開始状態・疎な投影設定・固定モデル一覧・個人指示除外・共有Python依存とshim・CLI0.159.0・実行器・採点源・全担当集計・時間境界を保持する。profileのN、再利用件数、今回予算と識別子だけを変え、runtime等の実効条件は既存2件と機械照合する。設定M24、実同時1を既存2件と揃える。

比較の正本は投影r2 Low N2の一次結果。実行前に結果hash、既存2件の証拠hash、素材manifest、runtime identityとprofile条件の一致を確認し、comparison-preflight.json、reuse-compatibility-receipt.json、dispatch-plan.jsonを固定した。同じexecute関数を呼ぶ。モデル・推論設定はLowだけで、Medium・Highは発行しない。

低得点を含めて累積20件で終了し、自動再試行なし。無効runなら未発行分を停止し、N20達成のために無効を補充しない。N5・20・50の再現性判断に沿い、反例をN不足として延期しない。今回の頻度確認は依頼された上限まで実施する。

専用保存場所はSN7100のruns/astra-old-a01-exact-input-projection-r2-low-n20-20261003。個別workspace・home・全担当usage・操作証拠・終了文を保持する。全件の指示配送と最終状態を照合して採点し、過去結果は上書きしない。単独ケース・非登録診断で、Layer4のprompt比較にはしない。
