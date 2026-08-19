# P006 Codex frontier carrier作成前設計

> [!IMPORTANT]
> **状態**: `precreation_gate_fixed / static_counterexample_audit_required / candidate_not_created`

## 結論

P006はP005 `p005-portable-full-agent-codex-validation-terminal-projection-r1`を直接親とし、共通`FRONTIER`が構成済みのfrontierをCodexの一つの発行境界へ載せる`FRONTIER_CARRIER_CODEX`だけを追加する。P005の共通意味、validation terminal projection、actor、observation、methodおよびrecoveryは変更しない。

閉じる辺は次の一件である。

```text
frontier member Aを発行
  -> Aの個別resultをmodel-visible consumerへ配送
  -> 同じfrontierの未発行member Bを後続model outputから発行
```

全memberの個別invocationを一つのmodel outputへcommitした後は、runtime上の開始・完了順が直列でもよい。成功runのtool順、read範囲または判断順は転記しない。閉じるのは、全memberのcommit前に個別resultをmodelへ返せるpermissionだけである。

## 目的の固定

- 改善系列: C147を機種非依存の共通意味とplatform capabilityへ分離して一枚の`AGENTS.md`へ構成するPortable full-agent系列。
- required effect: P005で残ったaction前の追加model responseを許すfrontier途中result ingressを閉じる。
- preserved effect: P005のScore 4品質、validation carrierのterminal projection、個別invocation identity、真正dependency、fail-fast、actor provenanceおよび一枚配送。
- artifact relation: 管理用componentをcompositionで連結し、構成済み一枚を新しいP006 full bundleへbindする。componentをAgentへ追加readさせない。
- 評価変数: 後続評価ではprompt identityだけを変更し、Standard14、fixture、TaskSpec、oracle、Rating v14、`gpt-5.6-sol / medium`、CLI `0.146.0`、M=24、permission、runner、all-agent token accounting v1および集計を固定する。

## Candidate作成前の固定項目

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプトセット | P005、bundle SHA-256 `519e61d60afbeb71b6302caa1cef62da152540f730ae51e7a0b7184bfa9c5649`、root SHA-256 `2cb70ccd11fcfe605accf9b212050ed08b6db0eb0a522d502d35c33d58301681` |
| 基準状態の最短正常経路 | 共通`FRONTIER`が相互非依存memberを確定し、各memberを個別invocationとして一つのCodex model outputへcommitし、全result受領後に一度だけ次を判断する |
| 保存済み誤経路 | P005 Standard14 N=5のF08は5 / 5件で開始identity result後に対象readを別model responseから発行した。F07 dependency、F07 canonical、A02、F10 entrypointにも同形の追加action前waveがある |
| 既存境界で防げない理由 | 共通`FRONTIER`は途中resultを選択・抑止へ使うことを禁じるが、resultを受け取った後に「使っていない」と分類して残memberを発行できる。P005にはvalidation用carrierはあるがfrontier result ingressのownerがない |
| 追加するpredicate | `frontier_dispatch_ready`と`frontier_dispatch_terminal`。前者は共通`FRONTIER`が閉じたmember集合の搬送準備、後者は全memberの一model-output commitと全result収集を一つの発行遷移へ閉じる |
| 変更が消す判断点 | memberごとの再分類、部分集合だけの先行発行、個別result受領後の続行判断、compound commandによるidentity代替、途中commentaryまたはyield |
| 新たに増える判断点 | 構成済みfrontierが0件、1件、複数件のどれか、および固定platform surfaceで全memberを一model outputへcommit可能か。taskごとのcapability自己判定は増やさない |
| 品質維持 | 固定Standard14 14 Caseで全run Score 4を要求し、case別Score分布を保持する。frontier機序はtrace診断で分け、3 KPIへ追加しない |
| 逆結果の停止条件 | Score 4未達、真正dependency越境、部分発行、compound代替、P005 validation closure退行、P005よりtokensまたはelapsedの一方でも増加、あるいはC147比の未回収costが縮まらない場合は停止する |

