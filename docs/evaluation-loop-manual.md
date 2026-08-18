# Evaluation loop manual

## 1. 対象

この文書は、`scripts/evaluation_loop.py`で1 runを実行・採点し、`scripts/atomic_run_registry.py`で各runを独立保存して、任意のrun selectionを集計・比較する方法を説明する。従来のprompt-set result経路も履歴互換として扱う。

基盤にはprompt作成、quality rater用prompt、優劣判定、採用、release判断、THE-CAPTION本体反映を含めない。

### 今後の標準全体試験

今後のTHE-CAPTION向け全体試験は、[`the-caption-standard14-r1`](../evaluations/sets/the-caption-standard14-r1/README.md)の14項目で実施する。

標準14項目は、従来のF項目12件とA01・A02で構成する。各項目を5回実行した場合も、70 runを個別登録する。`N=5`は保存identityやrunの束ではなく、analysisがcaseごとに選ぶ件数である。

一部項目だけの原因確認は対象試験として分離する。A01・A02を除いた旧12項目の実行を、今後の全体試験完了として扱わない。

旧12項目の評価集合と結果は履歴として保持する。標準14項目の結果と互換比較へ混ぜない。

## 2. 4 Layerとsubcommand

| Layer | subcommand | 役割 |
| --- | --- | --- |
| 1. Evaluation set | `freeze-set` | set revisionとfixtureをcycleへ固定する |
| 1. Evaluation coverage | `bind-coverage` | このcycleで発行・登録するcaseとiterationを実行前に固定する |
| 1. Comparison generation | `prepare-comparison-layer1` | 保存済み基準resultのLayer 1を検証し、比較cycleへ複製する |
| 1. Comparison preflight | `preflight-comparison` | profile、capsule、global planを基準resultへ照合して発行を許可する |
| 2. Execution | `run` | 1 prompt setの1 case / 1 iterationを実行する |
| 3. Quality rating | `rate` | 1 runへ0〜4のscoreを記録する |
| 4. Atomic registration | `atomic_run_registry.py register-run` | 採点済み1 runをregistryへ追記する |
| 4. Legacy import | `atomic_run_registry.py import-result` | 既存prompt-set resultのrunを元result不変のまま索引化する |
| 1. Atomic pool seed | `atomic_run_registry.py seed-pool` | 基準poolの実効条件から、run 0件の新prompt poolを固定する |
| 4. Missing dispatch | `atomic_run_registry.py plan-missing` | poolの既存runをcase別に数え、不足runだけを固定する |
| 4. Selection | `atomic_run_registry.py select-runs` | 分析に用いるrun ID集合をwrite-onceで固定する |
| 4. KPI analysis | `atomic_run_registry.py aggregate-selection` | selectionから3 KPIを集計する |
| 4. KPI comparison | `atomic_run_registry.py compare-analyses` | 実効互換な2 analysisの差分viewを作る |
| 4. 履歴互換 | `record-result` / `compare` | 従来のprompt-set resultを登録・比較する |

`reaccount-result`はroot-only v3 resultを変更せずall-agent resultを追記する履歴補正interface、`query-results`はregistryのread-only取得interfaceである。各書込subcommandは既存artifactを上書きしない。

## 3. 必要なもの

1. `revision`を持つEvaluation set source
2. caseごとのrepository fixture directory
3. 1つの`prompt_set_identity`用Run capsule
4. run成果を0〜4で採点できるquality rater
5. 新規または既存のresult registry directory

capsuleへsecretやcredentialを直接保存しない。非公開のraw run evidenceをrepositoryへcommitしない。

## 4. Evaluation set source

```text
/path/to/evaluation/
├── set.json
├── fixture-a/
└── fixture-b/
```

最小形式は次のとおり。

```json
{
  "schema_version": "the-caption-prompt.evaluation-set-source/v2",
  "set_id": "<set family identity>",
  "revision": "<immutable set revision>",
  "cases": [
    {
      "id": "<case id>",
      "fixture": "fixture-a",
      "payload": {
        "<model-visible parameter>": "<value>"
      }
    }
  ]
}
```

`fixture`は`set.json`からの相対pathで指定する。基盤が解釈するsource fieldは`set_id`、`revision`、caseの`id`と`fixture`である。それ以外は変更せず固定setへcopyする。macOSでは独立性を保つclonefile-backed Copy-on-Writeを先に試し、使用できないfilesystemでは通常copyへfallbackする。物理copy方式はset identityへ含めない。

`freeze-set`はcase別fixture identityとset content identityを計算する。fixture identityは`.git`内部を除くpath、type、mode、file content、symlink targetに結び付く。

