# Candidate215 packet source region closure ADR9 r2 N=5結果

## 結論

Candidate215は45 / 45 valid、除外0件だったが、Scoreは`4 / 1 = 41 / 4`で品質gateを通過しなかった。packetへ投影したregionと重なるreadまたはcontainer全体のreadは0件、rootによるreviewer-owned targetの先読みも0件であり、Candidate214で閉じた再取得経路は再開していない。

一方、同じcontainer内の未投影・非重複regionを読む合法経路は13回、9 runで実際に使われ、ADR06は5 / 5で期待`blocked`へ一致した。この点はCandidate214のcontainer一律閉鎖より改善した。ただしpacket construction receiptのregionは一貫して固定されず、ADR03の1件とADR05の2件では必要なinventory / contract regionへ到達せず、存在しないpaired targetを読んで`unavailable`となった。さらにADR07の1件ではpaired targetだけを観測した後、packetに含まれなかったinventory / contractを同一containerから取得できず、期待`completion_ready`に対して`unavailable`となった。

また、ADR07とADR09ではterminal dispositionを分けるために不要な同一container内の非重複region readが7回、4 runに残った。したがってCandidate215は`quality_failed / mechanism_failed / stopped`である。停止条件に従い、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-packet-source-region-closure-r1`
- bundle SHA-256: `da08a220485f0e48fe38165ec379ae52c60a0cbef9b225b92fc3edb7ff855a4f`
- profile: `candidate215-packet-source-region-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 215.373秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 41 / 45 |
| terminal一致 | 41 / 45 |
| artifact境界一致 | 44 / 45 |
| reviewer cardinality一致 | 45 / 45 |
| required command一致 | 14 / 14 |
| forbidden canary delivery | 0 |

command collectorは5件をprotocol違反として検出したが、いずれも保存済みmachine-bound exit statusを認識しなかった偽陽性であり、実際のexit status欠落は0件だった。

低品質4件は次のとおりである。

- ADR03 iteration 3: 期待`blocked`、実際`unavailable`。
- ADR05 iteration 1と4: 期待`blocked`、実際`unavailable`。
- ADR07 iteration 2: 期待`completion_ready`、実際`unavailable`。成果物変更とrequired commandも行われなかった。

## 機序

| 固定gate | 結果 |
|---|---:|
| packet投影regionの重複またはwhole-container read | 0回 |
| 必要な非重複region read | 13回、9 run |
| 不要な非重複region read | 7回、4 run |
| packet caseの誤paired read | 3回 |
| reviewer mixed read | 0回 |
| reviewer manifest外read | 0回 |
| root reviewer-owned target preread | 0 / 30 |
| ADR03〜ADR06 terminal一致 | 17 / 20 |
| ADR07 paired targetだけの経路 | 1 / 5 |
| ADR09 paired targetだけの経路 | 3 / 5 |
| review result admission一致 | 41 / 45 |
| review result effect一致 | 41 / 45 |

### 成立した部分

- packetへ投影したregionと重なるreadまたはcontainer全体の再readは0件だった。
- rootのreviewer-owned target先読みは0件だった。
- 同じcontainer内の固定非重複regionを読む経路は実際に13回使われ、9 runで必要な反例を成立させた。
- ADR06はCandidate214で残った1件の誤停止を含め5 / 5で期待`blocked`へ一致した。
- reviewer cardinality、canary、mixed source、manifest外sourceの境界は維持した。

Candidate215は「同じfileなら全部禁止」ではなく、「packetと重ならない構造領域なら必要時に読める」という経路自体を初めて実行上で確認した。

### 残った誤経路

Candidate215の`source_region_structurally_fixed`は、packet itemの供給元resultがcanonical selectorまたはregionを直接bindした場合だけreceiptへregionを残す。実runではrootが`design-admission.json`全体を先に読み、その受領済み構造objectからpacket用の部分を選んだ。元のread result自体にはselectorがないため、packet構築時にどの部分を選んだかがreceiptへ固定されず、container fallbackとfixed regionがrunごとに揺れた。

その結果、同じ入力であっても、必要なinventory / contractだけを読むrun、paired targetへ逸れるrun、必要regionを一切読めないrun、必要でないinventory / contractまで読むrunが併存した。これはfield名やcase名の対応不足ではなく、受領済み構造objectからpacket itemを作った時点の投影経路を、機械的な出所identityとして固定していないことが原因である。

## 今回から見える次の軸

次に固定すべきなのは、repository read時のselectorではなく、packet構築時に受領済み入力objectのどの構造regionを実際に投影したかである。

必要な境界は次のようになる。

1. packet itemを作る時点で、admission済み入力objectからliteral itemへ使ったexact structural projection pathをconstruction receiptへ固定する。
2. 元のrepository readがcontainer全体でも、投影元が一意ならそのregionだけを閉じる。
3. 複数origin、変換で出所が不明、または一意に投影できないitemだけはcontainer fallbackへ戻す。
4. reviewer readは、固定した投影regionと重ならず、未確定のterminal dispositionを直接分けるregionだけを許可する。

これは名前や意味をcaseへ対応させる案ではない。AIがpacketを構築した実際のデータ依存を構造的provenanceとしてmaterializeし、そのidentityだけで誤経路を閉じる案である。Candidate215は修正再実行せず、C147を直接基盤とする別Candidateの作成前gateで検討する。

## KPI

登録resultの中央値は次のとおりである。

| KPI | Candidate215 |
|---|---:|
| `quality_score` | 91.667 |
| all-agent `total_tokens` | 1,107,529 |
| `elapsed_seconds` | 701.666 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate215_ADR9_completed / valid_45 / score4_41 / score1_4 / quality_failed / mechanism_failed / stopped / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

実行batchはresult登録後にsealし、最終圧縮を完了した。execution evidence archiveのSHA-256は`88d4bbe79d6eca0f06032e19b895a8845987bc83060d813abe0542aa12d0d5b1`、final evidence archiveは`61a858cd27569697928c8b80d4303afe2c6be04b849084db5fb5724a258dc365`である。Layer 1と`cycle/layer4/result-registration.json`は非圧縮で保持した。

## 一次アーティファクト

- [登録result](e459b816c1ae4b97b2a776252b6f3367.json)
- [品質監査](candidate215-packet-source-region-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate215-packet-source-region-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate215-packet-source-region-closure-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate215-packet-source-region-closure-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate215-packet-source-region-closure-implementation-audit.md)
