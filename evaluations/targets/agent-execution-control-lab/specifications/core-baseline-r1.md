# Core Baseline設計 r1

## 結論

現行の`agentic-retrieval`経路は、Core Review測定の診断prototypeであり、現行Claude PRレビューのBaselineとして未qualificationである。Baselineを名乗るには、PRレビュー機能仕様への適合と、現行workflowからCore経路への意味保存を別々に証明する。

## 比較元

比較元は、ターゲットref `8cd97283e60f13393fb1302c601c9a4fe0a5381f`にある`.github/workflows/claude-pr-review.yml`のClaude PRレビューoperationである。このworkflow全体をIntegration Baseline候補とする。

現行workflowの過去runは実行経路の診断証拠であり、固定fixtureによる正式Baseline resultではない。

## Core経路へ残す責務

Core Baseline候補は次を保持する。

- 同じClaude Code Action familyと固定commit
- 同じmodel identity
- 同じレビュー機能仕様
- PR metadata、diff、changed path、適用規則、対象本文をreviewer自身がtoolで取得するagentic retrieval
- repository writeを伴わないレビュー判断
- findingとsummaryの生成

Core測定から次を除外する。

- PR eventとqueue
- 実PRのcheckoutおよびGitHub API遅延
- inline commentとsummary commentの投稿
- GitHub上の再レビュー、修正、merge gate

除外した処理の性能はIntegration測定で扱う。Core resultからIntegration全体の速度を推定しない。

## 現行workflowとの対応

| 現行workflowの責務 | Core Baseline候補 | admission evidence |
| --- | --- | --- |
| PR title / body取得 | `fixture-tool metadata` | 同一fixtureから同じ論理値を返すreceipt |
| changed path取得 | `fixture-tool changed-paths` | path集合と順序規則のreceipt |
| PR diff取得 | `fixture-tool diff` | 改行を含む論理diff identityのreceipt |
| repository規則確認 | `fixture-tool rules` | rootと局所規則の選択・優先順位receipt |
| 対象ファイル参照 | `fixture-tool files` | reviewerが到達できるpathと内容のreceipt |
| レビュー判断 | Claude Code Action | Action、model、prompt、tool policyのidentity |
| GitHub投稿 | Coreでは除外 | Integration Baselineで別測定 |

値が同じであることだけでなく、reviewerが利用できる情報と禁止入力が同じ意味を持つことを確認する。

## prompt identity

Baseline promptは独立したimmutable artifactとして固定し、content SHA-256をprofileへbindする。workflow内の可変なinline文字列や「現行構成と同じ」という説明だけをprompt identityにしない。

Core用の追加指示は、固定fixture toolの使用方法とGitHub書込禁止に限定する。レビュー観点、finding条件、severityをCore専用に変更しない。現行workflowとの差分は対応表へ全件記録する。

既存`.github/workflows/pr-review-measure-core.yml`のinline promptは独立したprompt artifactへbindされていないため、正式Baseline identityとして不足している。

## Baseline admission gate

次の順で全件を満たした場合だけ、Core経路をBaselineとしてprofileへ登録する。

1. [`pr-review-function-r1.md`](pr-review-function-r1.md)に適合するreview contract revisionがある。
2. case設計監査を通過したEvaluation set revisionがある。
3. expected findingが機能仕様から導出され、意味同一性をgraderが扱える。
4. 現行workflowとCore経路の入力対応receiptが全項目で成立する。
5. Action、model、prompt、tool policy、permission、sandbox、timeoutを固定する。
6. prompt identity以外を含む全comparison conditionsをprofileへ固定する。
7. 機能qualificationの反復数、個別pass条件、停止条件を実行前に固定する。

このgateは速度測定前に行う。gate用runで速度差やCandidate採否を判断しない。

## Candidate Aとの比較開始条件

Core Baseline admission後に、同じ機能仕様、Evaluation set、model、Action、出力schema、rating contractをCandidate Aへ複製する。変更軸は情報取得経路だけに限定する。

BaselineとCandidate Aの各runを発行する前にpreflight receiptを保存し、prompt identityとtool policy以外の実効互換条件を機械照合する。Baselineが未qualificationの間はCandidate A、残りcase、N=5、Integrationを発行しない。

## 既存runの扱い

`pr-review-core-r1`と`pr-review-core-r2`で実行したrunは、workflow、schema、collector、graderの接続を確認したdiagnostic evidenceとして保持する。次の理由によりBaseline quality resultへ使わない。

- PRレビュー機能仕様より先にcaseとoracleを作った。
- `PRR-C01/r1`が複数path findingの意味同一性を表現できない。
- Core promptの独立identityがない。
- 現行workflowとfixture toolの入力対応receiptがない。

既存runを新仕様で再採点しない。条件を満たした新しいcase、contract、profile revisionによる将来runだけを正式result候補とする。