保存済みresultとの比較では`freeze-set`を使わない。`git clone`等による再生成はprocessの`umask`によってfile / directory modeが変わり得るためである。基準resultと対応する保存済みLayer 1を`prepare-comparison-layer1`へ渡し、検証済みの実体から比較cycleを生成する。

固定setの一部だけを対象試験として発行する場合は、一件目の`run`より前に`bind-coverage`でcaseとiteration数を固定する。これによりset identityとTaskSpecを変えず、coverageだけをresultの互換条件として分離できる。coverage外の`run`は拒否し、`record-result`はbound coverage全件が揃わなければ停止する。

### reasoning effortの運用基準

2026-07-27以降に新規作成する通常のprompt比較profileは、reasoning effortを`medium`へ固定する。例外は、reasoning effort自体を比較変数にする試験と、既存`high` resultの互換条件をそのまま再現する追試だけである。

reasoning effortはcomparison conditionである。既存`high` profileとresultは履歴として変更せず、`medium` profileを新しいidentityで追加する。`high`と`medium`のresultを同一のLayer 4 comparisonへ混ぜない。

### 実行前のresult再利用とcampaign scheduling

新しいslotをmaterializeする前に、atomic registryの同じ`pool_key`からcase別の保存run数を数える。各caseの必要件数との差だけを`plan-missing`へ固定する。例えばStandard14のF03だけ5件あり、全caseを5件へ揃える場合、F03は再実行せず残る13 case × 5 = 65 runだけを発行する。

```bash
ATOMIC=scripts/atomic_run_registry.py

# 既存N=5 resultのrunを独立索引へ追加する
python3 "$ATOMIC" import-result \
  --registry "$REGISTRY" \
  --result-id <n5-result-id>

# 新しいpromptを初めて実行する場合は、基準poolの実効条件から空poolを作る
python3 "$ATOMIC" seed-pool \
  --registry "$REGISTRY" \
  --reference-pool-key <reference-pool-key> \
  --prompt-identity /path/to/candidate-profile.json

# 各caseの保存run数から不足slotだけをplanへ出す
python3 "$ATOMIC" plan-missing \
  --registry "$REGISTRY" \
  --pool-key <pool-key> \
  --desired-count 100 \
  --output /new/path/missing-to-100.json
```

`plan-missing`の`desired-count`は各caseへ要求する件数であり、runまたはpool identityへ含めない。各missing slotは独立した`sample_id`、case ID、dispatch用の局所iterationを持つ。case間で同じ`sample_id`へ束ねない。`prepare_atomic_plan.py`はこのplanから不足capsuleだけを生成する。

`seed-pool`はrunを捏造せず、基準poolのcase別実効条件とcomparison keyだけを新しいprompt identityへbindする。生成したv3 global planも`preflight-comparison`へ渡し、基準resultとの完全なprofile互換性、dispatch plan hash、全capsule path / hash / sample IDを`comparison-preflight/v2`へ固定してから発行する。

```bash
python3 layer2/extensions/parallel_execution/prepare_atomic_plan.py \
  --template /path/to/CASE-A-template.json \
  --template /path/to/CASE-B-template.json \
  --dispatch-plan /new/path/missing-to-100.json \
  --registry "$REGISTRY" \
  --cycle /path/to/extension-cycle \
  --evaluation-loop scripts/evaluation_loop.py \
  --duration-hints /path/to/profile.json \
  --resource-class /path/to/resource-class.json \
  --output /new/path/atomic-global-plan
```

各runの`rate`完了後、prompt-set result完成を待たず個別登録する。

```bash
python3 "$ATOMIC" register-run \
  --registry "$REGISTRY" \
  --pool-key <pool-key> \
  --cycle /path/to/extension-cycle \
  --run-id <rated-run-id>
```

必要件数が揃った時点でrun ID集合を固定し、集計する。

```bash
python3 "$ATOMIC" select-runs \
  --registry "$REGISTRY" \
  --pool-key <pool-key> \
  --count 100 \
  --output /new/path/selection.json

python3 "$ATOMIC" aggregate-selection \
  --registry "$REGISTRY" \
  --selection /new/path/selection.json \
  --output /new/path/analysis.json
```

`select-runs`はcaseごとに要求件数を選び、selection iterationへ組み合わせる。selection iterationはKPI集計上の対応付けであり、実行時の束または共通sample identityではない。

