# Candidate216 packet construction projection ADR9 r2 N=5結果

## 結論

Candidate216は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 44 / 1`で、Candidate215の41 / 4から品質失敗を1件まで減らした。packet projectionと重なるreadまたはwhole-container read、packet caseからpaired targetへ逸れるread、rootによるreviewer-owned target先読みはすべて0件だった。

同じcontainer内の必要非重複region readは13回、9 runで成立し、ADR03からADR06の期待terminalは19 / 20へ改善した。一方、ADR06 iteration 5ではcurrent inventory instanceをpacketでもdirect observationでも確定できず、期待`blocked`に対して`unavailable`となった。

さらにADR07 / ADR09では、paired targetだけで足りるrouteがそれぞれ1 / 5、2 / 5に留まり、既にrootがadmitしたinventory / contractをpacketへ安定して渡さずreviewerが同じcontainerから再取得する経路が14回、7 runに残った。品質が通ったrunでも不要readがあるため、Candidate216は`quality_failed / mechanism_failed / stopped`である。停止条件に従い、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-packet-construction-projection-r1`
- bundle SHA-256: `77a0f660d7066bee128785814517a7899d18086e0c0617b9bc90feebe3995eb6`
- profile: `candidate216-packet-construction-projection-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 213.866秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 44 / 45 |
| terminal一致 | 44 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

低品質はADR06 iteration 5の1件だけである。独立reviewerは正しく起動し、成果物を変更せず安全側に停止したが、`export-c`がcurrent inventory instanceかを確定できず、期待`blocked`に対して`unavailable`となった。有効runなので除外または再実行していない。

## 機序

| 固定gate | 結果 |
|---|---:|
| packet projection重複またはwhole-container read | 0回 |
| 必要な非重複region read | 13回、9 run |
| ADR07 / ADR09の不要design-container read | 14回、7 run |
| packet caseの誤paired read | 0回 |
| reviewer mixed read | 0回 |
| reviewer manifest外read | 0回 |
| root reviewer-owned target preread | 0 / 30 |
| ADR03〜ADR06 terminal一致 | 19 / 20 |
| ADR07 paired targetだけのroute | 1 / 5 |
| ADR09 paired targetだけのroute | 2 / 5 |
| review result admission一致 | 44 / 45 |
| review result effect一致 | 44 / 45 |

### 成立した部分

- Candidate215に残ったpacket caseのpaired targetへの逸脱3回は0回になった。
- packet projectionと重なるreadまたはwhole-container readは0件を維持した。
- root先読み、mixed source、manifest外source、canary配送は0件だった。
- ADR03〜ADR06の期待terminalはCandidate215の17 / 20から19 / 20へ改善した。
- 45件中44件は期待terminalと成果物境界へ一致した。

construction時のprojectionをsource identityの生成点にする方向は、同じcontainer内の必要routeを一律閉鎖せず、誤った別containerへ逃げるrouteを閉じる点では有効だった。

### 残った誤経路

Candidate216はpacket itemへ採用した値のprojection regionを固定したが、各required review propositionを判定するために、admission済みのどのcurrent valueをpacketへ含める必要があるかまでは閉じていない。

保存traceでは二つのrouteが併存した。

1. rootがadmit済みinventory / contractのliteral valueをpacketへ含め、reviewerはpaired targetだけを読む。
2. rootがsemantic projection、boundary、authority、normative contract、scope、manifestだけでpacketを作り、reviewerがinventory / contractをrepositoryから再取得する。

両routeともprojection重複readは避けているため、region conflictだけでは後者を閉じられない。ADR06の品質失敗は、必要なcurrent inventory valueがpacketにもdirect observationにも入らなかったrouteである。

## 今回から見える次の軸

次に固定すべきなのはsource regionの粒度ではなく、review propositionごとのadmission済み入力閉包である。

```text
required review proposition
  -> 判定に直接必要なoperand集合
  -> admission済みcurrent valueはpacket inputへ固定
  -> 未admit operandだけをreview evidence consumerへ残す
```

必要な境界は次のようになる。

1. packet構築前に、各required review propositionの真偽を分ける直接operandをbindする。
2. operandのcurrent valueが既にadmission済みなら、名前や意味対応ではなく、そのpredicate dependencyとしてpacketへ含める。
3. packetへ含めたoperandはcurrent evidenceとして閉じ、reviewerの再read対象にしない。
4. 未admit、missing、unreadableまたはnon-valueのoperandだけを、terminal dispositionを分けるevidence consumerへ残す。
5. proposition supportが閉じた時点で、別dispositionだけに必要な未発行operandを失効する。

これは成功runのread順を手順化する案でも、inventory等のfield名をcaseへ対応させる案でもない。AIがreview判定を行う時のpredicateとoperandの依存関係を先に閉じ、既に持っている値を取り直すrouteと、必要値をpacketから落とすrouteを同時に消す案である。Candidate216は修正再実行せず、C147を直接基盤とする別Candidateの作成前gateで検討する。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate216 |
|---|---:|
| `quality_score` | 100.000 |
| all-agent `total_tokens` | 1,130,089 |
| `elapsed_seconds` | 720.522 |

5組の集約中央値では1件の低品質runが隠れる。品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate216_ADR9_completed / valid_45 / score4_44 / score1_1 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

result登録後に実行batchをsealし、最終圧縮した。

- execution archive SHA-256: `bdf191a6f0a7084c3ca0732728e9ad3eebe2d58a0f154693a041f87b00ebb449`
- execution seal SHA-256: `99feab0cadfb9f34af41842d21154bf17ca1ab5345fa7aef156150fe95375768`
- final archive SHA-256: `956175332d215a49cf0faca7b23880bcc3b6c2644d3cda36c9d56cd278766008`
- final manifest SHA-256: `f8316e7302abab4a632fdaf86404a0746324ee333cc3a0a18cb1b8594ed66310`

## 一次アーティファクト

- [登録result](cb903e23e6a14ebea156351c16963cad.json)
- [品質監査](candidate216-packet-construction-projection-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate216-packet-construction-projection-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate216-packet-construction-projection-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate216-packet-construction-projection-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate216-packet-construction-projection-implementation-audit.md)
