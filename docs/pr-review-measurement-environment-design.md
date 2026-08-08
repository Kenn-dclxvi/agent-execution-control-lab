# PRレビュー測定環境設計

## 位置付け

この文書は、GitHub上のAI PRレビューを高速化する前に、現行方式と代替方式を同一条件で比較するための**測定環境全体の設計**を記録する文書である。PRレビュー機能の成果条件は[`PRレビュー機能仕様 r1`](../evaluations/targets/agent-execution-control-lab/specifications/pr-review-function-r1.md)、現行workflowとCore経路の対応およびBaseline admission gateは[`Core Baseline設計 r1`](../evaluations/targets/agent-execution-control-lab/specifications/core-baseline-r1.md)を上位の正本とする。

2026-08-08の仕様監査で、既存case、oracle、rating contract、`agentic-retrieval`経路、r2 N=2がこの2文書より先に作られていたことを確認した。既存runはworkflow、schema、collector、graderの接続を示すdiagnostic evidenceとして保持し、正式Baseline qualificationまたはquality resultへ使用しない。PRR-C01/r3によるCore repetition 1も三回実行したが、すべて`execution_failed`となった。後続の実行互換監査でCore経路が現行workflowと異なる条件を複数含むことを確認したため、この三件も診断証拠としてだけ保持する。Core Baselineは未qualificationであり、Candidate A、残り5 case、N=5、Integrationは未実行である。

現在の自動レビューは`.github/workflows/claude-pr-review.yml`で`anthropics/claude-code-action@v1`を使用している。現行workflowは、PR差分・説明の取得、適用規則の確認、レビュー判断、inline comment、総括commentまでをClaude Codeの一つのagent operationとして実行する。

この設計の目的は、Anthropic純正Actionの良否を先に決めることではない。まず、現行方式のどこに時間を使っているかを分解し、レビュー品質を維持したまま削減可能な実行経路を特定する。

この作業はPRレビュー基盤の測定設計であり、prompt Candidate、既存evaluation result、release、本体projectionを変更しない。

## 結論

最初の比較は、モデル間比較ではなく、**同じClaudeを使った実行経路比較**とする。

- **Integration Baseline**: 現行の`anthropics/claude-code-action@v1`。Claude Code自身がPR情報取得、規則確認、レビュー判断、GitHubへの結果反映まで行う。
- **Core Baseline (`agentic-retrieval`)**: 固定したClaude Code Actionを使い、Claude自身がread-onlyのfixture toolからmetadata、diff、changed path、rules、対象ファイルを取得して判断する。GitHubへは投稿しない。
- **Candidate A**: GitHub Actions側でPR差分、PR metadata、changed path、適用規則を決定論的に収集し、Claudeにはレビュー判断を主に担当させる。

最初の研究質問は次とする。

> 同一レビュー対象・同一レビュー規則・同一モデル条件で、PR情報取得をClaude Codeのagent loopから決定論的な前処理へ移すことで、レビュー品質を維持したまま実行時間を削減できるか。

Codex reviewer、別モデル、直接API、self-hosted runner、自動修正はこの比較へ混ぜない。Candidate Aで実行経路差の効果を確認した後に、別の比較軸として追加する。

## 実装済みアーティファクト

実装の入口は[`evaluations/targets/agent-execution-control-lab/README.md`](../evaluations/targets/agent-execution-control-lab/README.md)とする。

