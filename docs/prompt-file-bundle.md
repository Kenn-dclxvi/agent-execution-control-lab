# Prompt file bundle方式

## 1. 目的

Prompt file bundle方式は、比較対象のprompt setを単一の文字列として渡すのではなく、THE-CAPTION内で使用されるファイル構成と相対pathを保ったまま固定し、実行用fixtureへ配置する方式である。

この方式は、次を目的とする。

- baselineとcandidateを独立したprompt identityとして再現できるようにする
- `AGENTS.md`と参照文書のpath関係を実運用と揃える
- prompt変更とcase fixtureの不具合をGit上で区別する
- 実行後も、どのファイル内容をimmutableなprompt set identityとして使ったか検証できるようにする
- quality raterへprompt identityを開示せず、成果だけをblindで採点できるようにする

本書はprompt setをLayer 2の実行workspaceへ供給する配下機能を定義する。評価基盤の4 Layer、3 KPI、KPI comparison schemaは変更しない。

本書はfile bundle方式の設計と実装境界を記録する。exporter、最初のbaseline / candidate、Codex execution adapterは実装済みである。rating viewとblind rater入力境界は未解決であり、artifactが存在しても評価済み、採用済み、本体反映済みであることを示さない。

## 2. 入力の分離

1回の評価runで使用する入力は、少なくとも次の3種類へ分離する。

| 入力 | 内容 | model-visible |
| --- | --- | --- |
| case fixture | 固定commitのTHE-CAPTIONへ`seed.patch`を適用した開始状態 | repositoryの状態として見える |
| prompt bundle | `AGENTS.md`と、それが参照するprompt関連ファイル | 見える |
| case task | Agentへ依頼する作業文 | 見える |

oracle、grader、expected result、quality score、保存resultとKPI比較viewは、これらへ含めずAgentから分離する。

`seed.patch`とprompt bundleは用途が異なる。

- `seed.patch`は、固定commitから評価対象の壊れた状態を再現する。
- prompt bundleは、その壊れた状態へどのprompt setで取り組むかを固定する。

## 3. Repository内の保存形

baseline、candidate、releaseは既存の別pathを維持する。評価へ投入するbaselineとcandidateは、どちらも解決済みのfull bundleとして保存する。

```text
agent-execution-control-lab/
└── prompts/
    ├── baselines/
    │   └── <baseline-id>/
    │       ├── manifest.json
    │       └── files/
    │           ├── AGENTS.md.txt
    │           ├── docs/
    │           │   └── <prompt reference file>
    │           └── prompts/
    │               └── <prompt file>
    ├── candidates/
    │   └── <candidate-id>/
    │       ├── manifest.json
    │       └── files/
    │           ├── AGENTS.md.txt
    │           ├── docs/
    │           │   └── <prompt reference file>
    │           └── prompts/
    │               └── <prompt file>
    └── releases/
        └── <release-id>/
```

`files/`以下は、THE-CAPTIONへ配置するときの相対pathをそのまま表す。ただし`AGENTS.md`と`CLAUDE.md`は、at-rest格納時に`.txt`を付けた名前で保存し、実行workspaceへのoverlay時に本来のtarget名へ復元する。

```text
bundle内(at-rest格納)                  実行workspace内(overlay後)
files/AGENTS.md.txt                ->  AGENTS.md
files/CLAUDE.md.txt                ->  CLAUDE.md
files/docs/prompt-guide.md         ->  docs/prompt-guide.md
files/prompts/implement.md         ->  prompts/implement.md
```

このリポジトリはprompt setそのものをデータとして保存するため、`AGENTS.md`や`CLAUDE.md`を実体名でbundle内へ置くと、CodexやClaude Codeがbundleを編集・調査する作業で、評価対象のprompt本文をrepository instructionとして自動読込してしまう。これを構造的に避けるため、自動読込対象のbasename(`AGENTS.md` / `CLAUDE.md`)だけは`.txt`付きで格納し、リポジトリ内へ自動読込対象名を残さない。格納形式は`storage_format`で表す（第5節）。

