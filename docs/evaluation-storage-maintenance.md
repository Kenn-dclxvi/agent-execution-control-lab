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

## 通常試験と8時間runのseal・圧縮

複数workspaceを持つ通常試験と、多数batchを1つの長期run配下へ保存する試験は、直下run単位のGCではなく`layer2/extensions/long_run_storage/`を使う。通常試験では試験root、長期runでは各batch rootを同じ`--batch`引数へ渡す。容量guard、clonefile必須の物理複製、実行後のworkspace pruning、登録後の`tar.zst`圧縮を行う。

実行直後のsealはblind rating用成果を先に固定し、完全なworkspaceと自己完結fixtureを含むarchiveをstreaming生成する。圧縮後のmember hashと`zstd -t`を検証してからworkspaceのlive copyだけを削除し、Layer 1 fixtureは次batchのclone元かつ固定済みartifactとして保持する。再生成契約をその代替にしない。Layer 3/4に必要なartifactは直接参照できる状態で残す。result登録後の最終compactはLayer 2〜4のevidenceを再度sealし、Layer 1、`result-registration.json`、最小summaryを直接参照できる状態で残す。完全な復元にはexecution archiveとfinal archiveの両方を使用する。

標準のdispatch停止はfree 25 GiB、hard floorは20 GiBである。次batch見積りを差し引いた予測free bytesがdispatch停止値を下回る場合も、新規batchを投入しない。command、保持物、復元方法は[Long-run storage extension](../layer2/extensions/long_run_storage/README.md)を参照する。

## 維持手順

1. 大規模runの前後に`audit`する。
2. ローカルの新規試験は`THE_CAPTION_EVAL_COPY_MODE=clonefile`でfail closedし、qualificationでclonefileと通常copyのfixture identity一致、source / destinationの変更分離を確認する。別filesystemで通常copyが必要な場合だけ、必要容量を確認したうえで`auto`または`copy`を明示する。
3. auditでGit pack重複が増えた場合は`deduplicate-packs`をdry-run、適用する。
4. 週次に標準3日保持でGC manifestを作り、候補と参照状態を確認してから適用する。
5. 3 GiB超過ではunreferenced scratchと外部runtime複製を調べ、5 GiB超過またはfree 40 GiB未満では新規大規模runを止めて監査する。
6. registry、公開済み評価文書、v1 / v2履歴artifactはこのGCで変更しない。
7. 複数runを持つ通常試験では、採点に必要なviewの固定後にexecution seal、result登録後にfinal compactを行う。
8. 8時間runでは各batchの直前にcapacity guard、実行直後にexecution seal、result登録後にfinal compactを行う。
