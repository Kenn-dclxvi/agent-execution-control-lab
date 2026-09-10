# Codex CLI version共存試験環境設計

## 位置づけ

この文書は、ChatGPT Desktop / Remoteを最新runtimeへ追従させながら、試験harnessから過去のCodex CLIを固定して呼び出すための評価・運用基盤設計である。2026-08-19にhost-local runtime registry、固定version alias、mutable `codex-current`およびdefault standalone CLI更新までを導入した。run別`CODEX_HOME` provisioner、既存runner統合、非評価transport probeおよび評価実行はまだ行っていない。

この環境が固定するのはCLI bundleとローカル実行状態である。サーバー側model、model alias、account policy、利用可能featureまたはbackendの挙動まではCLI bundleだけで固定できない。したがって、過去CLIで実行したという事実を過去runtime全体の完全再現と呼ばない。

## 必須成果

1. ChatGPT Desktop / Remoteは、アプリ自身が管理する内蔵runtimeと`~/.codex`を従来どおり使用できる。
2. 試験harnessは、`PATH`上の`codex`ではなく、登録済みの具体的なCLI bundleを選択できる。
3. 一つの比較または実行waveを開始した後は、`current`の更新、Desktop更新またはstandalone updaterの更新が、そのwaveのCLI identityを変更できない。
4. CLIのversion文字列だけでなく、bundle bytes、platform、署名、呼出しpath、adapter、model、reasoning、permission、状態隔離方式およびtoken accountingをreceiptへ固定する。
5. 各atomic runは、別runやDesktopと`config.toml`、`models_cache.json`、skills、plugins、memories、sessionおよび一時更新を共有しない。
6. persisted sessionを必要とするall-agent token accountingでは`--ephemeral`を使わず、集計とsealが終わるまでrun固有sessionを保持する。

## 2026-08-19時点の観測

| 役割 | path | 観測version | SHA-256 |
| --- | --- | --- | --- |
| shell既定 | `/Users/kenn/.local/bin/codex` → `/Users/kenn/.codex/packages/standalone/current/bin/codex` | `codex-cli 0.148.0` | 下の0.148.0と同一 |
| 保存済みstandalone | `/Users/kenn/.codex/packages/standalone/releases/0.144.0-aarch64-apple-darwin/` | `codex-cli 0.144.0` | main binary `978740e6bcbd9af2f850823b723fb74f16d8d1e44de05f7dd6737ae631f72017` |
| 保存済みstandalone | `/Users/kenn/.codex/packages/standalone/releases/0.146.0-aarch64-apple-darwin/` | `codex-cli 0.146.0` | main binary `ae1d3ffe6d48aec6a4dc3f50e7eb8e0d11962485a6a9406c5a7012139383da02` |
| 保存済みstandalone | `/Users/kenn/.codex/packages/standalone/releases/0.148.0-aarch64-apple-darwin/` | `codex-cli 0.148.0` | main binary `b0308517b20543012fa2171aa3d46ce455a7456c4eb2a552ab9468ba4eeb1e50` |
| Desktop内蔵 | `/Applications/ChatGPT.app/Contents/Resources/codex` | `codex-cli 0.148.0-alpha.15` | main binary `7645c3caf5607e4528eb3a15b12496c284c2a918939aed34e863c760c1b421e7` |

四つのmain binaryはいずれもApple code signingの`TeamIdentifier=2DC432GLL2`を観測した。standalone releaseにはcompanion executableと同梱toolがあるため、保存単位をmain binary一個に縮小せずrelease directory全体とする。

依頼中の`0.140`と`0.147`は構成例であり、現在のhost-local registryには登録していない。必要になった場合はexact releaseを別途取得して同じ登録gateへ通す。

## 導入済みcommand

| command | 更新追従 | 2026-08-19のversion | 用途 |
| --- | --- | --- | --- |
| `codex` | する | `0.148.0` | 通常利用のdefault standalone CLI |
| `codex-current` | する | `0.148.0` | currentを明示する便宜alias。formal dispatchではpreflight freezeが必要 |
| `codex-0.144` | しない | `0.144.0` | immutable registry bundle |
| `codex-0.146` | しない | `0.146.0` | immutable registry bundle |
| `codex-0.148` | しない | `0.148.0` | immutable registry bundle |