Codexは`AGENTS.md`をrepository rootから実行current working directoryまでpath階層に従って発見し、近い階層の指示を後から適用する。したがって、bundle内のファイルを1 directoryへ平坦化しない。root以外の`AGENTS.md`を対象に含める場合も、元の相対pathを維持する。at-restの`.txt`格納はこのpath階層を保ったまま、末尾のbasenameだけを変える。

bundleへ含めるpathは、固定した対象commit上でAgentが参照できるprompt関連ファイルを列挙して決める。作成者の想定だけで参照ファイルを省略しない。

## 4. Full bundle

評価入力には、baselineに対する差分だけでなく、各prompt setで使用するファイル一式を保存する。

```text
baseline bundle
├── manifest.json
└── files/          # baselineだけで内容が完結する

candidate bundle
├── manifest.json
└── files/          # candidateだけで内容が完結する
```

candidate作成中にdiffを利用してもよいが、`evaluation_ready`へ進める前にfull bundleへ解決する。これにより、後からbaselineが変化してもcandidateの実体が変わらず、各prompt setを単独で再現できる。

## 5. Manifestとidentity

各bundleは`manifest.json`で由来、対象path、ファイルhash、bundle全体のidentityを固定する。

```json
{
  "schema_version": "the-caption-prompt.bundle/v1",
  "storage_format": "instruction-suffixed/v1",
  "prompt_identity": "<prompt identity>",
  "source": {
    "repository": "Kenn-dclxvi/THE-CAPTION",
    "commit": "<source commit>",
    "tree": "<source tree>"
  },
  "files": [
    {
      "target": "AGENTS.md",
      "type": "file",
      "sha256": "<content sha256>"
    },
    {
      "target": "docs/prompt-guide.md",
      "type": "file",
      "sha256": "<content sha256>"
    }
  ],
  "bundle_sha256": "<bundle identity>"
}
```

`files`は`target`で昇順に並べる。現在のexporterは、schema versionと順序を固定した各entry全体をcanonical JSONへ変換して`bundle_sha256`を計算する。通常fileのentryにはtarget、type、mode、Git blob SHA-1、content SHA-256を含め、symlinkのentryにはtarget、type、mode、Git blob SHA-1、link targetを含める。`target`は常に実行workspaceでの実体名(`AGENTS.md`など)であり、at-restの`.txt`格納名ではない。

`storage_format`はat-rest格納形式を表す。

- `tree/v1`: `files/<target>`を実体名で格納する（従来。key省略時もこれとして扱う）。
- `instruction-suffixed/v1`: `AGENTS.md` / `CLAUDE.md`のbasenameを持つtargetだけ`files/<target>.txt`で格納し、symlinkのlink targetも同様に`.txt`へ写像する。

`bundle_sha256`は`{schema_version, files}`だけをhashする識別子であり、`storage_format`はhash対象に含めない。したがって同一内容のbundleを別の`storage_format`で格納しても`bundle_sha256`は変わらない。既存bundleを`tree/v1`から`instruction-suffixed/v1`へ再格納しても、identityは不変である。

`instruction-suffixed/v1`では、格納pathの写像が一意・可逆でなければならない。basenameが`AGENTS.md.txt` / `CLAUDE.md.txt`のtarget（instruction名にsuffixを付けた形）は、`AGENTS.md` / `CLAUDE.md`の格納形と衝突し逆写像で別targetへ潰れるため、この形式では表現不能なtargetとして予約・拒否する。`tree/v1`は恒等写像のため、いかなるtargetも表現できる。exporterとverifierは、`target_from_stored(stored_relpath(target)) == target`が成立しないtargetを`BundleError`で拒否する。

実行adapterはoverlay前に次を検証する。

