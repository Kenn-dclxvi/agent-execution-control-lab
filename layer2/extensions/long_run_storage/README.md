# Long-run storage extension

## 目的

8時間程度の反復実行でstorage枯渇を起こさないため、batch dispatch前の容量guard、Layer 1のclonefile必須化、実行直後のevidence seal、登録後の最終圧縮を提供する。評価基盤のLayer、KPI、schema、比較条件は変更しない。

このextensionが作るarchiveとreceiptはraw evidenceであり、評価済み、採用済み、release済みを意味しない。非公開のraw archiveはcommitしない。

## 長期controllerへの組み込み順

各batchについて、次の順序を固定する。

1. `guard`で次batchを投入できるか確認する。
2. `materialize-layer1`で前batchのLayer 1をAPFS clonefileとして複製する。
3. Layer 2を実行し、全slotをterminalにする。
4. `seal-batch`でvalid runのall-agent usageとrating viewを検証する。
5. 完全なworkspaceとLayer 1 fixtureを含むseal archiveをstreaming生成し、圧縮後の全member hash検証後にだけworkspaceのlive copyを削除する。Layer 1 fixtureは次batchのclone元として保持する。
6. 削除記録に含まれるworkspaceと完全一致するCodexの`projects`設定だけを削除する。
7. Layer 3採点とLayer 4 result登録後に`compact-batch`を実行する。

前batchの`cycle/layer1`を通常copyするcontrollerは使わない。clonefileを利用できない場合はbatchを開始せず停止する。

## Capacity guard

標準値は新規dispatch停止25 GiB、hard floor 20 GiBである。`estimated-next-batch-gib`を指定した場合は、次batch作成後の予測free bytesでdispatchを判断する。停止時はexit code 3を返すため、controllerは正常な容量停止として扱える。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py guard \
  --path /absolute/path/to/verification-root \
  --sample-log /absolute/path/to/long-run/capacity-samples.jsonl \
  --estimated-next-batch-gib 2.5
```

sample logはappend-only JSONLである。hard floor未満では、新規archive作成も含めて自動継続せず、人が容量を回復してから再開する。

## Layer 1 materialization

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py materialize-layer1 \
  --source /absolute/path/to/source-cycle/layer1 \
  --destination /absolute/path/to/new-batch/cycle/layer1 \
  --receipt /absolute/path/to/new-batch/layer1-materialization.json
```

標準は`THE_CAPTION_EVAL_COPY_MODE=clonefile`相当でfail closedする。別filesystemで通常copyを明示的に許す場合だけ`--allow-copy-fallback`を付ける。このfallbackは8時間runの標準運用にはしない。

## Execution seal

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py seal-batch \
  --batch /absolute/path/to/batch-001
```

標準では`$CODEX_HOME/config.toml`、未設定時は`~/.codex/config.toml`も保守する。対象は、このbatchの`execution-prune-receipt.json`に記録されたworkspace pathとの完全一致だけである。別評価や通常projectの存在しないpathは削除しない。設定は有効なTOMLであることを更新前後に確認し、同時更新を検出した場合は最大3回再試行する。結果は`compact/codex-project-config-prune-receipt.json`へwrite-onceで記録する。この保守に失敗してもexecution sealと評価結果は失効させず、command結果へ`warning`を返す。

一時的に保守を無効化する場合だけ`--skip-codex-config-cleanup`を指定する。別の設定を使う検証では`--codex-config /absolute/path/to/config.toml`を指定できる。

valid runごとに次を確認する。

- `all-agent-usage/v1`と1件以上のsessionが存在する
- adapterのprompt overlay commitと最終変更pathが存在する
- bundle manifestのtargetを除いた`rating-view/result.diff`を生成できる
- `final-response.txt`と、機械的なpass/failを推定しない`validation.json`を固定できる

`result.diff`は一時Git indexを使うため、tracked変更、削除、untracked成果を含み、実workspaceのindexを変更しない。bundle targetだけをblind viewから除外する。

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

archiveは完全なworkspace、自己完結したLayer 1 fixture、空directoryを含む。非圧縮tar全体を一時作成せず、tarからzstdへstreamingし、long-distance matchingで反復workspace内の同一内容を圧縮する。圧縮後のarchiveを再展開streamとして読み、member set、type、mode、regular file content、symlink target、`zstd -t`を検証する。manifestとarchiveを書けた後にworkspaceのlive copyだけを削除し、Layer 1 fixtureは次batchのclone元かつ固定済みartifactとして保持する。再生成契約を保存artifactの代替にはしない。ratingに必要なcase、execution、usage、rating view、capsule、bindingは未圧縮のまま残すため、Layer 3を後続実行できる。

除外runはquality rating対象ではないためrating viewを作らないが、terminalな`excluded`を確認し、workspaceをarchiveへ含めて検証したうえでlive copyを削除する。valid runのall-agent usageが1件でも不完全ならbatch全体をpruneしない。

## Final compact

Layer 3採点とLayer 4 result登録が完了したbatchだけを最終圧縮する。

```bash
python3 layer2/extensions/long_run_storage/long_run_storage.py compact-batch \
  --batch /absolute/path/to/batch-001
```

`cycle/layer4/result-registration.json`とexecution seal receiptを必須とし、Layer 2〜4のlive evidenceを`compact/final-evidence.tar.zst`へ保存してhash検証する。検証後はLayer 2〜3とrunner evidenceを削除し、次を直接参照可能な状態で残す。

- `compact/`のarchive、manifest、receipt
- `cycle/layer1/`の固定set、case、自己完結fixture
- `cycle/layer4/result-registration.json`
- batch直下の`summary.json`と`plan.json`（存在する場合）

完全なbatchは保持中の`cycle/layer1/`を起点とし、execution archiveを先に、final archiveを後から同じ空directoryへ展開して復元する。execution archiveにもLayer 1の同一内容を含むため、live fixtureを失った場合もarchiveだけで復元できる。前者がfixtureとworkspaceを、後者がLayer 3 ratingとLayer 4登録を含む。

```bash
mkdir /absolute/path/to/restored-batch
zstd -dc /absolute/path/to/execution-evidence.tar.zst \
  | tar -xf - -C /absolute/path/to/restored-batch
zstd -dc /absolute/path/to/final-evidence.tar.zst \
  | tar -xf - -C /absolute/path/to/restored-batch
```

sealまたはcompactの再実行は既存outputを上書きせず拒否する。archiveを削除する保持期限はこのextensionでは決めず、別の明示的なretention判断へ残す。
