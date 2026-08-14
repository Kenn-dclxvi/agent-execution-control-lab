# Candidate222 review source observation view ADR9 r2 N=5結果

## 結論

Candidate222は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 41 / 4`で、artifact境界は45 / 45、required commandは15 / 15、forbidden canary deliveryは0件だった。

しかし、目的である必要reviewの完遂とsource delivery境界は成立しなかった。必要reviewは30件中29件で起動したが、review result admissionは42 / 45、期待terminalと変更効果は41 / 45だった。ADR03からADR06では20 / 20 runでrootがreview前にwhole design containerを受領し、packet非配送のinventory / contractsを含むmixed-owner admissionが再発した。必要なreviewer direct observationは12 / 20に留まった。

したがってCandidate222は`quality_failed / mechanism_failed / stopped`である。有効runを保持し、repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-source-observation-view-r1`
- bundle SHA-256: `6ccb9fa020e65898e5a445d37db1338fa75cc917116fd09a6e87fc48d0dcdfad`
- profile: `candidate222-review-source-observation-view-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 213.701秒

TaskSpec、case、fixture、oracle、rating、runtime、permissionおよびexecutor条件は変更していない。比較変数はCandidate promptだけである。

## 必要reviewの結果

| 指標 | 結果 |
|---|---:|
| 必要reviewer起動 | 29 / 30 |
| review result admission一致 | 42 / 45 |
| review result effect一致 | 41 / 45 |
| ADR03〜ADR06 terminal一致 | 16 / 20 |
| artifact境界一致 | 45 / 45 |
| required command一致 | 15 / 15 |
| forbidden canary delivery | 0 |

Score 1の4件は、ADR03の2件、ADR04の1件、ADR05の1件で、期待した`blocked`ではなく`unavailable`になった。うちADR05の1件は必要reviewer自体が起動しなかった。有効runなので除外または再実行していない。

## observation view機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| rootによるreviewer-owned targetの先行取得 | 20 / 20 packet case |
| mixed-owner root admission | 20 / 20 packet case |
| 必要なreviewer direct observation | 12 / 20 packet case |
| rootとreviewerの同一値二重消費 | 12 / 20 packet case |
| ADR07 paired targetだけのroute | 3 / 5 |
| ADR09 paired targetだけのroute | 4 / 5 |
| paired caseでpacket-carried projectionを再読 | 6回 |
| review不要時のreviewer起動 | 0 run |
| manifest外read | 0回 |
| 基本review機序通過 | 41 / 45 |
| observation viewを含む全機序通過 | 22 / 45 |

### 得られた手がかり

Candidate222はpre-review root authorityから将来operation用viewを削除したが、実際のrootは45 / 45 runで最初にdesign container全体を読んだ。20 packet caseのうち、明示的なpacket projection commandへ狭まったのは3件だけで、それらもinventory / contractsをprojectionへ含めた。残りは`sed`によるwhole-source outputだった。

つまり、`observation view`を概念として定義するだけでは、repository readが返すobservable outputをそのviewへ物理的に閉じられなかった。モデルがwhole-source readを禁止条項へ反しても実行できる能力が残り、受領後の分類禁止も実行不能性を作らなかった。

C221では、whole containerを将来の`root_operation_set`へ再分類したことが主因だと仮定した。C222はその集合をpre-review authorityから削除しても同じ20 / 20のmixed-owner deliveryが残ったため、この説明を棄却した。残る因果辺は、rootがpacketを作るためのliteral値を同じcontainerから取得する必要と、そのreadがwhole-container outputも返せる能力の結合である。

この結果は[`review carrier bootstrap authority監査`](../../docs/review-carrier-bootstrap-authority-audit.md)の累積閉鎖台帳へ接続した。次の検討では、rootがpacketを構築する正常carrierと、rootへwhole containerを返さない境界を、変更しないmodel-visible inputから同時に証明する。分類名、禁止文または条件を同じread surfaceへ追加するだけのCandidateは作成しない。

## KPI

| KPI | Candidate222 |
|---|---:|
| `quality_score` | 91.667 |
| all-agent `total_tokens` | 1,215,298 |
| `elapsed_seconds` | 727.665 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate222_ADR9_completed / valid_45 / score4_41 / score1_4 / quality_failed / mechanism_failed / stopped / next_candidate_not_created / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

- execution archive SHA-256: `66c33173a9ec44f37199201f1099263bc66d243f9d7d5ca9999679cb5edf3426`
- execution seal SHA-256: `1f20e25a2ee7bd9de816c4406376719ec2a4eee03cb0293ed1c759178debc2b3`
- final archive SHA-256: `e0fc71363f22452ad38a79155261c860bf7a4cd88ff530993de4cc3d633b0268`
- final manifest SHA-256: `53b6b007ba0b1749fe99bbed6a6a352a3501d8a883ad633bf9a564207e6f9d2f`

## 一次アーティファクト

- [登録result](2d337430230841bd9cda2c938fa3536b.json)
- [品質監査](candidate222-review-source-observation-view-adr9-r2-n5-quality-audit-r1.json)
- [基本機序監査](candidate222-review-source-observation-view-adr9-r2-n5-mechanism-base-audit-r1.json)
- [observation view機序監査](candidate222-review-source-observation-view-adr9-r2-n5-mechanism-audit-r1.json)
- [Candidate222設計](../../docs/candidate222-review-source-observation-view-design.md)
- [実行準備監査](../../docs/candidate222-review-source-observation-view-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate222-review-source-observation-view-implementation-audit.md)