| アーティファクト | 役割 | 現在状態 |
|---|---|---|
| `evaluations/targets/agent-execution-control-lab/contracts/pr-review-core-r1.json` | comparison、Action、model、quality gateのidentity | `pilot_probe_blocked` |
| `evaluations/targets/agent-execution-control-lab/specifications/pr-review-function-r1.md` | caseとratingより上位のPRレビュー成果条件 | r1固定 |
| `evaluations/targets/agent-execution-control-lab/specifications/core-baseline-r1.md` | 現行workflowとの対応とBaseline admission gate | r1固定・Baseline未qualification |
| `evaluations/targets/agent-execution-control-lab/prompts/baselines/claude-pr-review-core-r1` | source promptとCore Baseline prompt候補 | 固定済み・admission blocked |
| `evaluations/targets/agent-execution-control-lab/contracts/baseline-input-mapping-r1.json` | 現行workflowとCore入力の対応 | `unsatisfied` |
| `evaluations/targets/agent-execution-control-lab/prompts/baselines/claude-pr-review-core-r3` | authority packetとread-only repository snapshotへ接続したCore Baseline候補 | 入力対応成立・Baseline未qualification |
| `evaluations/targets/agent-execution-control-lab/contracts/baseline-input-mapping-r3.json` | 現行workflowとCore入力の最終対応receipt | `satisfied` |
| `evaluations/targets/agent-execution-control-lab/contracts/baseline-execution-parity-r1.json` | 現行workflowとCore候補の実行互換監査 | `unsatisfied`・Core追加実行をblock |
| `evaluations/targets/agent-execution-control-lab/contracts/baseline-repository-snapshot-r1.json` | 固定tree、fixture overlay、利用可能path集合のidentity | 固定済み |
| `evaluations/targets/agent-execution-control-lab/cases/PRR-C01/r3` | 新しい入力identityを持つheld-out fixture | 独立case設計監査通過・未実行 |
| `evaluations/targets/agent-execution-control-lab/contracts/prr-c01-r3-case-design-audit-r1.json` | 機能仕様からの導出と複数path finding identityの独立監査receipt | `satisfied` |
| `evaluations/targets/agent-execution-control-lab/contracts/baseline-repository-snapshot-prr-c01-r3-r1.json` | PRR-C01/r3固有のread-only snapshot identity | 固定済み・診断runで使用 |
| `evaluations/targets/agent-execution-control-lab/profiles/pr-review-agentic-retrieval-c01-r3-qualification-n2-r1.json` | Core機能確認の初回N=2条件 | 固定済み・履歴profile |
| `evaluations/targets/agent-execution-control-lab/contracts/pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json` | profileと全依存identity、2 slot、停止条件の機械照合 | 初回実行条件の履歴 |
| `evaluations/targets/agent-execution-control-lab/contracts/pr-review-core-r2.json` | 当時のprofile、rating、3 KPI identity | diagnostic履歴 |
| `evaluations/targets/agent-execution-control-lab/rating-contracts/pr-review-finding-quality-v1.json` | 当時のhard gateを0〜4の`quality_score`へ写像 | diagnostic履歴 |
| `evaluations/targets/agent-execution-control-lab/profiles/pr-review-agentic-retrieval-c01-qualification-n2-r1.json` | PRR-C01の独立2反復条件 | diagnostic履歴 |
| `evaluations/targets/agent-execution-control-lab/cases/PRR-C01/r1`〜`PRR-C06/r1` | model-visible入力とmodel-invisible oracle | 6件固定済み・未qualification |
| `evaluations/targets/agent-execution-control-lab/schemas/` | fixture、review output、run resultのschema | r1実装済み |
| `evaluations/targets/agent-execution-control-lab/tools/pr_review_measurement.py` | fixture検証、入力生成、許可field抽出、採点、集計 | 実装済み |
| `evaluations/targets/agent-execution-control-lab/tools/pr_review_fixture_tool.py` | Core Baseline用のread-only入力取得 | 実装済み |
| `evaluations/targets/agent-execution-control-lab/results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md` | 既存r2 N=2の現在解釈 | diagnosticへ再分類 |
| `.github/workflows/pr-review-measure-core.yml` | 手動起動のprepare / review / grade | 変換後Core経路の診断workflow・追加実行停止 |
| `tests/test_pr_review_measurement.py` | model-visible境界、hard gate、terminal status、workflow境界の回帰検証 | 実装済み |

Core Review workflowは、prepare jobだけでrepositoryをcheckoutし、reviewer jobへmodel-visible artifactと読み取り専用snapshotだけを渡す。reviewer jobには`.git`と`oracle.json`が存在しないことを開始前に検証する。grader jobはreviewer終了後に別checkoutを行い、sanitized review outputだけをoracleへ照合する。この構成は測定境界としては明確だが、実PRのgit worktreeとGitHub toolを使う現行workflowをそのまま再現していない。PRR-C01/r3の三回の結果と旧r2 workflowのrunはdiagnostic履歴のまま変更しない。

Core Baseline候補r3は、固定target treeへcaseの変更後本文をoverlayした`.git`なしread-only repository snapshotを使用する。materializerとtool policyはcase IDに依存せず、snapshot identityとmodel-visibleな利用可能path集合はcase固有receiptへ固定し、reviewerは限定fixture toolからだけ参照する。PRR-C01/r3ではcase設計の独立監査、case固有snapshot、fresh N=2 profile、当時のCore条件内でのpreflightまで成立した。repetition 1は三回とも失敗し、実行互換監査も`unsatisfied`である。repetition 2、Candidate A、後続測定は発行しない。