poolの一部caseだけを比較へ再利用する場合は`--case-id`を繰り返す。選択済みatomic runを後続の`prepare-comparison-layer1`へ渡せる基準resultにする場合は、同じ条件を固定したprofileで`register-selection-result`を実行する。新しいrunは発行せず、selection内のrun identityとprofile条件が完全一致する場合だけimmutable resultを登録する。

```bash
python3 "$ATOMIC" select-runs \
  --registry "$REGISTRY" \
  --pool-key <pool-key> \
  --count 5 \
  --case-id TC-A01-LATENT-MODE-POLICY \
  --case-id TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING \
  --output /new/path/reference-selection.json

python3 "$ATOMIC" register-selection-result \
  --registry "$REGISTRY" \
  --selection /new/path/reference-selection.json \
  --profile /path/to/matching-reference-profile.json
```

candidate固有のquality・mechanism gateがある場合はcandidate slotだけを先に実行する。candidate resultが有効かつ採点可能になった後は、mechanismの成否と分離して、保存済み互換baselineがある場合は3 KPI比較を主結果へ含める。mechanism不通過はKPI比較を止める条件にしない。

mechanismへ100％成立を要求するのは、そのmechanismの成立・不成立と品質再現性の成否が常に一致し、相関が100％であることを互換する証拠で確認した場合だけとする。この対応が確認されていないcost経路のmechanism成立率は原因診断に使う観測値であり、1件の不成立を追加NまたはStandard14の自動停止条件にしない。品質を維持したうえで、all-agent `total_tokens`と`elapsed_seconds`がともに減った場合はcost改善方向とする。一方が増えた場合は、その増加をまずcost退行として記録し、追加costが品質、必要な正常経路または明示された制約を維持するために必要だったかをtraceで監査する。必要性を確認できない場合は`unjustified_cost_regression`とし、減少した別指標で相殺しない。必要性を確認できた場合だけ`tradeoff_requires_human_judgement`として人間へ交換条件を提示する。保存済み互換baselineがない場合はKPI比較未完了を明示し、baseline slotを新規発行するかを別途固定する。この扱いは[Candidate110で固定した訂正](candidate110-validation-ticket-decision-boundary-design.md)に従う。

保存済みresultを基準にする比較cycleは、次の順序で準備する。

```bash
python3 "$CLI" prepare-comparison-layer1 \
  --registry "$REGISTRY" \
  --reference-result-id <result_id> \
  --reference-layer1 /path/to/reference/cycle/layer1 \
  --cycle "$CYCLE"
```

このcommandは、基準resultのcontent SHA-256、compatibility key、Evaluation set identity、全fixture identityと保存Layer 1の実体を照合する。照合後にLayer 1をcopyし、基準resultのcase / iteration coverageを固定する。内容が同じでもmodeが異なるLayer 1は生成前に拒否する。

target固有の手順でcandidate profile、Run capsule、global planを生成した後、最初のslotより前に次を実行する。

```bash
python3 "$CLI" preflight-comparison \
  --cycle "$CYCLE" \
  --profile /path/to/candidate-profile.json \
  --global-plan /path/to/global-plan.json \
  --registry "$REGISTRY" \
  --reference-result-id <result_id>

python3 "$CLI" verify-comparison-preflight --cycle "$CYCLE"
```

preflightは、prompt identity以外の全compatibility、設定上の`M`、発行対象case / iteration、各capsuleのidentityとcomparison conditionsを照合する。legacy planではprofileの全coverage、atomic planではhash固定したdispatch planの不足slot集合との一致を要求する。成功時だけ`comparison-preflight.json`をwrite-onceで作る。`run`も実行直前にreceipt、profile、global plan、capsuleを再検証するため、receipt欠落、改ざん、準備後の条件変更はadapter起動前に停止する。

複数prompt setの新規slotは、prompt setごとのcycleを維持したまま[`campaign_runner.py`](../layer2/extensions/parallel_execution/campaign_runner.py)の一つのglobal queueへ入れる。明示した`resource_class`が一致すれば、analysis condition、coverage、局所反復数が異なるplanも同じqueueへ入れられる。queueは同一case / sampleの比較対象を近接配置したうえでworkerを空けず、このhostでは`M=24`を上限とする。

## 5. Run capsule v2

1 prompt set、1 case、1 iterationにつき1つ用意する。

atomic経路では`execution-capsule/v3`を使う。`binding.sample_id`を必須とし、`comparison_conditions.repetition_condition`を持たない。`iteration`はcycle内でcapsuleを一意にする局所dispatch番号であり、run poolまたは分析上の`N`を表さない。`prepare_atomic_plan.py`は既存v2 templateからv3 capsuleを生成し、repetition conditionを除去する。

