# Evaluation target instances

評価対象repository（target）ごとの計測系列を別管理する台帳である。この文書はtarget instanceの登録、layout、境界の正本とする。評価基盤自体のLayerと境界は[`docs/prompt-comparison-workflow.md`](../../docs/prompt-comparison-workflow.md)、領域規則は[`evaluations/AGENTS.md`](../AGENTS.md)を正本とする。

instanceが登録されていることは、評価済み、採用済み、release済み、本体反映済みのいずれも意味しない。

## 2層の境界

計測基盤はtarget非依存の**kernel**と、target固有の**instance**に分ける。2026-07-26に実測した現在の帰属は次のとおりである。

| 層 | 含まれるもの | 実測した根拠 |
| --- | --- | --- |
| kernel（target非依存） | `scripts/prepare_case_fixture.py`、`scripts/evaluation_loop.py`とLayer 2〜4の実行経路、`layer2/`、3 KPI、compatibility key、append-only registry | fixture固定のCLI引数は`--case` / `--source-repo` / `--output`のみで、target repositoryはparameter。`scripts/`と`layer2/`の`.py`はtarget repositoryによる実行分岐を持たない |
| instance（target固有） | case artifact、profile、set、rating contract、prompt bundle（baseline / candidate / route / release）、target固有の採点補助module | rating contractは`boundary_rules`と`case_quality_rules`をcase ID単位で内包する。`scripts/quality_audit_policy.py`と`scripts/standard14_quality_audit.py`はtarget側のsource pathをhard-codeする |

制御prompt本文（`SPEC`〜`RECOVERY`の13 label）は見出し語を除きproject固有語彙を持たないため、instance間で出発点として流用できる。ただしbundleのtarget mapはtarget側のdirectory構造に依存するため、bundleはinstance固有artifactとして扱う。

## 登録済みinstance

| target_id | layout | visibility | 第三者再現 | descriptor | 状態 |
| --- | --- | --- | --- | --- | --- |
| `the-caption` | `legacy_root` | private | 不可 | [`the-caption/target.json`](the-caption/target.json) | 既存計測系列。実行可能な現行instance |
| `click` | `namespaced` | public | 可 | [`click/target.json`](click/target.json) | control-free baseline bundleのみ作成済み。case、rating contract、profile、resultは未作成 |

`click`（`pallets/click`、BSD-3-Clause）はgate 1〜9の判定と14項目coverage対応を[`docs/public-target-selection-phase0.md`](../../docs/public-target-selection-phase0.md)で確定して登録した。**登録は評価の実施を意味しない。** 現時点でrating contractが未作成のため`current_rating_contract`は`null`であり、runを実行できる状態ではない。段階計画は[`docs/research-backlog.md`](../../docs/research-backlog.md)の項目10を参照する。

## layout

| layout | 意味 |
| --- | --- |
| `legacy_root` | artifact rootがrepository rootの共有path（`evaluations/cases`、`prompts/candidates`など）に置かれている。`the-caption`のみに許可する |
| `namespaced` | artifact rootが`evaluations/targets/<target_id>/`配下に閉じている。新規instanceはこちらを使う |

`the-caption`のartifact pathを移動しない。既存testは`ROOT / "evaluations/profiles/..."`形式で個別profileを直接参照し、`evaluations/results/`のresultはwrite-onceである。移動して得られるのはlayoutの対称性だけで、既存試験の実行可能性とimmutable historyを損なう。`legacy_root`はこの非対称を明示的に受け入れるための宣言であり、暫定措置ではない。

## instance間の境界

- `target_repository_ref`はcompatibility keyの一項目である（[`evaluations/AGENTS.md`](../AGENTS.md)）。**別instanceのresultを同一比較へ入れない。**
- rating contractをinstance単位で作り直す以上、`quality_score`の絶対値をinstance間で比較しない。観察できるのは各instance内の差と、方向の一致だけである。
- kernelへtarget固有の分岐、path、case IDを追加しない。target固有の採点はinstance側のmoduleへ置く（[`scripts/AGENTS.md`](../../scripts/AGENTS.md)）。
- 既存instanceのartifact、result、identityを新instance追加の都合で変更しない。
- executor変更とtarget変更を同一比較単位へ混ぜない。

## 新instanceの追加手順

1. [`docs/research-backlog.md`](../../docs/research-backlog.md)項目10のtarget選定gate 1〜9を実測で判定する。
2. `evaluations/targets/<target_id>/target.json`を`layout: namespaced`で作成する。
3. artifact root（`cases/` `profiles/` `sets/` `rating-contracts/` `results/`）を同directory配下に作る。
4. 最小1 caseをfixture qualificationし、bit-identical bundleでnull calibrationを行う。
5. この台帳の登録済みinstance表へ追記する。
6. baselineから測り直す。既存instanceのresultを比較対象にしない。