## Diagnostic N=2

PRR-C01の`agentic-retrieval`を独立2反復で実行し、2件ともmodel identityと3 KPIを取得した。当時のcontractによるscoreは`1 / 4`だった。ただし、PRR-C01のoracleが複数path findingの意味同一性を表現できず、Core経路もBaseline admissionを通過していない。このためscoreをBaseline性能へbindしない。数値の履歴は元の[`N=2要約`](../evaluations/targets/agent-execution-control-lab/results/pr-review-agentic-retrieval-c01-qualification-n2_2026-08-08.md)、現在解釈は[`diagnostic再分類receipt`](../evaluations/targets/agent-execution-control-lab/results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)を正本とする。

## 現在の観測値

現行workflowのGitHub Actions logで、少なくとも次を観測している。これらは測定環境完成後の正式Baseline resultではなく、測定設計の起点となる診断値である。

### 成功run

GitHub Actions run `31206301268`、job `92958106876`。

- job開始: 2026-08-07T18:18:09Z付近
- job終了: 2026-08-07T18:19:57Z付近
- 全体: 約109秒
- Claude Code result `duration_ms`: `80718`
- `num_turns`: `7`
- model: `claude-sonnet-5`
- Claude Code Action内部ではBun、依存package、OIDC/App token、Claude Code本体、project settings等の準備を行っている
- Claude Code v2.1.224のinstall開始から実行可能になるまで約13秒を観測した

### 失敗run

GitHub Actions run `31209804488`、job `92969634871`。

- job開始: 2026-08-07T19:04:00Z付近
- job終了: 2026-08-07T19:04:44Z付近
- 全体: 約44秒
- Claude Code result `duration_ms`: `15758`
- `num_turns`: `6`
- `permission_denials_count`: `1`
- Claude実行が約16秒で失敗しても、job全体は約44秒を要した

この2件から、現時点では次を仮説とする。

1. 成功runではagent loopが主要な時間要因である。
2. agent実行が短くても、GitHub RunnerとClaude Code Actionの初期化に無視できない固定費がある。
3. 総経過時間だけでは、Action初期化削減とagent loop削減を区別できない。

正式な結論は、この文書に基づく測定環境で再測定したresultだけから出す。

## 測定対象の分解

一つのPRレビューを次の区間へ分ける。

```text
PR event / workflow dispatch
        |
        v t0
GitHub queue
        |
        v t1
Setup
- runner preparation
- action / CLI preparation
- checkout
        |
        v t2
Input preparation
- PR diff
- PR metadata
- changed paths
- applicable repository instructions
        |
        v t3
Reviewer
- model / agent execution
- review judgment
        |
        v t4
GitHub reporting
- inline comment
- summary comment
        |
        v t5
complete
```

### 時間KPI

| key | 定義 | 主な意味 |
|---|---|---|
| `queue_ms` | `t1 - t0` | GitHub側の待ち時間。実装比較の主KPIにしない |
| `setup_ms` | `t2 - t1` | runner、checkout、Action、CLI等の初期化固定費 |
| `input_ms` | `t3 - t2` | diff、metadata、rules等の入力準備 |
| `review_ms` | `t4 - t3` | reviewerが判断を完了するまでの時間 |
| `report_ms` | `t5 - t4` | GitHubへ結果を反映する時間 |
| `execution_ms` | `t5 - t1` | workflow開始後の実行時間。速度比較の主KPI |
| `e2e_ms` | `t5 - t0` | dispatchから完了までの利用者体感 |

`queue_ms`はGitHub側の負荷やrunner割当の外乱を受けるため、Candidate採否の主KPIにはしない。`execution_ms`と`review_ms`を主に比較し、`e2e_ms`は運用上の参考値として保持する。

## 測定を二層へ分ける

レビュー判断の性能とGitHub連携の性能を混ぜない。

### 1. Core Review測定

```text
fixed fixture
    |
    v
reviewer
    |
    v
review result
```

GitHubへのinline commentやsummary commentを発行しない。測定対象は、入力準備、reviewer実行、finding結果とする。

目的:

- agent loopを減らした効果を直接測る
- GitHub API遅延をreviewer性能へ混ぜない
- 同じfixtureをBaselineとCandidate Aへ反復投入できるようにする

### 2. Integration測定

```text
fixture PR
    |
    v
reviewer
    |
    v
inline comment / summary comment
```

GitHubへの結果反映まで含める。

目的:

