# long-run storage拡張

## 目的

8時間程度の反復実行でストレージ枯渇を起こさないため、バッチのdispatch前の容量ガード、Layer 1のclonefile必須化、実行直後のevidence seal、登録後の最終圧縮を提供する。評価基盤のLayer、KPI、schema、比較条件は変更しない。

この拡張が作るアーカイブとreceiptは生のエビデンスであり、評価済み、採用済み、release済みを意味しない。非公開の生アーカイブはcommitしない。

## 長期コントローラへの組み込み順

各バッチについて、次の順序を固定する。

1. `guard`で次バッチを投入できるか確認する。
2. `materialize-layer1`で前バッチのLayer 1をAPFS clonefileとして複製する。
3. Layer 2を実行し、全スロットをterminalにする。
4. `seal-batch`でvalid runのall-agent usageとrating viewを検証する。
5. 完全なワークスペースとLayer 1 fixtureを含むsealアーカイブをストリーミング生成し、圧縮後の全メンバーのhash検証後にだけワークスペースのlive copyを削除する。Layer 1 fixtureは次バッチのclone元として保持する。
6. 削除記録に含まれるワークスペースと完全一致するCodexの`projects`設定だけを削除する。
7. Layer 3採点とLayer 4 result登録後に`compact-batch`を実行する。

前バッチの`cycle/layer1`を通常のコピーで複製するコントローラは使わない。clonefileを利用できない場合はバッチを開始せず停止する。

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
  --batch /absolute/path/to/batch-001
```

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
  --batch /absolute/path/to/batch-001
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
