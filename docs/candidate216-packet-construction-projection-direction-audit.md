# Candidate216 packet construction projection 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `evaluation_not_started`

## 監査対象

[Candidate216作成前設計](candidate216-packet-construction-projection-design.md)が、Candidate215で成立した固定非重複region routeを維持しながら、container全体のinput resultからpacketへ選んだ部分をconstruction時のprojection receiptへ固定できるかを確認した。

## 直接観測できる入力

- packet itemを構築するadmission済みinput result identity
- repository source container identity
- input object内でliteral itemへ選択したstructural path、rangeまたはsubtree
- requested targetのcontainer / region identity
- region間の同一、祖先、子孫、重複、非重複

field名の意味、case名、命題名、期待resultまたは別sourceとのvalue equalityはprojection生成に使わない。

## Candidate215失敗への適用

Candidate215ではrootがcontainer全体をadmitした後、その一部をpacketへ選んだ。Candidate216はsource read resultのselector有無ではなく、この選択操作そのものをprojection identityの生成点にする。

packet itemがadmission済みobjectの一つのsubtreeからliteralに作られた場合、そのexact pathをreceiptへ固定する。inventory / contract regionがそのpathと非重複で、requested resultが未確定のterminal dispositionを直接分ける場合はread可能である。packetへ使ったsubtreeの同一、親、子または重複regionは再readできない。

## 曖昧projection監査

複数sourceの結合、要約、計算変換または一意なstructural originを持たないitemではprojection regionを推測しない。同じ値を持つfield、名前が対応するfieldまたは後から説明可能なfieldを出所へ昇格せず、repository-backed itemはcontainer fallbackで閉じる。

これにより、materializationできないものを許可へ推測するrouteは増えない。一方、literal structural projectionが一意な通常itemを、元readがwhole-containerだったという理由だけでfallbackへ落とすrouteを消す。

## 正常経路監査

| 経路 | construction / region状態 | permission |
|---|---|---|
| packetだけでterminal support成立 | projection固定済み | 追加readなし |
| whole inputから一意なsubtreeをpacketへ選択 | construction時にprojection materialize | exact regionをreceiptへ固定 |
| packet projectionの同一・包含・重複read | conflict | 禁止 |
| 同じcontainerの固定非重複regionがterminalを分ける | non-conflict + consumer true | そのregionだけ許可 |
| 同じcontainerの固定非重複regionがterminalを分けない | consumer false | 禁止 |
| 複数origin、要約、変換、出所不明 | projection unavailable | container fallback |
| 別containerの必要paired success | non-conflict | direct read可 |
| 別containerの必要paired missing | non-conflict | missing resultを`unavailable`へbind |
| review permission denied | packet未作成 | reviewer / readなし |
| review不要 | packet未作成 | Candidate147通常経路 |

## 成功手順を規定していないこと

設計は「先にpacketを判定する」「inventoryを後に読む」といった順序を要求しない。construction receiptはpacket itemを作る同じoperationのoutputであり、review permissionはそのreceiptとrequested targetの構造関係、既存のterminal-effect consumerだけで決まる。

## 判断

Candidate216は、Candidate215のregion permissionを別candidateから継承するのではなく、C147へ一つの構造provenance境界として再構成する。元readがwhole-containerでもconstruction時のliteral projectionを一意に固定し、曖昧時だけfallbackするため、必要非重複routeと投影元再read禁止を両立できる。未解決反例はない。

したがってCandidate147を直接baseとするCandidate216 bundleの作成を許可する。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- packet constructionと同じoperationでexact structural projectionをmaterializeする。
- source read時のselector欠落だけでcontainer fallbackへ落とさない。
- value equality、意味、field名または後続推測でprojectionを作らない。
- 一意でないprojectionだけをcontainer fallbackへbindする。
- fixed non-overlap regionにもterminal-effect consumerを要求する。
- Candidate215その他の失敗Candidate本文を親にしない。

## 参照

- [Candidate216作成前設計](candidate216-packet-construction-projection-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate215 ADR9結果](../evaluations/results/candidate215-packet-source-region-closure-adr9-r2-n5_2026-08-14.md)
