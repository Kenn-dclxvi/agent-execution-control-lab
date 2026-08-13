# Candidate206 admitted evidence current ADR9・Standard14 N=5結果

## 結論

Candidate206はADR9とStandard14の品質・機序gateを通過したが、最適化gateは通過しなかった。`admitted_evidence_current`によってmodel-visibleなroot instructionの再取得を0件へ減らせることは実証した。一方、Standard14中央値はCandidate175比でtokenが7.77%減ったがelapsedが12.40%増え、支配的なcost改善にならなかった。

したがって、関係の機序は成立済み知見として保持するが、現在の一律追加文言を採用、release、projectionまたは次Candidateの親にはしない。

## 比較境界

- Candidate206: `the-caption-3ce91a4-admitted-evidence-current-r1`
- comparison carrier: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- Candidate175を使う理由: 保存済みADR9とStandard14が品質・機序とも通過しており、H1だけを二段階で測定できるため
- 非含有: Candidate176以降の失敗系譜の機構
- Candidate175の位置づけ: 比較用carrierだけであり、採用、release、projectionまたはC147の置換ではない

## ADR9 r2 N=5

- result: `aee4cdf149ef43de9305b1a3138ebe59`
- reference result: `eba0a4bc1d0e4391afa631462b8daccb`
- valid: 45 / 45
- excluded: 0
- Score 4: 45 / 45
- required reviewer start: 25 / 25
- unnecessary reviewer start: 0
- ADR06 forbidden canary delivery: 0
- unadmitted change: 0
- root instruction本文再取得: Candidate175 7 run、Candidate206 0 run

ADR9中央値はCandidate175比でtoken `-24,757`（`-2.20%`）、elapsed `+21.491秒`（`+2.93%`）だった。品質とreview機序を維持したため、事前条件どおりStandard14へ進んだ。

## Standard14 N=5

- result: `0aba77ffad0848e5be7e635f96293070`
- reference result: `c31b560bce92400293c7b3bc40715246`
- valid: 70 / 70
- excluded: 0
- Score 4: 70 / 70
- command protocol violation: 0
- monthly numeric location: exact 5 / 5
- root instruction本文再取得: Candidate175 7 run、Candidate206 0 run

Candidate175の7件はF10 monthly 5件、F08 1件、F07 canonical 1件だった。Candidate206では全て0件になった。開始inputへ含まれないpath-local instructionの取得は、F10 monthly 5 / 5、F10 inventory 5 / 5、F08 5 / 5、A02 1 / 1でCandidate175と同じrun coverageを保持した。

| KPI中央値 | Candidate175 | Candidate206 | 差 |
|---|---:|---:|---:|
| quality | 100 | 100 | 0 |
| all-agent token | 1,692,063 | 1,560,614 | -131,449（-7.77%） |
| elapsed | 804.940秒 | 904.776秒 | +99.836秒（+12.40%） |

H1の主対象であるF10 monthlyのcase中央値も、tokenは`-9,506`（`-8.9%`）だがelapsedは`+9.527秒`（`+20.3%`）だった。全体token差にはF02、F06などroot再取得差がないcaseの変動も含まれるため、`-7.77%`全体をH1の単独因果値にはしない。

## 判断

- quality: `passed`
- mechanism: `passed`
- optimization: `failed_no_kpi_dominance`
- adoption: `not_authorized`
- release: `not_created`
- runtime projection: `not_projected`
- next-candidate parentage: `not_granted`

結果が全件合格でも、elapsed増加は追加品質ではなく追加costである。token低下と相殺して一つの最適解だと決める重みは事前に固定していないため、Candidate206を現時点の最適化として採用しない。C147の現行機能理解には「受領済みevidenceを失効まで再利用する正の関係は実際に行動を変える」という成立済み知見だけを戻す。
