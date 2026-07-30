# Parallel execution extension

## 目的

独立したLayer 2 runを外側並列度`M`で実行する。wave barrierとglobal queueを提供する。複数prompt set、異なるcoverage、異なるdispatch件数の新規runも、cycleを分離したまま同じ`resource_class`のcampaign global queueへ統合できる。

このextensionはcontroller起動、客観的`external_failure`の再実施、OS sample、実行summaryだけを扱う。採点、result登録、複数prompt set比較、改善、release判断は行わない。

1 planの全capsuleは同じ`prompt_set_identity`と`comparison_conditions`を持たなければならない。重複する`case_id / iteration`は実行前に拒否する。

## Wave plan

caseごとにRun capsule templateを1つ用意する。generatorはその他の値を変更せず、`binding.iteration`だけを`1..N`へ展開する。

```bash
python3 layer2/extensions/parallel_execution/prepare_plan.py \
  --template /absolute/path/to/F01-template.json \
  --template /absolute/path/to/F02-template.json \
  --iterations 3 \
  --cycle /absolute/path/to/frozen-cycle \
  --evaluation-loop /absolute/path/to/scripts/evaluation_loop.py \
  --max-workers 2 \
  --output /absolute/path/to/new-parallel-inputs
```

同じiterationのcaseを`max_workers`件ずつwaveへ置き、全job終了後に次waveへ進む。plan schemaは`the-caption-prompt.parallel-execution-plan/v3`、`schedule_policy`は`wave_barrier`である。

## Global queue

空いたworkerへ次のslotを投入する。複数plan campaignでは同一case / sampleの比較対象を近接配置し、group間はlongest-firstにする。duration hintは処理時間短縮にだけ使い、KPI、quality score、互換条件の補正には使わない。

```json
{
  "duration_hints_seconds": {
    "F01": 120,
    "F02": 45
  }
}
```

```bash
python3 layer2/extensions/parallel_execution/prepare_global_plan.py \
  --template /absolute/path/to/F01-template.json \
  --template /absolute/path/to/F02-template.json \
  --iteration 1 \
  --iteration 2 \
  --cycle /absolute/path/to/frozen-cycle \
  --evaluation-loop /absolute/path/to/scripts/evaluation_loop.py \
  --duration-hints /absolute/path/to/duration-hints.json \
  --output /absolute/path/to/new-global-inputs
```

`--max-workers`の既定は、履歴上このhostでqualification済みの`24`である。別host、model、Agent条件または別`M`は新しい`comparison_conditions.executor_parameters`として固定し、必要なqualificationを別cycleで行う。既存v1 / v2 profileは変更しない。

## 複数prompt setのcampaign queue

比較対象ごとのcycleとprompt identityは混ぜない。ただし、実行待ちの独立runは[`campaign_runner.py`](campaign_runner.py)で一つのpair-aware queueへ入れる。旧planは同一comparison conditionsを要求する。新planは同一の明示`resource_class`と`max_workers=24`を持てば、analysis condition、coverage、dispatch件数が異なっても同じqueueへ投入できる。旧planと`resource_class` planを同じcampaignへ混ぜない。

不足runだけを生成する場合は[`prepare_atomic_plan.py`](prepare_atomic_plan.py)を使う。このcommandはatomic dispatch plan、run pool、固定Layer 1、case templateの実効条件を照合し、missing slotだけへ共有`sample_id`を付けた`execution-capsule/v3` global planを作る。v3 capsuleは`repetition_condition`を持たず、dispatch件数をrun identityへ流入させない。

```bash
python3 layer2/extensions/parallel_execution/campaign_runner.py \
  --plan /absolute/path/to/prompt-1/global-plan.json \
  --runner-output /absolute/path/to/prompt-1/parallel-run \
  --plan /absolute/path/to/prompt-2/global-plan.json \
  --runner-output /absolute/path/to/prompt-2/parallel-run \
  --plan /absolute/path/to/prompt-3/global-plan.json \
  --runner-output /absolute/path/to/prompt-3/parallel-run \
  --campaign-output /absolute/path/to/campaign-run \
  --max-workers 24
```

queueは任意個のplanに属する全slotを推定所要時間の長い順に並べる。同時実行可能なslotが24件未満なら全件を開始し、24件以上なら空いたworkerへ次slotを直ちに投入する。prompt setごとの直列campaignは、dependencyまたは明示的な停止gateがある場合だけ使用する。

保存済みの互換resultがあるprompt setは新しいplanへ含めない。candidate固有のquality・mechanism gateはcandidateだけを先に実行し、gate通過後にKPI baselineが必要になった時点で保存resultを照合する。不足する新規slotだけをcampaign queueへ投入する。

## 実行

```bash
python3 layer2/extensions/parallel_execution/parallel_runner.py \
  --plan /absolute/path/to/plan.json \
  --output /absolute/path/to/new-runner-evidence
```

outputはwrite-onceで次を作る。

```text
runner-evidence/
├── plan.json
├── attempts.jsonl
├── os-samples.jsonl
└── summary.json
```

`attempts.jsonl`とOS sampleはmodel-visible入力ではない。Layer 2のworkspace、capsule、binding、execution artifactはcycle内へ保存される。resource競合、workspace衝突、未分類controller failureがあるcycleはprompt set resultへ登録しない。

8時間程度の反復controllerでは、各batchの前後に[long-run storage extension](../long_run_storage/README.md)を組み込む。parallel runnerはstorage削除を行わず、全slotがterminalになった後に別commandでevidenceをsealする。