1. manifestに記載された全targetが`files/`内に存在する
2. manifestにないファイルが`files/`内に存在しない
3. 各ファイルのSHA-256が一致する
4. 再計算した`bundle_sha256`が一致する
5. targetが絶対pathまたは`..`を含まず、workspace外を指さない

manifestは実行制御用であり、Agentのworkspaceへ配置しない。実際に使用したmanifestはRun capsule側の証跡として固定し、quality raterへは渡さない。

## 6. Layer 2での展開

同じ互換条件で比較するprompt setは、同じidentityのLayer 1 fixtureを別cycleへ固定する。Layer 2は各runでfixtureをcopyし、そのcycleのprompt bundleをoverlayする。

```text
Layer 1の固定fixture
固定commit + seed.patch適用済み
            |
            v
       run用workspace
            |
     prompt bundleをoverlay
            |
            v
       固定case taskでAgentを実行
```

展開後の概念上のworkspaceは次のようになる。

```text
<run workspace>/
├── .git/
├── AGENTS.md                         # bundleから配置
├── docs/                             # bundle対象pathを配置
├── prompts/                          # bundle対象pathを配置
├── src/
│   └── domain/
│       └── market_units_snapshot.py  # seed.patchで壊した対象
└── tests/
```

Run capsuleの`binding.prompt_set_identity`へimmutable identityを、`parameters`へ基盤が解釈しないbundle pathと期待hashを持たせる。

```json
{
  "binding": {
    "prompt_set_identity": {
      "name": "<prompt identity>",
      "bundle_sha256": "<expected bundle sha256>"
    }
  },
  "parameters": {
    "prompt_bundle": "/absolute/path/to/<bundle-id>",
    "bundle_sha256": "<expected bundle sha256>"
  }
}
```

adapterは期待identityを検証した後だけoverlayする。同じcycleの全caseと全iterationでは、同じ`prompt_set_identity`と`bundle_sha256`を使用する。

Python dependencyは[`shared-python-runtime.md`](shared-python-runtime.md)の`venv_shim`で共有できる。単純な外部`.venv` symlinkはworkspace-local path contractを壊すため使用しない。

### Fixture conditionとのtarget衝突

caseのseed対象pathとbundleのtarget pathが同じ場合、overlayによって壊した条件そのものが消える。逆順でseedを適用すると評価対象promptをcase側で改変するため、どちらの順序も有効なprompt set resultにならない。

`prepare_evaluation_set.py`はcase capsuleへ`fixture_condition_paths`を記録する。Layer 2 adapterはbundleを変更する前に、manifestのtargetとの積集合を検査し、1 pathでも一致したらfail closedする。

```text
fixture_condition_paths: tests/AGENTS.md
bundle target:           tests/AGENTS.md
                         ^ collision -> 実行しない
```

この場合はcaseを削除せず、`prompt_target_collision`として保管する。実行可能にするには、prompt identityを維持したままfixture conditionを別pathまたは別の観測方法へ分離した新revisionが必要である。

## 7. Git状態の分離

bundleを単純にoverlayしただけでは、Agentからprompt変更とcase seedが同じ未commit変更に見える可能性がある。

```text
 M AGENTS.md
 M docs/prompt-guide.md
 M src/domain/market_units_snapshot.py
```

これを避けるため、Agent実行前に次を行う。

1. bundleを検証してoverlayする
2. bundleのtarget pathだけをstageする
3. 固定したauthor、committer、timestamp、messageでprompt overlay commitを作る
4. bundleに変更がないprompt setでも同じ手順にできるよう、必要ならempty commitを許可する
5. legacyのdirty seedはstageせず残し、committed seedはseed commitを親履歴として保持する

実行開始時の`git status --short`は、原則としてseed対象だけを示す。

```text
 M src/domain/market_units_snapshot.py
```

prompt overlay commitへstageできるpathはmanifest記載pathだけとし、seed対象やAgentの成果を混入させない。commit / tree identityはRun capsuleの証跡へ記録する。

## 8. Model-visibleとmodel-invisibleの境界

