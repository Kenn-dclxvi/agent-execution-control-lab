# target instance instructions

`evaluations/targets/`の指示は、target instanceの登録情報を保守し、namespaced instanceのartifactを既存`the-caption`系列と混ぜずに管理するための規則を扱う。root `AGENTS.md`と[`evaluations/AGENTS.md`](../AGENTS.md)を追加適用する。

instanceの登録、`legacy_root` / `namespaced` layout、kernel / instance境界の定義は[`README.md`](README.md)を正本とする。この`AGENTS.md`は、その定義を変更せずにartifactを追加・更新する際の作業規則を正本とする。

## Registry maintenance

- instance追加時は`target.json`へtarget identity、layout、visibility、現行rating contractなどdescriptorが必要とする参照だけを固定する。gate command、prompt bundle、result実体をdescriptorへ複製しない。
- `README.md`の登録済みinstance表は現在台帳とし、instance追加、layout変更、状態要約の変更があった場合だけ追従させる。
- instanceが登録済みであることと、評価済み、採用済み、release済み、target本体へ反映済みであることを混同しない。
- `legacy_root`は既存`the-caption`だけに許可し、そのartifact pathを対称化のために移動しない。新instanceは`evaluations/targets/<target_id>/`へ閉じる`namespaced` layoutを使う。
- 別instanceのcase、profile、set、rating contract、prompt bundle、resultを同一比較へ混ぜない。instance間では`quality_score`の絶対値を比較しない。

## Namespaced artifact lifecycle

`namespaced` instance配下では、[`evaluations/AGENTS.md`](../AGENTS.md)のcase、profile、4 Layer、compatibility、model-visible、immutable historyの規則を同じ意味で適用する。

- `cases/`: case revision、fixture identity、model-visible / model-invisible境界を固定し、結果確認後に既存revisionを上書きしない。
- `sets/`: set revisionとcase membershipを固定し、既存revisionを上書きしない。
- `profiles/`: model、reasoning、runtime / CLI、permission、set / case、rating、repetition、停止条件を実行前に固定する。結果確認後の変更は新revisionにする。
- `rating-contracts/`: instance固有のcase ruleを持つ独立contractとして管理し、変更時は新contract ID / revisionを追加する。過去resultを新contractで再採点しない。
- `results/`: write-onceの一次resultを保持し、READMEは要約と所在だけを持つ。別instanceのresultへ統合しない。

## Namespaced prompt lifecycle

`evaluations/targets/<target_id>/prompts/`はpath上[`prompts/AGENTS.md`](../../prompts/AGENTS.md)を自動継承しないため、この領域規則から同文書のbaseline / candidate / route / release lifecycleを明示的に準用する。

- baselineはsource repository / commitまたはtree / source path / content SHA-256へbindし、取得後にin-place変更しない。
- candidateはbaseline identity、解く問題、変更軸、非目標、事前gateを固定し、一つのcandidateで一つのpredicateまたは一つの構成軸だけを扱う。
- routeはbase全文を複製せず、適用条件とdelta identityを固定する。
- release、approval、runtime projectionは別状態として扱う。release artifactの存在だけで採用またはtarget本体反映を意味しない。
- instance間でbundleを共有artifactとして扱わない。本文をbyte-identicalに水平適用する場合もtarget mapを含むbundle identityはinstance固有に固定する。

## README index

namespaced instance配下のREADMEは、artifactの現在の索引、用途、状態要約、一次artifactへの導線を示す。

- 作成・更新規則はこの`AGENTS.md`またはtarget固有`AGENTS.md`へ置き、READMEへ重複させない。
- score、KPI、停止判断はresult本体を正とし、READMEの要約を判定根拠へ格上げしない。
- 過去の実行経緯をREADMEへ長く再掲せず、resultまたは`docs/`の設計・分析文書へ委譲する。
- README整理のために既存artifact、result、identityを変更しない。

## New instance gate

新instanceを追加する場合は、評価slot発行前に次を完了する。

1. target選定の根拠と再現性を`docs/`の研究記録へ固定する。
2. `evaluations/targets/<target_id>/target.json`を`layout: namespaced`で作成する。
3. 必要なartifact rootを同directory配下へ作る。
4. 最小caseをfixture qualificationし、同一baseline bundle identityの独立resultで実行系の安定性を確認する。
5. `README.md`の登録済みinstance表へ追加する。
6. 既存instanceのresultを比較元にせず、そのinstance内のbaselineから計測する。