- 実運用の`execution_ms`と`e2e_ms`を確認する
- inline位置、comment生成、GitHub API処理の成立を確認する
- Core Review測定では見えないAction固有の固定費を測る

Core Reviewで品質gateを通過しないCandidateをIntegration測定へ進めない。

## 比較条件

BaselineとCandidate Aで、次を同一に固定する。

- 対象fixture revision
- base / head identity
- PR title / body相当入力
- changed files
- root `CLAUDE.md`
- changed pathへ適用される局所`AGENTS.md`
- レビュー観点
- findingの許容範囲
- model familyとmodel identity。固定できない場合はrun recordへ実測値を保存し、identityが異なるrunを同一比較へ混ぜない
- reviewerを起動するActionまたはCLIのrevision。Actionを使う場合は可変tagではなくcommit SHAへbindする
- 認証方式、GitHub permissions、sandbox
- workflow revisionとtimeout
- repetition数

最初の比較では次を変更しない。

- レビュー観点そのもの
- severity policy
- findingの期待値
- fixture内容
- model provider
- 自動修正処理
- re-review処理

一つの比較で複数軸を変更しない。

情報取得のtool policyだけは比較対象となる実行経路差である。Core Baselineはread-onlyのfixture tool、Candidate Aは準備済み入力のReadへ固定する。GitHub書込、任意のshell、追加情報取得は両variantで許可しない。

## fixture設計

Live PRだけを比較対象にしない。入力差を除くため、固定fixtureを用意する。

最小セットは6ケースとする。

| case | 主対象 | expected finding |
|---|---|---|
| `PRR-C01` | repository規律違反 | 1件 |
| `PRR-C02` | 評価アーティファクト整合違反 | 1件 |
| `PRR-C03` | secret・非公開log混入 | 1件 |
| `PRR-C04` | 文書品質違反 | 1件 |
| `PRR-C05` | 複数カテゴリの複数finding | 複数件 |
| `PRR-C06` | clean control | 0件 |

fixtureは、レビュー対象となる差分、PR metadata相当、適用規則、expected findingを同一revisionとしてbindできる構造にする。

### fixtureの要件

- expected findingはpath、対象行または対象範囲、カテゴリ、違反内容を機械比較できる形で持つ
- clean controlを必ず含める
- 一つのcaseへ不必要に複数の独立要因を入れない。ただし`PRR-C05`のみ複数findingの処理確認を目的として例外とする
- fixture生成時に秘密情報の実物を使わない。`PRR-C03`は明示的なダミー値を使う
- fixture revisionを変えた場合、旧resultと同一比較へ混ぜない

## 品質gate

速度改善は品質gate通過後にだけ評価する。

最初のgateは複雑な総合scoreではなく、次のhard gateとする。

```text
required finding miss = 0
clean control major false positive = 0
review contract violation = 0
```

### 保存する品質指標

| key | 意味 |
|---|---|
| `expected_findings` | fixtureが要求するfinding数 |
| `true_positive` | expected findingと対応したfinding数 |
| `false_negative` | 見落としたexpected finding数 |
| `false_positive` | expected findingに対応しない指摘数 |
| `path_accuracy` | 対象path一致 |
| `line_accuracy` | inline位置または対象範囲の妥当性 |
| `category_accuracy` | 規律カテゴリ一致 |
| `scope_violation_count` | 好みの相違、対象外改善など契約外指摘数 |
| `summary_complete` | 必須観点の総括が揃っているか |

findingの文言完全一致は要求しない。fixture側で意味上同一と判定できるexpected finding identityを定義し、そのidentityへbindできるかで判定する。

## 1 runのSSOT

runごとの一次記録はJSONとする。Markdown summaryはJSONを入力に生成し、JSONと競合する現在値を手書きで複製しない。

現行r2 schemaの要点:

