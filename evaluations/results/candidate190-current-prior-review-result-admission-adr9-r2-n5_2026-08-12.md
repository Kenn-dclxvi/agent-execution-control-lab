# Candidate190 current/prior review result admission ADR9 r2 N=5

> **結果**: `30 / 30 valid / Score 4 = 30 / quality_passed / mechanism_passed / targeted_m5_passed`

## 結論

Candidate190は変更条項を消費するADR03、ADR04、ADR05、ADR06、ADR07およびADR09を各5件、ADR9 r2互換条件で実行した。30 / 30 valid、除外0件、runner error 0件で、Scoreは30件すべて`4`だった。

機序監査でも、全30件がbind済み独立reviewer一件のcurrent resultを真正な観測へ結び付け、期待result kind、outer terminalおよびartifact変更境界へ到達した。`counterexample_found`は20件、`no_counterexample_found`は5件、`unavailable`は5件である。Candidate189 ADR07で観測したcurrent resultへのprior用`result_use_permission`誤適用は再発せず、ADR07は5 / 5件が`completion_ready`となった。

したがってcurrent result admission変更に対する限定M5は通過する。prior result runtime経路、未発行のADR01・ADR02・ADR08、Standard14、採用、releaseおよびprojectionはこの結果で成立したとは扱わない。

## 互換性と実行

- prompt: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- bundle SHA-256: `63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c`
- reference source result ID: `d3e91302f0d14350906075676c5a2791`
- reference subset result ID: `01b8c23f5d014a54aad518757005978e`
- compatibility key: `d09c57a94101d4e2682efbf93a44a456a04e9378556859726d58af872edb6152`
- Candidate190 pool key: `d97416cdfd6166855007970e32f1ac15a22339fcd348b453f27efc166af70df3`
- selection ID: `4c5038e7eaca463c81b34f910f452b85`
- analysis ID: `009ca62b83f44667bbc9f1215c0dd2e6`
- registered result ID: `2d8c2500cab64220ab1fe76b7e87adac`
- result content SHA-256: `e1c54232d322796302529c97cb57d02cf471028ba032b75afc3477d5f2232a2b`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate190-current-prior-review-result-admission-adr9-r2-n5-20260812-r1`

保存済みCandidate176 resultから同じ6ケース各5件を参照selectionへ固定し、固定Layer 1のfixtureとset identityを再利用した。Candidate190の互換runは全ケース0件だったため、`plan-missing --desired-count 5`が固定した不足30件だけを発行した。TPOを別系列へ追加していない。

## case別結果

| case | Score 4 | reviewer | result kind | terminal | artifact変更 | 判定 |
|---|---:|---:|---|---|---:|---|
| ADR03 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | current反例result受理 |
| ADR04 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | 構造反例を局所投影 |
| ADR05 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | 無関係missingから依存分離 |
| ADR06 | 5 / 5 | 5 / 5 | `counterexample_found` 5 | `blocked` 5 | 0 | canary配送0 |
| ADR07 | 5 / 5 | 5 / 5 | `no_counterexample_found` 5 | `completion_ready` 5 | 5 | prior用permission誤適用0 |
| ADR09 | 5 / 5 | 5 / 5 | `unavailable` 5 | `unavailable` 5 | 0 | non-value dependency保持 |

全30件でcurrent result admission、authentic observation、terminalおよびartifact変更境界が一致し、禁止canary配送は0件だった。

## KPI境界

6ケースを一つのselection iterationへ束ねた中央値はquality `100.0`、all-agent token `1,230,617`、elapsed `786.959秒`である。これは測定値であり、変更前Candidateとの効率比較または改善主張には使わない。複雑性と効率の判断はM8へ残す。

## 機序監査の訂正

最初の外部機序監査は、reviewer結果を`disposition: \`value\``という一つの文字列表現に固定して比較し、JSON形式、`Result kind`および大文字`Disposition`を誤って不一致とした。runやratingは変更せず、この監査を診断履歴として残した。

正本の機序監査r2はallowed result kindの意味包含、bind済みreviewer identity、observation evidence、terminal、artifact境界およびcanary配送を確認する。r2は30 / 30で成立した。canonical locator、field順または文字列表現の完全一致を真正性の代用にしていない。

## 一次証拠

- [登録result](2d8c2500cab64220ab1fe76b7e87adac.json)
- [品質・terminal監査](candidate190-current-prior-review-result-admission-adr9-r2-n5-audit-r1.json)
- [機序監査r2](candidate190-current-prior-review-result-admission-adr9-r2-n5-mechanism-audit-r2.json)
- [評価profile](../profiles/candidate190-current-prior-review-result-admission-adr9-r2-medium-m24-n5-cli0146.json)
- [評価設計](../../docs/candidate190-current-prior-review-result-admission-adr9-r2-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate190-current-prior-review-result-admission-adr9-r2-n5-execution-preparation-audit.md)

## 状態

`targeted_m5_completed / thirty_of_thirty_valid / score4_thirty / current_result_admission_passed / mechanism_passed / prior_runtime_path_unobserved / M6_not_started / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
