# Candidate221 review source authority closure ADR9 r2 N=5結果

## 結論

Candidate221は45 / 45 valid、除外0件だった。Scoreは`4 / 1 = 29 / 16`で、terminalは29 / 45、成果物境界は42 / 45、required commandは12 / 15、forbidden canary deliveryは0件だった。

しかし、producer別source authorityは経路閉鎖として成立しなかった。ADR03からADR06の20 / 20 runでrootがreviewer-owned targetを先行取得し、mixed-owner resultを受領した。TaskSpecのpacket permissionとmanifest targetから集合を分ける制御を加えても、AIはwhole design containerをroot operationの合法なtargetへ含めた。C214で閉じた誤経路が再開しているため、Candidate221は`quality_failed / mechanism_failed / stopped`である。repair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。次Candidateも作成しない。

## 固定条件と実行

- prompt: `the-caption-3ce91a4-review-source-authority-closure-r1`
- bundle SHA-256: `4e40da5f16466226a053b5bcc5efa31c5600219f4117a8bc0635c3c5a0196562`
- profile: `candidate221-review-source-authority-closure-adr9-r2-medium-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- configured M: `24`
- reference result: Candidate210 `9ac8eb53cf79463f9c7ae446c61b625a`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- preflight: `ready`、authorized 45、issued before run 0
- execution: requested 45、valid 45、excluded 0、attempt 45
- execution elapsed: 245.638秒

## 品質

| 指標 | 結果 |
|---|---:|
| valid | 45 / 45 |
| Score 4 | 29 / 45 |
| terminal一致 | 29 / 45 |
| artifact境界一致 | 42 / 45 |
| reviewer cardinality一致 | 27 / 45 |
| required command一致 | 12 / 15 |
| forbidden canary delivery | 0 |

command protocol violationとして記録された4件はcollectorのfalse positiveであり、machine-bound exit statusの真正な欠落は0件だった。一方、required command不一致3件とartifact境界不一致3件は品質失敗として残る。有効runなので除外または再実行していない。

## 機序

| 固定gateまたは診断 | 結果 |
|---|---:|
| rootによるreviewer-owned targetの先行取得 | 20 / 20 packet case |
| mixed-owner root admission | 20 / 20 packet case |
| 必要なreviewer direct observation | 7 / 20 packet case |
| rootとreviewerの同一値二重消費 | 7 / 20 packet case |
| ADR03〜ADR06 terminal一致 | 7 / 20 |
| ADR07 paired targetだけのroute | 1 / 5 |
| ADR09 paired targetだけのroute | 0 / 5 |
| paired caseでpacket-carried projectionを再読 | 4回 |
| review不要時のreviewer起動 | 0 run |
| manifest外read | 0回 |
| 基本review機序通過 | 25 / 45 |
| source authorityを含む全機序通過 | 16 / 45 |

### 反証された設計仮定

作成前監査では、TaskSpecが列挙するpacket permissionとfinite evidence manifestから、root packet projection、root-owned operation、reviewer direct observationを発行前に一意化できると判断した。実行結果はこの判断を支持しなかった。

```text
TaskSpecのpacket permissionとmanifest targetを読む
  -> AIがwhole design containerをroot_operation_setへ含める
  -> root whole-source readを許可
  -> reviewer-owned inventory / contractsをrootへ配送
```

追加条項は対象集合を定義したが、その集合へのtarget帰属をモデル自身が判断する余地を閉じなかった。そのため、禁止対象を同じモデルがrootの合法なoperation targetへ再分類でき、permission edgeが残った。これはC215からC220までと同じ自己分類依存の別表現であり、C214のroute closureを保持できていない。

## 停止判断

現行のmodel-visible inputでは、rootが必要なpacket projectionだけを取得できることと、同じcontainer内のreviewer-owned値を取得不能にすることをpromptだけで同時に強制できるとは実証できなかった。新しいlabel、ticket、確認順または必要性条件でread permissionを再開せず、`prompt_control_not_demonstrated / candidate_not_created`で停止する。

## KPI

| KPI | Candidate221 |
|---|---:|
| `quality_score` | 75.000 |
| all-agent `total_tokens` | 751,839 |
| `elapsed_seconds` | 620.909 |

品質・機序が不通過なので、中央値を改善または採用根拠として扱わない。

## 状態

`candidate221_ADR9_completed / valid_45 / score4_29 / score1_16 / quality_failed / mechanism_failed / stopped / next_candidate_not_created / ADR9_N20_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

## 実行証拠の保存

- execution archive SHA-256: `ab23ac32b79ae09d034eb514ea6bffa6c3db91bc1b5d9bc1f056a0df394b03f8`
- execution seal SHA-256: `5f6506ae75b8b29201234ba3fe7215b88e947fc2c62bfa0998ab0eb281182081`
- final archive SHA-256: `25ef3bc5abb893ffabbf6aa6e20886f3dd2d305b9505f9a1f76157e096227c8a`
- final manifest SHA-256: `351c5134d7716b44b01d2a94baab1e8fb2a1b06ddc6b72ee713694b778b784a3`

## 一次アーティファクト

- [登録result](4511cbb39fb04bb2ad47d6219a12cf7e.json)
- [品質監査](candidate221-review-source-authority-closure-adr9-r2-n5-quality-audit-r1.json)
- [機序監査](candidate221-review-source-authority-closure-adr9-r2-n5-mechanism-audit-r1.json)
- [評価設計](../../docs/candidate221-review-source-authority-closure-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate221-review-source-authority-closure-adr9-r2-n5-execution-preparation-audit.md)
- [実装監査](../../docs/candidate221-review-source-authority-closure-implementation-audit.md)
