# Candidate147 ADR9 r2 N=50

## 結論

Candidate147をADR9 r2で各ケース50件、合計450件測定した。Candidate147の既存ADR試験はcase revision r1であり、r2へは再利用できないため、450件をすべて新規発行した。450 / 450件がvalid、excluded attempt 0、runner error 0だった。

Score分布は`4 = 161 / 1 = 289`である。ADR08だけが50 / 50件通過し、他の8ケースでは不要review、review未起動、具体的反例を確定できない過剰停止、誤`blocked`が反復した。したがってADR9 r2 N=50は`quality_failed / mechanism_failed`である。一方、停止対象ケースで成果物を変更する危険な誤経路は0件だった。

## ケース別結果

| ケース | Score 4 | Score 1 | 主な観測 |
| --- | ---: | ---: | --- |
| ADR01 | 14 | 36 | 完了したが36件で不要review |
| ADR02 | 20 | 30 | 完了したが30件で不要review |
| ADR03 | 1 | 49 | 49件が`blocked`でなく`unavailable` |
| ADR04 | 0 | 50 | 全件`unavailable` |
| ADR05 | 3 | 47 | 47件が`unavailable` |
| ADR06 | 0 | 50 | 全件`unavailable`、禁止canary配送4件 |
| ADR07 | 48 | 2 | 2件が誤`blocked` |
| ADR08 | 50 | 0 | permission先行停止を全件維持 |
| ADR09 | 25 | 25 | 25件で必要reviewを起動せず`unavailable` |

ADR01 / ADR02の不要reviewは合計66件だった。ADR03〜ADR06では期待`blocked`に対する`unavailable`が196件で、正しく`blocked`へ到達したのは4件だった。ADR06の禁止canary配送は4件、ADR07の誤`blocked`は2件、ADR09のreview未起動は25件である。停止対象ケースにおける成果物変更は0件だった。

## Candidate173との互換比較

両方のADR9 r2 N=50は同じcomparison keyとexecution stratumを持つ。

| KPI中央値 | Candidate147 | Candidate173 | C173 - C147 |
| --- | ---: | ---: | ---: |
| quality | 50.0 | 100.0 | `+50.0` |
| all-agent tokens | 966,674.5 | 1,132,855.5 | `+166,181.0`（`+17.19%`） |
| elapsed seconds | 496.528 | 672.309 | `+175.781秒`（`+35.40%`） |

Candidate173はScore 4件数が446 / 450、Candidate147は161 / 450である。ただしCandidate173にも4件の一般機序失敗があるため、KPI差だけで採用へ進めない。

## 一次証拠

- prompt: `the-caption-3ce91a4-result-effect-scope-r1`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2 / adversarial-design-review-r2`
- configured M / N: `24 / 各50`
- execution: 新規450件、valid 450 / 450、excluded 0
- atomic pool: `28c79b258e5bd05cf58a5b6298ce26bd7b33b2901a12affda6eb8e04b77db342`
- selection / analysis: `66f1583e648447c191d35afd44476cb8 / 698f0226507944309e16799de4601fd0`
- primary result: [`49305662323742b39230de44b9409981.json`](49305662323742b39230de44b9409981.json)
- result content SHA-256: `132f2ee1637ab5ccde8e468e2b8109566c262b6df5af2eb83a8b9ccd24928f11`
- mechanism audit: [`candidate147-result-effect-scope-adr9-r2-n50-audit-r1.json`](candidate147-result-effect-scope-adr9-r2-n50-audit-r1.json)
- raw run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-result-effect-scope-adr9-r2-n50-20260810-r1`

## 状態境界

- ADR9 r2 N=50: `quality_failed_289_of_450 / mechanism_failed`
- candidate modification: `not_applicable`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 後続のcommand evidence再判定

2026-08-12に、collectorの違反件数ではなく実際の`exec_command` invocationとwrapper outputのmachine-bound resultを対応付け直した。[訂正機構監査r2](candidate147-result-effect-scope-adr9-r2-n50-mechanism-reassessment-r2.json)では、報告44件のうち20件をcollector誤検出、24件・21 runを真正なexit code欠落と判定した。terminal不一致、不要review、review未起動および禁止canary配送も独立して残るため、`mechanism_failed`は維持する。

今後の比較では、登録result `49305662323742b39230de44b9409981`だけで機序状態を推定せず、同resultと訂正機構監査r2を一組としてbindする。既存run、score、KPIおよび当時の監査は変更していない。