## 責務の分離

```text
ChatGPT Desktop / Remote
  └─ アプリ内蔵runtime + /Users/kenn/.codex
     試験harnessから参照しない

Codex evaluation runtime registry
  ├─ immutable runtime bundles
  ├─ runtime manifests
  └─ mutable alias metadata
     preflightまでしか参照しない

試験harness
  ├─ aliasをexact runtime identityへ解決
  ├─ compatibility preflightを保存
  ├─ atomic runごとのCODEX_HOMEを作成
  ├─ exact binaryをabsolute pathで起動
  └─ private evidenceを収集後にrunをseal
```

Desktopの内蔵binaryを直接formal runへ使わない。アプリ更新でpathが同じままbytesが変わるためである。standalone updaterが管理する`/Users/kenn/.codex/packages/standalone/current`も同じ理由でformal runへ直接使わない。

## 配置

実装時のhost-local正本を次のように置く。

```text
/Users/kenn/.local/share/codex-eval/
├── runtimes/
│   ├── codex-cli-0.144.0-aarch64-apple-darwin-<bundle-sha256>/
│   │   ├── bundle/                  # release directory全体。登録後は変更禁止
│   │   └── manifest.json
│   ├── codex-cli-0.146.0-aarch64-apple-darwin-<bundle-sha256>/
│   └── codex-cli-0.148.0-aarch64-apple-darwin-<bundle-sha256>/
├── aliases/
│   ├── codex-0.144.json
│   ├── codex-0.146.json
│   ├── codex-0.148.json
│   └── codex-current.json           # mutable。dispatch receiptでは使用禁止
├── auth-seeds/                       # mode 0700。repositoryと公開resultの対象外
│   └── <auth-context-id>/
└── locks/

/Users/kenn/repos/_verification/codex-eval-runs/
└── <campaign-id>/<slot-id>/
    ├── codex-home/                   # atomic run専用CODEX_HOME
    ├── workspace/
    ├── private/
    └── run-receipt.json
```

runtime registryを`~/.codex`の外へ置く。Desktop、Remote、standalone updater、session保守および試験runtime保守の書込み対象を分離するためである。repositoryにはbinary、credential、生sessionまたは非公開raw logをcommitしない。

## Runtime登録contract

`manifest.json`は最低限、次を持つ。

```json
{
  "schema_version": "codex-eval-runtime-manifest/v1",
  "runtime_id": "codex-cli-0.146.0-aarch64-apple-darwin-<bundle-sha256>",
  "product": "codex-cli",
  "version_output": "codex-cli 0.146.0",
  "target": "aarch64-apple-darwin",
  "bundle_path": "/Users/kenn/.local/share/codex-eval/runtimes/<runtime-id>/bundle",
  "entrypoint": "bin/codex",
  "bundle_sha256": "<canonical-tree-hash>",
  "entrypoint_sha256": "<sha256>",
  "codesign_team_identifier": "2DC432GLL2",
  "source": {
    "kind": "preserved-standalone-release | desktop-copy | verified-download",
    "observed_path": "<source-path>",
    "observed_at": "<RFC3339>"
  },
  "registration_status": "registered"
}
```

登録は次をすべて満たした場合だけ成功とする。

- sourceを新しいruntime directoryへcopyし、copy後のcanonical tree hashを計算する。
- entrypointの`--version`が申告versionと完全一致する。
- platformがhostと一致する。
- `codesign --verify --deep --strict`とTeam Identifier観測をreceiptへ残す。
- bundle内のsymlinkがbundle外を指していない。
- 登録先に同じ`runtime_id`がある場合、bytesが完全一致するときだけ再利用する。
- 登録後のbundleは読取り専用とし、自己更新を実行しない。

main binary hashとbundle hashを分ける。main binaryが同じでもcompanion executableや同梱toolが違えば別runtime identityとする。

## Aliasとwrapperのcontract

利用者向けには次の名前を提供できる。

```text
codex-0.144
codex-0.146
codex-current
```

