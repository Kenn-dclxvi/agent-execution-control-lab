# click target instructions

`evaluations/targets/click/`はpublic target `pallets/click`のnamespaced evaluation instanceを扱う。root、[`evaluations/AGENTS.md`](../../AGENTS.md)、[`evaluations/targets/AGENTS.md`](../AGENTS.md)を追加適用する。instance identityと現在状態は[`target.json`](target.json)、登録状態は[`../README.md`](../README.md)を正本とする。

## Fixture qualification

既存Click case系列と同じfixture policyで新revisionを作る場合は次を守る。別policyを導入する場合は、既存revisionを変更せず新しい設計・case revisionとして固定する。

- gate commandはtarget repository rootをcwdとして実行する。cwd外実行で生じるseed非依存失敗をprompt qualityへ混ぜない。
- seedは固定target commitへ適用可能な逆patchとして保存し、`git apply --check`で適用可能性を確認する。
- 既存case系列では2026-05-01以降のsource changeから`src/`部分をseed化している。この選定境界を既存revisionへ遡及変更しない。
- seed patchは純粋なdiffだけをmodel-visible fixtureへ含める。commit messageやreference postimageを推測できる`git show` headerを混ぜない。
- seed由来commitとreference implementationはraterのforbidden inputとして扱い、model-visible TaskSpecやrating inputへ漏らさない。

## Execution profile

- 2026-07-27以降の新規通常比較はreasoning effort `medium`を運用基準とする。既存`high` resultは履歴として保持し、reasoningが異なるresultを同一comparisonへ混ぜない。
- profileは`codex_cli`、Python、runtime identity、permission、token accountingを固定する。CLIまたはruntime identityが異なるresultを同一comparisonへ混ぜない。
- gate実行ではworkspace側`src`を解決するため、現行Click profileが要求する`PYTHONPATH=src`境界を維持する。runtime shimだけでsource importを代替したとみなさない。
- F07-Pの現行offline lock確認はconsole scriptの所在へ依存させず、profile / TaskSpecが固定したmodule invocationを正とする。
- `max_workers`とatomic run再利用の共通規則は親[`evaluations/AGENTS.md`](../../AGENTS.md)を正とし、このtargetのready slot数へ合わせて設定値を変更しない。

## Rating contract

- Click rating contractはcase ID単位のruleを持つinstance固有artifactであり、`the-caption`側contractをそのまま参照して採点しない。
- 現行contractは`target.json`の`current_rating_contract`を正とする。contract変更は新revisionとして追加し、既存resultを再採点しない。
- required gateのcwd、seed provenanceのforbidden input、Click固有diagnosticはcontract本体へ固定する。これらをREADMEの説明だけで変更しない。
- kernelへ登録するのはcontract identity、SHA-256、collector schema、policyなどtarget非依存の参照情報に限定し、Click case IDやtarget pathによる分岐を追加しない。

## Prompt bundle

Clickの`prompts/`には親[`evaluations/targets/AGENTS.md`](../AGENTS.md)が準用するprompt lifecycleを適用する。

- root `AGENTS.md`、repository sub-AGENTS、Repository Authorityなど異なる配置は、それぞれ一つの構成軸としてbundle identityへ固定する。
- THE-CAPTION由来本文をbyte-identicalに水平適用しても、Click側target mapとmanifestを持つ別instance artifactとして固定する。
- donor candidateの評価・採用・projection状態をClickへ継承しない。Click内での評価resultと採用判断を別に行う。

## README index

`cases/`、`profiles/`、`sets/`、`rating-contracts/`、`results/`、`prompts/`のREADMEは現在のartifact索引と一次artifactへの導線に限定する。

- fixture qualification、runtime、contract revision、prompt lifecycleの規則はこの`AGENTS.md`へ置く。
- 個別resultのscoreやKPIをREADMEへ詳細再掲せず、result本体へ委譲する。
- 失敗revision、未rating profile、非互換resultも履歴artifactとして保持し、README整理のために削除または上書きしない。
