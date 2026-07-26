# click prompt bundles

target instance `click`のprompt bundleを置く。`baselines/`が比較元、`candidates/`が構築中の候補である。

制御prompt本文（`SPEC`〜`RECOVERY`の13 label）はinstance間で出発点として流用できるが、bundleのtarget mapはtarget側directory構造に依存するためinstance固有artifactとして扱う。`pallets/click`には`AGENTS.md`階層、project context index、role promptがいずれも存在しないため、bundleはroot `AGENTS.md`の1 targetで閉じる。

## baselines

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-control-free-r1`](baselines/click-00e592c-control-free-r1/manifest.json) | 1 | `7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9` | 制御prompt不在。root `AGENTS.md`を空fileへ固定する |

control-free条件の固定方法は`the-caption`側の[`control-free-generic`](../../../../prompts/candidates/the-caption-3ce91a4-control-free-generic-r1/manifest.json)に合わせた。あちらは19 targetのうちAGENTS.md 5件を空fileへ置換してrepository情報文書を残すが、clickには対応する情報文書が存在しないため1 targetのみとなる。

`overlay_bundle`でclickのworkspaceへ適用できることを実測で確認している（適用前は`AGENTS.md`不在、適用後は0 byteのregular file）。

## candidates

| prompt identity | target数 | bundle SHA-256 | 条件 |
| --- | ---: | --- | --- |
| [`click-00e592c-validation-wrapper-precedence-r1`](candidates/click-00e592c-validation-wrapper-precedence-r1/manifest.json) | 1 | `4cf14889a07da0ede098bf813a005e0cda224916f7bafa32b8cdf2fc4a99b91a` | Bundle B。THE-CAPTION Candidate81のroot本文をbyte-identicalに水平適用。Std14評価済み |

Candidateは一つのpredicateまたは一つの変更軸だけを扱い、作成前gate 9項目（[`prompts/AGENTS.md`](../../../../prompts/AGENTS.md)）を通してからbundleを作る。Bundle Bは個別predicateを分離せず、固定済みC81全文の有無を一つの構成軸として扱う。設計境界は[`Click C81全文水平適用`](../../../../docs/click-c81-full-portability-design.md)を正本とする。