```json
{
  "schema_version": "the-caption-prompt.execution-capsule/v3",
  "binding": {
    "prompt_set_identity": {"name": "<name>", "revision": "<revision>"},
    "case_id": "<case>",
    "iteration": 1,
    "sample_id": "planned:<dispatch-plan>:<sample>"
  },
  "comparison_conditions": {
    "model": "<model>",
    "executor_parameters": {"max_workers": 24}
  }
}
```

省略した他の実効条件はv2と同じである。`repetition_condition` keyは含めない。

```json
{
  "schema_version": "the-caption-prompt.execution-capsule/v2",
  "binding": {
    "prompt_set_identity": {
      "name": "the-caption-example",
      "revision": "r3",
      "bundle_sha256": "<lowercase SHA-256>"
    },
    "case_id": "CASE-001",
    "iteration": 1
  },
  "comparison_conditions": {
    "target_repository_ref": "owner/repo@<commit>",
    "model": "<model identity>",
    "agent_environment": {
      "agent": "codex",
      "version": "<version>"
    },
    "task_spec": {
      "CASE-001": "<TaskSpec revision>"
    },
    "permission": "workspace-write/never",
    "executor_parameters": {
      "reasoning_effort": "medium",
      "token_accounting": {
        "scope": "all_agents",
        "revision": "v1",
        "source": "codex_rollout_final_usage_by_workspace"
      }
    },
    "repetition_condition": {
      "iterations": 3,
      "order": "case-major"
    }
  },
  "adapter": {
    "argv": ["python3", "/path/to/executor.py"]
  },
  "parameters": {
    "prompt_bundle": "/path/to/bundle",
    "bundle_sha256": "<lowercase SHA-256>",
    "<prompt固有またはadapter固有parameter>": "<value>"
  }
}
```

`prompt_set_identity`は`name`に加え、`revision`または`bundle_sha256`を必須とする。比較相手のconditionは指定しない。同じcycleの全capsuleは同一identityと同一`comparison_conditions`を使用する。

`comparison_conditions`はprompt identity以外の比較互換条件である。次を必須とする。

- `target_repository_ref`
- `model`
- `agent_environment`
- `task_spec`
- `permission`
- `executor_parameters`
- `repetition_condition.iterations`

値の内部は`repetition_condition.iterations`以外opaqueだが、result間ではcanonical JSONとして完全一致を要求する。prompt bundle pathやprompt固有hashを`executor_parameters`へ入れない。実行順、外側並列度、reasoningなど比較対象間で固定する値はここへ入れる。

Codex adapterでmodel-visible capability catalogを固定する場合は、`agent_environment.model_visible_capability_catalog`へ`apps_enabled / plugins_enabled / plugin_sharing_enabled / expected_sha256 / schema_version`を保存する。現行`v1`は3 featureを`false`へ固定する。adapterは各root rolloutからskills / apps / plugins blockを抽出し、SHA-256不一致を`model_visible_capability_catalog_mismatch`として除外する。identity artifactは`layer2/extensions/<run_id>/model-visible-capability-catalog/identity.json`へ保存する。

## 6. Executor contract

`run`は`adapter.argv`を独立したfixture copy内でshellを介さず実行する。Layer 1と同じくCopy-on-Writeを使用できる場合は利用するが、workspaceの変更は固定fixtureへ反映されない。executorへ次の環境変数を渡す。

| 変数 | 内容 |
| --- | --- |
| `EVAL_CASE_FILE` | 固定済みcase capsule |
| `EVAL_RUN_CAPSULE_FILE` | 固定済みRun capsule |
| `EVAL_USAGE_FILE` | executorがall-agentの`total_tokens`とaccounting identityを書く一時JSON |
| `EVAL_RUN_STATUS_FILE` | 外部要因による除外を通知する一時JSON |
| `EVAL_EXTENSION_DIR` | 詳細分析用のopaque directory |

executorは終了までに次を書く。

```json
{
  "schema_version": "the-caption-prompt.token-usage/v2",
  "token_accounting": {
    "scope": "all_agents",
    "revision": "v1",
    "source": "codex_rollout_final_usage_by_workspace"
  },
  "total_tokens": 12345
}
```

`total_tokens`はroot agentと全descendant SA sessionの最終usage合計でなければならない。基盤がKPIとして解釈するtoken値は0以上の整数`total_tokens`だけである。root / SA別値、input / output内訳、turn別値は`EVAL_EXTENSION_DIR/all-agent-usage/`または別featureへ保存し、rating、result登録、比較viewへ入力しない。全sessionの最終usageが揃わない場合は`codex_all_agent_usage_incomplete`として除外し、値を推定しない。`elapsed_seconds`は基盤が計測する。

