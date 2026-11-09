# 検証storageの維持

## 目的

検証用cloneの独立性とappend-only resultを維持したまま、同一fixtureとGit objectの物理複製を抑え、期限切れscratch runだけを検証付きで削除する。

この運用はKPI、互換条件、prompt set result、比較viewを変更しない。raw evidenceの削除をprompt setの優劣、採用、release判断へ読み替えない。

## Copy-on-Write materialization

`scripts/evaluation_loop.py`のLayer 1 fixture固定とLayer 2 workspace作成は、`scripts/storage_copy.py`を使用する。標準の`auto` modeはmacOSの`/bin/cp -cR`を試し、clonefileを利用できないfilesystemでは`shutil.copytree`へfallbackする。

どちらのmodeも次の境界を維持する。

- sourceとdestinationは別directoryで、片方の変更を他方へ反映しない
- symlinkをsymlinkとして保持する
- hardlinkとGit alternatesを使わない
- copy方式をevaluation set identity、互換条件、3 KPIへ含めない

明示的な切替は環境変数`THE_CAPTION_EVAL_COPY_MODE`で行う。

| 値 | 動作 |
| --- | --- |
| `auto` | clonefileを試し、失敗時に通常copyへfallbackする |
| `clonefile` | clonefileを必須とし、使用できなければfail closedする |
| `copy` | 常に通常copyを使う |

## Audit

検証rootと、このrepositoryに保存したraw evidence参照を一緒に監査する。

```bash
python3 scripts/evaluation_storage.py audit \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --repository /Users/kenn/repos/agent-execution-control-lab
```

reportはrun別のallocated bytes、最終更新からの日数、repository参照、外部からのsymlink、`layer4/result-registration.json`、Git pack重複量を出す。標準値は次のとおり。

- unreferenced scratch保持: 3日
- soft limit: 3 GiB
- hard limit: 5 GiB

soft / hard limitは運用上の調査開始点であり、raw evidenceを自動削除する許可ではない。filesystem free spaceはreport値を監視し、40 GiB未満になったら新規大規模runの前にauditする。

### Git packの物理重複

self-contained fixtureの`.git/objects/pack/`は論理的には各cloneへ保持したまま、byte-identicalな`.pack`だけをclonefileで再materializeできる。dry-runは全対象のSHA-256を検証してwrite-once manifestを作る。

```bash
python3 scripts/evaluation_storage.py deduplicate-packs \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --manifest /tmp/evaluation-pack-dedup-manifest.json
```

適用時は全source / targetのsizeとSHA-256、Git pack lock不在を先に再検証し、同じdirectoryの一時cloneから原子的に置換する。

```bash
python3 scripts/evaluation_storage.py deduplicate-packs \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --manifest /tmp/evaluation-pack-dedup-manifest.json \
  --apply \
  --receipt /tmp/evaluation-pack-dedup-receipt.json
```

pathとbyte内容は維持され、置換後の各packは独立に変更できる。hardlink、Git alternates、共有object directoryは使わない。`du`は共有blockを各fileへ計上することがあるため、実際の回収量はreceiptのfilesystem free bytes差分で確認する。

### 安定した通常ファイルの物理重複

別APFS containerへの`rsync`でLayer 1やworkspace全体のclonefile関係が失われた場合は、Git pack以外の安定した通常ファイルも共有blockへ戻せる。標準では24時間以上更新されていない64 KiB以上のファイルだけを対象とし、`.tar.zst`、Git pack、hardlink、symlink、lockを除外する。dry-runは内容、mode、owner、flags、mtime、拡張属性をwrite-once manifestへ固定する。

```bash
python3 scripts/evaluation_storage.py deduplicate-files \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --manifest /tmp/evaluation-file-dedup-manifest.json
```

適用時は全source / targetを再検証し、各targetの置換直前と置換後にも内容と拡張属性を確認する。圧縮アーカイブを展開せず、pathと独立変更可能性を維持する。

```bash
python3 scripts/evaluation_storage.py deduplicate-files \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --manifest /tmp/evaluation-file-dedup-manifest.json \
  --apply \
  --receipt /tmp/evaluation-file-dedup-receipt.json
```

## Guarded GC

自動GC候補は、次をすべて満たす`<root>/runs/`直下directoryだけである。

1. repository内に絶対path参照がない
2. storage内の別pathからsymlink参照されていない
3. 配下に`layer4/result-registration.json`がない
4. 最終更新から`scratch-days`以上経過している

まずwrite-once manifestを作る。