## 責務境界

### 共通`FRONTIER`が所有するもの

- result effect scopeと相互非依存性の判定。
- frontier memberのoperation、actor、target、permission、methodおよび期待result種別の固定。
- 真正dependencyを持つoperationを別frontierへ残す判断。

P006はこれらを再判定しない。`FRONTIER`本文も変更しない。

### `FRONTIER_CARRIER_CODEX`が所有するもの

- 構成済みfrontier identityを一つのCodex dispatch groupへbindする。
- 複数memberを一つのmodel outputから個別tool callとしてcommitする。
- 全member commit前の個別result、progress、commentary、notification、mediaまたはyieldのmodel-visible ingressをdenyする。
- 各memberのresult identityとterminal statusを保持し、全件受領後に一度だけ共通consumerへ返す。

0件ではtoolを発行しない。1件ではcarrier用の追加roundや別admissionを作らず、その一件を通常の個別invocationとして発行する。複数件を一model outputへcommitできない場合はsubsetへ縮退せず、そのfrontierを`unavailable`へbindする。

### 所有しないもの

- frontier memberの追加、削除、並べ替え、再分類またはmethod選択。
- 実行開始・完了の物理的同時性。
- shell compound command、外部wrapper、runner変更、tool adapter変更またはruntime変更。
- validation plan、validation fail-fast、terminal projectionおよびcontinuation identity。
- Case固有のcommand、path、read範囲、oracleまたはexpected result。

## 直接親と非継承

直接親はP005である。P006はP005の全componentをbyte保持し、新しいCodex frontier carrier componentだけを追加する。

- Candidate193は現在responseへのfrontier一対一bindingを示す設計sourceだが、review系列、20条項全文および評価状態を継承しない。
- Candidate205は抽象frontierだけではCodexの発行表面を保持できなかった反例であり、直接親ではない。
- Candidate253からCandidate258までは自然語条件追加で途中result routeが残った反例であり、本文を継承しない。
- C147はKPI比較基準と失われたplatform surfaceのsourceであり、P006の直接親ではない。
- P001からP004までのvalidation設計、評価状態および失敗routeを復活させない。

## platform能力

同じCLI `0.146.0`のC147保存traceでは、相互非依存invocationを一つのmodel responseから個別tool callとしてcommitするrouteが観測済みである。P005とC147の差はruntime変更ではなくprompt構成差である。したがってP006は既存surfaceへbindでき、executor、runner、tool adapterまたはruntimeの変更を要求しない。

`model output`は配送・発行境界を指す。toolの実行開始順や完了順を同時にする要求ではない。全tool callが先にcommit済みなら、runtimeが順次実行して個別resultを返してもこの境界を満たす。

## 作成gate

次の静的反例をすべて閉じた場合だけP006 bundleを作成する。

1. 0件または1件のfrontierへ余分なcarrier roundを加える。
2. subsetだけをcommitし、最初のresult後に残memberを発行する。
3. resultを判断へ使っていないという自己分類で途中ingressを許す。
4. tool実行順とmodel-output commit境界を混同する。
5. shell compound commandでmember identityを失う。
6. carrier内でmember、methodまたはpermissionを再bindする。
7. 真正dependencyを持つoperationを同じdispatch groupへ入れる。
8. missing、unreadableまたは矛盾後に初めて許される追加observationを先行commitする。
9. readも禁止する開始gateを越えてreadをcommitする。
10. taskごとのcapability自己判定または追加admissionを作る。
11. platform surfaceが使えない時にsubset発行へfallbackする。
12. P005 validation carrierを変更または再開する。
13. 全member commit前にcommentary、notification、mediaまたはyieldへ途中状態を出す。
14. 全result受領後に同じfrontierへmemberを追加して再開する。

一件でもblocking counterexampleが残る場合は`candidate_not_created`とし、共通`FRONTIER`へ条件を足さずplatform carrier境界を再設計する。
