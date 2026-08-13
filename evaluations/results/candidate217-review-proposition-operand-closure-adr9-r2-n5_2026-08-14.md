# Candidate217 review proposition operand closure ADR9 r2 N=5結果

## 結論

Candidate217は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 40 / 5`で、terminal、reviewer cardinality、review result admission / effectはいずれも40 / 45だった。成果物境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件である。

決定的だったのは、`model-visible fixed input`と`reviewer packetへ合法的に投影できるinput`が同じではなかったことである。ADR03からADR06のTaskSpecは`consumer_inventory`と`consumer_contracts`を固定入力とする一方、reviewer packetをsemantic projection、境界、authority、適用時のboundary normative contract、必須scope、manifestだけに限定していた。C217はadmission済みdirect operandをpacketへ必須化し、reviewer-owned observationへの再分類を禁じたため、全20 runで供給先を失うcarrier conflictを作った。

5 runはreviewerを起動せず期待`blocked`に対して`unavailable`へ停止した。残り15 runは同じ矛盾を抱えたままreviewerを起動した。したがってC217は`quality_failed / mechanism_failed / stopped`であり、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-proposition-operand-closure-r1`
- bundle SHA-256: `627c8e27541e0b6ab96129e19121def1a43a289d903222d8260d52cf66507056`
- profile: `candidate217-review-proposition-operand-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 222.048秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 40 / 45 |
| terminal一致 | 40 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 40 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

低品質5件はADR03 iteration 1、ADR05 iteration 1・4、ADR06 iteration 2・4である。すべて期待`blocked`に対して`unavailable`となり、reviewerは0件、成果物変更は0件だった。有効runなので除外または再実行していない。

## 機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| fixed input / packet carrier conflict | 20 / 20 packet case |
| closureがreviewer起動を止めたrun | 5 |
| conflictを残したままreviewerを起動したrun | 15 |
| admission済みoperand再read | 12回、7 run |
| packet projection重複またはwhole-container read | 0回 |
| packet caseの誤paired read | 2回 |
| reviewer mixed read | 0回 |
| manifest外read | 0回 |
| ADR03〜ADR06 terminal一致 | 15 / 20 |
| ADR07 paired targetだけのroute | 5 / 5 |
| ADR09 paired targetだけのroute | 4 / 5 |
| review result admission / effect一致 | 40 / 45 |

### 成立した部分

- ADR07は5 / 5でpaired targetだけを読み、C216の同系列に残った不要design-container readを閉じた。
- ADR09も4 / 5でpaired targetだけとなった。
- packet projection重複またはwhole-container read、mixed read、manifest外read、canary配送は0件だった。
- 必須operandの供給不能を検出した5件では、reviewer resultを捏造せず安全側の`unavailable`へ停止した。

operandを命題のpredicate dependencyから固定する方向は、名前やcase対応なしに不要な再取得を減らす点では働いた。しかし、operandを固定した後の供給先をpacketだけへ寄せたため、TaskSpecが許さないcarrierを要求した。

### 失敗経路

今回の失敗は「問題を解く証拠がなかった」のではない。必要値は固定入力として存在し、試験によって供給契約の矛盾が具体的に観測された。

```text
required review proposition
  -> direct operandは固定入力として存在
  -> rootがcurrent valueをadmit
  -> TaskSpecはそのvalueをreviewer packetへ許可しない
  -> C217はreviewer-owned observationへの移管も禁止
  -> packetにもobservationにも合法的にbindできない
```

5件はこの矛盾を正直に停止へ反映した。15件はreviewerを起動したが、C217が要求した完全なinput closureを満たした証拠にはならない。さらに7 runではrootが固定入力containerを読んだ後、reviewerがinventory / contractsを合計12回再読した。

## 今回から見える次の軸

次に閉じるべきなのはoperandの名前でもread順でもなく、値をadmitする前の合法carrier選択である。

```text
required review proposition
  -> direct operand
  -> TaskSpecが許すcarrierを先に固定
     -> packet-projectable: root-owned admission + packet receipt
     -> packetへ運べない: reviewer-owned direct observation
     -> どちらも不可: unavailable
  -> owner以外はcurrent valueを先に消費しない
```

`model-visible`はrootがcontainerを読めることを示しても、その中の全valueをreviewer packetへ投影できることまでは示さない。packetへ運べないdirect operandをreviewerが必要とするなら、そのvalueの観測責任を最初からreviewer-ownedに残し、rootはそのcurrent valueを先にadmitしない必要がある。

これは成功runの「rootはここを読まず、reviewerが後で読む」という順番を手順化する案ではない。TaskSpecのpacket permissionとpredicate dependencyから所有権を先に決め、同じvalueをroot admissionとreviewer observationの両方から消費できる辺を閉じる案である。C217を修正再実行せず、C147を直接基盤とする別Candidateの作成前gateで反例監査する。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate217 |
|---|---:|
| `quality_score` | 91.667 |
| all-agent `total_tokens` | 971,502 |
| `elapsed_seconds` | 699.856 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate217_ADR9_completed / valid_45 / score4_40 / score1_5 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

result登録後に実行batchをsealし、最終圧縮した。

- execution archive SHA-256: `58a4ca5c538784f5d24bdc7736934fabd5de02a220c3ab12e248c78971b0de87`
- execution seal SHA-256: `66dd8c1d2b83407d2d3ce91c05769ac063c61b9b13901f7ed1fa64b9a5256746`
- final archive SHA-256: `7f8c080b34925cd90ae87b728666ff1d88b67a1cd576e5814f748d7981aa2635`
- final manifest SHA-256: `eefc4e4939774e06202325bc1b3e3963306e17605e987ffa0180b323c709082d`

## 一次アーティファクト

- [登録result](906c23433e3c4ac7ba679b916f0bb311.json)
- [品質監査](candidate217-review-proposition-operand-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate217-review-proposition-operand-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate217-review-proposition-operand-closure-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate217-review-proposition-operand-closure-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate217-review-proposition-operand-closure-implementation-audit.md)
