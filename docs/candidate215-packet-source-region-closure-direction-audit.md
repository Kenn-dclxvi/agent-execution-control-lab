# Candidate215 packet source region closure 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `evaluation_not_started`

## 監査対象

[Candidate215作成前設計](candidate215-packet-source-region-closure-design.md)が、Candidate214の投影元再読0件を維持しながら、同一container内の未投影・非重複regionへ必要時に到達できるかを確認した。

## 直接観測できる入力

- packet itemを供給したinput resultのcontainer identity
- input resultに固定されたcanonical selector / region identity
- manifest targetのcontainer / region identity
- requested targetがwhole containerか固定regionか
- region間の同一、祖先、子孫、重複、非重複

内容の意味、field名、scope名または期待resultは照合に使わない。

## Candidate214失敗への適用

Candidate214の4件では、packetへ使用したsemantic、authority、boundary等のregionと、未投影inventory / contract regionが同じfile内で非重複だった。Candidate215では双方のregionが固定されていれば`review_read_conflicts=false`になり、terminal dispositionを分ける命題を直接bindできる場合だけ観測できる。

このreadでcurrent inventory membershipとcontractが成立すれば、reviewerは具体的instance、適用規範、固定designとの矛盾、general design effectをbindして`counterexample_found`を返せる。rootが判断を補完する必要はない。

## 投影元再読を再開しないこと

packet source regionとrequested regionが同一、祖先、子孫または重複ならconflictである。selector名、部分抽出、hash、存在確認または別commandへ変えても開かない。

requested targetがwhole containerでregionを固定しない場合、そのreadはpacket source regionを包含するためconflictになる。receipt側regionが固定されない場合も非重複を証明できずcontainer fallbackでconflictになる。

## 正常経路監査

| 経路 | region relation | permission |
|---|---|---|
| packetだけでterminal support成立 | 任意 | 追加readなし |
| packet sourceの同一 / 包含 / 重複read | conflict | 禁止 |
| 同じcontainerの未投影・非重複regionがterminalを分ける | non-conflict | そのregionだけ許可 |
| 同じcontainerの非重複regionだがterminalを分けない | non-conflictだがconsumer false | 禁止 |
| receipt region不明 | container fallback | 同一container read禁止 |
| target region不明のwhole-container read | packet regionを包含 | 禁止 |
| 別containerの必要paired success | non-conflict | direct read可 |
| 別containerの必要paired missing | non-conflict | missing resultを`unavailable`へbind |
| review permission denied | packet未作成 | reviewer / readなし |
| review不要 | packet未作成 | Candidate147通常経路 |

## 成功手順を規定していないこと

設計は「inventoryを先に読む」「packetを先に判定する」といった判断順を要求しない。read permissionは、packet receiptとrequested targetのregion relation、およびrequested resultのterminal effectだけで決まる。

## 判断

Candidate215は、Candidate214のcontainer一律閉鎖をregion精度へ狭める一つの変更軸である。必要な同一container内・非重複regionを回復しつつ、投影元regionの同一・包含・重複再読を閉じられる。region不明時のcontainer fallbackにより、不明を許可へ推測する経路も残さない。

したがってCandidate147を直接baseとするCandidate215 bundleの作成を許可する。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- fixed source regionをreceiptへ保持する。
- container一致だけでfixed non-overlap regionを禁止しない。
- region不明時だけcontainer fallbackを使う。
- non-overlap regionにもterminal-effect consumerを要求する。
- Candidate214その他の失敗Candidate本文を親にしない。

## 参照

- [Candidate215作成前設計](candidate215-packet-source-region-closure-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate214 ADR9結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
