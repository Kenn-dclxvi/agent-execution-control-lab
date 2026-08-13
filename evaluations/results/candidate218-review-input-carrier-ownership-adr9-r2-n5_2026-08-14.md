# Candidate218 review input carrier ownership ADR9 r2 N=5結果

## 結論

Candidate218は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 43 / 2`で、terminalは43 / 45、成果物境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件だった。

一方、狙ったconsumer ownershipは実行経路を閉じなかった。ADR03からADR06の20 / 20 runで、rootがpacket配送禁止かつreviewer direct observation所有の`consumer_inventory`と`consumer_contracts`を含むresultを取得した。19 / 20 runではreviewerも同じ値を直接観測し、残る1 runではreviewer resultがその二値をpacket-carriedとして受領したと明記した。rootとreviewerの所有を排他的に宣言しても、一般のrepository evidence発行許可がmixed-owner container readを先に開いたままだったためである。

さらに、review不要なADR01 / ADR02で不要reviewer起動が7件、ADR07 / ADR09でpaired target以外のdesign-container再読が17回残った。したがってCandidate218は`quality_failed / mechanism_failed / stopped`であり、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-input-carrier-ownership-r1`
- bundle SHA-256: `04c2e670eabf659b24139429246ad1e640e5162297b4fd999a0565efd8762f73`
- profile: `candidate218-review-input-carrier-ownership-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 249.710秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 43 / 45 |
| terminal一致 | 43 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 38 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

低品質2件はADR04 iteration 1・4である。どちらも具体的な`consumer-d`反例候補まで観測したが、欠落したpaired-scope evidenceを反例成立にも必須と扱い、期待`blocked`に対して`unavailable`となった。有効runなので除外または再実行していない。

## 機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| rootによるreviewer-owned値の先行取得 | 20 / 20 packet case |
| mixed-owner root admission | 20 / 20 packet case |
| rootとreviewerの同一値二重消費 | 19 / 20 packet case |
| 必要なreviewer direct observation | 19 / 20 packet case |
| 禁止packet配送をreviewer resultで直接確認 | 2 run |
| ADR03〜ADR06 terminal一致 | 18 / 20 |
| ADR07 paired targetだけのroute | 2 / 5 |
| ADR09 paired targetだけのroute | 1 / 5 |
| paired caseでpacket-carried design projectionを再読 | 17回 |
| review不要時のreviewer起動 | 7 run |
| manifest外read | 0回 |
| 基本review result admission / effect等の機序通過 | 35 / 45 |
| ownershipを含む全機序通過 | 11 / 45 |

### 成立した部分

- 45件すべてが有効に完了し、成果物境界は45 / 45で守られた。
- required commandは15 / 15、forbidden canary deliveryは0件、manifest外readも0件だった。
- ADR03、ADR05、ADR06では期待`blocked`を15 / 15で維持した。
- ADR08はpermission denied時のreviewer非起動と`unavailable`を5 / 5で維持した。
- ADR04の3 / 5では、reviewer-owned direct observationから具体的な反例を成立させて`blocked`へ到達した。

four-way ownershipは、必要値が存在しないから停止する問題ではなく、誰がその値を消費できるかを分ける観点としては有効だった。しかし、その分類がrepository evidenceの発行可能集合に接続されなかったため、実際のroute制御にはならなかった。

### 失敗経路

```text
TaskSpecからconsumer ownerを分類
  -> REVIEW_INPUT_OWNERSHIP上はrootとreviewerを排他的に宣言
  -> 一般EVIDENCE_GATEはrootのcontainer readを依然許可
  -> mixed-owner result全体がroot modelへ返る
  -> reviewerが同じ値をdirect observationで再読
     またはroot取得値がpacketへ流れる
```

問題は、結果を「admitしない」と後から判断できるかではない。mixed-owner current valueをrootへ返すinvocation自体が合法なままなので、reviewer-owned値をrootが消費できる失敗routeが残っている。

ADR04の2件は別の残存辺も示した。具体的反例のsupportが揃った後でも、別terminalだけを分けるpaired-scope observationの欠落を`unavailable`へ伝播させた。terminal kindが一つ成立した時点で、他kindだけに必要な未観測値を失効する境界が実行上は弱い。

## 今回から見える次の軸

次の打ち手は、ownership分類を独立した説明規則として追加することではなく、repository evidence invocationの発行条件そのものへconsumer ownerを組み込むことである。

```text
required predicate
  -> value identityとconsumer ownerをcurrent value取得前に固定
  -> evidence invocationへownerとexact projectionをbind
  -> root invocationはroot-owned projectionだけを返せる場合に限り発行
  -> owner境界を越えるresultになり得るinvocationは未発行のまま閉じる
  -> reviewer-owned observationはreview producerのconsumerだけが発行
```

これは「rootが先に特定の`jq`を使う」という成功手順ではない。一般`EVIDENCE_GATE`からmixed-owner container readへ至る辺を消し、rootとreviewerで許されるresult集合を発行前から分離する案である。また、一つのterminal kindがsupportされた後は、別kindだけに必要な未発行observationがそのresultを`unavailable`へ戻せないよう、terminal supportとevidence失効を同じ境界へ接続する必要がある。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate218 |
|---|---:|
| `quality_score` | 100.000 |
| all-agent `total_tokens` | 1,258,789 |
| `elapsed_seconds` | 834.607 |

5組の集約中央値が100でも、45 atomic run中2件がScore 1である事実は変わらない。品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate218_ADR9_completed / valid_45 / score4_43 / score1_2 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

result登録後に実行batchをsealし、最終圧縮した。

- execution archive SHA-256: `737f50cc920d1bae24863342436e177894ddbefd4d560ee024196a458f120a85`
- execution seal SHA-256: `f392cdc04d2f69d0a28157c1b778b9c6bb717e3ff218b35f553a09f095c98e41`
- final archive SHA-256: `a4ce47cda52848ae2b0bba87d3fa342b11edf39f316a537ecce7936cf8ceb07a`
- final manifest SHA-256: `637790defa0d9a8c7705d1695cddb33de45a76b57f6975338703278de819d33c`

## 一次アーティファクト

- [登録result](b2fb3f264739493bb5a3985829161701.json)
- [品質監査](candidate218-review-input-carrier-ownership-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate218-review-input-carrier-ownership-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate218-review-input-carrier-ownership-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate218-review-input-carrier-ownership-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate218-review-input-carrier-ownership-implementation-audit.md)
