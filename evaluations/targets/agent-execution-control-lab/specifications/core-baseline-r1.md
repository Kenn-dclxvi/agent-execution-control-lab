# Core Baseline設計 r1

## 結論

現行の`agentic-retrieval`経路は、Core Review測定の診断prototypeであり、現行Claude PRレビューのBaselineとして未qualificationである。Baselineを名乗るには、PRレビュー機能仕様への適合、入力値の対応、実行条件の互換性を別々に証明する。

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

`claude-pr-review-core-r1`を[`prompt artifact`](../prompts/baselines/claude-pr-review-core-r1/README.md)として作成した。固定target refのsource promptと、レビュー観点を意味保存したCore prompt候補を分離して保持する。現在の入力対応判定は[`baseline-input-mapping-r1`](../contracts/baseline-input-mapping-r1.json)を正本とし、局所規則とrepository readの対応が未成立のためadmissionを開放しない。

局所規則の選択は[`baseline-authority-selection-r1`](../contracts/baseline-authority-selection-r1.json)で、root `CLAUDE.md`のsymlink解決、changed path祖先の`AGENTS.md`探索、浅い順の適用、content identityまで固定した。ただしauthority原文をmodel-visible packetへ接続していないため、入力対応は部分成立に留める。

`claude-pr-review-core-r2`では、選択receiptを固定treeへ再照合してauthority原文packetを生成し、Candidate Aの直接Readとagentic fixture toolの`rules`へ同じJSONを渡す。これによりauthority入力は成立した。現在の対応判定は[`baseline-input-mapping-r2`](../contracts/baseline-input-mapping-r2.json)を正本とし、残るblockは差分外repository read範囲である。

`claude-pr-review-core-r3`では、固定target treeへschema v2 caseの変更後本文をoverlayし、`.git`を含まないread-only repository snapshotを生成する。agentic reviewerは`list-files`と`file PATH`だけでsnapshotを参照し、repository外path、`.git`、書込へ到達できない。materializerとtool policyはcase IDに依存せず、各caseのsnapshot tree、fixture、利用可能path集合、aggregate content identityをcase固有receiptへ固定する。入力対応の代表receiptは[`baseline-repository-snapshot-r1`](../contracts/baseline-repository-snapshot-r1.json)へ`PRR-C01/r2`で固定した。これにより[`baseline-input-mapping-r3`](../contracts/baseline-input-mapping-r3.json)のsource-to-Core入力対応は成立した。

入力対応の成立はBaseline qualificationではない。case設計が機能仕様から独立にqualificationされ、現行workflowとの実行互換監査を通過し、Action、model、tool policy、permission等をprofileへ固定したpreflightを通過するまでevaluation slotを発行しない。

## 実行互換監査

[`baseline-execution-parity-r1`](../contracts/baseline-execution-parity-r1.json)で、固定target commitの現行workflowと、三回目のCore実行条件を比較した。レビュー観点とmodel-visibleな論理入力値は対応している。一方で、PR eventの有無、git worktreeの有無、Action revision、modelの固定方法、turn上限、利用可能tool、出力契約、GitHubへの書込み条件が一致しない。このため監査状態は`unsatisfied`であり、現在のCore経路は元workflowをそのまま移したBaselineではない。

PRR-C01/r3の三回の実行結果は、変換後のCore経路で発生した問題を示す診断証拠として保持する。これらを現行workflowの機能または性能を測ったBaseline resultとして扱わない。

## Baseline admission gate

次の順で全件を満たした場合だけ、Core経路をBaselineとしてprofileへ登録する。

1. [`pr-review-function-r1.md`](pr-review-function-r1.md)に適合するreview contract revisionがある。
2. case設計監査を通過したEvaluation set revisionがある。
3. expected findingが機能仕様から導出され、意味同一性をgraderが扱える。
4. 現行workflowとCore経路の入力対応receiptが全項目で成立する。
5. 現行workflowを変更しない対照実行で、Action revision、reported model、turn挙動、tool到達性を観測する。
6. 現行workflowからCore経路へ変える条件を一項目ずつ分離し、実行互換receiptを成立させる。
7. Action、model、prompt、tool policy、permission、sandbox、timeoutを固定する。
8. prompt identity以外を含む全comparison conditionsをprofileへ固定する。
9. 機能qualificationの反復数、個別pass条件、停止条件を実行前に固定する。

このgateは速度測定前に行う。gate用runで速度差やCandidate採否を判断しない。

## Candidate Aとの比較開始条件

Core Baseline admission後に、同じ機能仕様、Evaluation set、model、Action、出力schema、rating contractをCandidate Aへ複製する。変更軸は情報取得経路だけに限定する。

BaselineとCandidate Aの各runを発行する前にpreflight receiptを保存し、prompt identityとtool policy以外の実効互換条件を機械照合する。実行互換監査が`unsatisfied`である現在はCore Baselineの追加runを発行しない。Baselineが未qualificationの間はCandidate A、残りcase、N=5、Integrationも発行しない。

## 既存runの扱い

`pr-review-core-r1`と`pr-review-core-r2`で実行したrunは、workflow、schema、collector、graderの接続を確認したdiagnostic evidenceとして保持する。次の理由によりBaseline quality resultへ使わない。

- PRレビュー機能仕様より先にcaseとoracleを作った。
- `PRR-C01/r1`が複数path findingの意味同一性を表現できない。
- Core promptの独立identityがない。
- 現行workflowとfixture toolの入力対応receiptがない。

既存runを新仕様で再採点しない。条件を満たした新しいcase、contract、profile revisionによる将来runだけを正式result候補とする。
