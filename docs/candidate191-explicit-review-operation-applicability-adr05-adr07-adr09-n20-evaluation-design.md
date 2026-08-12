# Candidate191 ADR05・ADR07・ADR09 N=20拡張評価設計

> **状態**: `completed / existing_n5_reused / new_45_valid / cumulative_60_score4 / mechanism_passed`

## 結論

Candidate191の限定M5で成立した三result kindから、過去に低頻度失敗または経路不安定を観測したADR05、ADR07、ADR09だけを累積N=20へ拡張する。Candidate191 M5の適格な各5件を再利用し、各ケースの不足15件、合計45件だけを新規発行対象として固定する。

- ADR05: `counterexample_found`と無関係missingのdependency分離。C176 N=50で反例観測と無関係missingを一resultへ束ねたterminal失敗があり、C147とC176の訂正機序監査でも真正なcommand evidence違反が残った経路。
- ADR07: 必要観測完了後の`no_counterexample_found`。Candidate189でcurrent resultへsaved prior result用permissionを誤適用した直接修正経路。
- ADR09: 判断依存入力不足時の独立review起動、`unavailable`およびnon-value dependency。過去Candidateでreview省略または危険な変更が不安定だった経路。

ADR03、ADR04、ADR06は同じreview-required経路の基本成立をM5で確認済みであり、今回の低頻度リスクを追加で区別しないため拡張しない。ADR01、ADR02、ADR08およびTPOを別比較系列として追加しない。

## 固定条件

- profile: `candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-medium-m24-cli0146`
- reference profile: `candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-reference-n5-medium-m24-cli0146`
- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- evaluation set: ADR9 r2
- coverage: ADR05、ADR07、ADR09の累積各20件
- reuse: Candidate191 M5の各5件、合計15件
- new slots: 各15件、合計45件
- max workers: `24`

case、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor挙動および保存済みLayer 1はCandidate191 M5から変更しない。`N`とdispatch iterationはatomic run identityへ含めない。M5の登録result `b71bcb211b064977900bce9aa0132cd4`と訂正機序監査r3を一組として再利用可否を判断し、旧機序監査r2単独の停止判定を用いない。

## 実行前gate

1. Candidate191 M5 poolから3ケース各5件を固定selectionへ選ぶ。
2. selectionを登録し、3ケースN=5のreference resultをwrite-onceで固定する。
3. 同じprompt identityと実効条件のpoolで既存件数が各5件と確認する。
4. `plan-missing --desired-count 20`が不足15件×3ケースだけを固定する。
5. 3 template、45 capsule、global plan、resource classおよびprompt identityを照合する。
6. Candidate191 M5の保存済みLayer 1を再利用し、comparison preflightと再検証が`ready`になるまで一件も発行しない。

不一致が一項目でもあれば45件を発行せず停止する。

## 完了判定

累積60 / 60 validかつScore `4`で、各20件について一reviewer、期待result kind、authentic observation、terminal、artifact変更境界、局所dependencyおよび禁止情報非配送が成立することを要求する。新規または累積の一件でもquality・mechanism不一致ならresultを保持して停止し、M7全体へ進まない。

N=20で結論を変え得る低頻度失敗を観測しない限りN=50は発行しない。通過してもprior result runtime経路、Standard14全14ケース、採用、releaseまたはprojectionは未判定である。

comparison preflightは不足45件だけを`ready`として承認した。実行準備のidentityと未発行境界は[`Candidate191 M6実行準備監査`](candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-execution-preparation-audit.md)を正本とする。

固定planの45件は45 / 45 valid、Score `4 = 45`で、既存15件との累積は60 / 60 valid、Score `4 = 60`となった。訂正済みcommand-evidence基準を含む機序監査も通過し、N=20で結論を変え得る低頻度失敗を観測しなかったためN=50は発行しない。結果は[`Candidate191 ADR05・ADR07・ADR09 N=20`](../evaluations/results/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20_2026-08-12.md)を正本とする。

`candidate191_m6_completed / selected_three_high_risk_cases / existing_fifteen_reused / new_forty_five_valid / cumulative_sixty_score4 / mechanism_passed / N50_not_issued`
