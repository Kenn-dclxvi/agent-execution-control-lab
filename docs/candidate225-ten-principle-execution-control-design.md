# Candidate225 10原則実行制御 Standard14 N=5試験設計

## 結論

Candidate225は、Candidate147のroot `AGENTS.md`にある一般実行制御を、利用者が指定した10節の自然文へ全置換する再構成Candidateとする。Candidate147以外のprompt fileは変更しない。Candidate214からCandidate224までのreview制御は継承しない。

初回評価は、利用者が指定したStandard14 14ケース×N=5だけに固定する。Candidate225の70 runだけを新規発行し、比較基準には同じ実効互換条件を持つ保存済みCandidate147 Standard14 resultを使う。

## 作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| 基準の最短正常経路 | 利用者が求める結果を固定し、必要な変更前証拠だけを取得し、一つの実装方針で変更し、固定した検証を完了して終了する |
| 保存済み問題経路 | FreeではA01 5 / 5件が未固定値を推測して変更へ進み、F08では方針確定に不要な変更前commandが残った。Candidate160ではrootによる担当判定のやり直しが1件あり、Candidate162の基準F03では具体的な検証実行票が最初のcommand前に0 / 5件だった |
| 再構成目的 | C147の機械的な13条項を、利用者指定の10節へ置換したときも、成果と手段、変更前調査、producerとterminal result、結果影響範囲、検証、権限拒否、環境回復の境界を一貫して維持できるかを測る |
| 既存authorityだけでは防げない理由 | Standard14のTaskSpecとpath-local authorityは対象固有の成果と方法を定めるが、未固定成果の推測、担当外再判定、consumerのない再調査、停止効果の過剰伝播、検証再入を全ケース共通には閉じない |
| 変更する範囲 | root `AGENTS.md`だけを利用者指定本文へ全置換する。その他18 targetはCandidate147と同一byteを保持する |
| 消す問題経路 | 未固定成果をrepositoryから推測する経路、実装方法だけを利用者へ質問する経路、同一判定の再生成、未完了結果の補完、consumerのない再調査、無関係な停止伝播、検証中の再探索、権限拒否の迂回、判定条件を変える環境回復 |
| 維持する正常経路 | 実装方法はrepository authorityから選び、独立確認はまとめ、担当結果はそのまま採用し、必要な検証だけを順に完了する。担当を使わない通常のroot実行も許可する |
| 新規判断と影響 | 10節の見出しと目的説明が増える。各節の個別因果効果はStandard14全体の結果から分離せず、C147より短いことだけを改善根拠にしない |

## 評価境界

- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- N: 各ケース5件、合計70 run。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Python 3.14.5、Codex CLI 0.146.0、all-agent token accounting v1。
- permission: `workspace-write / never`。
- configured M: 24。
- comparison: Candidate147の保存済み互換run。新しい比較baselineは発行しない。

## 判定と停止条件

品質は70 / 70 validかつrateable、全件Score 4を合格条件とする。KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`だけをCandidate147と比較する。個別節の機序成立、採用、releaseおよびTHE-CAPTION本体への反映は、このN=5結果だけでは決めない。

prompt identity以外の互換条件が一つでも不一致、preflight receiptが`ready`でない、発行対象が70件でない、validかつrateableなrunがケース別5件に達しない、または評価不能があれば結果登録を停止する。一件でもScore 4未満なら品質不通過として保存し、KPIの良否を採用根拠にしない。

## 現在状態

Standard14 N=5は70 / 70 validかつrateable、70 / 70 Score `4`で完了した。Candidate147比はall-agent token中央値`+112.61%`、elapsed中央値`+19.84%`で、cost改善は観測されなかった。利用者の追加指定による現在記録のCandidate163確認済み5文統合版との比較は、品質同値、token`+4.84%`、elapsed`-7.06%`でtradeoffとなった。個別節・文の機序、採用、releaseおよびprojectionは判断していない。

`standard14_n5_completed / quality_passed / c147_cost_increased / candidate163_tradeoff / adoption_not_decided / release_not_created / projection_not_performed`

[評価結果](../evaluations/results/candidate225-ten-principle-execution-control-standard14-n5_2026-08-14.md)を参照する。