ただしaliasは便宜的な選択名であり、評価identityではない。動作は次に限定する。

1. harness preparationでalias manifestを読む。
2. aliasが指す`runtime_id`を解決する。
3. manifest、bundle hash、entrypoint hash、署名および`--version`を再検証する。
4. exact absolute pathとmanifest hashをpreflight receiptへ保存する。
5. dispatchはaliasを再解決せず、receiptにあるexact pathだけを使う。

`codex-current`は「その場の最新版」を試すdiagnostic用途に限る。formal comparisonではpreflightが`current`をexact `runtime_id`へ解決した後にだけ使える。wave途中でaliasが変わっても、既発行receiptは変わらない。

wrapperは引数を暗黙に追加しない。versionごとのflag差を隠すとadapter identityが不明になるため、CLI flagsは評価Profileとadapterが明示する。wrapperが担当するのはruntime解決、identity検証、起動およびreceipt用観測だけである。

## `CODEX_HOME`隔離contract

`CODEX_HOME`はCLI version単位ではなくatomic run単位にする。同じversionでも並行slotが一つのhomeを共有してはならない。

run開始時には空の`codex-home/`をmode `0700`で作り、認証に必要なmaterialだけをprivate `auth-seed`からcopyする。次はcopyしない。

- `config.toml`
- `models_cache.json`
- `skills/`
- `plugins/`
- `memories/`
- `rules/`
- `sessions/`、`archived_sessions/`および履歴database
- Desktop / Remoteのglobal state

公式CLI referenceでは、`--ignore-user-config`は`$CODEX_HOME/config.toml`を読み込まないが、authenticationは引き続き`CODEX_HOME`を使う。また`--ephemeral`が抑止するのはsession rolloutのdisk保存である。このため、instruction隔離と認証隔離を同じflagで済ませず、home自体を分ける。

認証materialはsecretであり、raw bytes、tokenまたはcredential hashをpublic resultへ出さない。private receiptには`auth_context_id`、auth mode、seed generation、login statusの成否だけを残す。credential更新が必要な場合は評価slot中に共通seedを書き換えず、lock下で新しいseed generationを作り、そのgenerationを次waveのpreflightへ固定する。

## Atomic run lifecycle

1. **prepare**: Profile、exact runtime、adapter、model、reasoning、permission、fixture、TaskSpec、oracle、rating、token accountingおよびauth contextをbindする。
2. **preflight**: runtime bundleを再検証し、`CODEX_HOME`が新規であること、出力先が未使用であること、adapterがそのCLI versionの必須flagsをsupportすることを確認する。
3. **provision**: run固有homeを作り、認証materialだけをcopyする。
4. **execute**: exact absolute pathを呼び、`CODEX_HOME=<run-home>`をprocess environmentへ明示する。`PATH`の`codex`へfallbackしない。
5. **collect**: stdout、stderr、exit、単調時計elapsed、terminal usage、root thread identityおよび必要なdescendant sessionをprivate領域へwrite-onceで保存する。
6. **seal**: 実行後のversion/hash drift、session completeness、token accountingおよび出力schemaを確認し、receiptをsealする。
7. **retain / compact**: raw sessionはaccountingと監査が完了するまで保持する。その後の圧縮または削除は、既存long-run storageのreceipt-bound手順へ渡し、実行と同時に行わない。

all-agent token accountingがpersisted root / descendant sessionを要求するProfileでは`--ephemeral`を禁止する。単発でsession accountingを使わない非評価probeだけが、別の`session_mode`として`--ephemeral`を選べる。

## Compatibility key

CLI共存後も、比較可能性はCLI versionだけでは決まらない。最低限、次をcompatibility keyへ含める。

- `runtime_id`、bundle hash、entrypoint hash
- adapter source hashとadapter contract revision
- model identifierと、snapshotかmutable aliasかの区別
- reasoning effort
- permission / sandbox / approval
- feature flagsおよびmulti-agent条件
- instruction、config、rules、skills、plugins、memoriesの隔離contract
- `CODEX_HOME` scopeとsession mode
- token accounting revisionとelapsed boundary
- target、case、fixture、TaskSpec、oracle、ratingおよびprompt identity
- host architectureと、結果へ影響し得るOS / Python / harness identity

