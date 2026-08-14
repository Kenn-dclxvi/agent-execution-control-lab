# Candidate175 / Candidate208 ADR9 r2累積N=50機序比較

## 結論

Candidate208のN=50監査で固定した現在の機序定義をCandidate175の全450件へ同じように適用した。機序不通過runはCandidate175の138 / 450に対してCandidate208は23 / 450で、Candidate208が115件少なかった。

主差は、reviewerがclosed sourceまたは正確でないread setを使う経路と、最終的に`counterexample_found`となったrunでdirect readを先に発行する経路である。Candidate208はこれらを大幅に減らしたが0件にはしておらず、両Candidateとも機序gateは不通過である。

## 同一定義比較

| 機序 | Candidate175 | Candidate208 | C208 − C175 |
|---|---:|---:|---:|
| 機序不通過run | 138 / 450 | 23 / 450 | -115 |
| reviewer cardinality一致 | 449 / 450 | 450 / 450 | +1 |
| review result admission一致 | 449 / 450 | 448 / 450 | -1 |
| review result effect一致 | 447 / 450 | 449 / 450 | +2 |
| routing complete | 299 / 300 | 300 / 300 | +1 |
| root prereadなし | 298 / 300 | 297 / 300 | -1 |
| reviewer exact read set一致 | 191 / 300 | 282 / 300 | +91 |
| reviewer closed-source read | 139 | 20 | -119 |
| reviewer mixed read | 66 | 8 | -58 |
| reviewer outside read | 73 | 12 | -61 |
| counterexample result | 199 | 199 | 0 |
| 反例成立後readなし | 101 / 199 | 189 / 199 | +88 |
| 反例成立後read | 98 / 199 | 10 / 199 | -88 |

複数の機序違反は同じrunで重複し得るため、read件数を加算して不通過run数にはしない。

## Candidate175のケース別不通過

| case | 不通過run |
|---|---:|
| ADR03 | 18 / 50 |
| ADR04 | 20 / 50 |
| ADR05 | 40 / 50 |
| ADR06 | 22 / 50 |
| ADR07 | 15 / 50 |
| ADR09 | 23 / 50 |
| ADR01・ADR02・ADR08 | 0 / 150 |

C175の失敗はreview必須6ケースへ限定され、特にADR05の40 / 50が大きい。品質はADR03・ADR04の3件だけが失敗した一方、品質Score `4`でもread発行資格を満たさないrunが多数あるため、品質と機序を分けて扱う必要がある。

## 解釈境界

この比較はCandidate208で固定した機序predicateをCandidate175へ遡及適用した観測比較である。Candidate175の当時のN=5 gateや採用状態を履歴上書きしない。また、C175のhistorical contractが全direct readを明示的に禁止していたと事後認定するものでもない。

比較から言えるのは、現在必要としている「counterexample certificate成立後にconsumerを持たないreadを発行しない」「reviewerはclosed sourceではなくexact direct targetだけを読む」という境界に対して、C208はC175より明確に近いが、まだ23 / 450件の誤経路を残している、という範囲である。

## 一次証拠

- comparison receipt: [`candidate175-candidate208-adr9-r2-n50-mechanism-comparison-r1.json`](candidate175-candidate208-adr9-r2-n50-mechanism-comparison-r1.json)
- Candidate175 mechanism audit: [`candidate175-review-operation-admission-closure-adr9-r2-n50-mechanism-audit-r1.json`](candidate175-review-operation-admission-closure-adr9-r2-n50-mechanism-audit-r1.json)
- Candidate208 summary audit: [`candidate208-result-kind-evidence-domain-adr9-r2-n50-summary-audit-r1.json`](candidate208-result-kind-evidence-domain-adr9-r2-n50-summary-audit-r1.json)
