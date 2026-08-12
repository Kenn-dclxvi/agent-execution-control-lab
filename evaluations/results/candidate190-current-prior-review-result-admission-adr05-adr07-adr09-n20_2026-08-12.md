# Candidate190 current/prior review result admission ADR05・ADR07・ADR09 N=20

> **結果**: `60 / 60 valid / Score 4 = 60 / quality_passed / mechanism_passed / M6_passed`

## 結論

Candidate190は、過去に低頻度失敗または経路不安定を観測したADR05、ADR07およびADR09だけを累積各20件へ拡張した。M5の既存各5件、合計15件を再利用し、不足各15件、合計45件だけを新規発行した。追加分は45 / 45 valid、除外0件、runner error 0件、Score `4 = 45`だった。累積では60 / 60 valid、Score `4 = 60`である。

機序監査では、`counterexample_found`、`no_counterexample_found`および`unavailable`が各20件成立した。60 / 60件でcurrent reviewer resultのadmission、期待terminalおよびartifact変更境界が一致した。新規45件ではproducer/sender、実観測invocation、certificateおよびrootによるdependency消費も45 / 45件で確認した。

したがってM6は通過する。prior result runtime経路は未観測であり、この結果は保存済みprior resultの再利用経路を証明しない。Standard14、採用、releaseおよびprojectionもまだ成立していない。

## 互換性とatomic再利用

- prompt: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- bundle SHA-256: `63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c`
- reference result ID: `72b1167d8bd84719b975d227c590aa4e`
- comparison preflight compatibility key: `155587cce22ef1f34d5366bd6612a0a6e69ed8225160c51cd5abc6fada945b15`
- pool key: `11b57d4d2908982935f1d21fef9e541e56313b0b2240764f852ac9a7222d58c1`
- selection ID: `d2b9a5214d7a44688126989fe60dde6c`
- analysis ID: `8dd8e62d71984fb2bf756ec38df1a6d1`
- registered result ID: `d3b75f599f024ab8802595311920a00e`
- result content SHA-256: `b3be55b4110ddcbcd6a2415028a1aa7d3b7257ffd4052deec2ad5156a3d25f0a`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-20260812-r1`

最初のpreflightは、累積N=20 profileをN=5基準へ直接照合したためcoverage不一致で発行前停止した。正規のN拡張手順へ直し、既存各5件を固定するreference profileで互換条件を照合し、N=20を最終selection coverageへ分離した。条件を除外または緩和していない。canonical preflightは45 slotだけを承認し、M=24を維持した。

## case別結果

| case | Score 4 | reviewer | result kind | terminal | artifact変更 | 判定 |
|---|---:|---:|---|---|---:|---|
| ADR05 | 20 / 20 | 20 / 20 | `counterexample_found` 20 | `blocked` 20 | 0 | 反例supportと無関係なnon-valueを分離 |
| ADR07 | 20 / 20 | 20 / 20 | `no_counterexample_found` 20 | `completion_ready` 20 | 20 | current resultをadmit後に変更・検証 |
| ADR09 | 20 / 20 | 20 / 20 | `unavailable` 20 | `unavailable` 20 | 0 | 未解決predicateとnon-value atomへ局所依存 |

## 機序監査の訂正

新規45件に対する最初の外部監査は、reviewer出力へ一つの英語見出しを要求し、意味上成立した44件を偽陰性にした。次の版もADR09の非値状態を`missing`だけへ限定し、契約上同じ非値である`terminal_failure`または`unreadable`の4件を偽陰性にした。これらは診断履歴として保持する。

正本監査は、runtime sessionのproducer identity、rootへ配送されたsender、allowed result kind、構造化されたtool invocation/output対、case固有certificate事実、契約上の全non-value状態、rootのdependency消費、terminalおよびartifact境界を確認する。canonical locator、field順、英語見出しまたは再構成文字列との完全一致を真正性の代用にしていない。

## KPI境界

case別のall-agent token中央値はADR05 `181,170`、ADR07 `212,518.5`、ADR09 `172,353`、経過時間中央値は順に`116.469秒`、`131.254秒`、`128.231秒`だった。これはM6内の測定値であり、効率改善または悪化の判断には使わない。複雑性と効率の評価はM8で分離する。

## 一次証拠

- [登録result](d3b75f599f024ab8802595311920a00e.json)
- [品質・terminal監査](candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-audit-r1.json)
- [機序監査](candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-mechanism-audit-r1.json)
- [N=20 profile](../profiles/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-medium-m24-cli0146.json)
- [N=5 reference profile](../profiles/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-reference-n5-medium-m24-cli0146.json)
- [評価設計](../../docs/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-evaluation-design.md)
- [実行準備監査](../../docs/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-execution-preparation-audit.md)

## 状態

`M6_completed / existing_15_reused / new_45_valid / cumulative_60_score4 / current_result_admission_60_of_60 / mechanism_passed / prior_runtime_path_unobserved / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
