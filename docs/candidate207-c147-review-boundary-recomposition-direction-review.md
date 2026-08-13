# Candidate207 C147 review境界再構成 保存trace事前反証

## 結論

修正後のC207本文案に対する保存trace事前反証は`blocking_counterexample=0 / candidate_creation_allowed / evaluation_not_started`である。

初回本文案には、投影済みcounterexample certificateとdirect read eligibilityの直接関係が不足していた。C202の9 / 20先読みとC203の2 / 20残存失敗を当てると、単に「未解決resultを変えられる観測」とした条件だけでは、packetを判定する前のmanifest readを禁止できなかった。この反例を受け、先行operationやreceiptを作らず、`projected_counterexample_established(packet)=true`をdirect-read consumerの否定条件へ直接入れた。

この修正後は、保存済み誤経路のいずれも本文上許可されない。一方、LLMがpredicateを実行時に正しくbindするかは未観測であり、ADR9の機序gateで確認する。静的反証通過は品質・機序通過を意味しない。

## 反証対象

- C147 ADR9 r2 N=50のreview要否、required reviewer欠落、過剰`unavailable`、canary配送、ADR07 result汚染
- C173 ADR9 r2 N=50のADR05 missing優先、ADR06 canary配送、ADR07 forbidden-input contamination
- C175/C202の投影済みcounterexample成立前direct read
- C203の不要reviewer、projection receipt不一致、残存direct read
- C191 Standard14の開始identityと許可readの逐次化

C173、C175、C191、C202、C203は親または比較基準ではなく、C147直接child本文案を反証する保存証拠としてだけ使う。

## 保存誤経路との対応

| 保存誤経路 | 本文案へ当てた結果 | 判定 |
| --- | --- | --- |
| C147 ADR01/02の不要review | supplied boundaryがdirect authority closure、exhaustive validation、implementation-local effectへbindされ、`prechange_review_requirement_state=not_required`。producer applicabilityはfalse | 閉じる |
| C147 ADR03〜06のreview省略・過剰`unavailable` | autonomous/open/non-exhaustive/general-design-change boundaryが`required`を成立させ、permission allowed時だけproducerを一件起動 | 閉じる |
| C147 ADR06 / C173 ADR06のcanary配送 | `CONTEXT`がhistory、untrusted prior result、root予想およびforbidden source全体をpacket membershipから除外 | 閉じる |
| C147 ADR07誤blocked / C173 ADR07 contamination | `no_counterexample_found`は全scope successへbindし、forbidden inputはpacket外。真正なproducer resultをrootが汚染扱いへ再生成できない | 閉じる |
| C147 ADR09 review未起動 / C173 ADR05 reviewer前停止 | manifest descriptorとtarget valueを分離し、missing targetをreviewer-owned observationにする | 閉じる |
| C173 ADR05の成立済みcounterexampleを別missingで失効 | 一つの有効な`counterexample_found` certificateを別scope missingで失効させない | 閉じる |
| C175/C202のcounterexample前direct read | `projected_counterexample_established(packet)=true`なら`review_observation_consumer_ready=false` | 修正後に閉じる |
| C203 ADR01/02不要review | 「TaskSpecがreviewを記載」のみではrequiredにせず、supplied boundary recordのeffect条件まで要求 | 閉じる |
| C203 projection receipt不一致 | 新しいprojection receipt、acknowledgement、完全一致operationを作らない。packet値そのものをterminal predicateとconsumerが読む | 同じ誤経路を導入しない |
| C203 ADR05残存mixed read | packet上certificate成立時はdirect read consumer自体がfalse。forbidden source全体もpacket外 | 閉じる |
| C191 Standard14の44 / 45逐次化 | C147 `DECISION_BOUNDARY`を逐語維持し、review requirement stateをtool operationまたはmodel-step barrierにしない | 同じ逐次化を導入しない |

## 正常経路保持

### C147 Standard14

TaskSpecがartifact変更前review contractと判定対象boundary record集合を明示しない場合、`REVIEW_BOUNDARY`はreview operationを作らない。C147の開始identity、許可read、evidence consumer、validation closureおよび共同発行は変更しない。

`producer_execution_required`の置換は、明示producer operationにapplicabilityまたはpermissionが明示される場合だけその値を追加で消費する。criterion owner、risk ownerまたは`review`等の役割語だけではproducerを選ばない既存境界を維持する。

### ADR9 closed boundary

ADR01/02ではreview contract内にproducer identityが存在してもrequirement stateが`not_required`なので、producerを起動せずC147のimplementation・validation経路へ進む。

### ADR9 required boundary

ADR03〜07/09では、review requirement、permission、producer、packet、observation、terminalを別のmodel step列として定義しない。必要なrepository inputの受領後、bind済みpredicateに従って既存producer/evidence lifecycleを使う。

## C202反例による本文修正

修正前:

```text
review_observation_consumer_ready := ... requested resultが未解決のallowed review dispositionをbind可能 ...
```

修正後:

```text
review_observation_consumer_ready := ... projected_counterexample_established(packet)=false ∧ requested resultが未解決のallowed review dispositionをbind可能 ...
```

「counterexampleを先に判定する」とは書かない。packet上certificateの成立をread eligibilityと同じpredicateの否定条件へ入れるため、先行review step、materialized receipt、projection acknowledgementまたは逐次発行を要求しない。

## 残る実測対象

| risk | ADR9 / Standard14 gate |
| --- | --- |
| supplied boundaryから`not_required / required`を安定してbindできない | ADR01/02 reviewer 0、ADR03〜07/09 reviewer 1 |
| packet counterexampleが成立してもmanifest readを発行する | ADR03〜06 counterexample前direct read 0 / 20 |
| packet値をreceiptへ再構成し、起動またはresult admissionを失う | required reviewer 30 / 30、正しいterminal 30 / 30 |
| missing targetをpacket不備へ戻す | ADR09 reviewer 5 / 5、`unavailable` 5 / 5 |
| forbidden sourceまたはcanaryを配送する | ADR06 0 / 5 |
| review非適用経路へproducer・step・costを流入させる | Standard14 reviewer 0 / 70、共同発行退行0、C147比3 KPI |

## 判断

- C147直接基盤: `confirmed`
- failed lineageの本文継承: `none`
- 保存counterexampleの消費: `complete_for_candidate_creation`
- 手順化されたreview lifecycle: `not_included`
- blocking counterexample: `0 after revision`
- Candidate207 bundle作成: `allowed`
- ADR9発行: `not_yet_authorized; static verification and comparison preflight required`

## 一次参照

- [C207本文案・作成前監査](candidate207-c147-review-boundary-recomposition-draft.md)
- [C202 M5原因分析](candidate202-m5-causal-analysis.md)
- [C203 ADR9結果](../evaluations/results/candidate203-certificate-gated-review-read-adr9-r2-n5_2026-08-13.md)
- [C173 ADR9 N=50機序監査](../evaluations/results/candidate173-concrete-counterexample-adjudication-adr9-r2-n50-audit-r1.json)
- [C175 ADR9・Standard14 N=5](../evaluations/results/candidate175-review-operation-admission-closure-adr9-standard14-n5_2026-08-10.md)
- [C191 Standard14 cost機序再判定](../evaluations/results/candidate191-standard14-cost-mechanism-reassessment-r1.json)