```json
{
  "schema_version": 2,
  "comparison_revision": "pr-review-core-r2",
  "profile_id": "pr-review-agentic-retrieval-c01-qualification-n2-r1",
  "quality_rating_contract": "pr-review-finding-quality-v1",
  "result_id": "pr-review-core-r2:PRR-C01:agentic-retrieval:r1:a123456",
  "case_id": "PRR-C01",
  "fixture_revision": "r1",
  "variant": "agentic-retrieval",
  "repetition": 1,
  "attempt": 123456,
  "base_sha": "...",
  "head_sha": "...",
  "model": {
    "requested": "claude-sonnet-5",
    "reported": "claude-sonnet-5"
  },
  "workflow_revision": "pr-review-measure-core-r2",
  "github_run_id": "123456",
  "reviewer_executor": {
    "type": "github_action",
    "identity": "anthropics/claude-code-action",
    "revision": "6b082c41935b4c8a3b8b0ef85ba4ba4d9eeb8975",
    "claude_authentication": "claude_code_oauth_token",
    "github_authentication": "job_scoped_github_token",
    "permission_profile": "review-read-only-r1",
    "sandbox": "claude-code-action-default",
    "tool_policies": {
      "agentic-retrieval": "fixture-tool-read-only-r1",
      "deterministic-input": "prepared-input-read-only-r1"
    },
    "timeout_seconds": 900
  },
  "timing": {
    "queue_ms": null,
    "setup_ms": null,
    "input_ms": 0,
    "action_step_ms": 0,
    "review_ms": 0,
    "report_ms": null,
    "execution_ms": 0,
    "e2e_ms": null
  },
  "runtime": {
    "turns": null,
    "input_tokens": null,
    "output_tokens": null,
    "total_tokens": null,
    "reported_cost_usd": null
  },
  "quality": {
    "observed": true,
    "expected_findings": 1,
    "true_positive": 1,
    "false_positive": 0,
    "false_negative": 0,
    "path_accuracy": 1,
    "line_accuracy": 1,
    "category_accuracy": 1,
    "clean_control_major_false_positive": 0,
    "scope_violation_count": 0,
    "review_contract_violation": 0,
    "summary_complete": true
  },
  "quality_score": 4,
  "result": "pass"
}
```

### 記録上の規則

- 取得できない値を推定しない。`null`を許容する
- `turns`、token、costはproviderまたはActionが安定して一次値を出す場合だけ保存する
- model identityを必ず保存する
- workflow、ActionまたはCLI、認証、permission、sandbox、tool policy、timeoutのidentityを保存する
- GitHub run ID、job ID、開始・終了timestampもdiagnostic fieldとして保存する
- エラーrunを速度比較の成功runへ混ぜない。ただし固定費分析のdiagnostic resultとして保持する
- retryしたrunは同じrepetitionへ上書きせず別attempt identityを持つ
- `pass`、`quality_failed`、`invalid_output`、`execution_failed`、`timeout`、`cancelled`、`measurement_incomplete`を別statusとして保存する

## 反復と実行順

初期比較は各case `N=5`とする。

同一variantをまとめて実行せず、可能な範囲でBaselineとCandidate Aを交互に実行する。

例:

```text
A1 -> B1
B2 -> A2
A3 -> B3
B4 -> A4
A5 -> B5
```

目的は、時間帯、provider負荷、GitHub runner状態などの系統的な時間差を一方のvariantへ偏らせないことである。

### 集計

主集計:

- `median(execution_ms)`
- `median(review_ms)`
- `median(e2e_ms)`

補助集計:

- 最小 / 最大
- p25 / p75。Nが小さいpilotでは参考値として扱う
- 成功率
- finding recall / false positive件数

平均値だけで採否を決めない。

## Baselineの扱い

Baselineの機能、対応関係、admission gateは[`Core Baseline設計 r1`](../evaluations/targets/agent-execution-control-lab/specifications/core-baseline-r1.md)を正本とする。以下は測定環境全体がBaselineを変更しないための補助規則である。

現行`.github/workflows/claude-pr-review.yml`は、削除や内部最適化を先に行わない。Baseline identityを保持する。固定fixtureの入力対応だけではこのidentityを再現したことにならないため、trigger、workspace、Action revision、reported model、turn挙動、tool、出力方法、permissionも別の実行互換receiptで確認する。

測定準備では次を守る。

1. 現行workflowの自動起動を停止する場合、review promptとAction構成を同じ変更で最適化しない。
2. Baseline測定用に手動起動経路が必要なら、現行構成を意味変更せず再現する専用workflowまたは固定revisionを作る。
3. Candidate Aの実装とBaselineの再定義を同じ比較単位へ混ぜない。
4. 過去のrun `31206301268`等はdiagnostic evidenceとして保持するが、正式なN=5 Baseline resultの代替にはしない。

## Candidate Aの責務境界

Candidate Aでは、情報収集をモデル判断からできるだけ分離する。

### GitHub Actions側

決定論的に次を準備する。

- PR diff
- PR title / body
- base / head SHA
- changed path一覧
- root `CLAUDE.md`
- changed pathへ適用される局所`AGENTS.md`
- 必要なら対象ファイル本文の限定範囲

