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

このリポジトリで作業するagentは、Candidate147（`the-caption-3ce91a4-result-effect-scope-r1`）で本体へ採用されたresult-effect-scope制御をrepository内作業へ適用する。制御原文は`prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1/files/AGENTS.md.txt`を正本とする。この適用はrepository保守のagent execution disciplineであり、Candidate147の評価結果を別target instanceへ一般化すること、prompt candidateとして採用すること、releaseまたはtarget本体へprojectionすることを意味しない。

- ユーザーの依頼で固定されたTaskSpecを成果生成のauthorityとする。
- repositoryから確定できる事実は実測する。
- 確定できない成果値を推測で補完しない。
- repository evidenceは、nonterminalなrequired predicateが`unobserved`で、現在欠けている観測値と、そのresultがpredicate stateをbindできるconsumerが固定されている場合だけ取得する。これはread数制限ではなく、未観測effect、TaskSpec-required確認、適用中instruction、比較互換性、Claim根拠、diff / statusによる変更範囲確認など、未確定predicateを動かすreadを禁止しない。
- `result_effect_scope`を、受領resultがtarget / permission / method / stop conditionを変え得る未発行operation classの集合として固定する。result待ちはその集合に属するoperationだけへ適用し、task全体または無関係なoperationへ伝播させない。ただし、比較試験の実行前gateなどrepositoryが明示する広い停止条件は優先する。
- 開始identityのdriftがartifact変更とrequired commandだけを禁止し、許可済みreadのtargetまたはpermissionを変えない場合、identity確認とそのreadを同じmodel stepから発行する。共同resultを受領して正常と判定するまで、artifact変更とrequired commandだけを発行しない。drift時にreadも禁止される場合、またはidentity resultがread target / permissionを変え得る場合はreadも待つ。
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

- 保存済みresultを基準に品質、token、elapsed、採用可否を比較する試験では、評価slotを一件でも発行する前に基準resultを一意にbindし、宣言したprompt identity以外の互換条件が完全一致することを証明するpreflight receiptを保存する。
- 一項目でも不一致、未固定、未確認があれば、評価slotを一件も発行しない。不一致の値と理由を報告して停止する。実行後に不一致を発見して結果を参考値へ降格する進め方を禁止する。
- 試験ごとに実行環境を最適化しない。保存済み基準resultと比較する場合は、その基準で固定したLayer 1を再利用する。
- 照合する互換条件の内訳、preflight command、Layer 1再利用、atomic run経路、並列上限の固定値は`evaluations/AGENTS.md`を正本とする。

## 共通の変更規律

- 一つの変更では一つの判断または一つのartifact単位を扱う。
- 依頼が要求しないartifactを変更しない。
- 既存artifactと周辺経路を破壊しない。
- 正本と履歴を区別する。
- 履歴artifactを現在解釈へin-placeで書き換えない。
- prompt変更と評価条件変更を同じ比較単位へ混ぜない。
- root `README.md`は入口と要約に限定し、詳細な履歴やCandidate全系譜を戻さない（配下READMEの詳細一覧は対象外）。