bundleの`files/`以下はmodel-visibleである。次はmodel-invisibleとしてworkspaceへ置かない。

```text
model-visible
├── bundleのfiles/以下
├── case task
└── case fixtureの作業状態

model-invisible
├── manifestとprompt set binding
├── seed.patchそのもの
├── private case data
├── oracle
├── grader prompt
├── expected result
├── quality score
└── KPI比較情報
```

Agentは配置されたpromptを読むことができるが、それがbaseline、candidate、releaseのどれであるかを示すlabelは受け取らない。

## 9. Blind rating用の成果表示

実行後の完全なworkspaceにはprompt set固有のファイルが残る。完全なworkspaceをそのままquality raterへ渡すと、prompt内容からidentityを推測できる可能性がある。

推奨案は、完全な実行証跡とは別にblind rating用の成果表示を生成することである。

```text
layer2/evidence/<run_id>/
├── workspace/               # 完全な実行証跡
├── rating-view/
│   ├── result.diff          # bundle targetを除外した成果差分
│   ├── validation.json      # test commandと結果
│   └── final-response.txt   # Agentの最終応答
├── usage.json
└── execution.json
```

`result.diff`から除外するのはmanifestに記載されたbundle targetだけとする。Agentが変更した実装、test、その他の成果pathは残す。

quality raterへ渡す範囲を該当caseのmodel-visible taskと`rating-view/`に限定する。`manifest.json`、Run capsule、bindings、完全なworkspaceは渡さない。完全なworkspaceはexecution sealまでliveで保持し、その後もworkspace全体を含むlossless raw evidence archiveとseal manifestで固定artifactとして保持する。

このrating viewはLayer 2が作る実行証跡の配下機能であり、新しいLayerまたはKPIを追加するものではない。

`layer2/extensions/long_run_storage/`のexecution sealは、このblind evidenceをLayer 2配下機能として生成・検証する。`result.diff`は一時Git indexからtracked変更、削除、untracked成果を取得し、bundle manifestのtargetだけを除外する。`validation.json`はadapter exitと変更pathを記録するが、Agentの最終応答に書かれたtest結果から機械的なpass/failを推定しない。

ratingにはmodel-visible caseと生成済み`rating-view/`だけを渡す。seal archive、Run capsule、binding、oracle、grader、expected result、prompt identityはblind rating入力へ含めない。

## 10. 実行時directoryの全体像

次はSection 9のrating view案を採用した場合のdirectory案であり、現在の固定schemaではない。

```text
<cycle>/
├── layer1/
│   ├── set.json
│   └── fixtures/
│       └── <case id>/               # 固定済みの壊れたfixture
├── layer2/
│   ├── evidence/
│   │   └── <blind run id>/
│   │       ├── workspace/           # bundle適用後の完全なrun
│   │       ├── rating-view/         # blind採点へ渡す成果
│   │       ├── usage.json
│   │       └── execution.json
│   ├── capsules/
│   │   └── <blind run id>.json      # bundle identityを含む。raterへ渡さない
│   ├── bindings/
│   │   └── <blind run id>.json      # prompt set binding。raterへ渡さない
│   └── extensions/
│       └── <blind run id>/
├── layer3/
│   └── ratings/
└── layer4/
    └── result-registration.json
```

## 11. Bundleへ含めるものと含めないもの

bundleへ含めるものは、Agentの行動へ影響するprompt setの構成要素に限定する。

| 含める | 含めない |
| --- | --- |
| root `AGENTS.md` | case fixture |
| 対象にする階層別`AGENTS.md` | `seed.patch` |
| `AGENTS.md`から参照される指示文書 | case task |
| promptとして読み込ませるfile | oracle / grader |
| prompt set identityに含めるmodel-visible設定file | expected result |
| 必要なsymlinkとそのlink target | run log / score / KPI比較情報 |

README、説明用sample、履歴文書などがAgentから読める場所に存在しても、それがprompt setの一部でない場合はbundleへ自動的に含めない。含めるpathの判断はmanifest revisionとして明示する。

