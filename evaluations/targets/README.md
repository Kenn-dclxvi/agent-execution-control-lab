# 評価ターゲットインスタンス

評価対象（ターゲット）ごとの計測系列を別管理する台帳である。対象はrepository snapshotまたはsemantic protocolであり、この文書はターゲットインスタンスの**登録、layout、kernel / インスタンス境界の定義**を正本とする。インスタンスの追加・更新と`namespaced`アーティファクトの運用規則は[`AGENTS.md`](AGENTS.md)、評価基盤自体のレイヤーと境界は[`docs/prompt-comparison-workflow.md`](../../docs/prompt-comparison-workflow.md)を正本とする。

インスタンスが登録されていることは、評価済み、採用済み、release済み、本体反映済みのいずれも意味しない。

## 2層の境界

計測基盤はターゲット非依存の**kernel**と、ターゲット固有の**インスタンス**に分ける。

| 層 | 含まれるもの | 境界 |
| --- | --- | --- |
| kernel（ターゲット非依存） | `scripts/prepare_case_fixture.py`、`scripts/evaluation_loop.py`とLayer 2〜4の実行経路、`layer2/`、3 KPI、互換条件、append-only registry | target subjectはパラメータとして受け、ターゲット固有のパス、case ID、分岐を持たない |
| インスタンス（ターゲット固有） | ケース、プロファイル、セット、rating contract、プロンプトバンドル、result、ターゲット固有の採点補助 | repository fixtureまたはsemantic protocol、TaskSpec、case rule、bundle target mapへbindする |

制御プロンプト本文をインスタンス間の出発点として流用することはできるが、バンドルのtarget mapはターゲット側のディレクトリ構造に依存する。したがってプロンプトバンドルを含む評価アーティファクトはインスタンス固有アーティファクトとして扱う。

## 登録済みインスタンス

| target_id | layout | visibility | 第三者再現 | ディスクリプタ | 状態 |
| --- | --- | --- | --- | --- | --- |
| `the-caption` | `legacy_root` | private | 不可 | [`the-caption/target.json`](the-caption/target.json) | 既存計測系列。実行可能な現行インスタンス |
| `click` | `namespaced` | public | 可 | [`click/target.json`](click/target.json) | Bundle A Std14とCandidate125水平適用N=5完了。採用は未実施 |
| `agent-execution-control-lab` | `namespaced` | public | 可 | [`agent-execution-control-lab/target.json`](agent-execution-control-lab/target.json) | PRレビュー測定系列。機能仕様r1固定、Core Baseline未qualification、正式result 0件 |
| `portable-instruction-semantic-conformance` | `namespaced` | public | 可 | [`portable-instruction-semantic-conformance/target.json`](portable-instruction-semantic-conformance/target.json) | control-freeで測定成立。portable full-agent N=1は14 / 14 valid、7 / 14 score 4でquality停止し、C147 referenceは未発行 |

`the-caption`のvisibilityは、計測が固定した移行前treeの可視性を指す。2026-08-01〜08-03の移行で公開された[`Kenn-dclxvi/the-caption`](https://github.com/Kenn-dclxvi/the-caption)は履歴を切り出し直しており、このインスタンスが固定するcommit / treeを含まない。したがって公開版は既存インスタンスの現在状態ではなく、`click`と同格の別インスタンスとして登録する。登録時期はrelease計測が必要になった時点とし、それまでこの表へ追加しない。時間境界は[`docs/repository-overview.md`](../../docs/repository-overview.md)の「対象リポジトリの公開移行」を正本とする。

`click`（`pallets/click`、BSD-3-Clause）はターゲット選定と14項目coverageを[`docs/public-target-selection-phase0.md`](../../docs/public-target-selection-phase0.md)で固定したpublicインスタンスである。Bundle AのStd14 baselineは[`click Std14 result`](click/results/click-control-free-standard14-n5_2026-07-26.md)を一次resultとする。後続アーティファクトの所在は[`click/`](click/)配下の各索引を参照する。

`agent-execution-control-lab`は、このリポジトリ自身のPRレビュー実行経路を固定fixtureで診断するpublicインスタンスである。ターゲットrefと移行前probeの境界は[`target.json`](agent-execution-control-lab/target.json)、アーティファクトの所在と未qualification状態は[`README.md`](agent-execution-control-lab/README.md)を参照する。

`portable-instruction-semantic-conformance`はrepository snapshotではなく、固定operation ledgerへの一回応答を対象とするsemantic protocolインスタンスである。`target_repository_ref`を持たず、subject、runtime、prompt identityを分ける。登録bytes、測定基盤qualificationと未決定の採用境界は[`README.md`](portable-instruction-semantic-conformance/README.md)を参照する。

## layout

| layout | 意味 |
| --- | --- |
| `legacy_root` | アーティファクトのrootが共有パス（`evaluations/cases`、`evaluations/profiles`、`prompts/candidates`など）に置かれている。既存`the-caption`のみに許可する |
| `namespaced` | アーティファクトのrootが`evaluations/targets/<target_id>/`配下に閉じている。新規インスタンスはこちらを使う |

`the-caption`のアーティファクトのパスは移動しない。既存のプロファイル / resultは現在のパスとidentityへbindされており、layout対称化のための移動は不変の履歴を損なう。`legacy_root`はこの非対称を明示的に保持する宣言であり、暫定措置ではない。

## インスタンス間の境界

- repository targetの`target_repository_ref`とsemantic protocol targetの`target_subject_ref`は、それぞれ比較の互換条件の一部である。target kindが異なるresultまたは別インスタンスのresultを同一比較へ入れない。
- rating contractはインスタンス固有のcase ruleを持つため、`quality_score`の絶対値をインスタンス間で比較しない。
- kernelへターゲット固有のパス、case ID、実行分岐を追加しない。ターゲット固有のアーティファクトと採点補助はインスタンス側へ閉じる。
- 新インスタンス追加の都合で既存インスタンスのアーティファクト、result、identityを変更しない。
- executor変更とターゲット変更を同一比較単位へ混ぜない。

新インスタンスの追加手順と`namespaced`アーティファクトの更新規則は[`AGENTS.md`](AGENTS.md)を参照する。
