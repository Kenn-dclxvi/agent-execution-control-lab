# 試験storage seal拡張

## 目的

通常試験と長期実行でストレージ枯渇を起こさないため、発行前の容量ガード、Layer 1のclonefile必須化、採点・登録後の検証付き一括圧縮を提供する。旧二段階保存の互換経路も保持する。評価基盤のLayer、KPI、schema、比較条件は変更しない。directory名とCLIの`batch`表記は履歴互換のため保持するが、直下に`cycle/`を持つ通常の試験rootにも同じsealとcompactを適用できる。

この拡張が作るアーカイブとreceiptは生のエビデンスであり、評価済み、採用済み、release済みを意味しない。非公開の生アーカイブはcommitしない。

## 新しい通常試験の標準経路

2026-11-09から、新しい通常試験と長期実行の各バッチでは、採点・結果登録後の一括圧縮を標準とする。以下の旧二段階処理は既存試験の継続・復元用の互換経路として維持する。

次回試験に向けた、固定済みLayer 1と作業コピーの内容・属性を分離して重複を除く方式は、[最小容量方式の登録](../../../docs/evaluation-storage-maintenance.md#次回試験に向けた最小容量方式の登録2026-11-09)にまとめている。保存済み70実行で検証済みだが、通常経路への実装は未完了である。以下の`archive-batch`は現行の一括圧縮であり、新方式へ切り替わったとは扱わない。次回適用前の実装・検証と、利用者への試験内容の確認は登録文書の手順に従う。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py archive-batch \
  --batch /absolute/path/to/trial-root
```

全実行が終了し、valid runの使用量・採点・採点証拠、および`cycle/layer4/result-registration.json`があることを確認する。`--cycle-path`は同じ試験内の別名cycleを指定できる。一括圧縮の前に`seal-batch`を実行して作業コピーを消さない。

使用量記録はCodexの`all-agent-usage/v1`とClaudeの`claude-all-agent-usage/v1`に対応し、どちらも非負の整数の合計値と空でないセッション記録を必要とする。保存済みの記録形式は変更しない。

`compact/`を除く試験一式を通常のtarとzstd（既定level 3、窓128 MiB）で圧縮する。`zstd -t`と別の一時領域への展開後の照合を行い、パス集合・種類・内容・リンク先・権限・ACL・所有者・ファイルフラグ・更新時刻・拡張属性が一致することを確認する。`com.apple.provenance`と格納用最上位ディレクトリの更新時刻だけを一致条件から除く。ファイルや作業コピー内の更新時刻、他の拡張属性は除外しない。これらの例外はマニフェストに記録する。

元データの同時変更、復元不一致、未採点、登録記録の欠落、容量不足では削除を開始しない。成功時だけ`cycle/layer2/evidence/<run_id>/workspace`を削除する。共通環境へのリンクはリンクとして保存し、削除時にもリンク先をたどらない。共通環境・固定済みLayer 1・結果の登録記録・その他の実行証拠は残す。利用者のCodex設定を変更する処理は呼び出さない。

出力は`compact/batch-evidence.tar.zst`、`batch-archive-manifest.json`、`batch-prune-receipt.json`。既存出力を上書きせず、旧形式の記録がある試験は拒否する。削除記録の`status: complete`を通常試験の完了条件とする。失敗時は元データを保持し、残った圧縮記録を確認してから再開方法を決める。

復元は新しい空のディレクトリへ行う。

```bash
mkdir /absolute/path/to/restored-batch
zstd -dc /absolute/path/to/batch-evidence.tar.zst \
  | tar --acls --xattrs -xpf - -C /absolute/path/to/restored-batch
```

固定済み評価セットの保管場所と結果の外部registryは引き続き保持する。アーカイブ内の参照先を勝手に変更せず、再集計には保存済みの選択記録と単価表を使う。この処理は保存方法の変更であり、実行条件・採点・KPIを変更しない。

### 停止済みの既存試験を現状のまま保存する

結果登録・採点・使用量記録の完全性は、評価結果として扱うための条件であり、既存ファイルを復元するための条件ではない。履歴保持と評価状態の区別はルートの`AGENTS.md`、結果登録の条件は[`prompt-comparison-workflow.md`](../../../docs/prompt-comparison-workflow.md)に従う。欠落した証拠や未完了の状態は補完せず、そのまま保存する。

既存試験の保守を明示的に依頼された場合は、対象へ書き込む試験プロセスが停止していることを確認し、次を使う。複数の試験が親ディレクトリを共有する場合も、対象cycleそのものを圧縮単位にすることで、兄弟の試験や親の記録を変更しない。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py archive-batch \
  --batch /absolute/path/to/cycle --cycle-path . --preserve-existing
```

この指定では、実在する`layer2/evidence/*/workspace`を保存対象とし、登録・採点・実行終了記録の欠落を拒否理由にしない。通常の一括圧縮と同じ完全復元・属性照合・元データ不変の確認を必須とし、検証後に作業コピーだけを削除する。Layer 1とその他の証拠、存在する登録記録は残す。圧縮用記録には`preserved-batch-archive/v1`と`preserved-batch-prune/v1`を使い、欠けている登録記録のハッシュは`null`とする。圧縮の完了を試験・採点・結果登録の完了へ読み替えない。通常試験の完了手順にはこの指定を使わない。

### 試験終了時の実行別ホームの保存

`workspace`だけでは、別の場所に生成される`codex-homes`内のキャッシュや実行記録は片付かない。今後の試験では、そのホームを使う全実行・再試行・関連バッチが終了し、書き込むプロセスが停止した後、作業コピーの圧縮に加えて次を必ず実行する。配置を推測せず、試験時に使った実際の`codex-homes`を指定する。複数ある場合はそれぞれを処理する。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py archive-homes \
  --source /absolute/path/to/model/codex-homes
```

実行ID（32桁の16進数）別の実ディレクトリだけを含む`codex-homes`を受け付ける。共通環境や利用者の`~/.codex`は対象にしない。キャッシュ、プラグイン、設定、セッションを省略せず、全体を隣の`codex-homes.archive/homes.tar.zst`へ保存する。完全復元時の照合項目と2項目の除外条件は通常の一括圧縮と同じとし、削除直前の元データ不変とアーカイブのSHA-256も確認してから、指定された`codex-homes`だけを削除する。リンク先へは書き込まない。Layer 1、結果登録記録、共通環境は対象外のまま保持する。

`codex-homes.archive/manifest.json`にパス・内容・属性・実行ID・アーカイブのハッシュを保存し、`prune-receipt.json`の`status: complete`をホーム保存の完了条件とする。既存出力は上書きしない。復元不一致や同時変更では削除せず、残された出力と元データを確認する。新しい試験の終了条件には、作業コピー側の削除記録と、使用した全ホームの削除記録の両方を含める。ホームを使わない試験には後者を要求しない。

復元時はマニフェストのSHA-256とアーカイブを照合し、空の元パスへ展開する。実行ID別ディレクトリが復元され、設定やセッション内の元パスは書き換えない。アーカイブは非公開の設定やログを含むためcommitしない。

```bash
mkdir /absolute/path/to/model/codex-homes
zstd -dc /absolute/path/to/model/codex-homes.archive/homes.tar.zst | \
  tar --acls --xattrs -xpf - -C /absolute/path/to/model/codex-homes
```

## 旧二段階処理と長期実行への組み込み順


通常試験では試験root、長期runでは各batchについて、次の順序を固定する。

1. `guard`で次バッチを投入できるか確認する。
2. `materialize-layer1`または`THE_CAPTION_EVAL_COPY_MODE=clonefile`を使い、Layer 1とworkspaceの物理複製をAPFS clonefileへ限定する。
3. Layer 2を実行し、全スロットをterminalにする。
4. `seal-batch`でvalid runのall-agent usageとrating viewを検証する。
5. 完全なワークスペースとLayer 1 fixtureを含むsealアーカイブをストリーミング生成し、圧縮後の全メンバーのhash検証後にだけワークスペースのlive copyを削除する。Layer 1 fixtureは次バッチのclone元として保持する。
6. 削除記録に含まれるワークスペースと完全一致するCodexの`projects`設定だけを削除する。
7. Layer 3採点とLayer 4 result登録後に`compact-batch`を実行する。

Layer 1またはworkspaceを通常のコピーで暗黙に複製するcontrollerは使わない。clonefileを利用できない場合は試験または次batchを開始せず停止する。

## 容量ガード

標準値は新規dispatch停止25 GiB、hard floor 20 GiBである。`estimated-next-batch-gib`を指定した場合は、次バッチ作成後の予測free bytesでdispatchを判断する。停止時はexit code 3を返すため、コントローラは正常な容量停止として扱える。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py guard \
  --path /absolute/path/to/verification-root \
  --sample-log /absolute/path/to/long-run/capacity-samples.jsonl \
  --estimated-next-batch-gib 2.5
```

sample logはappend-only JSONLである。hard floor未満では、新規アーカイブ作成も含めて自動継続せず、人が容量を回復してから再開する。

## Layer 1 materialization

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py materialize-layer1 \
  --source /absolute/path/to/source-cycle/layer1 \
  --destination /absolute/path/to/new-batch/cycle/layer1 \
  --receipt /absolute/path/to/new-batch/layer1-materialization.json
```

標準は`THE_CAPTION_EVAL_COPY_MODE=clonefile`相当でfail closedする。別ファイルシステムで通常のコピーを明示的に許す場合だけ`--allow-copy-fallback`を付ける。このfallbackは8時間runの標準運用にはしない。

## Execution seal

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py seal-batch \
  --batch /absolute/path/to/trial-or-batch-root
```

過去試験の保守で採点済み`rating-view`が存在する場合だけ、`--reuse-existing-rating-views`を指定できる。既存の3ファイル構造、validationとadapter evidence、final response、対応するLayer 3 ratingを照合し、`result.diff`を採点時の正本として上書きせずにarchiveへ含める。不一致または余分なentryがあればseal前に停止する。

再試行履歴により正本cycleが`cycle-r3`などの別名で保存されている場合は、batch内の実ディレクトリを`--cycle-path cycle-r3`で明示する。絶対path、batch外、`..`、symlink経由は拒否する。`compact-batch`にも同じ`--cycle-path`を指定し、execution seal receiptとの一致を必須とする。

標準では`$CODEX_HOME/config.toml`、未設定時は`~/.codex/config.toml`も保守する。対象は、このバッチの`execution-prune-receipt.json`に記録されたワークスペースのパスとの完全一致だけである。別評価や通常のプロジェクトの存在しないパスは削除しない。設定は有効なTOMLであることを更新前後に確認し、同時更新を検出した場合は最大3回再試行する。結果は`compact/codex-project-config-prune-receipt.json`へwrite-onceで記録する。この保守に失敗してもexecution sealと評価結果は失効させず、command結果へ`warning`を返す。

一時的に保守を無効化する場合だけ`--skip-codex-config-cleanup`を指定する。別の設定を使う検証では`--codex-config /absolute/path/to/config.toml`を指定できる。

valid runごとに次を確認する。

- `all-agent-usage/v1`と1件以上のsessionが存在する
- adapterのprompt overlay commitと最終変更のパスが存在する
- bundle manifestのtargetを除いた`rating-view/result.diff`を生成できる
- `final-response.txt`と、機械的なpass/failを推定しない`validation.json`を固定できる

`result.diff`は一時Git indexを使うため、tracked変更、削除、untracked成果を含み、実ワークスペースのindexを変更しない。bundle targetだけをblind viewから除外する。

次をwrite-onceで作る。

```text
batch-001/
├── compact/
│   ├── execution-evidence.tar.zst
│   ├── execution-seal.json
│   └── execution-prune-receipt.json
└── cycle/layer2/evidence/<run_id>/rating-view/
    ├── result.diff
    ├── validation.json
    └── final-response.txt
```

アーカイブは完全なワークスペース、自己完結したLayer 1 fixture、空のディレクトリを含む。非圧縮tar全体を一時作成せず、tarからzstdへストリーミングし、long-distance matchingで反復ワークスペース内の同一内容を圧縮する。圧縮後のアーカイブを再展開のストリームとして読み、member set、type、mode、regular file content、symlink target、`zstd -t`を検証する。manifestとアーカイブを書けた後にワークスペースのlive copyだけを削除し、Layer 1 fixtureは次バッチのclone元かつ固定済みアーティファクトとして保持する。再生成契約を保存アーティファクトの代替にはしない。ratingに必要なケース、execution、usage、rating view、capsule、bindingは未圧縮のまま残すため、Layer 3を後続実行できる。

除外runはquality rating対象ではないためrating viewを作らないが、terminalな`excluded`を確認し、ワークスペースをアーカイブへ含めて検証したうえでlive copyを削除する。valid runのall-agent usageが1件でも不完全ならバッチ全体をpruneしない。

## 最終圧縮

Layer 3採点とLayer 4 result登録が完了したバッチだけを最終圧縮する。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py compact-batch \
  --batch /absolute/path/to/trial-or-batch-root
```

`cycle/layer4/result-registration.json`とexecution seal receiptを必須とし、Layer 2〜4のlive evidenceを`compact/final-evidence.tar.zst`へ保存してhash検証する。検証後はLayer 2〜3とrunner evidenceを削除し、次を直接参照可能な状態で残す。

- `compact/`のアーカイブ、manifest、receipt
- `cycle/layer1/`の固定セット、ケース、自己完結fixture
- `cycle/layer4/result-registration.json`
- バッチ直下の`summary.json`と`plan.json`（存在する場合）

完全なバッチは保持中の`cycle/layer1/`を起点とし、executionアーカイブを先に、finalアーカイブを後から同じ空のディレクトリへ展開して復元する。executionアーカイブにもLayer 1の同一内容を含むため、live fixtureを失った場合もアーカイブだけで復元できる。前者がfixtureとワークスペースを、後者がLayer 3 ratingとLayer 4登録を含む。

```bash
mkdir /absolute/path/to/restored-batch
zstd -dc /absolute/path/to/execution-evidence.tar.zst \
  | tar -xf - -C /absolute/path/to/restored-batch
zstd -dc /absolute/path/to/final-evidence.tar.zst \
  | tar -xf - -C /absolute/path/to/restored-batch
```

sealまたはcompactの再実行は既存の出力を上書きせず拒否する。アーカイブを削除する保持期限はこの拡張では決めず、別の明示的なretention判断へ残す。