## 12. Failure条件

次の場合はAgentを起動せず、runを正式評価へ使用しない。

- manifestまたはfile hashが一致しない
- bundleに未記載fileがある
- unsafeなtarget pathがある
- overlay後の内容がmanifestと一致しない
- prompt overlay commitへmanifest外の変更が混入した
- seed対象以外の予期しない未commit変更が実行前にある
- registryで比較するresult間のfixture、case task、model、permission、反復条件が一致しない
- rating viewへbundle targetまたはprompt set identityが漏れた

Codex adapterが既知の外部要因をstderrの客観的signatureから検出した場合、`EVAL_RUN_STATUS_FILE`へ`status: excluded`、`category: external_failure`、安定した`reason_code`を出力する。Layer 2はraw artifactと`exclusion.json`を保持し、このattemptを採点・KPI比較・有効iteration数から除外する。同じcase / iterationを再実施する。Agentの自己申告だけでは除外しない。

現在自動検出するsignatureは`collab spawn failed: no thread with id:`で、reason codeは`codex_collab_parent_thread_missing`である。`timeout_ms must be at least 10000`などAgentによる不正なtool parameter、analytics送信失敗、ephemeral sessionのhook transcript警告、backgroundのmodel refresh失敗は、このsignatureだけではrun経路が無効になったと確定できないため自動除外しない。

multi-agent実行では親threadをCodexのthread storeから解決できる必要がある。`codex exec --ephemeral`では親thread欠落が3attempt連続で再現したため、Codex adapterはsessionを既定のlocal storeへpersistする。session fileは非公開のlocal run evidenceであり、repositoryへcommitしない。session modeは`comparison_conditions.agent_environment`へ固定し、mode変更後は新しいcycleとenvironment revisionとして扱う。

## 13. 現在の実装境界

現在の実装状態は次のとおりである。

| 項目 | 状態 |
| --- | --- |
| 明示pathからのbaseline export | 実装済み |
| baselineのbit-identicalなcandidate複製 | 実装済み |
| manifest、file identity、bundle hash検証 | 実装済み |
| symlinkを保ったfull bundle | 実装済み |
| 自動読込対象名を避けるinstruction-suffixed格納とoverlay時の実体名復元 | 実装済み。既存bundleは`bundle_sha256`不変で再格納 |
| fixtureへのoverlay | 実装済み |
| deterministicなprompt overlay commit | 実装済み |
| `codex exec`実行とroot＋全SAの`total_tokens`取得 | 実装済み |
| Codex collaborationの親thread欠落を自動検出し、attemptを除外して同じslotを再実施可能にする | 実装済み |
| multi-agent用のpersisted parent session | 実装済み。ephemeral modeは親thread欠落が再現したため不採用 |
| 固定commitからのprompt path自動発見 | 未実装。最初のbundleは17 pathを明示指定 |
| blind rater入力境界 | manual v3でmodel-visible caseと必要なblind evidenceへ限定 |
| rating viewまたは代替遮蔽機能 | 未実装。正式なfile bundle ratingの残課題 |
| 1 prompt set、全case、`1..N`のrun生成・実行automation | 実装済み。parallel execution extension v3 |
| case qualification | `r1`は`case_revision_not_qualified`、`r2`は`execution_qualified_null_calibration_failed` |

最初のbundleとnull calibrationの結果は`evaluations/results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md`、`evaluations/results/TC-F01-r2_identical-bundle-pilot_2026-07-15.md`、`evaluations/results/TC-F01-r2_identical-bundle-n10_2026-07-15.md`を参照する。

## 14. 関連文書

- `docs/repository-contract.md`
- `docs/prompt-comparison-workflow.md`
- `docs/evaluation-loop-manual.md`
- [CodexのAGENTS.md仕様](https://learn.chatgpt.com/docs/agent-configuration/agents-md.md)