GitHub Actions側でレビュー判断を行わない。

### Reviewer側

入力済み情報を基に次だけを行う。

- 規則への適合判定
- finding生成
- finding category / path / lineの決定
- summary生成

Candidate Aの初期版では、Reviewer自身に追加の`gh pr diff`や`gh pr view`を要求しない。入力不足が観測された場合は、追加toolを無条件に許可するのではなく、不足した入力identityをresultへ記録してfixture / input preparation側を見直す。

## 公式リポジトリのworkflow調査

2026-08-08に、次の公式リポジトリを固定commitで確認した。

- OpenAI Codex: [`openai/codex@3aae5d8`](https://github.com/openai/codex/tree/3aae5d885bac39c1262491aa3fd100dfd8b3919f)
- Claude Code: [`anthropics/claude-code@2bb6069`](https://github.com/anthropics/claude-code/tree/2bb60696142b493eafaeacfe00eac51d16c50c4f)

これらは実運用workflowの構造を確認する参考実装である。fixture固定、同条件反復、quality gateを備えた比較試験ではないため、速度、品質、採用可否のエビデンスとして扱わない。

### OpenAI Codexリポジトリ

Codexリポジトリでは、PR時の短い検証と`main`反映後の重い検証を分けている。PRではBazel中心の主要検証と小さいCargo検証を行い、完全なクロスプラットフォーム検証はpost-mergeへ分離している。この方針は[workflow方針](https://github.com/openai/codex/blob/3aae5d885bac39c1262491aa3fd100dfd8b3919f/.github/workflows/README.md)に明示されている。

Codex Actionを使うissue automationでは、次の構造が確認できる。

1. GitHub Actions側がissue等の入力をJSONへ決定論的に準備する。
2. `openai/codex-action`をcommit SHAで固定し、`sandbox: read-only`と限定permissionsで判断を実行する。
3. `output-schema`で構造化結果を取得する。
4. 後続jobがJSONを検証・正規化してからGitHubへの変更を行う。

具体例は[Issue Translator](https://github.com/openai/codex/blob/3aae5d885bac39c1262491aa3fd100dfd8b3919f/.github/workflows/issue-translator.yml)と[Issue Deduplicator](https://github.com/openai/codex/blob/3aae5d885bac39c1262491aa3fd100dfd8b3919f/.github/workflows/issue-deduplicator.yml)である。前者はmodel入力をuntrusted contentとして明示し、reviewer相当のjobとGitHub反映jobをpermissionsごと分けている。後者は空結果時の代替経路を別jobにし、各model出力を正規化してから次段へ渡している。

また、`.github/codex/labels/`では、汎用PRレビューとRust固有レビューを別promptとして管理し、event JSONに含まれるbase / head refsを利用する。[codex-review.md](https://github.com/openai/codex/blob/3aae5d885bac39c1262491aa3fd100dfd8b3919f/.github/codex/labels/codex-review.md)と[codex-rust-review.md](https://github.com/openai/codex/blob/3aae5d885bac39c1262491aa3fd100dfd8b3919f/.github/codex/labels/codex-rust-review.md)から、共通レビュー契約と領域固有規則を分離する構造を確認できる。ただし、このlabel経路は本設計のBaselineまたはCandidate Aではなく、後続の別方式候補である。

### Claude Codeリポジトリ

Claude Codeリポジトリの一般的な[Claude Code workflow](https://github.com/anthropics/claude-code/blob/2bb60696142b493eafaeacfe00eac51d16c50c4f/.github/workflows/claude.yml)は、全PRへの自動レビューではない。issue comment、review comment、review本文等に`@claude`が含まれる場合だけ起動し、repository checkout、read-onlyのGitHub permissions、OIDC、明示modelでClaude Code Actionを実行する。

自動issue triageでは、[issue単位のconcurrencyとtimeout](https://github.com/anthropics/claude-code/blob/2bb60696142b493eafaeacfe00eac51d16c50c4f/.github/workflows/claude-issue-triage.yml)を設定し、書込可能な補助scriptの呼出回数を`CLAUDE_CODE_SCRIPT_CAPS`で制限している。duplicate処理も[専用workflow](https://github.com/anthropics/claude-code/blob/2bb60696142b493eafaeacfe00eac51d16c50c4f/.github/workflows/claude-dedupe-issues.yml)へ分離されている。

さらに、`.github/`配下のworkflow変更で`allowed_non_write_users`が追加された場合に警告commentを出す[セキュリティ検査](https://github.com/anthropics/claude-code/blob/2bb60696142b493eafaeacfe00eac51d16c50c4f/.github/workflows/non-write-users-check.yml)がある。これは、外部入力を受けるagent workflowではtrigger許可とrepository書込権限を独立したリスクとして扱う必要があることを示す。

### 本設計への反映

公式リポジトリの構造から、次を本測定環境へ採用する。

1. **入力準備、reviewer、結果正規化、GitHub反映を別stepまたは別jobにする。** ReviewerへGitHub書込権限を与えず、Integrationのreporterだけに必要最小限の権限を付与する。
2. **Reviewer出力をschemaで固定する。** finding、category、path、line、summaryをJSONで受け、schema不適合をreview失敗と区別した`invalid_output`として保存する。
3. **外部入力を命令として扱わない。** PR title、body、diff、comment、対象ファイル本文をuntrusted review inputとしてreview contractと分離する。
4. **Action identityを固定する。** 本番workflowの可変`@v1`をそのまま比較identityにせず、測定時に解決したcommit SHA、model identity、workflow revisionをrun recordへ保存する。
5. **権限と認証を比較条件へ入れる。** GitHub permissions、OIDCまたはOAuth、sandboxが異なるrunを同一comparison revisionへ混ぜない。tool policyはvariantごとの固定値とし、同じvariant内で異なるrunを混ぜない。
6. **Core Reviewを短い経路、Integrationを重い経路として分離する。** N=5を通常PRの待ち時間へ載せず、手動dispatchの測定経路で実行する。通常PRへの導入判断は固定result完成後の別operationとする。
7. **timeoutと重複起動を明示的に扱う。** case / variant / repetition / attemptを一意にし、同一identityの重複runを防ぐ。通常運用のstale run取消をそのまま測定へ適用せず、timeoutまたは取消runは成功runと分けて保存する。
8. **領域固有規則は入力カプセルとして合成する。** Codexリポジトリの領域別review promptは参考にするが、本比較中にvariant別promptを作らない。root規則、changed pathへ適用される局所規則、共通review contractを同じ決定論的処理で両variantへ供給する。

採用しないものは次である。

- CodexとClaudeのモデル間比較をCandidate Aへ混ぜること
- labelまたは`@mention`起動をN=5測定のidentityとして使うこと
- modelへGitHub書込を許可したままCore Reviewを測ること
- 本番workflowのcancel動作を測定runへ無条件に流用すること
- 公式リポジトリで使われているという理由だけでqualityまたは速度を成立済みとみなすこと

## Phase 0で固定した実装条件

実装開始に必要な条件は次へbindした。

1. Core BaselineとCandidate Aは同じ`anthropics/claude-code-action` commit `6b082c41935b4c8a3b8b0ef85ba4ba4d9eeb8975`を使う。
2. Core Baselineは固定fixture toolから情報を取得し、Candidate Aは完成済み`review-input.json`を読む。review contract、fixture、model、出力schemaは共通とする。
3. Reviewer出力はActionの`structured_output`を受け、schema適合済みfieldだけを次jobへ渡す。Actionの生出力はartifactへ保存しない。
4. `execution_file`はSDKの最終`result`から`duration_ms`、`num_turns`、`total_cost_usd`、`usage`を取得し、`system/init`からmodel identityを取得する。`input_tokens`は`usage.input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens`の合計とする。message、tool出力、環境値は保存しない。
5. model-invisible oracleはreviewerと別jobへ置き、reviewer workspaceに`.git`、`oracle.json`を含めない。
6. reviewer jobはjob-scoped `github.token`とread-only permissionsを使い、GitHub投稿処理を持たない。Claude API認証は両variantとも`CLAUDE_CODE_OAUTH_TOKEN`へ固定する。
7. `attempt`はGitHub run IDへbindし、同じrepetitionのretryを別identityとして保持する。
8. Action stepは12分、reviewer jobは15分を上限とし、schema不適合、実行失敗、取消、計測不完全を成功runと分ける。

## pilot probeの観測結果

PRR-C01の両variantを使い、Phase 4へ進む前のprobeを実施した。

1. 固定Action commitで`structured_output`が6 fixtureすべてについてschema適合するか。
2. `execution_file`からmodel identity、`duration_ms`、`num_turns`を安定して取得できるか。取得できない値は`null`のまま保持する。
3. Action step境界の`execution_ms`とAction内部の`review_ms`をvariant間で同じ定義として取得できるか。
4. Core Baselineのfixture tool経路が、現行の`gh pr diff` / `gh pr view`経路を比較するための診断経路として十分か。不足する入力identityがあればcomparison revisionを変える。
5. model identityが要求値と実測値で一致するか。一致しない場合、または実測不能の場合は比較を停止する。
6. inline `line_accuracy`の許容範囲とIntegrationのtimestamp取得点。これはCore Review gate通過後に固定する。

1〜5はPRR-C01で観測できた。JSON Schema draft宣言はClaude Code CLIへそのまま渡せなかったため、schema正本を変えずAction入力から宣言だけを除外した。runtimeはSDK最終`result`を基準に取得し、model identity、`duration_ms`、`num_turns`、cost、cache込みtokenを抽出できた。

最終attemptでは`agentic-retrieval`がrequired findingをoracleと同じpath identityで返して`pass`した。一方、`deterministic-input`は同じ`prompt_evaluation_separation`違反をprompt側pathで指摘し、oracleが固定した評価profile側pathとは一致しなかった。加えて評価profile側には`state_separation`を返したため、grader上はrequired findingの`false_negative=1`となり`quality_failed`である。意味的に近い指摘を同一findingとするかは、現在のoracleを事後変更せず、新しいcomparison revisionの要否として判断する。

6はCore Review gate未通過のため未観測のまま保持する。未観測値を推定で補完しない。

## 実装段階

| Phase | 内容 | 完了条件 | 現在状態 |
|---|---|---|---|
| 0 | PRレビュー機能仕様 | caseとratingより上位の成果条件が固定される | r1固定 |
| 1 | Baseline設計 | 現行workflowとの対応とadmission gateが固定される | r1固定・admission未実施 |
| 2 | fixtureとrating qualification | 仕様から導出したcase、oracle、rating contractが独立監査を通過する | PRR-C01/r3とquality contract v3の独立監査通過 |
| 3 | Baseline admission | 入力対応、実行互換、prompt identity、実効条件、機能反復gateが成立する | 入力対応は成立。実行互換は`unsatisfied`。repetition 1の三回は失敗し、追加実行停止 |
| 4 | Candidate A pilot | qualification済みLayer 1でBaselineとCandidate Aの接続を確認する | 未実行 |
| 5 | N=5 | 全caseを交互順序でN=5実行する | 未実行 |
| 6 | 比較result | quality gate通過可否と時間KPI中央値を固定resultとして保存する | 未実行 |
| 7 | Integration | Core Reviewで採用候補となったCandidateだけGitHub commentまで含めて測る | 未実装・未実行 |

## 停止条件

次の場合は、速度優位が見えていてもCandidate採用判断を停止する。

- required findingを1件でもmissした
- clean controlで重大なfalse positiveが出た
- BaselineとCandidateでmodel identityが比較不能な形で変わった
- fixture revisionが途中で変わった
- timing区間の定義がvariant間で一致していない
- reviewer以外の処理がレビュー判断へ介入し、比較軸が複数変わった
- run resultの一次JSONを再現できない

停止後は、失敗resultを削除せず原因を分類し、条件を変える場合は新しいcomparison revisionとして扱う。

## この段階で実装しないもの

- Claude findingからのCodex自動修正
- reviewer / fixer / re-reviewerのproducer分離
- ClaudeとCodexの異種モデル比較
- Codex reviewerへの置換
- merge gate
- self-hosted runner
- GitHub App / PATへの認証再設計
- model cost最適化

これらはレビュー測定環境が成立し、Candidate Aのquality / timing resultが得られた後の別作業とする。

## 再開条件

1. 対象となる実PRとGitHub commentの書込みを明示的に許可した場合だけ、現行workflowを変更しないsource control runを実行する。
2. source control runからAction revision、reported model、turn挙動、tool到達性を固定する。
3. 現行workflowからCoreへ変える条件を一項目ずつ新しいrevisionへ分け、各段階でterminal resultと実行互換を確認する。
4. 実行互換receiptが`satisfied`になった後に、新しいprofileとpreflightでCore Baseline qualificationを計画する。
5. Core repetition 1がscore `4`、model一致、計測完全を満たした場合だけrepetition 2を発行する。
6. 2件とも個別pass条件を満たした場合だけCore Baseline機能qualificationを成立させる。

停止中はN=5、Integration、レビュー方式の置換、自動修正の再接続、既存evaluation resultの変更まで広げない。