promptまたはtask behaviorではない外部要因を客観的証跡から検出した場合だけ、executorは次を出力できる。

```json
{
  "schema_version": "the-caption-prompt.run-status/v1",
  "status": "excluded",
  "category": "external_failure",
  "reason_code": "<stable reason code>"
}
```

excluded attemptはraw artifactを保持するが、採点とKPIへ入力せず、有効なcase / iteration slotを占有しない。同じcapsuleを再実行する。Agentの自己申告や最終応答だけを除外根拠にしない。

### Observation delivery実験条件

Codex adapterは、`comparison_conditions.executor_parameters.observation_delivery`が次の完全一致objectである場合だけ、code mode限定のbuffered executionを有効にする。

```json
{
  "schema_version": "the-caption-prompt.observation-delivery/v1",
  "mode": "code_mode_only_buffered_exec",
  "direct_tool_result_delivery": "disabled",
  "nested_tool_result_delivery": "code_local_until_return"
}
```

この値はexecutor comparison conditionであり、compatibility keyへ含まれる。指定なしのcontrol resultと通常のprompt比較へ混ぜない。adapterは有効時だけ`layer2/extensions/<run_id>/observation-delivery/audit.json`へ経路監査を保存する。現行機構は直接tool resultを閉じるが、外側code callのreturn回数を制約しない。[F02 N=5 executor A/B](../evaluations/results/candidate81-observation-delivery-executor-ab-v14-medium-f02-n5_2026-07-29.md)では直接result 0件を確認した一方、model再入削減は確認できなかった。

成功したrequired validationのraw outputを配送しない実験では、上記`observation_delivery`に加えて`executor_parameters.success_delivery`を次へ完全一致させる。

```json
{
  "schema_version": "the-caption-prompt.success-delivery/v1",
  "mode": "success_silent_failure_unchanged",
  "deterministic_success_delivery": "command_and_exit_code_only",
  "failure_delivery": "unchanged_tool_result",
  "intermediate_status_delivery": "start_blocking_or_60s_only"
}
```

required validationは一つのcode call内で個別発行する。全成功時は完全なcommand文字列とexit codeだけを返し、stdout / stderrをmodelへ配送しない。raw command evidenceはlocal rolloutへ保持する。nonzero、unknown、permission要求時は後続を止め、tool resultを変更せず返す。[F02 N=5](../evaluations/results/candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md)ではsuccess mechanism 5 / 5とtoken中央値`-17.86%`を確認したが、失敗経路と別caseへの一般化は未確認である。

`success-delivery/v2`はinstruction-based v1から、対象commandの実行、成功raw保存、成功receipt生成、失敗raw返却をexecutor wrapperへ移す。profileはcaseごとのexact argvとrequired command group indexを一対一で固定する。直接pytestと、script path / SHA-256を固定したpytest-only wrapperだけを許可する。compound commandとallowlist外argvは実行前に拒否する。

成功時のstdout / stderrは`layer2/extensions/<run_id>/success-delivery/raw-command-evidence/`へbyte数とSHA-256付きで保存し、modelへはreceiptだけを返す。通常のnonzero exitとsignal終了はstdout / stderrと終了状態を維持する。auditはv2ではrequired tokenの部分一致を使わず、wrapper markerとruntime policyのexact argvでvalidation callを同定する。[F02](../evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f02-n5_2026-07-29.md)と[F06](../evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f06-n5_2026-07-29.md)は各5 / 5 score `4`、mechanism 5 / 5だった。後続の[F06 matched A/B](../evaluations/results/candidate81-success-delivery-executor-ab-v14-medium-f06-n5_2026-07-29.md)ではoutput合計`-64.47%`に対しtoken合計`+22.29%`、elapsed合計`+7.63%`だったため、model-visible wrapper方式を停止しStd14へ進めない。

## 7. 1 prompt set resultの登録

以下ではpathを次のように表す。

```bash
CLI=/Users/kenn/repos/agent-execution-control-lab/scripts/evaluation_loop.py
CYCLE=/tmp/prompt-set-baseline-r3
REGISTRY=/tmp/the-caption-prompt-result-registry
```

### Layer 1: setを固定する

```bash
python3 "$CLI" freeze-set \
  --set /path/to/evaluation/set.json \
  --cycle "$CYCLE"
```

cycleは空でなければならない。固定後にsource setやfixtureを変更してもcycleへ反映されない。

この`freeze-set`経路は新規Evaluation setまたは基準resultを持たない単独評価用である。保存済みresultとの比較には前節の`prepare-comparison-layer1`経路を使う。

