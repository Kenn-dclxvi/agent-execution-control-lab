# click prompt bundle index

`click` target instanceのprompt bundleを引くための索引である。baseline / candidate lifecycle、instance間の水平適用、bundle identityの規則は[`../AGENTS.md`](../AGENTS.md)を正本とする。各bundleのtarget map、source identity、bundle SHA-256はmanifestを正とする。

## baselines

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-control-free-r1`](baselines/click-00e592c-control-free-r1/manifest.json) | 1 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` | 制御prompt不在。root `AGENTS.md`を空fileへ固定する |
| [`click-00e592c-no-agents-r1`](baselines/click-00e592c-no-agents-r1/manifest.json) | 0 | `62570c22091a0e5c3431c5be416222987c6d4251fa634d633c6c6ebcee8ab82c` | root・subとも`AGENTS.md`を配置しないempty bundle |

## candidates

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-validation-wrapper-precedence-r1`](candidates/click-00e592c-validation-wrapper-precedence-r1/manifest.json) | 1 | `4cf14889a07da0ede098bf813a005e0cda224916f7bafa32b8cdf2fc4a99b91a` | Bundle B。THE-CAPTION Candidate81のroot本文をbyte-identicalに水平適用。Std14評価済み |
| [`click-00e592c-repository-subagents-r1`](candidates/click-00e592c-repository-subagents-r1/manifest.json) | 3 | `7f2c7f336ebcbbbfcd04ea7b25bd08840f31da73daadf404b5ac4a73d00b23cd` | rootなし。`docs`・`src`・`tests`へClick固有sub `AGENTS.md`を配置。Std14 Medium評価済み（配置・露出比較） |
| [`click-00e592c-repository-authority-r1`](candidates/click-00e592c-repository-authority-r1/manifest.json) | 3 | `fc81314aec37546950daf623509e8b423db32bcff696ee6f7d33bc6342458c3f` | rootなし。既存3 sub本文を維持し、`src/AGENTS.md`へcommand API authorityを追加。F10 Medium N=5評価済み |
| [`click-00e592c-c81-repository-authority-r1`](candidates/click-00e592c-c81-repository-authority-r1/manifest.json) | 4 | `e3aa97e5417fdcf75cf93480136537fa2f31fda6bb6611b59e97de3e2cc6d277` | C81 root本文とRepository Authority 3本文をbyte-identicalに合成。Std14 r2 Medium評価済み |
| [`click-00e592c-criterion-complete-single-target-continuation-r1`](candidates/click-00e592c-criterion-complete-single-target-continuation-r1/manifest.json) | 1 | `2a94d070a9f2a4f130f50b33e341d45ece09eeb38113c486acc4bae71a513e3c` | THE-CAPTION Candidate125のroot本文をbyte-identicalに水平適用。Std14 r2 Medium N=5をCLI 0.146.0で評価済み |

状態列相当の説明は索引用の要約であり、評価状態は[`results/`](../results/README.md)の一次resultを正とする。donor側Candidateの採用・release・projection状態はClickへ継承しない。

## 設計導線

| 構成軸 | 設計記録 |
| --- | --- |
| C81全文水平適用 | [`Click C81全文水平適用`](../../../../docs/click-c81-full-portability-design.md) |
| Repository sub-AGENTS | [`Click repository sub-AGENTS比較設計`](../../../../docs/click-repository-subagents-comparison-design.md) |
| Repository Authority | [`Click repository authority availability比較設計`](../../../../docs/click-repository-authority-availability-design.md) |
| C81 + Repository Authority | [`Click C81 / C81 + Repository Authority Std14 r2比較設計`](../../../../docs/click-c81-repository-authority-standard14-r2-design.md) |
