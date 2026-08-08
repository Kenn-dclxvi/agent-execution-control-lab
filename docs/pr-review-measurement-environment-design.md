# PRレビュー測定環境設計

## 位置付け

この文書は、GitHub上のAI PRレビューを高速化する前に、現行方式と代替方式を同一条件で比較するための**測定環境設計**を固定する引き継ぎ文書である。2026-08-08時点で、ここに記載する代替レビューworkflow、fixture、collector、比較resultは未実装・未評価である。

現在の自動レビューは`.github/workflows/claude-pr-review.yml`で`anthropics/claude-code-action@v1`を使用している。現行workflowは、PR差分・説明の取得、適用規則の確認、レビュー判断、inline comment、総括commentまでをClaude Codeの一つのagent operationとして実行する。

この設計の目的は、Anthropic純正Actionの良否を先に決めることではない。まず、現行方式のどこに時間を使っているかを分解し、レビュー品質を維持したまま削減可能な実行経路を特定する。

この作業はPRレビュー基盤の測定設計であり、prompt Candidate、既存evaluation result、release、本体projectionを変更しない。

## 結論

最初の比較は、モデル間比較ではなく、**同じClaudeを使った実行経路比較**とする。

- **Baseline**: 現行の`anthropics/claude-code-action@v1`。Claude Code自身がPR情報取得、規則確認、レビュー判断、GitHubへの結果反映まで行う。
- **Candidate A**: GitHub Actions側でPR差分、PR metadata、changed path、適用規則を決定論的に収集し、Claudeにはレビュー判断を主に担当させる。

最初の研究質問は次とする。

> 同一レビュー対象・同一レビュー規則・同一モデル条件で、PR情報取得をClaude Codeのagent loopから決定論的な前処理へ移すことで、レビュー品質を維持したまま実行時間を削減できるか。

Codex reviewer、別モデル、直接API、self-hosted runner、自動修正はこの比較へ混ぜない。Candidate Aで実行経路差の効果を確認した後に、別の比較軸として追加する。

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

初期schema案:

```json
{
  "schema_version": 1,
  "case_id": "PRR-C01",
  "fixture_revision": "r1",
  "variant": "anthropic-action",
  "repetition": 1,
  "base_sha": "...",
  "head_sha": "...",
  "model": "claude-sonnet-5",
  "timing": {
    "queue_ms": 0,
    "setup_ms": 0,
    "input_ms": 0,
    "review_ms": 0,
    "report_ms": 0,
    "execution_ms": 0,
    "e2e_ms": 0
  },
  "runtime": {
    "turns": null,
    "input_tokens": null,
    "output_tokens": null,
    "reported_cost_usd": null
  },
  "quality": {
    "expected_findings": 1,
    "true_positive": 1,
    "false_positive": 0,
    "false_negative": 0,
    "scope_violation_count": 0
  },
  "result": "pass"
}
```

### 記録上の規則

- 取得できない値を推定しない。`null`を許容する
- `turns`、token、costはproviderまたはActionが安定して一次値を出す場合だけ保存する
- model identityを必ず保存する
- GitHub run ID、job ID、開始・終了timestampもdiagnostic fieldとして保存する
- エラーrunを速度比較の成功runへ混ぜない。ただし固定費分析のdiagnostic resultとして保持する
- retryしたrunは同じrepetitionへ上書きせず別attempt identityを持つ

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

現行`.github/workflows/claude-pr-review.yml`は、削除や内部最適化を先に行わない。Baseline identityを保持する。

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

## 未確定事項

以下はこの文書では確定しない。Phase 0でrepository authorityと実測から決める。

1. Core Review Baselineを`anthropics/claude-code-action@v1`のままGitHub投稿なしで成立させる方法。高レベルActionの出力制約により難しい場合、BaselineはIntegration測定だけに残し、Core Reviewは別の同等条件を定義する必要がある。
2. Candidate AでClaudeを呼ぶ実行方式。Claude Code Actionの低レベル構成、Claude Code CLI、APIのどれを使うかは、model identityと入力条件をBaselineへどこまで合わせられるかで決める。
3. timestamp取得点。GitHub Actions step境界、Action内部event、provider result timestampのどれを各`t0`〜`t5`へbindするか。
4. inline `line_accuracy`の許容範囲。同一行必須か、同一hunk内の対象範囲を許すか。
5. expected findingの意味一致判定を完全な決定論的ruleで実装できるか。難しい場合でも、評価用LLMを即追加せず、まず限定されたcategory/path/rule identityで判定する。
6. model identityがsubscription側で自動更新された場合の比較停止条件。

未確定事項を便宜的に補完して実装を進めない。

## 実装段階

| Phase | 内容 | 完了条件 |
|---|---|---|
| 0 | 測定契約確定 | 未確定事項のうち実装開始に必要な項目がbind済み |
| 1 | fixtureとrun schema | 6 fixtureとexpected finding、run JSON schemaが固定される |
| 2 | Baseline collector | 現行方式の`t0`〜`t5`または取得可能な区間とquality resultを保存できる |
| 3 | Candidate A最小実装 | deterministic input preparation + Claude reviewがCore Reviewで動作する |
| 4 | pilot | 6 case × Baseline/Candidate A × N=1でschema、collector、quality判定を検証する |
| 5 | N=5 | 全caseを交互順序でN=5実行する |
| 6 | 比較result | quality gate通過可否と時間KPI中央値を固定resultとして保存する |
| 7 | Integration | Core Reviewで採用候補となったCandidateだけGitHub commentまで含めて測る |

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

## Codexへの次作業

この文書を実装指示へ変換する場合、最初の変更単位は**測定環境の骨格だけ**とする。

推奨する最初の作業:

1. 現行`.github/workflows/claude-pr-review.yml`と関連する自動修正workflowを読み、現状のtriggerとside effectを一覧化する。
2. 測定用アーティファクトの配置先を、既存のevaluation基盤と混同しない形で決める。
3. `PRR-C01`〜`PRR-C06`のfixture schemaとrun result schemaを提案する。
4. timestamp取得可能点とGitHub Actions log / Action outputから取得できるruntime値をprobeする。
5. Phase 0の未確定事項を、実測結果とともにこの文書の新revisionまたは後続設計文書へ固定する。

この最初の作業では、レビュー方式の置換、自動修正の再接続、既存評価resultの変更まで広げない。
