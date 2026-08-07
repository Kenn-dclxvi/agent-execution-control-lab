# click target instructions

`evaluations/targets/click/`は公開ターゲット `pallets/click`の`namespaced`な評価インスタンスを扱う。ルート、[`evaluations/AGENTS.md`](../../AGENTS.md)、[`evaluations/targets/AGENTS.md`](../AGENTS.md)を追加適用する。instance identityと現在状態は[`target.json`](target.json)、登録状態は[`../README.md`](../README.md)を正本とする。

## Fixture qualification

既存のClickケース系列と同じfixture policyで新しいrevisionを作る場合は次を守る。別のpolicyを導入する場合は、既存revisionを変更せず新しい設計・case revisionとして固定する。

- ゲートコマンドはターゲットリポジトリのルートをcwdとして実行する。cwd外実行で生じるseed非依存の失敗をプロンプト品質へ混ぜない。
- seedは固定target commitへ適用可能な逆パッチとして保存し、`git apply --check`で適用可能性を確認する。
- 既存ケース系列では2026-05-01以降のsource changeから`src/`部分をseed化している。この選定境界を既存revisionへ遡及変更しない。
- seed patchは純粋な差分だけをmodel-visibleなfixtureへ含める。commit messageやreference postimageを推測できる`git show`のヘッダを混ぜない。
- seed由来のcommitとreference implementationはraterのforbidden inputとして扱い、model-visibleなTaskSpecやrating inputへ漏らさない。

## 実行プロファイル

- 2026-07-27以降の新規通常比較はreasoning effort `medium`を運用基準とする。既存の`high` resultは履歴として保持し、reasoningが異なるresultを同一比較へ混ぜない。
- プロファイルは`codex_cli`、Python、runtime identity、permission、token accountingを固定する。CLIまたはruntime identityが異なるresultを同一比較へ混ぜない。
- ゲート実行ではワークスペース側の`src`を解決するため、現行のClickプロファイルが要求する`PYTHONPATH=src`境界を維持する。runtime shimだけでsourceのimportを代替したとみなさない。
- F07-Pの現行のoffline lock確認はconsole scriptの所在へ依存させず、プロファイル / TaskSpecが固定したmodule invocationを正とする。
- `max_workers`とatomic run再利用の共通規則は親の[`evaluations/AGENTS.md`](../../AGENTS.md)を正とし、このターゲットのreadyなスロット数へ合わせて設定値を変更しない。

## Rating contract

- Clickのrating contractはcase ID単位のruleを持つインスタンス固有のアーティファクトであり、`the-caption`側のcontractをそのまま参照して採点しない。
- 現行contractは`target.json`の`current_rating_contract`を正とする。contract変更は新しいrevisionとして追加し、既存resultを再採点しない。
- 必須ゲートのcwd、seed provenanceのforbidden input、Click固有の診断情報はcontract本体へ固定する。これらをREADMEの説明だけで変更しない。
- kernelへ登録するのはcontract identity、SHA-256、collector schema、policyなどターゲット非依存の参照情報に限定し、Clickのcase IDやターゲットのパスによる分岐を追加しない。

## プロンプトバンドル

Clickの`prompts/`には親の[`evaluations/targets/AGENTS.md`](../AGENTS.md)が準用するプロンプトのライフサイクルを適用する。

- ルートの`AGENTS.md`、repository sub-AGENTS、Repository Authorityなど異なる配置は、それぞれ一つの構成軸としてbundle identityへ固定する。
- THE-CAPTION由来の本文をバイト単位で同一のまま水平適用しても、Click側のtarget mapとマニフェストを持つ別インスタンスのアーティファクトとして固定する。
- donor candidateの評価・採用・projection状態をClickへ継承しない。Click内での評価resultと採用判断を別に行う。

## README索引

`cases/`、`profiles/`、`sets/`、`rating-contracts/`、`results/`、`prompts/`のREADMEは現在のアーティファクト索引と一次アーティファクトへの導線に限定する。

- fixture qualification、ランタイム、contract revision、プロンプトのライフサイクルの規則はこの`AGENTS.md`へ置く。
- 個別resultのscoreやKPIをREADMEへ詳細に再掲せず、result本体へ委譲する。
- 失敗したrevision、未ratingのプロファイル、非互換のresultも履歴アーティファクトとして保持し、README整理のために削除または上書きしない。