固定setの一部だけを発行する場合は、続けてcoverageを固定する。

```bash
python3 "$CLI" bind-coverage \
  --cycle "$CYCLE" \
  --case-id CASE-001 \
  --iterations 5
```

`--case-id`は複数指定できる。coverageはwrite-onceであり、実行後にcaseやiterationを追加しない。全setを実行する既存cycleでは省略でき、その場合は固定set全件を登録条件とする。

### Layer 2: case / iterationを実行する

```bash
python3 "$CLI" run \
  --cycle "$CYCLE" \
  --capsule /path/to/run-capsules/CASE-001-i1.json
```

全caseについて`iteration: 1`から`comparison_conditions.repetition_condition.iterations`まで実行する。同じcase / iterationのvalid runは重複できない。excluded attemptだけは同じslotで再実施できる。

### Layer 3: blind採点する

quality raterへ渡すのは次だけである。

- `$CYCLE/layer1/set.json`の該当caseにあるmodel-visible情報
- `$CYCLE/layer2/evidence/<run_id>/`の必要なblind evidence
- 現行契約`outcome-abstract-condition-preserving-owner-diagnostic-v13`が要求するall-agent command evidence view（collector schemaは`all-agent-command-evidence/v5`）
- 同契約が要求するowner-producer evidence view（`owner-producer-evidence/v1`）

`layer2/bindings/`、Run capsule、oracle、grader、expected result、prompt identityは渡さない。v13では加えて、実行役へ提示していない正解条件・質問項目・試験コマンドと、提示した抽象条件から推定した特定コマンドを必須試験として扱う判断も渡さない。

v13のscore `4`は、実行役へ提示した成果条件と禁止境界の充足（`case_quality_rules`で`diagnostic_only`とした提示要素を除く）と、コマンド名までmodel-visibleに明示された必須試験の成功証拠を要件とする。**owner-producer evidenceは診断だけに使用し、成果品質の点数を変更しない**（`owner_producer_evidence_policy`は`diagnostic_only`）。v8時代の「owner-producer evidenceが不一致ならscore `4`を記録できない」手順は、v1〜v8で採点した既存resultの条件として保持し、v9以降の新規runへ適用しない。

TaskSpecがcriterion ownerを固定したrunは、採点前に次を実行する。

まず、各runでall-agent usageへbindされたrootとrecursive descendantのattempted、successful、failed commandを、workspace pruneより前にmaterializeする。新規runは`command-evidence-protocol/v1`をcomparison conditionへ固定し、required commandを1 commandずつ実行してstructured `exit_code`を保存する。required command callがない場合はtask-level未実行として採点する。callがあり非zero exitをbindできる場合はtask-level command failureとして採点する。callはあるがexitをbindできない場合は`command_evidence_incomplete`としてrunを除外し、同じslotを再試行する。

順序付きrequired commandをrootの一つのmodel stepへ閉じる診断では、`command-evidence-protocol/v2`を別comparison conditionとして使用できる。v2はroot producerへ、1回のcustom exec wrapper内から各commandを列挙順の個別`tools.exec_command`として発行し、nonzeroまたはunavailableで後続を止め、完了済み全resultを一度だけmodelへ返すようmodel-visibleに指定する。shell compound commandは許可しない。v1とv2は評価条件が異なるため同一Layer 4 comparisonへ混ぜず、protocol診断として扱う。

許可pathの上限はLayer 2 adapterの`unexpected_changed_paths`をSSOTとする。Layer 3は成果に必須のpathが存在することだけを確認し、許可済みtest fileを独自のsource-only一覧で再び禁止しない。

caseが作る試験基盤所有のtemporary outputは、宣言したpathだけをadapterがmodel実行後に削除する。削除失敗はquality scoreへ混ぜず、`adapter_owned_teardown_failed`のexternal failureとして除外する。

command format違反とmodelによるadapter-owned pathのcleanup試行は`evaluation-diagnostics`へrun ID付きで保存する。これらはquality KPIへ入れない。

```bash
python3 scripts/all_agent_command_evidence.py \
  --usage "$CYCLE/layer2/extensions/<run_id>/all-agent-usage/usage.json" \
  --root-events "$CYCLE/layer2/extensions/<run_id>/codex-adapter/codex-events.jsonl" \
  --output "$CYCLE/layer2/extensions/<run_id>/all-agent-command-evidence/evidence.json"
```

続いてowner-producer evidence viewを生成する。

```bash
python3 scripts/owner_producer_evidence.py \
  --cycle "$CYCLE" \
  --output "$CYCLE/layer3/owner-producer-evidence.json"
```

