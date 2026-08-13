# Candidate214 packet source container closure ADR9 r2 N=5結果

## 結論

Candidate214は45 / 45 valid、除外0件だったが、Scoreは`4 / 1 = 41 / 4`で品質gateを通過しなかった。Candidate213で残ったpacket投影元sourceの再readは6回から0回、rootによるreviewer-owned targetの先読みは1回から0回となり、実際にpacketへ使ったsourceの再取得経路は閉じた。

一方、同じrepository fileにあるという理由だけで、packetへ投影していないinventoryとconsumer contractの領域まで閉じた。ADR03 iteration 3、ADR05 iteration 1と4、ADR06 iteration 2では、reviewerが具体的反例を成立させるためにcurrent inventory membershipを必要としたが、同一containerの未投影領域を読めず、3件は存在しないpaired-scope targetを代替観測し、1件はreadなしで`unavailable`を返した。期待terminalはいずれも`blocked`だった。

したがってCandidate214は`quality_failed / mechanism_failed / stopped`である。停止条件に従い、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-packet-source-container-closure-r1`
- bundle SHA-256: `3acb157b05719ca0ebca1d1f3ecbb6f76a53965686532833e1bbbbabd9b9815c`
- profile: `candidate214-packet-source-container-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 227.792秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 41 / 45 |
| terminal一致 | 41 / 45 |
| artifact境界一致 | 45 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

4件はいずれも独立reviewerを正しく起動し、成果物を変更せず安全側に停止した。しかし、packetへ未投影のinventory membershipを取得できなかったため、具体的反例を`counterexample_found`へbindできず、期待`blocked`に対して`unavailable`となった。

## 機序

| 固定gate | 結果 |
|---|---:|
| packet-counterexample repository readなし | 17 / 20 |
| packet-counterexample repository read | 3回、3 / 20 run |
| packet投影元source再read | 0回 |
| packet-counterexample内paired-scope read | 3回 |
| reviewer mixed read | 0回 |
| reviewer manifest外read | 0回 |
| root reviewer-owned target preread | 0 / 30 |
| ADR07 pairedだけの必要direct observation | 5 / 5 |
| ADR07 `no_counterexample_found` | 5 / 5 |
| ADR09 pairedだけのmissing direct observation | 5 / 5 |
| ADR09 `unavailable` | 5 / 5 |
| review result admission一致 | 41 / 45 |
| review result effect一致 | 41 / 45 |

### 成立した部分

- Candidate213のpacket投影元source再read6回を0回にした。
- Candidate213のroot reviewer-owned target先読み1回を0回にした。
- reviewer cardinality、artifact境界、required command、canary境界は全件一致した。
- ADR07は5 / 5で必要なpaired sourceだけを観測して`no_counterexample_found`を返した。
- ADR09は5 / 5で同じsourceのmissingだけを観測して`unavailable`を返した。
- projected source、mixed source、manifest外sourceのreadは0件だった。

source containerを構造identityとして閉じる方向は、同じ値をfield、selectorまたは部分抽出として取り直す経路には有効だった。

### 残った誤経路

Candidate214の`review_read_conflicts`は、source regionの重複判定より先に、同じcontainer identityに属する全targetを一律に競合とした。このため、packetへ実際に投影した`general_design.semantic`、authority、boundaryなどだけでなく、投影していない`consumer_inventory`と`consumer_contracts`も読めなくなった。

ADR03とADR06ではnormative contractのinstance inputから候補instanceの属性は分かったが、そのinstanceがcurrent inventoryに属する命題を確定できなかった。ADR05では外部consumerとcontract自体がpacketに含まれなかった。3 runは別containerのpaired-scope targetを読んだが、そのfileは存在せず、残り1 runはreadなしで停止した。これは「証拠がないから解決不能」ではなく、必要な証拠へ到達する合法routeをcontainer全体の閉鎖で自ら潰した失敗である。

## 今回から見える次の軸

次に閉じるべきなのはfile全体ではなく、packet construction receiptへ実際にbindしたsource regionと重なるreadだけである。

必要な境界は次のようになる。

1. receiptに固定region identityがある場合、同じcontainerというだけでは禁止せず、同一・祖先・子孫・重複regionだけを閉じる。
2. region identityを固定できないpacket itemだけは、container全体を保守的に閉じる。
3. 未投影regionは、残るterminal dispositionを分ける命題を直接bindできる場合に限り、同じcontainer内でもreviewerが観測できる。
4. 実際にpacketへ使っていないmanifest entryをreceiptへ昇格せず、rootの先読みにも使わない。

これはcase名、field名または意味の対応表をpromptへ埋める案ではない。packet構築で受領した構造region identityと、要求read targetの構造関係だけでpermissionを決める。Candidate214を修正再実行せず、C147を直接基盤とする別Candidateの作成前gateで、このregion精度が必要routeと不要routeを両立できるか確認する。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate214 |
|---|---:|
| `quality_score` | 91.667 |
| all-agent `total_tokens` | 1,063,312 |
| `elapsed_seconds` | 676.615 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate214_ADR9_completed / valid_45 / score4_41 / score1_4 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

実行batchはresult登録後にsealし、最終圧縮を完了した。execution evidence archiveのSHA-256は`ee6efa7a9033edd991e763b0e862dfc9de85729e64aaf2950be64dae8d1b2e05`、final evidence archiveは`6692c002044661d07f814a6b8c6250875be5a2902d86abf5f6ba0657fa5adadd`である。Layer 1と`cycle/layer4/result-registration.json`は非圧縮で保持した。

## 一次アーティファクト

- [登録result](385575fdc9694959af1c86042c3705c2.json)
- [品質監査](candidate214-packet-source-container-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate214-packet-source-container-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate214-packet-source-container-closure-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate214-packet-source-container-closure-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate214-packet-source-container-closure-implementation-audit.md)
