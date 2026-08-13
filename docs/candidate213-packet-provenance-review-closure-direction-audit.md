# Candidate213 packet provenance review closure 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `evaluation_not_started`

## 監査対象

[Candidate213作成前設計](candidate213-packet-provenance-review-closure-design.md)が、packet valueの意味、case名、field名またはscope名の対応を使わず、Candidate212で観測したsource再readを閉じながら必要な未投影source経路を残すかを確認した。

これはCandidateの効果を証明する監査ではない。保存traceへ一般的なsource identity permission境界を当て、Candidate作成前gateを確認する。

## 直接観測できる入力

rootはpacketを構築する時点で次を観測できる。

- TaskSpecから直接配送するinput identity
- repositoryから取得し、packetへsemantic valueを投影したsource identity
- reviewerへ配送するpacket identity
- TaskSpec-fixed finite evidence manifestのtarget identity

したがって、packetへ値を供給したrepository sourceのexact集合は、値の意味を分類せず固定できる。reviewer read targetとのmembership照合もidentity比較だけで行える。

## Candidate212 traceへの適用

### packet投影元再read

Candidate212で観測した22回の投影元再readは、いずれもpacket構築に使用済みのsource identityをreviewerが再びtargetにした。命題の同一性を問わず、全件で`review_source_read_forbidden=true`となる。

packet-counterexample内の15回は次のように閉じる。

| case | Candidate212投影元再read | Candidate213境界 |
|---|---:|---|
| ADR03 | 3 | closed source membershipで禁止 |
| ADR04 | 0 | 既存read-free経路を維持 |
| ADR05 | 9 | closed source membershipで禁止 |
| ADR06 | 3 | closed source membershipで禁止 |

### paired-scope read 2回

ADR05のpaired-scope sourceはpacket投影元ではないため、closed source membershipだけでは禁止されない。ただしCandidate212の同じrunは、paired read前に投影元inventory / contractを再読して具体的反例を構成した。

Candidate213では投影元再読を発行できない。packetからterminal supportが成立する場合は、未投影sourceであっても`review_evidence_consumer_ready=false`となる。成立しない場合にpaired resultがdispositionを分け得るかは実試験で判定する。ここを成功runの判断順として規定しない。

paired readが一件でも残れば、全packet-counterexample read 0の停止条件でCandidate213を不通過にする。

## 正常経路監査

| 経路 | packet source | 未投影source | permission結果 |
|---|---|---|---|
| packet内に具体的反例あり | closed | terminal support成立後は不要 | 全readなし |
| packetに反例なし、必須観測未実施 | closed | success / non-valueがdispositionを分けるtarget | 未投影targetだけread可 |
| 必須観測success | closed | terminal support完成 | 後続readなし |
| 必須観測non-value | closed | `unavailable` support完成 | 後続readなし |
| review permission denied | packet未作成 | なし | reviewer / readなし |
| review不要 | packet未作成 | なし | Candidate147通常経路 |

ADR07 / ADR09のpaired-scope sourceはpacketへ投影されていないため、必要観測のpermissionを維持する。packet投影元だけは追加確認として読めない。

## 成功手順を義務化していないこと

Candidate213は「packetを先に判定する」「inventoryよりpairedを後に読む」などの順序を要求しない。

どの時点でも、read targetがclosed source setに含まれればpermissionがなく、含まれない場合もterminal support成立後はconsumerがない。この二つはtool順と独立した発行境界である。

## 新しい誤経路を増やさないこと

- packet valueからproposition labelを生成しない。
- field名をsource identityへ対応させない。
- manifest全体をclosed sourceまたはrequired evidenceへ昇格しない。
- 未投影sourceを一律禁止しない。
- closed source集合をreviewerに再構成させない。
- rootにreview judgementを実行させない。

## 判断

Candidate213のsource closureは、Candidate212で観測した投影元再read 22回を意味分類なしで禁止でき、ADR07 / ADR09の未投影paired observationを保持する。

ADR05のpaired read 2回までterminal support境界で閉じるかは未評価であり、ADR9 r2 N=5のzero-tolerance gateで判定する。この不確実性はCandidate作成を妨げないが、一件でも再発した場合は機序不通過として停止する。

したがってCandidate147を直接baseとするCandidate213 bundleの作成を許可する。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- packet source identity集合をreviewer起動前に固定する。
- closed sourceへのreviewer readを例外なく禁止する。
- 未投影sourceはdisposition-changing consumerがある場合だけ許可する。
- Candidate212のprompt本文、case固有語、field-to-proposition mappingを継承しない。

## 参照

- [Candidate213作成前設計](candidate213-packet-provenance-review-closure-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate212 ADR9結果](../evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5_2026-08-13.md)