`owner_producer_evidence.py`のexit `0`は全valid runでowner-producer evidenceがbindできたこと、exit `1`は1件以上で欠落または不一致があることを示す。**現行のv13ではこのexit codeをscoreの上限へ変換しない。** owner-producer evidenceは`diagnostic_only`であり、exit `1`のrunも診断として記録したうえで、提示した成果条件・禁止境界・コマンド名まで明示された必須試験の充足だけで0〜4を採点する（充足していればscore `4`を記録する）。実装も`owner_producer_evidence_policy`が`score_4_gate`のrevisionだけscore `4`を拒否する。

F10 MonthlyまたはD01のtargeted reviewを採点する場合は、[`targeted_review_quality_audit.py`](../scripts/targeted_review_quality_audit.py)を使う。`--expected-set-id`、`--expected-set-revision`、`--expected-run-count`を明示し、rating contract IDはvalid bindingの`comparison_conditions.quality_rating.contract_id`から一意に取得する。campaign固有scriptから`monthly_review_failures`または`monthly_review_rating`をcontract IDなしで呼び出してはならない。v11以降の数値lineはdiagnosticであり、v10既定値へfallbackさせない。

v1〜v8では同じexit `1`がscore `4`の拒否条件だった。この扱いはv8以前で採点した既存resultの条件として保持し、v9以降の新規runへ適用しない。

```bash
python3 "$CLI" rate \
  --cycle "$CYCLE" \
  --run-id <run id> \
  --score 3 \
  --reason "<scoreの短い事実根拠>"
```

scoreは0、1、2、3、4のいずれかとする。excluded runは採点しない。

### Layer 4: resultをappend-only登録する

```bash
python3 "$CLI" record-result \
  --cycle "$CYCLE" \
  --registry "$REGISTRY"
```

全caseと`1..N`、全rating、all-agentの`total_tokens`、単一identity、単一`comparison_conditions`を検証し、次を新規作成する。

```text
$REGISTRY/results/<result_id>.json
$CYCLE/layer4/result-registration.json
```

同じcycleの再登録と既存resultの上書きを拒否する。別のprompt setは別cycleで同じ手順を実行し、同じregistryへ独立resultとして追記する。

### root-only v3 resultの再集計

保存済みCodex sessionから全runのusageを完全に復元できる場合は、まず`backfill_all_agent_usage.py`で独立したLayer 2 extensionを作り、次に元resultごとに`reaccount-result`を実行する。

```bash
python3 scripts/backfill_all_agent_usage.py \
  --registry "$REGISTRY" \
  --session-root /path/to/codex/sessions \
  --output /path/to/reaccounting-cycle

python3 "$CLI" reaccount-result \
  --registry "$REGISTRY" \
  --source-result-id <root-only result id> \
  --usage-root /path/to/reaccounting-cycle \
  --receipt-root /path/to/reaccounting-cycle/layer4
```

`reaccount-result`は元の`prompt-set-result/v1`を変更せず、`source_result_id`とall-agent accounting identityを持つ`prompt-set-result/v2`を新規登録する。不完全なsession usage、root token不一致、同じ元resultの再登録はfail closedする。

## 8. 保存resultの取得

全resultを取得する。

```bash
python3 "$CLI" query-results --registry "$REGISTRY"
```

次のfilterを任意に追加できる。

- `--prompt-name`
- `--prompt-revision`
- `--bundle-sha256`
- `--compatibility-key`
- `--token-scope root_agent|all_agents`

filterはregistryを変更しない。2件に限定せず、該当する全resultを返す。

## 9. 2つ以上の任意個比較

baseline、candidate1、candidate2の3 resultを一覧・比較する例を示す。

```bash
python3 "$CLI" compare \
  --registry "$REGISTRY" \
  --result-id <baseline result id> \
  --result-id <candidate1 result id> \
  --result-id <candidate2 result id> \
  --reference-result-id <baseline result id> \
  --output /tmp/three-prompt-view.json
```

`--result-id`は2回以上、任意回数指定できる。`--reference-result-id`は選択resultの1つでなければならない。

全resultの互換条件が一致した場合、viewは次を含む。

- 選択した全prompt setのidentity
- 各prompt setのiteration別3 KPIと中央値
- 各prompt setの除外attempt
- 各非reference resultをminuend、reference resultをsubtrahendとする3 KPI差分

`minuend_result_id`と`subtrahend_result_id`を各差分に明記する。referenceは採用状態や順位を意味しない。互換条件が1項目でも異なる場合はviewを作らない。

