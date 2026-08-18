# Repository contract

## 1. Artifact

このリポジトリが作るものは、THE-CAPTION向けのversioned prompt bundleと、その比較・評価・反映判断に必要な再現可能な根拠である。

このリポジトリ自体はTHE-CAPTIONのruntime正本ではない。`prompts/releases/`にbundleが存在しても、本体への反映または有効化は発生しない。

## 2. State

prompt bundleは次の状態を区別する。

| State | 意味 |
| --- | --- |
| `draft` | 構築中。比較判断へ使用しない |
| `evaluation_ready` | identityと評価条件を固定済み。評価開始可能 |
| `evaluated` | 固定profileで結果を取得済み。採用は未判断 |
| `release_candidate` | 評価範囲と未解決riskを確認し、反映候補に固定済み |
| `approved_for_projection` | THE-CAPTION本体への反映を明示承認済み |
| `projected` | 対象commitへの反映identityを記録済み |

状態は自動昇格させない。評価成功、release作成、承認、本体反映は別のgateとする。

## 3. Required identity

baseline、candidate、release、evaluation resultは、該当する範囲で次を固定する。

- target repositoryとstart commit / tree
- prompt source pathとcontent SHA-256
- model、reasoning設定、Agent / CLI version
- TaskSpec、permission、allowed / forbidden paths
- fixture、case revision、grader / oracle revision
- repetition、order、environment、実行時刻
- terminal outcome、変更path、validation結果

## 4. Evaluation boundary

- 同一比較内ではprompt以外の条件を揃える。
- 同一のprompt改善系列では固定benchmarkをCandidate間で再利用し、prompt identityだけを実験変数とする。benchmarkの結果を次Candidateの設計へ使ったことだけを理由に、case、set、TaskSpec、oracle、rating、profile条件またはruntimeを作り直さない。
- workerへ見せる入力と、fixture seed、oracle、grader、expected resultを分離する。
- coverageと同一caseのrepeatabilityを別軸で扱う。
- 固定benchmarkの反復結果はそのbenchmark内の比較根拠であり、blindまたは未見の根拠とは区別する。blind検証は事前に独立gateとして要求された場合だけ追加し、Candidateごとに更新しない。
- 評価契約の欠陥または目的変更でprompt以外を変える場合は別の評価系列とし、変更前後をprompt効果として比較しない。
- environment failureをpromptまたはtask behaviorの失敗へ混ぜない。
- 評価結果から言える範囲と、言えない範囲を併記する。

## 5. Projection boundary

THE-CAPTION本体への反映には、少なくとも次を別作業で固定する。

1. 対象THE-CAPTION commit
2. 反映するrelease identity
3. 変更対象path
4. required validation
5. rollback identity
6. commit、push、PR、merge、runtime有効化の許可

反映後は、release identityとTHE-CAPTION側のcommit identityをこのリポジトリへ記録する。

## 6. Storage re-encoding

既存のbaseline、candidate、releaseの内容改訂はin-placeで行わず、新しいrevisionまたはidentityを作る。これと区別して、artifact identityを保ったままat-rest格納表現だけを変える操作を、identity-preserving storage re-encodingとして許可する。

storage re-encodingは、次を全て満たす場合に限り、既存artifactへ同一pathで適用してよい。

- `bundle_sha256`と`files` entry（`target`、`type`、`mode`、content SHA-256、symlinkのlink target）が変わらない。
- prompt本文が変わらない（regular fileはbyte単位で不変）。
- 変更はat-rest格納表現に限る（物理格納path、symlinkのat-rest格納target、manifestの`storage_format`など、論理identityに含まれない項目）。
- 変更前後の`bundle_sha256`不変を検証で確認し、再格納の由来を記録する。
- verifierが変更前後の`storage_format`を両方解決でき、旧格納形式のartifactも引き続き検証できる。

`bundle_sha256`、`files` entry、prompt本文のいずれかが変わる変更は、storage re-encodingではなくcontent revisionとして扱い、新しいidentityで行う。storage re-encodingは評価状態、採用、release、projectionのgateを昇格させない。
