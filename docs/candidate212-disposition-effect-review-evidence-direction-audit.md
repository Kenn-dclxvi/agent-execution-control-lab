# Candidate212 disposition効果限定review evidence 方向監査

## 状態

- `direction_passed`
- `candidate_creation_allowed`
- `candidate_created`
- `evaluation_not_started`

## 監査対象

[Candidate212作成前設計](candidate212-disposition-effect-review-evidence-design.md)の`review_terminal_support`と`review_evidence_consumer_ready`が、ケース名、scope名またはobservation名の対応を使わず、ADR9 r2で必要な三つのreview経路を残せるかを確認した。

これはCandidateの効果を証明する監査ではない。保存済み入力とtraceから、promptへ置く一般的なpermission境界が作成前gateを満たすかを確認する。

## 判断単位

監査ではscopeやdescriptor名を対応付けず、各時点で次の三点だけを見る。

1. packetまたはadmission済み観測が、allowed terminal dispositionのsupportを既に完成しているか。
2. 完成していない場合、どの具体的命題が未確定か。
3. requested resultのsuccessとnon-valueが、残るallowed dispositionを異なる結果へ分けるか。

## 経路監査

| 経路 | 現在のsupport | 未確定命題 | requested resultの効果 | read permission |
|---|---|---|---|---|
| packet内に具体的反例あり | `counterexample_found`が完成 | なし | 別sourceの値はterminal kindを変えない | なし |
| packetに反例なし、必須観測未実施 | terminal未完成 | 必須観測のsuccess / non-value | successなら全必須命題を閉じ得て、non-valueなら`unavailable`を成立させ得る | あり |
| 必須観測success | `no_counterexample_found`が完成 | なし | 後続観測はterminal kindを変えない | なし |
| 必須観測non-value | `unavailable`が完成 | なし | 後続観測はterminal kindを変えない | なし |
| review permission denied | review producerを作らない | 判定対象外 | repository resultを消費できない | なし |
| review不要 | Candidate147通常経路 | 判定対象外 | review dispositionを消費できない | なし |

## 保存traceへの反証適用

### Candidate211のpaired-scope read

失敗runでは、packet内に具体的instance、規範、固定designとの直接矛盾およびgeneral-design effectが揃っていた。この時点で`counterexample_found` supportが完成する。

paired-scope resultのsuccess / non-valueはいずれも、そのcertificateを失効せず、別のadmissible terminal kindへ変えない。したがって`review_evidence_consumer_ready=false`となる。

### Candidate210のprojection source再read

inventoryまたはconsumer contractの値はpacketとprovenanceでadmission済みである。同じ命題のdirect sourceが存在しても、未確定命題は作られない。したがって同sourceへのconsumerは成立しない。

### 必要readの保持

packetに反例がなく、TaskSpec-requiredな命題のsuccess receiptがまだない場合、successとnon-valueは`no_counterexample_found`と`unavailable`を分け得る。この場合だけconsumerが成立する。

この判定はsource名やscope名ではなく、requested resultが未確定命題とterminal dispositionへ持つ効果に基づく。

## 成功手順を義務化していないこと

Candidate212は「packetを先に判定する」「一件ずつ読む」「counterexampleを考えてからmanifestを見る」という実行順を要求しない。

どのmodel stepでも、read発行時にadmission済みinputがterminal supportを完成しているならread permissionがなく、完成していなければrequested resultが残るdispositionを分ける場合だけpermissionがある。この境界はtool順と独立している。

## 新しい誤経路を増やさないこと

- scope-to-observation対応を追加しない。
- manifest全体をrequired evidenceへ昇格しない。
- packet valueをdirect sourceより弱い値へ降格しない。
- exact JSONだけを理由にvalidなproducer resultを拒否しない。
- `counterexample_found`のためのcertificateと、`no_counterexample_found`のための全必須命題closureを混ぜない。

## 判断

Candidate212のpredicateは、名称対応やcase分岐を使わず、保存traceで観測した不要read辺を閉じながら、必要なsuccess / non-value observation経路を残せる。

したがってCandidate147を直接baseとするCandidate212 bundleの作成を許可する。不要readが実際に0件になることと品質維持は未評価であり、ADR9 r2 N=5で確認する。

## Candidate作成時の拘束

- root `AGENTS.md`以外はCandidate147とbyte-identicalにする。
- review evidence consumerをterminal dispositionへの効果で限定する。
- case identity、固定path、scope identity、observation identityを本文へ入れない。
- Candidate211の`scope_evidence_binding`とexact JSON interfaceを継承しない。
- Candidate bundle作成と評価profile作成を同じ未監査変更へ混ぜない。

## 参照

- [Candidate212作成前設計](candidate212-disposition-effect-review-evidence-design.md)
- [Prompt制御設計原則](prompt-control-design-principles.md)
- [Candidate211 ADR9 N=5結果](../evaluations/results/candidate211-required-scope-review-interface-adr9-r2-n5_2026-08-13.md)