## 10. Directory

```text
<cycle>/
├── layer1/
│   ├── set.json
│   └── fixtures/
├── layer2/
│   ├── evidence/<run_id>/
│   │   └── exclusion.json            # excluded attemptだけ
│   ├── capsules/<run_id>.json
│   ├── bindings/<run_id>.json
│   └── extensions/<run_id>/<feature>/
├── layer3/
│   └── ratings/<run_id>.json
└── layer4/
    └── result-registration.json

<registry>/
├── runs/<atomic_run_id>.json
├── pools/<pool_key>.json
└── results/<legacy-result-id>.json
```

selection、analysis、comparisonは利用者が指定した新規pathへ作る。poolは条件索引だけを持ち、run member一覧や件数を持たない。

比較viewは利用者が指定した新規pathへ作る。cycle、registry result、既存viewを上書きしない。

## 11. 主なerror

| error | 原因 | 対応 |
| --- | --- | --- |
| `revision must be...` | Evaluation set revisionがない | immutable revisionをsourceへ追加する |
| `prompt_set_identity needs...` | identityが可変名だけ | revisionまたはbundle SHA-256を追加する |
| `one cycle may contain only one...` | 別identityまたは別互換条件を混在 | prompt set / 条件ごとにcycleを分ける |
| `run already exists for case/iteration` | valid slotを重複実行 | caseとiterationを確認する |
| `excluded run cannot be quality-rated` | 除外attemptを採点した | 同じslotを再実施してvalid runを採点する |
| `must cover every frozen case and iteration` | caseまたはiteration不足 | 全slotを実行・採点する |
| `observed iterations do not match...` | 実行数と反復条件が不一致 | `1..N`を揃えるか新しい条件で別cycleを作る |
| `compatibility keys do not match` | 固定条件が異なるresultを選択 | 同じkeyのresultをqueryする |
| `refusing to overwrite` | resultまたはview pathが既存 | 新規path / 新規cycleを使う |

## 12. v1 / v2 / v3との境界

v1の`decide`、v2の固定A / B比較、v3のprompt-set resultは履歴契約である。atomic run経路は既存artifactを変更しない。

v3 resultは`import-result`でcase rowごとのatomic runへ索引化できる。元resultのcontent hash、run ID、実行時provenanceを各recordへ保持し、元resultを再採点または上書きしない。

## 13. Storage maintenance

ローカルの新規試験では、Layer 1とLayer 2の物理複製を通常copyへ退避させないため、実行controllerへ`THE_CAPTION_EVAL_COPY_MODE=clonefile`を渡す。clonefileを使用できなければ、その試験はworkspaceを作らず停止する。別filesystemでの通常copyは、必要容量を別途確認して明示的に許可した試験だけで使う。

複数runを持つ通常試験も、8時間runと同じstorage sealを使用する。全Layer 2 runがterminalになり、all-agent usage、command evidence、owner-producer evidenceなど採点に必要なviewをworkspace削除前に固定した後、試験root（直下に`cycle/`があるdirectory）を`--batch`へ渡す。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py seal-batch \
  --batch /absolute/path/to/trial-root
```

採点後に遡ってsealする保守では、既存`rating-view`の構造、validation、final response、Layer 3 ratingとの対応を確認して採点時の`result.diff`を上書きせず保存する`--reuse-existing-rating-views`を明示する。再試行で正本cycleが別名の実ディレクトリに残る場合は`--cycle-path <relative-cycle-path>`をsealとcompactの両方へ同じ値で指定する。symlinkをcycleとして渡さない。

`seal-batch`は完全なworkspaceと自己完結fixtureを1つの検証済み`tar.zst`へ保存してから、live workspaceだけを削除する。Layer 3採点とLayer 4 result登録が完了したら、同じrootを最終圧縮する。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py compact-batch \
  --batch /absolute/path/to/trial-root
```

この順序を通常試験の完了条件とし、未登録の途中runや、採点用viewをまだ固定していないworkspaceを削除しない。検証cloneのcopy mode、容量監査、復元方法、期限切れscratchのguarded GCは[`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md)を参照する。登録済みresultまたはrepositoryから参照するraw evidenceは自動GCしない。

## 14. Self-test

```bash
cd /Users/kenn/repos/agent-execution-control-lab
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests/test_evaluation_loop.py \
  tests/test_evaluation_storage.py \
  tests/test_storage_copy.py \
  tests/test_run_codex_evaluation.py \
  tests/test_parallel_runner.py \
  tests/test_atomic_run_registry.py \
  tests/test_prepare_case_fixture.py
```
