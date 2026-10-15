# clickプロンプトバンドル索引

`click` ターゲットインスタンスのプロンプトバンドルを引くための索引である。baseline / candidateのライフサイクル、インスタンス間の水平適用、bundle identityの規則は[`../AGENTS.md`](../AGENTS.md)を正本とする。各バンドルのtarget map、source identity、bundle SHA-256はmanifestを正とする。

## baselines

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-control-free-r1`](baselines/click-00e592c-control-free-r1/manifest.json) | 1 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` | 制御プロンプト不在。root `AGENTS.md`を空のファイルへ固定する |
| [`click-00e592c-no-agents-r1`](baselines/click-00e592c-no-agents-r1/manifest.json) | 0 | `62570c22091a0e5c3431c5be416222987c6d4251fa634d633c6c6ebcee8ab82c` | root・subとも`AGENTS.md`を配置しない空のバンドル |
| [`click-00e592c-control-free-claude-md-r1`](baselines/click-00e592c-control-free-claude-md-r1/manifest.json) | 2 | `6a824a8c70711269c43e40b33e1b21e6196746dce63427d31c7057e676a7b9e0` | 空のroot `AGENTS.md`と、それを指す`CLAUDE.md`のリンク。空の`CLAUDE.md`はClaude Codeに読み込まれなかった |
| [`click-00e592c-control-free-loaded-instruction-r1`](baselines/click-00e592c-control-free-loaded-instruction-r1/manifest.json) | 2 | `c5437e5f5eaac8222896893ecb322903106aa57ff3c79777ff76270de59a0aa2` | root `AGENTS.md`に指示を含まない1文、`CLAUDE.md`はそのリンク。Claude Codeが必ず読み込み、`CLAUDE.md`を置くCandidateとキャッシュの条件を揃える費用比較用の制御なし |

## candidates

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-validation-wrapper-precedence-r1`](candidates/click-00e592c-validation-wrapper-precedence-r1/manifest.json) | 1 | `4cf14889a07da0ede098bf813a005e0cda224916f7bafa32b8cdf2fc4a99b91a` | Bundle B。THE-CAPTION Candidate81のroot本文をbyte-identicalに水平適用。Std14評価済み |
| [`click-00e592c-repository-subagents-r1`](candidates/click-00e592c-repository-subagents-r1/manifest.json) | 3 | `7f2c7f336ebcbbbfcd04ea7b25bd08840f31da73daadf404b5ac4a73d00b23cd` | rootなし。`docs`・`src`・`tests`へClick固有sub `AGENTS.md`を配置。Std14 Medium評価済み（配置・露出比較） |
| [`click-00e592c-repository-authority-r1`](candidates/click-00e592c-repository-authority-r1/manifest.json) | 3 | `fc81314aec37546950daf623509e8b423db32bcff696ee6f7d33bc6342458c3f` | rootなし。既存3 sub本文を維持し、`src/AGENTS.md`へcommand API authorityを追加。F10 Medium N=5評価済み |
| [`click-00e592c-c81-repository-authority-r1`](candidates/click-00e592c-c81-repository-authority-r1/manifest.json) | 4 | `e3aa97e5417fdcf75cf93480136537fa2f31fda6bb6611b59e97de3e2cc6d277` | C81 root本文とRepository Authority 3本文をbyte-identicalに合成。Std14 r2 Medium評価済み |
| [`click-00e592c-criterion-complete-single-target-continuation-r1`](candidates/click-00e592c-criterion-complete-single-target-continuation-r1/manifest.json) | 1 | `2a94d070a9f2a4f130f50b33e341d45ece09eeb38113c486acc4bae71a513e3c` | THE-CAPTION Candidate125のroot本文をbyte-identicalに水平適用。Std14 r2 Medium N=5をCLI 0.146.0で評価済み |
| [`click-00e592c-receive-form-file-read-range-r1`](candidates/click-00e592c-receive-form-file-read-range-r1/manifest.json) | 2 | `78546c434411c0450974f4757edc8bf013ae56e21f3cbebe32ee330e25ae6b74` | THE-CAPTION C316（リリース済み）のroot `AGENTS.md`と、それを指す`CLAUDE.md`のリンクを水平適用。Std14 r4をSonnet 5.5 lowで評価済み |
| [`click-00e592c-delegated-state-source-r1`](candidates/click-00e592c-delegated-state-source-r1/manifest.json) | 2 | `24a1f47997809da7aeb5ae522ee075f25a9cec1a9c014e4009f4fdfb0f679cab` | THE-CAPTION C318のroot `AGENTS.md`と、それを指す`CLAUDE.md`のリンクを水平適用。Std14 r4を4モデルで評価済み |
| [`click-00e592c-unconfirmed-location-search-r1`](candidates/click-00e592c-unconfirmed-location-search-r1/manifest.json) | 2 | `6fa96f2d6b72c4b0b9f3c2955e26dc4875ef36ca9152f6b605714a3d8b0cb462` | THE-CAPTION C319のroot `AGENTS.md`と、それを指す`CLAUDE.md`のリンクを水平適用。未評価 |

状態列相当の説明は索引用の要約であり、評価状態は[`results/`](../results/README.md)の一次resultを正とする。donor側Candidateの採用・release・projection状態はClickへ継承しない。

## 設計導線

| 構成軸 | 設計記録 |
| --- | --- |
| C81全文水平適用 | [`Click C81全文水平適用`](../../../../docs/click-c81-full-portability-design.md) |
| Repository sub-AGENTS | [`Click repository sub-AGENTS比較設計`](../../../../docs/click-repository-subagents-comparison-design.md) |
| Repository Authority | [`Click repository authority availability比較設計`](../../../../docs/click-repository-authority-availability-design.md) |
| C81 + Repository Authority | [`Click C81 / C81 + Repository Authority Std14 r2比較設計`](../../../../docs/click-c81-repository-authority-standard14-r2-design.md) |
