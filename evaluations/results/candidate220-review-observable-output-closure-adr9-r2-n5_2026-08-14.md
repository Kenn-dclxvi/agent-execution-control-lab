# Candidate220 review observable output closure ADR9 r2 N=5結果

## 結論

Candidate220は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 41 / 4`で、terminalは41 / 45、成果物境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件だった。

`review_work_item`によるreviewer起動制御は効いた。review不要なADR01 / ADR02の不要reviewerはCandidate219の9件から1件へ減り、reviewer cardinalityは43 / 45へ改善した。

しかし核心のobservable output closureは成立しなかった。ADR03からADR06の20 / 20 runでrootがreviewer用current valueを含むdesign resultを取得し、13件でreviewerとの二重消費になった。source availability、request intent、observable outputを分けても、AIはwhole-container resultをroutingとpacket constructionに必要なroot outputだと自己分類した。したがってCandidate220は`quality_failed / mechanism_failed / stopped`であり、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-observable-output-closure-r1`
- bundle SHA-256: `739719baebd5f7c993fc5f6e1bc9623f145617724ecc65cbca5a82da6ee47654`
- profile: `candidate220-review-observable-output-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 226.138秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 41 / 45 |
| terminal一致 | 41 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 43 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

低品質4件はADR04が3件、ADR06が1件で、期待`blocked`に対して`unavailable`となった。ADR04のうち1件はreviewer自体を起動せず、残りはreview resultが必要supportを閉じられなかった。有効runなので除外または再実行していない。

## 機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| rootによるreviewer用値の先行取得 | 20 / 20 packet case |
| mixed-owner root admission | 20 / 20 packet case |
| rootとreviewerの同一値二重消費 | 13 / 20 packet case |
| 必要なreviewer direct observation | 13 / 20 packet case |
| ADR03〜ADR06 terminal一致 | 16 / 20 |
| ADR07 paired targetだけのroute | 4 / 5 |
| ADR09 paired targetだけのroute | 2 / 5 |
| paired caseでpacket-carried design projectionを再読 | 4回 |
| review不要時のreviewer起動 | 1 run |
| manifest外read | 0回 |
| 基本review result admission / effect等の機序通過 | 40 / 45 |
| observable outputを含む全機序通過 | 20 / 45 |

### うまくできた部分

- review不要時のreviewer起動は9件から1件へ減り、`review_work_item`の残存性で起動を判断する方向は実行上の効果を示した。
- reviewer cardinality一致は36 / 45から43 / 45、基本機序通過は32 / 45から40 / 45へ改善した。
- 45件すべてが有効で、成果物境界45 / 45、required command 15 / 15、forbidden canary delivery 0件、manifest外read 0件を維持した。
- ADR03、ADR05は期待`blocked`を各5 / 5、ADR08はpermission denied時の非起動と`unavailable`を5 / 5で維持した。
- ADR07 paired-onlyはCandidate219の0 / 5から4 / 5へ改善した。

### 残った失敗経路

```text
TaskSpecからroot用routingとpacket constructionの目的をbind
  -> modelがwhole-container commandのobservable outputを
     rootの複数nonterminal predicateへ必要だと自己分類
  -> output closure成立と宣言して発行
  -> reviewer用current valueまでrootへ配送
```

Candidate219ではconsumer ticket、Candidate220ではobservable output集合へ表現を変えたが、どちらも「そのoutputが閉じているか」をmodel自身の意味判断だけに委ねた。禁止したいrouteと、そのrouteの発行可否を判定する主体が同じなので、whole-container resultを必要情報と再分類する余地が消えていない。

## 今回から見える次の軸

次の打ち手は、output closureをもう一度言い換えたり、modelへ別の確認手順を指示したりすることではない。失敗routeを合法にしている権限辺と、必要なpacket構築routeを分けて監査することである。

```text
TaskSpecのmodel-visible / read許可
  + Candidate147 EVIDENCE_GATEのtarget artifact許可
  + DECISION_BOUNDARYの共同read許可
  -> root whole-source readが合法
  -> reviewer用current valueまでrootへ配送
```

次は、この権限辺をcase名、field名、具体的selectorまたは成功時のtool順へ対応させずに除去できるかを、TaskSpecとCandidate147のauthority境界から確認する。同時に、その除去後もrootがreviewer packetを構築するための必要routeが残ることを証明する。

両立しない場合は、新しい自己申告証跡で補完せず、このrepository内のprompt制御では未解決として停止する。

## KPI

| KPI | Candidate220 |
|---|---:|
| `quality_score` | 91.667 |
| all-agent `total_tokens` | 1,132,909 |
| `elapsed_seconds` | 761.522 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate220_ADR9_completed / valid_45 / score4_41 / score1_4 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

- execution archive SHA-256: `da07bf5794327c52ed8f5539a849cae0bd3dc1dde101cc3d80aef6f559cc470a`
- execution seal SHA-256: `02a8f130b294e8e8ab354a07b3b10fb06fc1ff1d11a35f8ed514624cb6e19ac7`
- final archive SHA-256: `a9691d3349a3bdc920f3673f260c4ba1bc9704ed4b55010f6996656439ee9f8e`
- final manifest SHA-256: `144b687661450e8138f4652dc9436effae915c6a30e1a5412813d0411dd41ee9`

## 一次アーティファクト

- [登録result](8e128045822042ff9a14b23fbc12e6c4.json)
- [品質監査](candidate220-review-observable-output-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate220-review-observable-output-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate220-review-observable-output-closure-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate220-review-observable-output-closure-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate220-review-observable-output-closure-implementation-audit.md)
