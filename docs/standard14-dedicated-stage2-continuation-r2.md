# STD14専用素材の工程2継続記録 第2版

2026年10月4日。[工程2の第1版](standard14-dedicated-stage2-r1.md)で未接続だった採点入力を実装し、既存の実行器・収集器へ結んだ。モデル試験は0件。旧Node環境の完全同一性は、保存証拠の不足により未証明として残る。工程2の全条件を満たしたとは宣言しない。

## 今回の方針と維持条件

必要な成果は、保存された実行証拠から全14件を採点できる接続、正常・不正証拠の局所検査、旧F04環境の照合結果である。対象は既存の `standard14-dedicated-stage2` worktree、専用インスタンス内の実行・採点補助だけとした。既存実行器のバイトを保持したまま専用fixtureの入口を接続し、収集器v5とall-agent v1をそのまま呼ぶ。既存系列、工程1の5成果、model-visibleなfixture・TaskSpec・authority、採点の0〜4点の意味は変更しない。

旧executor、CLI、tool、hookを変更せず、モデルスロット、push、PR、merge、別チャット、担当委譲は発行しなかった。作業セッションの `gpt-6.1-sol / medium` は第1版の証拠を継続する。工程3は未実施である。

## 保存証拠から採点までの接続

新しい `runtime/execution_binding_r2.py` は、固定実行器 `run_old_a01_current_environment_n2_r1.py` と共有Python接続関数のhashを照合し、専用fixtureの開始証拠を保存する。元のexecute本文と収集器は変更しない。未採点の実行を品質4点や採点済みvalidへ補完せず、独立判定待ちとして扱う。

`runtime/evidence_bridge_r2.py` は、固定実行器が保存する `run.json`、`launch.json`、`events.jsonl`、`usage.json`、全担当rollout、終了応答、開始・最終tree、元JSON TaskSpecを一つの固定採点packetへ結ぶ。全担当usageは元rolloutの最終値と照合し、合計・session graph・workspaceを確認する。経過時間は元実行器のCLI開始〜返却の区間を使い、質問待機を除かない。候補名や条件名は採点判断へ渡さない。

全tool観測を列挙して、独立判定が一件ずつ操作分類を与える。操作の欠落、別packetへの判定、根・子担当自身による自己申告の判定入力は拒否する。終了応答は固定実行器の `final.txt` と末尾agent_messageを照合する。月次には固定seedの一diffと対象sourceの参照を含め、現在HEADの親を代用しない。

コマンド条件は元TaskSpecと非root正本だけから固定した。元収集器のsubstring一致だけでは、文字列を表示した操作までgate実行に見える可能性があるため、独立判定で実行意味、引数、対象cwdを照合する。未実行・失敗・開始済み終了不明は分け、終了不明だけを計測失敗とする。A02に未提示の `git diff --check` は追加しない。F06の明示diff確認は維持する。

意味判定は保存証拠のhashを持つ独立判定記録を入力する。自動で日本語の応答の正誤を推測する採点器へ置き換えず、元Rating14の独立内容判定を接続した。実コードの検査結果は独立判定のTrueでも上書きできない。A01は応答の語句を使わず状態と操作から判定し、F05の確認項目を移植しない。数値行や生成者情報を品質条件へ追加しない。判定入力の独立性の確認は入力の信頼境界であり、実行役のworker人数を採点する条件ではない。

## 接続の局所検証

[最新の局所検証](../evaluations/targets/standard14-dedicated-control/registrations/evidence-bridge-qualification-r3.json)では全14件の正常例と107件の不正・退行例を検査し、すべて成功した。正常例は実Python、shell、Nodeのsubprocessを使い、根と子担当の合成Codex記録を既存収集器へ通した。月次レビューは修復を実施せずseedのままにし、両optionの影響を述べる応答を判定した。

不正例にはpacket hash・caseの取り違え、観測やcriterionの省略、根担当の自己申告、証拠hashなし、未知のcriterion、終了応答の変更、実コード検査の上書き、A01のtest・revert、必須コマンドの未実行・失敗・終了不明、コマンド文字列を表示しただけの操作、rolloutと一致しないusageを含む。

合成usageは接続検査専用であり、実モデルのトークン実測値ではない。局所の経過時間もCLIモデル試験時間ではない。`evidence_origin=local_synthetic_no_model` を保持し、Layer 4へ登録しない。採点経路の局所成立と、実モデル応答を正しく判定できたという観測を混同しない。モデル試験を発行する経路は今回実行していない。

第2版の初回接続検査は[前段の102件](../evaluations/targets/standard14-dedicated-control/registrations/evidence-bridge-qualification-r2.json)として保持し、追加した5条件を含む最新検証を第3版の検証記録へ保存した。第1版の局所検証と固定記録もその場で書き換えていない。

## 旧Node環境との照合結果

[Node照合記録](../evaluations/targets/standard14-dedicated-control/registrations/node-environment-audit-r2.json)を保存した。旧F04のqualification receiptは `node v26.0.0; npm 11.12.1` とgate成功を記録している。現環境はこの版と一致し、packageとlockのバイトも旧sourceと一致した。現環境のNode/npm実体の絶対pathとhashを固定した。

lockが指定するcacheのうち161件は内容hashを検証できた。未存在70件はすべてoptionalで、darwin/arm64に適用される欠落は0件だった。今回の実npm ciはoffline設定で成功しており、現環境の実行可能性は局所確認できた。

ただし旧receiptは、当時のNode/npm binary hashとcache manifestを記録していない。その保存証拠から**当時の実体・cacheとの完全同一性は証明できない**。現在の版一致やoffline install成功で補完しない。これはコードの未実装ではなく、工程1が要求した環境同一性の証拠が不足する未完了条件である。旧素材とのコスト比較・互換性認定はしない。

## 現在の固定成果と残る条件

[継続成果の固定記録](../evaluations/targets/standard14-dedicated-control/registrations/source-freeze-r2.json)と[発行条件](../evaluations/targets/standard14-dedicated-control/registrations/admission-r2.json)を工程3へ渡す。第1版の採点接続未実装は解消した。実モデルでの使用実績は未観測であり、測定成立の確認は将来の28件の別ゲートである。

発行条件は `ready=false` を維持する。残るのは、旧Node実体・cacheの同一性未証明、工程3の全14対応最終確認、固定モデル一覧とCLI配送条件、空home・権限・全担当usage・時間区間、新集合Layer 1とatomic planの実行前照合である。旧Nodeの同一性を未確認のまま「確認済み」へ移すことや、F04を除いた発行は行わない。
