# Repository instructions

このrootには、全pathへ共通して適用する不変条件だけを残す。領域固有の配置、更新、検証、履歴保持規則は、対象領域の局所`AGENTS.md`を正本とする。対象pathに局所`AGENTS.md`がある場合は、その領域固有規則を追加適用する。

## Repository scope

- このリポジトリは、target instanceごとのprompt構築、比較、評価、release準備を扱う。登録instanceは`the-caption`（THE-CAPTION）と`click`（`pallets/click`）である。`the-caption`はrelease準備と本体投影まで進める現行instance、`click`はBundle A baselineを確立した公開targetで、Bundle比較、採用、release、本体反映は未実施である。instanceの登録と境界は`evaluations/targets/README.md`を正本とする。
- instance間でartifactを混ぜない。case、profile、set、rating contract、prompt bundle、resultはinstance固有artifactとして扱い、あるinstanceで成立した結果を他instanceの一般的効果として扱わない。target非依存のkernelとinstance固有artifactの帰属も`evaluations/targets/README.md`を正本とする。
- prompt制御上の問題を解く方法は、このリポジトリ内のprompt、TaskSpec、repository authority、評価artifactの境界へ限定する。repository外のexecutor、Codex CLI、tool adapter、runtime hook、外部wrapper、target runtimeの変更を、prompt Candidateの解決策、次案、backlog、再開条件として提案または実装しない。
- repository外の挙動や過去のexecutor試験は、保存済みresultの原因を分類するread-only診断証拠としてだけ参照できる。問題がrepository外の層でしか強制できない場合は、このリポジトリでは未解決として停止する。外部対応へ作業を広げない。評価基盤自体の保守は、ユーザーが明示的に依頼した別作業に限る。
- target本体のruntime変更は通常作業範囲に含めない。
- target本体への変更、push、PR、merge、runtime有効化は、明示的に依頼された別作業とする。

## 共通のartifact境界

- artifactが存在することと、評価済み、採用済み、release済み、本体反映済みであることを混同しない。
- baseline、candidate、release、evaluation result、approval、projectionを別の状態とgateとして扱う。
- secret、credential、非公開のraw run log、一時worktreeをcommitしない。
- 文書は原則として日本語で記述する。
- schema名、path、status、commandは再現性のため英語表記を許容する。

## Agent execution discipline

このリポジトリで作業するagentは、Candidate71（`the-caption-3ce91a4-validation-closure`）で本体へ採用されたvalidation-closure制御をrepository内作業へ適用する。制御原文は`prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/files/AGENTS.md.txt`を正本とする。

- ユーザーの依頼で固定されたTaskSpecを成果生成のauthorityとする。
- repositoryから確定できる事実は実測する。
- 確定できない成果値を推測で補完しない。
- 単一operationで完了する作業はroot自身で実行する。
- 独立した別operationが明示された場合だけ委譲する。
- 委譲した場合も、最終成果の受領、検証、報告はrootが担う。
- 変更後は、依頼と適用されるrepository規則が要求するrequired validation全体を確定する。
- required validationは依存関係を保った必要十分なwaveとして発行する。
- 各waveの全resultを受領してから一度だけ成否を判断する。
- 成否確定後は、TaskSpec追加要求、result失効、失敗原因調査などの根拠がない追加readや再検証を行わない。
- 検証していない成果を完了または成功として報告しない。
- tool callの成功を予測で語らず、実際のresultで確認する。

## 比較試験の実行前gate

- 保存済みresultを基準に品質、token、elapsed、採用可否を比較する試験では、評価slotを一件でも発行する前に基準resultを一意にbindする。
- 実行予定条件から、Evaluation set identity、全caseのfixture identity（path、type、mode、content、symlink targetを含む）、TaskSpec、case revision、rating、model、reasoning、Agent/runtime/CLI、permission、executor parameter、設定上の`M`、`N`とiteration集合を確定し、基準resultの互換条件と機械照合する。
- atomic run経路では、`N`、coverage、iteration集合、計画順序、`max_workers`をrunの実効互換条件へ含めない。これらはdispatch要求またはexecution provenanceとして固定する。prompt、Evaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingは引き続きrun単位で機械照合する。
- prompt比較では、事前に宣言したprompt identity以外の互換条件が完全一致することを実行前gateとする。完全一致を証明するpreflight receiptを保存してから実行する。
- Layer 4へ登録する試験では、発行予定のcase / iteration集合が固定Layer 1の全case coverageとresult schemaの登録条件を満たすこともpreflightで機械検証する。満たさない試験を非登録diagnosticとして実施する場合は、その状態と再利用不能なgateを一件目の発行前に明示する。
- 一項目でも不一致、未固定、未確認があれば、評価slotを一件も発行しない。不一致の値と理由を報告して停止する。実行後に不一致を発見して結果を参考値へ降格する進め方を禁止する。
- 試験ごとにfixture、file mode、runtime、設定上の並列上限などの実行環境を最適化しない。保存済み基準resultと比較する場合は、その基準で固定したLayer 1を再利用する。複数条件を新規実行する場合は、一つのLayer 1を先に固定して全条件へ複製する。
- 保存済みprompt-set resultとの履歴互換cycleは`prepare-comparison-layer1`で基準Layer 1から生成し、capsuleとglobal planの生成後に`preflight-comparison`を通す。比較用Layer 1を`freeze-set`で再生成しない。`comparison-preflight.json`がない、失効した、または改ざんされた旧経路cycleの`run`は禁止する。
- atomic run経路では、既存resultを`atomic_run_registry.py import-result`でrun単位へ索引化し、`plan-missing`で要求sample数との差だけをwrite-once dispatch planへ固定する。`prepare_atomic_plan.py`でpool identity、dispatch plan hash、prompt、Evaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、設定上の`M`を機械照合してから不足runだけを発行する。既存runを再実行せず、完了・採点後は各runを個別登録する。
- このhostの通常試験ではprofileの`max_workers`をqualification済み上限`M=24`へ固定する。readyなslotが24件未満でも設定値をslot数へ合わせて下げず、実際の同時実行数だけがready数に応じて24未満になり得る。

## 共通の変更規律

- 一つの変更では一つの判断または一つのartifact単位を扱う。
- 依頼が要求しないartifactを変更しない。
- 既存artifactと周辺経路を破壊しない。
- 正本と履歴を区別する。
- 履歴artifactを現在解釈へin-placeで書き換えない。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- root `README.md`は入口と要約に限定し、詳細な履歴やCandidate全系譜を戻さない（配下READMEの詳細一覧は対象外）。
- 対象pathに局所`AGENTS.md`がある場合、その領域固有規則を追加適用する。
