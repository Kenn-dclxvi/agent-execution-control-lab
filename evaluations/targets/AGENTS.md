# target instance instructions

`evaluations/targets/`の指示は、ターゲットインスタンスの登録情報を保守し、`namespaced`インスタンスのアーティファクトを既存`the-caption`系列と混ぜずに管理するための規則を扱う。ルートの`AGENTS.md`と[`evaluations/AGENTS.md`](../AGENTS.md)を追加適用する。

インスタンスの登録、`legacy_root` / `namespaced` layout、kernel / インスタンス境界の定義は[`README.md`](README.md)を正本とする。この`AGENTS.md`は、その定義を変更せずにアーティファクトを追加・更新する際の作業規則を正本とする。

## 台帳の保守

- インスタンス追加時は`target.json`へtarget identity、layout、visibility、現行のrating contractなど、ディスクリプタが必要とする参照だけを固定する。ゲートコマンド、プロンプトバンドル、resultの実体をディスクリプタへ複製しない。
- `README.md`の登録済みインスタンス表は現在台帳とし、インスタンス追加、layout変更、状態要約の変更があった場合だけ追従させる。
- インスタンスが登録済みであることと、評価済み、採用済み、release済み、ターゲット本体へ反映済みであることを混同しない。
- `legacy_root`は既存`the-caption`だけに許可し、そのアーティファクトのパスを対称化のために移動しない。新インスタンスは`evaluations/targets/<target_id>/`へ閉じる`namespaced` layoutを使う。
- 別インスタンスのケース、プロファイル、セット、rating contract、プロンプトバンドル、resultを同一比較へ混ぜない。インスタンス間では`quality_score`の絶対値を比較しない。

## namespacedアーティファクトのライフサイクル

`namespaced`インスタンス配下では、[`evaluations/AGENTS.md`](../AGENTS.md)のケース、プロファイル、4 Layer、互換条件、model-visible、不変の履歴の規則を同じ意味で適用する。

- `cases/`: case revision、fixture identity、model-visible / model-invisible境界を固定し、結果確認後に既存revisionを上書きしない。
- `sets/`: set revisionとcase membershipを固定し、既存revisionを上書きしない。
- `profiles/`: model、reasoning、runtime / CLI、permission、セット / ケース、rating、repetition、停止条件を実行前に固定する。結果確認後の変更は新しいrevisionにする。
- `rating-contracts/`: インスタンス固有のcase ruleを持つ独立したcontractとして管理し、変更時は新しいcontract ID / revisionを追加する。過去のresultを新しいcontractで再採点しない。
- `results/`: write-onceの一次resultを保持し、READMEは要約と所在だけを持つ。別インスタンスのresultへ統合しない。

## namespacedプロンプトのライフサイクル

`evaluations/targets/<target_id>/prompts/`はパス上[`prompts/AGENTS.md`](../../prompts/AGENTS.md)を自動継承しないため、この領域規則から同文書のbaseline / candidate / route / releaseのライフサイクルを明示的に準用する。

- baselineはsource repository / commitまたはtree / source path / content SHA-256へbindし、取得後にその場で変更しない。
- candidateはbaseline identity、解く問題、変更軸、非目標、事前ゲートを固定し、一つのcandidateで一つのpredicateまたは一つの構成軸だけを扱う。
- routeはbaseの全文を複製せず、適用条件とdelta identityを固定する。
- release、approval、runtime projectionは別状態として扱う。releaseアーティファクトの存在だけで採用またはターゲット本体反映を意味しない。
- インスタンス間でバンドルを共有アーティファクトとして扱わない。本文をバイト単位で同一のまま水平適用する場合も、target mapを含むbundle identityはインスタンス固有に固定する。

## README索引

`namespaced`インスタンス配下のREADMEは、アーティファクトの現在の索引、用途、状態要約、一次アーティファクトへの導線を示す。

- 作成・更新規則はこの`AGENTS.md`またはターゲット固有の`AGENTS.md`へ置き、READMEへ重複させない。
- score、KPI、停止判断はresult本体を正とし、READMEの要約を判定根拠へ格上げしない。
- 過去の実行経緯をREADMEへ長く再掲せず、resultまたは`docs/`の設計・分析文書へ委譲する。
- README整理のために既存のアーティファクト、result、識別子を変更しない。

## 新インスタンスのゲート

新しいインスタンスを追加する場合は、評価スロット発行前に次を完了する。

1. ターゲット選定の根拠と再現性を`docs/`の研究記録へ固定する。
2. `evaluations/targets/<target_id>/target.json`を`layout: namespaced`で作成する。
3. 必要なアーティファクトのルートを同じディレクトリ配下へ作る。
4. 最小ケースをfixture qualificationし、同一のbaseline bundle identityの独立したresultで実行系の安定性を確認する。
5. `README.md`の登録済みインスタンス表へ追加する。
6. 既存インスタンスのresultを比較元にせず、そのインスタンス内のbaselineから計測する。
7. そのインスタンスのcontrol-free baselineで、対象evaluation setの全ケースについて測定が成立し、`quality_score`、all-agent `total_tokens`、`elapsed_seconds`を比較可能なresultとして取得できることを確認する。

## 立ち上げ時の測定成立条件

新インスタンスのゲートの7は、case、fixture、実行環境、採点経路が成立し、3 KPIを欠落なく比較できることの確認である。`quality_score`は比較するKPIであり、特定の値を比較前の合否条件にしない。

- scoreが低い場合は、fixture、実行環境、ケース定義の不備と、reviewerが返した品質結果を分けて切り分ける。model-visible入力から正解を導出できない、実行依存が欠ける、採点不能といった不備があれば、当該case revisionを比較へ使わない（前例: `click`のF07-Pはr1でuv console script不在、r2でサンドボックス外のキャッシュ拒否により各3 / 3件がscore `3`となり、r3で環境を固定した。[`click Std14 result`](click/results/click-control-free-standard14-n5_2026-07-26.md)）。
- case設計と測定が有効であるにもかかわらず、見逃し、余分なfinding、不完全なfindingによってscoreが低い場合は、その値を有効な`quality_score`として保持する。再実行やcase変更によって比較前にscoreを引き上げない。
- この確認は小さい`N`でよい。判定は対象全ケースで測定が成立し、3 KPIが取得できることであり、KPIの値そのものではない。
- 確認後に低いscoreが観測された場合も同じ切り分けを行い、caseまたは測定の不備でなければ比較resultへ含める。
