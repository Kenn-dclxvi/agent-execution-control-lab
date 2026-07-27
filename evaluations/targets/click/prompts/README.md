# click prompt bundles

target instance `click`のprompt bundleを置く。`baselines/`が比較元、`candidates/`が構築中の候補である。

制御prompt本文はinstance間で出発点として流用できるが、bundleのtarget mapはtarget側directory構造に依存するためinstance固有artifactとして扱う。固定した`pallets/click` tree自体には`AGENTS.md`階層、project context index、role promptが存在しない。既存bundleはroot `AGENTS.md`だけを扱い、新しいrepository sub-AGENTS比較ではClickに実在する3領域だけを別構成として扱う。

## baselines

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-control-free-r1`](baselines/click-00e592c-control-free-r1/manifest.json) | 1 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` | 制御prompt不在。root `AGENTS.md`を空fileへ固定する |
| [`click-00e592c-no-agents-r1`](baselines/click-00e592c-no-agents-r1/manifest.json) | 0 | `62570c22091a0e5c3431c5be416222987c6d4251fa634d633c6c6ebcee8ab82c` | root・subとも`AGENTS.md`を配置しないempty bundle |

control-free条件の固定方法は`the-caption`側の[`control-free-generic`](../../../../prompts/candidates/the-caption-3ce91a4-control-free-generic-r1/manifest.json)に合わせた。あちらは19 targetのうちAGENTS.md 5件を空fileへ置換してrepository情報文書を残すが、clickには対応する情報文書が存在しないため1 targetのみとなる。

`overlay_bundle`でclickのworkspaceへ適用できることを実測で確認している（適用前は`AGENTS.md`不在、適用後は0 byteのregular file）。

## candidates

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-validation-wrapper-precedence-r1`](candidates/click-00e592c-validation-wrapper-precedence-r1/manifest.json) | 1 | `4cf14889a07da0ede098bf813a005e0cda224916f7bafa32b8cdf2fc4a99b91a` | Bundle B。THE-CAPTION Candidate81のroot本文をbyte-identicalに水平適用。Std14評価済み |
| [`click-00e592c-repository-subagents-r1`](candidates/click-00e592c-repository-subagents-r1/manifest.json) | 3 | `7f2c7f336ebcbbbfcd04ea7b25bd08840f31da73daadf404b5ac4a73d00b23cd` | rootなし。`docs`・`src`・`tests`へClick固有sub `AGENTS.md`を配置。Std14 Medium評価済み（配置・露出比較） |
| [`click-00e592c-repository-authority-r1`](candidates/click-00e592c-repository-authority-r1/manifest.json) | 3 | `fc81314aec37546950daf623509e8b423db32bcff696ee6f7d33bc6342458c3f` | rootなし。既存3 sub本文を維持し、`src/AGENTS.md`へcommand API authorityを追加。F10 Medium N=5評価済み |
| [`click-00e592c-c81-repository-authority-r1`](candidates/click-00e592c-c81-repository-authority-r1/manifest.json) | 4 | `e3aa97e5417fdcf75cf93480136537fa2f31fda6bb6611b59e97de3e2cc6d277` | C81 root本文とRepository Authority 3本文をbyte-identicalに合成。Std14 r2 Medium評価済み |

Candidateは一つのpredicateまたは一つの変更軸だけを扱い、作成前gate 9項目（[`prompts/AGENTS.md`](../../../../prompts/AGENTS.md)）を通してからbundleを作る。Bundle Bは個別predicateを分離せず、固定済みC81全文の有無を一つの構成軸として扱う。設計境界は[`Click C81全文水平適用`](../../../../docs/click-c81-full-portability-design.md)を正本とする。

Repository sub-AGENTS candidateは、root instructionなしのままpath-scopedなrepository情報だけを置く一つの構成軸である。比較条件と停止条件は[`Click repository sub-AGENTS比較設計`](../../../../docs/click-repository-subagents-comparison-design.md)を正本とする。

Repository Authority candidateは、配置・露出比較で不足したF10 authority availabilityを直接測る後続artifactである。既存Std14を変更せず、設計と全14 case監査は[`Click repository authority availability比較設計`](../../../../docs/click-repository-authority-availability-design.md)を正本とする。

C81 + Repository Authority candidateは、両donor本文を変更せず合成する一つの構成軸である。C81との組合せ条件と停止境界は[`Click C81 / C81 + Repository Authority Std14 r2比較設計`](../../../../docs/click-c81-repository-authority-standard14-r2-design.md)を正本とする。
