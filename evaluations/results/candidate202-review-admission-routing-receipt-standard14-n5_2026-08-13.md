# Candidate202 Standard14全14ケースN=5結果

> **結果**: `70 / 70 valid / Score 4 = 70 / quality_passed / mechanism_failed / stopped`

## 結論

Candidate202 `the-caption-3ce91a4-review-admission-routing-receipt-r1`を、利用者の明示的な追加許可に基づきStandard14全14ケースで各5回、合計70 atomic runs実行した。70 / 70がvalidで、external failure、再試行および除外は0件だった。固定rating contractでは全70件がScore 4となり、品質gateは通過した。

一方、開始identityの不一致がreadを禁止しない9実装ケース45件のうち31件で、identity確認だけを先に発行し、結果受領後に許可済みreadへ進んだ。Candidate175の同一経路は1 / 45である。Candidate202が保持する共同発行predicateに反し、追加model stepによるcontext再投入を生むため、Standard14機構gateは不通過とする。

ADR9の`quality_passed / mechanism_failed`判定も維持する。今回のStandard14品質通過はADR9 gate通過、採用、releaseまたはprojectionを意味しない。

## 実行結果

| 項目 | 結果 |
|---|---:|
| requested slots | 70 |
| valid | 70 |
| excluded / external failure | 0 / 0 |
| Score 4 | 70 |
| command protocol violation | 0 |
| child agent / 不要review producer | 0 / 0 |
| 開始identity単独発行 | 31 / 45 |

`owner-producer evidence`の`failed` 55件は、owner語列に対応する独立producerが存在しないという診断である。Standard14は独立review operationを要求していないため、これは期待される非起動であり、品質failureではない。月次レビューの数値位置診断は`exact=4 / mismatch=1`だったが、固定rating contractでは品質に影響しない。

## C175とのKPI比較

両resultのcompatibility keyは`cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`で一致する。

| KPI中央値 | Candidate175 | Candidate202 | C202 - C175 |
|---|---:|---:|---:|
| quality score | 100.0 | 100.0 | 0.0 |
| all-agent total tokens | 1,692,063 | 1,918,118 | +226,055（+13.36%） |
| elapsed seconds | 804.940 | 938.081 | +133.141（+16.54%） |

品質中央値は同じだが、Candidate202はtokenと経過時間の双方で悪化した。保存済みroot traceでは、readを禁止しない9実装ケースにおける開始identity単独発行がCandidate175の`1 / 45`から`31 / 45`へ増えており、KPI差と機構不一致の方向が一致する。

## 一次証拠

- [登録result](08c295a44f7b4a70873c7fc1c503f9e8.json)
- [品質監査](candidate202-review-admission-routing-receipt-standard14-n5-quality-audit-r1.json)
- [機構監査](candidate202-review-admission-routing-receipt-standard14-n5-mechanism-audit-r1.json)
- [C175比較](candidate202-review-admission-routing-receipt-standard14-n5-comparison-c175-r1.json)
- [評価設計](../../docs/candidate202-review-admission-routing-receipt-standard14-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate202-review-admission-routing-receipt-standard14-n5-execution-preparation-audit.md)

実行一次artifactは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate202-review-admission-routing-receipt-v14-medium-standard14-n5-cli0146-20260813-r1`に保存した。

## 状態

`candidate202_Standard14_completed / valid_70 / score4_70 / quality_passed / mechanism_failed / isolated_identity_31_of_45 / C175_reference_1_of_45 / ADR9_mechanism_failed_retained / stopped / adoption_not_decided / release_not_created / projection_not_performed`
