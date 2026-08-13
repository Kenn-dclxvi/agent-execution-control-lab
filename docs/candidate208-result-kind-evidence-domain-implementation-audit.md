# Candidate208 result kind別証拠境界 実装監査

## 結論

Candidate208はC207を直接基盤とし、root `AGENTS.md`の`TERMINAL`、`CONTEXT`、`EVIDENCE_GATE`だけへresult kind別証拠依存境界を実装した。新しいoperation、model-step barrier、review順序、receipt、台帳またはvalidation制御は追加していない。

ADR9 r2 N=5は45 / 45 Score `4`だったが、不要read 1件とroot preread 1件が残り、`quality_passed / mechanism_failed / stopped`である。

## identity

- prompt identity: `the-caption-3ce91a4-result-kind-evidence-domain-r1`
- direct base: `the-caption-3ce91a4-c147-review-boundary-recomposition-r1`
- bundle SHA-256: `be67f9dce76e57ac1b1f7535a4e1128f3f7b9f0b7810e55527d089d1cbd7f15f`
- root `AGENTS.md` SHA-256: `ff79fcf58e174adeb14362ccd9d3d1547cf74411b2c916a30c192ebf1aa831fa`
- root `AGENTS.md` Git blob: `791138b2d4dc20987838745a7a36aed7dc020194`
- changed target: `AGENTS.md`だけ

## 実装対応

| C207制御群 | C208の置換 |
| --- | --- |
| `TERMINAL` | `counterexample_found`、`no_counterexample_found`、`review_unavailable`の必要証拠集合を分離し、反例certificate外のmanifestをterminal dependencyから除外 |
| `CONTEXT` | manifest descriptorを許可可能な有限観測集合へ限定し、reviewer ownershipをprojection再取得義務としない |
| `EVIDENCE_GATE` | repository readを未解決result kindの必要証拠へbindし、packet反例成立時はcertificate外consumerを閉じる |

## 構造診断値

| prompt | 文字数 | UTF-8 bytes | top-level条項 |
| --- | ---: | ---: | ---: |
| C207 | 10,290 | 15,024 | 14 |
| C208 | 10,498 | 15,386 | 14 |
| 差 | +208 | +362 | 0 |

本文増加は一つの証拠依存境界に閉じている。実測ではC207比で品質中央値同値、token中央値`-1.83%`、elapsed中央値`-16.31%`だったため、この追加量をcost増とは判定しない。一方、機序不通過なので過不足の最終判定や採用判断へは進めない。

## 静的・実試験

- Candidate208集中テスト（結果記録後）: `5 passed`
- comparison preflight: 9ケース各5件、prompt identity以外一致、`max_workers=24`、不足45件、`ready`
- ADR9: 45 / 45 valid、45 / 45 Score `4`
- mechanism: packet反例成立後read 1 / 20、root preread 1 / 30、`failed`
- Standard14、N=20、repair rerun: 未開始
- 最終全テスト: `1294 passed, 1875 subtests passed`
- `git diff --check`: 通過

詳細は[ADR9結果](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n5_2026-08-13.md)を参照する。

## 後続のStandard14測定

上記停止後、利用者がADR05-i4の不要readとADR09-i5のroot prereadを明示的に受容し、ADR9の機序不通過を維持したまま通常経路のStandard14 N=5測定を再開した。70 / 70 valid、70 / 70 Score `4`で、Candidate206比はtoken中央値`+2.90%`、elapsed中央値`-4.49%`だった。この後続結果は上記ADR9停止時点の記録を書き換えず、採用または機序合格を意味しない。詳細は[Standard14結果](../evaluations/results/candidate208-result-kind-evidence-domain-standard14-n5_2026-08-13.md)を参照する。

後続測定の記録追加後はCandidate208集中テスト`6 passed`、全テスト`1295 passed, 1875 subtests passed`、`git diff --check`通過を確認した。

## 累積N=50追試

ADR9は既存N=5を再利用し、不足405件だけを追加して累積450件へ延長した。449 / 450 Score `4`で品質不通過、機序不通過は23 / 450件だった。N=5で低頻度だった反例成立後readとroot prereadはそれぞれ10 / 199件、3 / 300件として再現し、reviewer closed-source readも20件観測した。Standard14 N=50はADR9品質gateで発行していない。詳細は[累積N=50結果](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50_2026-08-13.md)を参照する。

累積N=50記録後はCandidate208集中テスト`7 passed`、全テスト`1296 passed, 1875 subtests passed`、profile index current、`git diff --check`通過を確認した。