```bash
python3 scripts/evaluation_storage.py gc \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --repository /Users/kenn/repos/agent-execution-control-lab \
  --manifest /tmp/evaluation-storage-gc-manifest.json
```

manifestには対象path、allocated bytes、file数、全contentのSHA-256を含む。適用時は参照条件、size、content hashを再検証し、1件でも変化していれば削除を開始しない。

```bash
python3 scripts/evaluation_storage.py gc \
  --root /Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement \
  --repository /Users/kenn/repos/agent-execution-control-lab \
  --manifest /tmp/evaluation-storage-gc-manifest.json \
  --apply \
  --receipt /tmp/evaluation-storage-gc-receipt.json
```

`manifest`と`receipt`は上書きしない。登録済みresult、文書から参照するraw evidence、共有fixtureの参照先は自動GC対象外である。

## 通常試験の一括圧縮

新しい通常試験と長期実行の各バッチは、採点・結果登録後に`archive-batch`で一式を1本の`tar.zst`へ保存する。別の一時ディレクトリへ展開した内容と元データを照合し、削除直前にも元データの不変を確認してから、終了済み実行の作業コピーだけを削除する。コマンドと完了条件は[実行手順](evaluation-loop-manual.md#13-storage-maintenance)、照合条件と復元方法は[圧縮処理の正本](../layer2/extensions/long_run_storage/README.md)に従う。

共通環境、固定済みLayer 1、結果の登録記録は保持する。試験条件やKPIを変更せず、圧縮は計測中の試験と競合させない。既存の二段階アーカイブはそのまま保持し、旧`seal-batch`・`compact-batch`の復元契約を維持する。

実行別ホームのキャッシュや実行記録が`workspace`とは別の`codex-homes`に残るため、今後はそのホームを使う全試験の終了時に`archive-homes --source <実際のcodex-homes>`も必須とする。全内容を圧縮・完全復元照合してから元ホームを削除し、隣の`codex-homes.archive`へアーカイブと検証・削除記録を残す。共通環境や固定済みデータを対象へ広げない。詳しくは[実行別ホームの保存](../layer2/extensions/long_run_storage/README.md#試験終了時の実行別ホームの保存)を参照する。

停止済みの既存試験を現状のまま保存する保守では、結果未登録や採点証拠不足は圧縮の妨げにしない。欠落も含む元の状態を完全復元できることを検証し、作業コピーだけを削除する。`--preserve-existing`の条件と手順は[圧縮処理の正本](../layer2/extensions/long_run_storage/README.md#停止済みの既存試験を現状のまま保存する)に従い、評価状態や結果登録の条件は変更しない。

一括圧縮では圧縮ファイルと復元照合用の一時領域も必要になる。元ファイルの論理サイズの2倍を一時使用量として見積もり、既存の容量ガードを通してから開始する。割当容量にはAPFSの共有領域が重複計上され得るため、削除記録には空き容量の前後値を残し、論理サイズの差を実際の回収量と呼ばない。

## 次回試験に向けた最小容量方式の登録（2026-11-09）

次回試験に向けた実装方針は、固定済みLayer 1と実行ごとの作業コピーについて、ファイル内容の重複を除き、配置・属性を別に保存する方式とする。保存済み1試験で復元・再採点・再集計まで検証済みだが、通常運用への組み込みは未完了である。上記の`archive-batch`がこの方式へ切り替わったとは扱わない。

### 保持するものと減らすもの

- 共通環境、固定済みLayer 1の正本、結果の登録記録を保持する。評価セットの版ごとにLayer 1を一度固定し、保管場所から複製する契約を維持する。`installation.json`と事前照合の記録は試験ごとに残す。
- 固定内容は内容のハッシュをキーに一度だけ保存する。ケースごとのパス、権限、所有者、リンク先、更新時刻、ACL、拡張属性、ファイルフラグは別に記録する。内容が同じで属性だけ違う場合に、内容を再保存しない。
- 実行時の作業コピーは独立して書き込める`clonefile`で作る。共有元へ変更が伝わるハードリンクは使わず、Git管理データも完全復元対象に含める。
- 終了後は固定内容への参照、新規・変更内容、実行ごとの配置・属性・証拠を保存する。70実行分の展開済みコピーを恒久保存しない。完全復元照合が通り、削除直前の元データの不変を確認したものだけを削除する。
- 復元・再採点は1実行ずつ展開して観測後に片付ける。モデル試験の並列上限や計測条件は変更せず、計測中に圧縮を競合させない。
- 過去試験ごとの実行環境の複製は恒久保存せず、再構築に必要な版・識別値・手順を残す。実行別ホームの証拠は保持し、共通環境や利用者の設定を削除対象に含めない。

照合から除外するのは、従来と同じく`com.apple.provenance`の値と最上位の格納ディレクトリの更新時刻だけとする。結果未登録や採点証拠不足は既存データの圧縮を妨げないが、欠落も含む元の状態を復元し、評価済みや登録済みへ状態を変更しない。

### 保存済みデータによる検証結果

対象はC319、`gpt-6.1-terra`、Standard14の14ケース×5回、2026-10-27の`round-2`に保存された70実行である。新しいモデル試験は実施していない。

| 項目 | 通常の一括圧縮 | 前回の差分試作 | 内容と属性を分離した試作 |
| --- | ---: | ---: | ---: |
| 保存容量（検証用メタデータを含む） | 58.37 MiB | 51.40 MiB | 26.34 MiB |
| 保存・復元検証中の追加容量の最大値 | 2.59 GiB | 1.59 GiB | 0.34 GiB |

今回の内訳は固定内容23.81 MiB、追加内容1.93 MiB、配置・属性など0.59 MiBである。通常の一括圧縮から約54.9%削減した。70実行の内容・属性の完全復元、保存済み観測、既存採点器による再採点、保存済み選択記録と登録記録を使った再集計が一致し、コピーへの書き込みが共有元へ影響しないことも確認した。元アーカイブは不変で、一時展開物は削除済みである。

容量の最大値は空き容量を0.1秒間隔で観測した値で、他の処理の変動を含み得る。モデル試験の実行中の最大容量は未計測であり、0.34 GiBを次回試験の必要容量としない。別試験でも固定内容を共有できる場合の追加保存量約2.53 MiBは条件付きの計算で、別試験の実測値ではない。

一次記録はSN7100の`/Volumes/SN7100/_verification/workspace-layer1-review-20261109/review.json`、`measured/report.json`、同ディレクトリの試作コードと圧縮成果物に置く。前回比較は`/Volumes/SN7100/_verification/minimal-storage-comparison-20261109/report.json`を参照する。非公開の生ログはリポジトリへ登録しない。

### 次回試験へ適用する前の作業

1. 試作を通常の保存・復元経路へ組み込む。試作のように既存の一括アーカイブを入力にするのではなく、終了した試験のファイルから直接保存する。Layer 1の固定・複製・事前照合と識別値の意味を維持する。
2. 参照中の固定内容の削除防止、内容の欠落・改変時の停止、中断後の再開を実装する。今回の試作は対象データにないACL・追加の拡張属性・ファイルフラグなどを拒否するため、それらの保持にも対応する。未対応の属性を黙って省略しない。
3. 保存済みの同じ1試験で、内容と属性、再採点、再集計、変更の分離、検証失敗時に元データを削除しないことを確認する。共通環境・固定済みLayer 1・登録記録を変更しない。
4. 適用準備が完了したら、次の新しいモデル試験を始める前に、モデル、プロファイル、試験内容・件数、保存方式を利用者へ提示して確認を得る。保存方式の検証を理由に追加試験を自動発行しない。事前照合の既存ゲートも通す。
5. 承認された試験の終了後に完全復元照合を行い、通過した作業コピーだけを削除する。保存容量、一時容量、空き容量の前後差を別々に記録する。準備未完了のまま新方式を適用済みとせず、旧方式へ無断で切り替えて試験を開始しない。

## 維持手順

1. 大規模runの前後に`audit`する。
2. ローカルの新規試験は`THE_CAPTION_EVAL_COPY_MODE=clonefile`でfail closedし、qualificationでclonefileと通常copyのfixture identity一致、source / destinationの変更分離を確認する。別filesystemで通常copyが必要な場合だけ、必要容量を確認したうえで`auto`または`copy`を明示する。
3. auditでGit pack重複が増えた場合は`deduplicate-packs`をdry-run、適用する。
4. 週次に標準3日保持でGC manifestを作り、候補と参照状態を確認してから適用する。
5. 3 GiB超過ではunreferenced scratchと外部runtime複製を調べ、5 GiB超過またはfree 40 GiB未満では新規大規模runを止めて監査する。
6. registry、公開済み評価文書、v1 / v2履歴artifactはこのGCで変更しない。
7. 新しい通常試験では、採点・結果登録後に`archive-batch`を実行し、削除記録の完了を確認する。
8. 長期実行でも各バッチの直前に容量ガードを通し、採点・結果登録後に`archive-batch`を行う。旧二段階処理は既存試験の継続・復元に限定する。
