# Candidate219 review evidence consumer admission ADR9 r2 N=5結果

## 結論

Candidate219は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 41 / 4`で、terminalは41 / 45、成果物境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件だった。

狙ったconsumer-bound issuanceは成立しなかった。ADR03からADR06の20 / 20 runで、rootがreviewer用current valueを含むdesign container resultを取得した。13件ではreviewerも同じ値を直接観測し、二重消費になった。Candidate本文はabstractなticketをconsumerとprojectionへbindしたが、AIはcontainer全体の取得を「model-visibleな固定入力からreview必要条件、permission、packet readinessを判定するroot request」と扱った。requestの目的をroot predicateへ結びつけても、実際にstdoutへ返るvalue projectionの境界にはならなかった。

さらに、review obligationが空のADR01 / ADR02で不要reviewerを9件起動し、ADR03 / ADR04 / ADR06の4件は期待`blocked`に対して`unavailable`になった。したがってCandidate219は`quality_failed / mechanism_failed / stopped`であり、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-evidence-consumer-admission-r1`
- bundle SHA-256: `5ec4728576b24b8dd4aceb45903cae6f9fe0f46b58bf382a3cbe4c50cdfabf95`
- profile: `candidate219-review-evidence-consumer-admission-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 202.805秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 41 / 45 |
| terminal一致 | 41 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 36 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

低品質4件はADR03が1件、ADR04が1件、ADR06が2件である。いずれも期待`blocked`に対してreviewer resultが`unavailable`となった。有効runなので除外または再実行していない。

## 機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| rootによるreviewer用値の先行取得 | 20 / 20 packet case |
| mixed-owner root admission | 20 / 20 packet case |
| rootとreviewerの同一値二重消費 | 13 / 20 packet case |
| 必要なreviewer direct observation | 13 / 20 packet case |
| 禁止packet配送をreviewer resultで直接確認 | 0 run |
| ADR03〜ADR06 terminal一致 | 16 / 20 |
| ADR07 paired targetだけのroute | 0 / 5 |
| ADR09 paired targetだけのroute | 4 / 5 |
| paired caseでpacket-carried design projectionを再読 | 4回 |
| review不要時のreviewer起動 | 9 run |
| manifest外read | 0回 |
| 基本review result admission / effect等の機序通過 | 32 / 45 |
| consumer admissionを含む全機序通過 | 10 / 45 |

### うまくできた部分

- 45件すべてが有効に完了し、成果物境界は45 / 45で守られた。
- required commandは15 / 15、forbidden canary deliveryは0件、manifest外readも0件だった。
- ADR05は期待`blocked`を5 / 5で維持した。
- ADR08はpermission denied時のreviewer非起動と`unavailable`を5 / 5で維持した。
- ADR09のpaired-only routeはC218の1 / 5から4 / 5へ増え、paired caseでのdesign projection再読は17回から4回へ減った。
- reviewer finalから直接確認できる禁止packet配送はC218の2件から0件になった。

ただし、二重消費が13件へ減った主因には必要なreviewer observation自体を7件失ったことが含まれる。root mixed-owner admissionは20 / 20のままであり、consumer分離が成立した結果とは扱わない。

### 失敗経路

保存traceのrootは、最初のrepository stepを次のように判断した。

```text
TaskSpecがdesign sourceをmodel-visibleな固定入力と記載
  -> rootがreview必要条件、permission、packet readinessの確認と解釈
  -> review_evidence_ticketを具体的なstdout shapeへbindしない
  -> start identityとdesign container全体readを同一stepで発行
  -> reviewer用current valueまでroot modelへ返る
```

Candidate219は「allowed targetやmodel-visibleだけでは発行しない」と書いたが、AIはwhole-container requestの目的全体をroot用routing predicateへbindした。`requested result projection`を宣言したことと、commandが返す全valueを実際に限定したことを区別できていない。

不要reviewerにも同じ曖昧さがある。`required review propositionまたはscope obligationがnonempty`という条件では、必須scopeが空でもtask-levelのdesign admission命題またはreview contract自体をnonempty propositionと解釈できた。reviewerを必要にする未解決の外部producer-owned predicateが存在するか、という実行上の制限へ閉じていなかった。

## 今回から見える次の軸

次の打ち手はticket概念をもう一段抽象化することではない。AIがrepository commandを発行するときに、意図したconsumerではなく、modelへ実際に返るstdoutの全valueを基準に発行可否を決める境界が必要である。

```text
未解決のproducer-owned predicateがある
  -> そのproducerだけに必要な観測値集合を固定
  -> repository commandのobservable output projectionを固定
  -> outputへ集合外valueが一つでも出得るcommandは未発行
  -> sourceがmodel-visible、固定入力、allowed pathでも例外にしない
```

またreviewer起動は、review contractや一般review命題の存在ではなく、rootが代行できず、packetでも充足済みでなく、独立producerのresultだけが分けられるnonterminal predicateが現に残っている場合へ限定する必要がある。

これは特定のfield、case、`jq`またはread順を覚えさせる案ではない。AI自身が解こうとしているpredicateと、toolから自分へ返る実際の情報量の差を発行前に判定し、過剰な出力を返すrouteを閉じる案である。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate219 |
|---|---:|
| `quality_score` | 100.000 |
| all-agent `total_tokens` | 1,258,156 |
| `elapsed_seconds` | 773.354 |

5組の集約中央値が100でも、45 atomic run中4件がScore 1である事実は変わらない。品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate219_ADR9_completed / valid_45 / score4_41 / score1_4 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

result登録後に実行batchをsealし、最終圧縮した。

- execution archive SHA-256: `a6d8b89b49526a9739b6b3a20ad378abbc2014eca0411031fd07a5aeb495c8a4`
- execution seal SHA-256: `c667b001ad62321ac8fcbca06023f9b99b732fe7456ad47e6d6ea93f1860e8a5`
- final archive SHA-256: `153eb99150196264323552648b018519bef1710fd917293ce0635b11732289fa`
- final manifest SHA-256: `807433a534d46b05507b172ec15c6f499ddf1cd502268ab138a1712aedbd5237`

## 一次アーティファクト

- [登録result](9834373597cb47b5b469f1d15962bf04.json)
- [品質監査](candidate219-review-evidence-consumer-admission-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate219-review-evidence-consumer-admission-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate219-review-evidence-consumer-admission-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate219-review-evidence-consumer-admission-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate219-review-evidence-consumer-admission-implementation-audit.md)
