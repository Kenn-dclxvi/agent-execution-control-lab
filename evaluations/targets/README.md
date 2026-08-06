# Evaluation target instances

評価対象repository（target）ごとの計測系列を別管理する台帳である。この文書はtarget instanceの**登録、layout、kernel / instance境界の定義**を正本とする。instanceの追加・更新とnamespaced artifactの運用規則は[`AGENTS.md`](AGENTS.md)、評価基盤自体のLayerと境界は[`docs/prompt-comparison-workflow.md`](../../docs/prompt-comparison-workflow.md)を正本とする。

instanceが登録されていることは、評価済み、採用済み、release済み、本体反映済みのいずれも意味しない。

## 2層の境界

計測基盤はtarget非依存の**kernel**と、target固有の**instance**に分ける。

| 層 | 含まれるもの | 境界 |
| --- | --- | --- |
| kernel（target非依存） | `scripts/prepare_case_fixture.py`、`scripts/evaluation_loop.py`とLayer 2〜4の実行経路、`layer2/`、3 KPI、compatibility、append-only registry | target repositoryはparameterとして受け、target固有path、case ID、分岐を持たない |
| instance（target固有） | case、profile、set、rating contract、prompt bundle、result、target固有の採点補助 | target repositoryのfixture、TaskSpec、case rule、bundle target mapへbindする |

制御prompt本文をinstance間の出発点として流用することはできるが、bundleのtarget mapはtarget側directory構造に依存する。したがってprompt bundleを含む評価artifactはinstance固有artifactとして扱う。

## 登録済みinstance

| target_id | layout | visibility | 第三者再現 | descriptor | 状態 |
| --- | --- | --- | --- | --- | --- |
| `the-caption` | `legacy_root` | private | 不可 | [`the-caption/target.json`](the-caption/target.json) | 既存計測系列。実行可能な現行instance |
| `click` | `namespaced` | public | 可 | [`click/target.json`](click/target.json) | Bundle A Std14とCandidate125水平適用N=5完了。採用は未実施 |

`click`（`pallets/click`、BSD-3-Clause）はtarget選定と14項目coverageを[`docs/public-target-selection-phase0.md`](../../docs/public-target-selection-phase0.md)で固定したpublic instanceである。Bundle AのStd14 baselineは[`click Std14 result`](click/results/click-control-free-standard14-n5_2026-07-26.md)を一次resultとする。後続artifactの所在は[`click/`](click/)配下の各索引を参照する。

## layout

| layout | 意味 |
| --- | --- |
| `legacy_root` | artifact rootが共有path（`evaluations/cases`、`evaluations/profiles`、`prompts/candidates`など）に置かれている。既存`the-caption`のみに許可する |
| `namespaced` | artifact rootが`evaluations/targets/<target_id>/`配下に閉じている。新規instanceはこちらを使う |

`the-caption`のartifact pathは移動しない。既存profile / resultは現在のpathとidentityへbindされており、layout対称化のための移動はimmutable historyを損なう。`legacy_root`はこの非対称を明示的に保持する宣言であり、暫定措置ではない。

## instance間の境界

- `target_repository_ref`はcomparison compatibilityの一部であり、別instanceのresultを同一comparisonへ入れない。
- rating contractはinstance固有のcase ruleを持つため、`quality_score`の絶対値をinstance間で比較しない。
- kernelへtarget固有のpath、case ID、実行分岐を追加しない。target固有のartifactと採点補助はinstance側へ閉じる。
- 新instance追加の都合で既存instanceのartifact、result、identityを変更しない。
- executor変更とtarget変更を同一比較単位へ混ぜない。

新instanceの追加手順とnamespaced artifactの更新規則は[`AGENTS.md`](AGENTS.md)を参照する。