別CLIで得たresultは、CLI差を独立変数として事前固定したruntime比較でだけ比較する。prompt-only comparisonの保存済み基準へ別CLIのrunを混ぜない。CLIを同じにしてもmutable model aliasまたはbackendが変わった可能性があれば、その差をprompt効果またはCLI効果へ帰属しない。

## 既存harnessへ必要な変更

現在の基盤には二種類の経路がある。

- `run_semantic_protocol_qualification.py`系列は`--codex <absolute-path>`を受け、version driftをpreflightで拒否する。この経路はexact binary固定の基礎をすでに持つ。
- `run_codex_evaluation.py`はcommandとversion観測にliteral `codex`を使い、`CODEX_HOME`をenvironmentから読む。この経路は`PATH`と呼出し元environmentに依存するため、そのままでは共存contractを満たさない。

実装時は、共通の`runtime_ref`を両経路へ渡し、次のように統一する。

```text
runtime_ref
  → registry resolver
  → exact binary + verified manifest
  → preflight receipt
  → run-specific CODEX_HOME
  → adapter subprocess
  → postflight identity verification
```

`run_codex_evaluation.py`からliteral `codex`を除き、Profileまたはpreflight receiptにないbinaryを起動不能にする。semantic qualification側もversion文字列だけでなくbundle hashとmanifest hashを検証する。既存resultやProfileは遡及変更せず、新しいruntime-registry revisionの比較系列として導入する。

## 導入順序と停止条件

### Phase 1: registryだけを作る

保存済み0.144.0と0.146.0をcopyし、manifest、tree hash、署名receiptおよびaliasを作る。Desktop、`~/.codex/packages/standalone/current`、既存runnerおよび評価結果は変更しない。

停止条件:

- source/copy hashの不一致
- signature不成立
- bundle外symlink
- 同じversion文字列でbytesが異なるbundleを一つのaliasへ上書きしようとした

### Phase 2: 非評価transport probe

各runtimeについて、空のrun固有homeへ認証materialだけを入れ、固定JSON一件でlogin status、JSONL transport、terminal usage、session保存およびerror event captureを確認する。probeはruntime capability確認であり、Candidateまたは比較resultにしない。

停止条件:

- model応答前のcache / skills / config互換エラー
- stdoutとstderrの個別保存不能
- exact runtime以外のprocess起動
- sessionまたはprimary usageの欠落
- auth seedの共有書換え

### Phase 3: harness統合

まず`--codex`をすでに持つsemantic qualification経路へbundle hash検証とrun home provisioningを追加する。次にliteral `codex`を持つ通常評価経路をruntime receipt必須へ変更する。

### Phase 4: current更新からの独立性試験

固定runtimeで非評価probeを開始し、別途`codex-current` aliasだけを更新する。既発行receiptが同じexact bundleを使い続け、Desktop / Remoteも従来の内蔵runtimeを使うことを確認する。これを通過するまでformal comparisonを発行しない。

## 採用する設計判断

- Desktop / Remote用`~/.codex`と試験homeを分ける。
- CLIは一個のbinaryではなくrelease bundle全体を保存する。
- aliasは選択UIに限定し、dispatch identityにはexact pathとhashを使う。
- `codex-current`はpreflight時にfreezeし、wave中の追従を禁止する。
- 認証以外のhome状態を新しいrunへcopyしない。
- persisted transcriptを使う測定では`--ephemeral`を使わない。
- 旧CLI固定とserver-side runtime固定を同義にしない。
- 0.144.0、0.146.0および0.148.0はhost-local registryへ登録済みとする。0.140 / 0.147は必要なexact releaseを取得できた後に同じgateで追加する。

## 公式仕様への参照

- [Codex CLI](https://learn.chatgpt.com/docs/codex/cli): standalone installer、sign-inおよび`codex exec`をrepeatable workflowから使えること。
- [Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli): `--ignore-user-config`、`--ephemeral`、`--strict-config`、`codex login status`およびCLI flagの正本。
- [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference): `$CODEX_HOME`、profile configおよびcredential store設定の正本。
