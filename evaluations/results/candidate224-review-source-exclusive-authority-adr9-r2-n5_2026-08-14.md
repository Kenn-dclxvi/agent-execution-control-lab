# Candidate224 review source exclusive authority ADR9 r2 N=5結果

## 結論

Candidate224は、変更していないADR9 r2を45 / 45 valid、除外0件で完了した。Scoreは`4 / 1 = 43 / 2`で、artifact境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件だった。

しかし、目的である必要な独立reviewの完遂とsource delivery境界は成立しなかった。必要な30件すべてで独立reviewerは起動したが、ADR06の2件では反例を確定できず`unavailable`となり、必要なreview判断が完了したのは28 / 30だった。ADR03からADR06の20 / 20 runでrootがreviewer所有値を含むsourceをreview前に受領し、必要なreviewer direct observationは9 / 20に留まった。

したがってCandidate224は`quality_failed / mechanism_failed / stopped`である。有効runを保持し、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-source-exclusive-authority-r1`
- bundle SHA-256: `63e01ac0c8d386e76aecdeda312f9fef2944fa22c0bec1af971a27d25d5a46b7`
- profile: `candidate224-review-source-exclusive-authority-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 341.633秒

TaskSpec、case、fixture、oracle、rating、runtime、permission、executor条件および既存test fileは変更していない。比較変数はCandidate promptだけである。

## 必要reviewの結果

| 指標 | 結果 |
|---|---:|
| 必要reviewer起動 | 30 / 30 |
| 必要なreview判断の期待結果一致 | 28 / 30 |
| 全caseのreview result admission一致 | 43 / 45 |
| review result effect一致 | 43 / 45 |
| ADR03〜ADR06 terminal一致 | 18 / 20 |
| artifact境界一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

Score 1の2件はADR06で、期待した`counterexample_found`と`blocked`ではなく`unavailable`となった。どちらもreviewerは起動し、成果物を変更せず安全に停止したため、欠落reviewをrootが補完する誤りではない。一方、必要な反例判断を完了できていないので目的達成とも扱わない。有効runのため除外または再実行していない。

## source exclusive authority機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| rootによるreviewer-owned targetの先行取得 | 20 / 20 packet case |
| mixed-owner root admission | 20 / 20 packet case |
| 必要なreviewer direct observation | 9 / 20 packet case |
| rootとreviewerの同一値二重消費 | 10 / 20 packet case |
| ADR07 paired targetだけのroute | 4 / 5 |
| ADR09 paired targetだけのroute | 4 / 5 |
| review不要時のreviewer起動 | 0 run |
| manifest外read | 0回 |
| 基本review機序通過 | 43 / 45 |
| source authorityを含む全機序通過 | 23 / 45 |

### 得られた手がかり

Candidate224はpre-review sourceを一般`EVIDENCE_GATE`から除外し、root packet projectionとreviewer observationを排他的なoperationとして定義した。それでもpacket case 20 / 20でrootは`design-admission.json`から`consumer_inventory`または`consumer_contracts`を含むoutputを受領した。禁止文、有限projectionおよびresult recipientの定義は、同じread surfaceがwholeまたはmixed-owner outputを返せる能力を閉じなかった。

ADR06の2件では、reviewerがinventoryとconsumer contractsではなく、同じfinite manifestに含まれる存在しない`paired-scope-evidence.json`を選んだ。r2は各observation targetとsuccess conditionを固定しているが、必要review scopeとその判断を直接閉じるobservation targetの対応をsource外carrierとしては固定していない。promptだけでその対応を作ると、C223と同様に評価入力にない新しいcarrier contractを実質的に導入する。

この二観測から、変更していないADR9 r2とprompt-onlyという現在の範囲では、C214のcontainer全体閉鎖を保ったまま正常packet carrierを開く改善は見込まない。rootがpacket literalを得るsourceとreviewerが直接観測するsourceが同じcontainerであるため、rootへsource readを再許可するとwhole-output能力も再び開く。必要な排他的carrierをTaskSpec、fixture、runtimeまたはtool adapterへ追加する変更は今回の許可範囲外である。したがって次Candidateは作成せず、未解決として保持する。

これは試験を増やせば解決するという意味ではない。既存45件が、必要reviewの完遂を妨げたdependencyと、rootの不要readを許したpermission edgeを直接示している。

## KPI

| KPI | Candidate224 |
|---|---:|
| `quality_score` | 100.000 |
| all-agent `total_tokens` | 1,133,836 |
| `elapsed_seconds` | 808.274 |

KPIは固定selectionの中央値である。品質・機序が不通過なので、改善または採用根拠として扱わない。

## 状態

`candidate224_ADR9_r2_completed / valid_45 / score4_43 / score1_2 / required_review_started_30_of_30 / required_review_decision_28_of_30 / root_mixed_owner_20_of_20 / quality_failed / mechanism_failed / stopped / next_candidate_not_created / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

- execution archive SHA-256: `c8c356a9bdb5eed1ffe6a8381947594ec17409efa5f22483125161cb2c383ff9`
- execution seal SHA-256: `9d797369371aab1a63c018bbb5f46b2777514662072cac5f3399df957c578ed7`
- final archive SHA-256: `add0582e3532700ab1e4e1e0844b8fc78e384425eee5fe0238c401769243256e`
- final manifest SHA-256: `403dc634b5d1e9eb7efbf771a57a50adcdf1829be88b872f8073525804e7fb47`

## 一次アーティファクト

- [登録result](cc43543650a84911ad6ad7ca0e1cde46.json)
- [品質監査](candidate224-review-source-exclusive-authority-adr9-r2-n5-quality-audit-r1.json)
- [基本機序監査](candidate224-review-source-exclusive-authority-adr9-r2-n5-mechanism-base-audit-r1.json)
- [source authority機序監査](candidate224-review-source-exclusive-authority-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate224設計](../../docs/candidate224-review-source-exclusive-authority-design.md)
- [実行準備監査](../../docs/candidate224-review-source-exclusive-authority-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate224-review-source-exclusive-authority-implementation-audit.md)
