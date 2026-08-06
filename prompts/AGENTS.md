# prompts instructions

`prompts/`の指示は、baseline、candidate、route、releaseのartifact lifecycleを扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。prompt制御の設計原則は`docs/prompt-control-design-principles.md`を正本とする。

## 共通

- baseline、candidate、route、releaseを別pathで管理する。
- prompt identity、source identity、bundle hash、変更targetを固定する。
- 既存bundleをin-placeで改訂しない。
- 変更時は新しいrevisionまたはidentityを作る。
- artifactの存在を評価済みまたは採用済みの根拠にしない。

## README index

- `baselines/README.md`、`candidates/README.md`、`routes/README.md`、`releases/README.md`は各artifact classの現在索引と所在を示す。bundle本文、manifest、evaluation result、release個別READMEの代替正本にしない。
- READMEへ評価状態やlifecycle状態を要約する場合は一次artifactへ到達できる導線を持たせ、要約だけを判定根拠にしない。
- artifact追加時は対応する索引を同じ変更で追従させる。索引整理のために既存bundle identity、manifest、評価resultを変更しない。
- 過去Candidateの形成経緯、評価数値、採用理由、rollback詳細を索引へ長く複製せず、evaluation result、`docs/`の研究記録、個別release READMEへ委譲する。

## Baseline

- baselineは取得元repository、commitまたはtree、source path、content SHA-256へbindする。
- 取得後のbaseline本文とmanifestを変更しない。
- baselineの評価状態はbaseline artifactではなく、独立したevaluation resultで表す。

## Candidate

新しいcandidateの作成前に、次を固定する。

1. 基準prompt set
2. 基準状態での最短正常経路
3. 保存済みtraceで確認した一つの誤経路
4. 既存TaskSpec、repository authority、repository stateだけでは防げない理由
5. 追加、置換、削除する一つのpredicate
6. そのpredicateが消す具体的な判断点またはcontext伝播
7. 新たに増える判断点、参照、例外
8. 品質維持を確認するcaseとscore分布
9. 期待と逆の結果になった場合の停止条件

加えて、次を守る。

- 一つのcandidateでは一つのpredicateまたは一つの変更軸だけを扱う。
- 解く問題、baseline identity、変更理由、非目標、評価状態を記録する。
- prompt短縮、label削減、構造変更だけを効率改善と判断しない。
- targeted評価で成果品質と狙った経路変化を確認する前に、expandedまたはcontinuous評価へ進めない。
- candidate固有のquality・mechanism gateではcandidateだけを先に実行する。gate前に比較相手のprofileや新規runを必須化しない。
- 比較resultが必要になった時点で保存済み互換resultを先に使い、不足するprompt set / slotだけを評価profileへ追加する。
- このhostの新規試験はprofileの`max_workers=24`を固定し、readyなslotが24件未満でも試験ごとに設定値を下げない。複数prompt setの新規slotは別cycleのまま共通global queueへ入れる。
- 保存済みtraceにない将来不安だけを理由として制御を追加しない。
- 新しいpredicateの追加より、既存predicateの置換、統合、削除を優先する。
- 作成前gateが未定義なら、candidate bundleと`evaluations/`配下の評価profileを先に作らない。

### Candidate索引

`prompts/candidates/README.md`はcandidate bundleの一覧と評価状態への導線を持つ索引とする。

- 一つのbundle identityにつき一行を持ち、baseline、変更軸、評価状態への導線を記録する。
- prompt identity、bundle hash、target mapの正本は各manifestとし、READMEへ複製して別identityを作らない。
- `not_evaluated`は評価resultが存在しない状態として索引へ記録できる。評価を実施した場合は対応する一次resultへリンクする。
- 採用、release status、approval、runtime projectionはCandidate評価状態と別軸であり、Candidate索引の状態列へ混ぜない。
- candidate bundleを追加・削除しない限り、索引再編だけを理由に既存行を現在解釈へ書き換えない。後続評価による状態更新は一次resultに基づいて行う。
- 索引変更後はcandidate bundle実体が索引から参照可能であることを確認する。

## Route

- routeは共通全文sourceへ実行前に合成する最小差分として扱う。
- route固有の差分を共通promptの新しい正本へ読み替えない。
- 適用条件、source identity、差分identity、合成後identityを固定する。
- routeでのみ成立する結果を、共通prompt全体の一般的効果として扱わない。

## Release

- release作成だけでは採用承認またはTHE-CAPTION本体への反映を意味しない。
- source candidate、評価範囲、未解決risk、release status、approval、projection、rollback identityを分離して記録する。
- 評価上の`stopped`と、別判断による`approved`または`projected`を混ぜない。
- THE-CAPTIONへの反映はrelease作成とは別operationとする。
- projection後も、元の評価状態と未解決riskを削除しない。

### Release索引

`prompts/releases/README.md`はrelease identityとlifecycleの現在台帳とする。

- 一つのrelease identityにつき一行を持ち、source candidate、評価要約、`release status`、`approval`、`runtime projection`を独立列で保持する。
- rollback identity、projection対象、PR / commit、未解決risk、評価の詳細は個別release READMEまたは一次evaluation resultを正とし、索引本文へ重複させない。
- release status、approval、runtime projectionのいずれかが後続operationで変化した場合だけ、一次artifactに基づいて該当列を追従させる。別軸の評価状態を理由に遡及変更しない。
- `projected`済みreleaseの後続評価で新しいriskが見つかっても、既存projection stateを自動的に取り消したものとして記述しない。
- 索引変更後はrelease directory実体が索引から参照可能であることを確認する。
