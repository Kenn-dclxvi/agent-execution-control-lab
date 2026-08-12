# Candidate190 ADR05・ADR07・ADR09 N=20拡張評価設計

> **状態**: `design_fixed / existing_n5_reused / preflight_not_started / zero_new_slots_issued`

## 結論

Candidate190の限定M5で成立した三result kindから、過去に低頻度失敗または経路不安定を観測したADR05、ADR07、ADR09だけを累積N=20へ拡張する。既存の適格な各5件を再利用し、各ケースの不足15件、合計45件だけを新規発行する。

- ADR05: `counterexample_found`と無関係missingのdependency分離。Candidate176 N=200とCandidate177で低頻度の証拠昇格・機序不一致を観測した経路。
- ADR07: `no_counterexample_found`のcurrent result admission。Candidate189で1 / 5件だけprior用permission誤適用を観測した直接修正経路。
- ADR09: `unavailable`のcurrent result admissionとnon-value dependency。過去Candidateでreview省略または危険な変更が不安定だった経路。

ADR03、ADR04、ADR06は同じ`counterexample_found`の基本経路としてN=5を通過し、今回の低頻度リスクを追加で区別しないため拡張しない。TPOまたは別系列を増やさない。

## 固定条件

- profile: `candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-medium-m24-cli0146`
- reference profile: `candidate190-current-prior-review-result-admission-adr05-adr07-adr09-reference-n5-medium-m24-cli0146`
- prompt: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- evaluation set: ADR9 r2
- coverage: ADR05、ADR07、ADR09の累積各20件
- reuse: Candidate190 M5の各5件、合計15件
- new slots: 各15件、合計45件
- max workers: `24`

case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動およびLayer 1はCandidate190 M5から変更しない。`N`とdispatch iterationはatomic run identityへ含めない。

## 実行前gate

1. Candidate190 M5 poolから3ケース各5件を固定selectionへ選ぶ。
2. 同じprompt identityと実効条件の3ケースpoolで既存件数が各5件と確認する。
3. `plan-missing --desired-count 20`が不足15件×3ケースだけを固定する。
4. 3 template、45 capsule、global plan、resource classおよびprompt identityを照合する。
5. 保存済みLayer 1のfixtureとset identityを再利用し、coverageだけを3ケース累積N=20へbindする。
6. comparison preflightと再検証が`ready`になるまで一件も発行しない。

不一致が一項目でもあれば45件を発行せず停止する。

## 完了判定

累積60 / 60 validかつScore `4`で、各20件について一reviewer、期待result kind、authentic observation、terminal、artifact変更境界、局所dependencyおよびADR06以外でも禁止情報非配送が成立することを要求する。新規または累積の一件でもquality・mechanism不一致ならresultを保持して停止し、Standard14へ進まない。

通過してもprior result runtime経路、Standard14、採用、releaseまたはprojectionは未判定である。

## 実行結果

固定planの不足45件だけを発行し、追加45 / 45、累積60 / 60がvalidかつScore `4`となった。三result kindは各20件で、current result admission、terminalおよびartifact変更境界も60 / 60で成立した。結果は[`Candidate190 ADR05・ADR07・ADR09 N=20`](../evaluations/results/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20_2026-08-12.md)を正本とする。

`candidate190_m6_completed / selected_three_high_risk_cases / existing_fifteen_reused / new_forty_five_valid / cumulative_sixty_score4 / quality_mechanism_passed`
