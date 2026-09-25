# Repository instructions

このルートには、全パスへ共通して適用する不変条件と、リポジトリ全体へ及ぶ規律を残す。規律の適用場面が特定領域に限られる場合も、規則本体はルートへ置き、その内訳は対象領域の局所`AGENTS.md`を正本とする。領域固有の配置、更新、検証、履歴保持規則も、対象領域の局所`AGENTS.md`を正本とする。対象パスに局所`AGENTS.md`がある場合は、その領域固有規則を追加適用する。

## Repository scope

- このリポジトリは、ターゲットインスタンスごとのプロンプト構築、比較、評価、release準備を扱う。登録インスタンスの識別子、layout、visibility、進行状態、およびインスタンス境界は`evaluations/targets/README.md`を正本とする。インスタンス個別の状態をルートへ複製しない。
- インスタンス間でアーティファクトを混ぜない。ケース、プロファイル、セット、rating contract、プロンプトバンドル、resultはインスタンス固有のアーティファクトとして扱い、あるインスタンスで成立した結果を他インスタンスの一般的効果として扱わない。ターゲット非依存のkernelとインスタンス固有アーティファクトの帰属も`evaluations/targets/README.md`を正本とする。
- プロンプト制御上の問題を解く方法は、このリポジトリ内のプロンプト、TaskSpec、repository authority、評価アーティファクトの境界へ限定する。リポジトリ外のexecutor、Codex CLI、tool adapter、runtime hook、外部wrapper、ターゲットのランタイムの変更を、プロンプトCandidateの解決策、次案、バックログ、再開条件として提案または実装しない。
- リポジトリ外の挙動や過去のexecutor試験は、保存済みresultの原因を分類する読み取り専用の診断証拠としてだけ参照できる。リポジトリ外の変更を必要とする案は、このリポジトリの解決案として採用せず、外部対応へ作業を広げない。ただし、その案の棄却を問題の検討終了とは扱わない。まず、リポジトリ内のprompt、TaskSpec、repository authority、評価アーティファクトで閉じられる別の境界へ問題を分解し直す。その範囲では強制できないことを証拠で確認した場合に限り、問題を解決済みにせず未解決として保留する。評価基盤自体の保守は、ユーザーが明示的に依頼した別作業に限る。
- ターゲット本体のランタイム変更は通常作業範囲に含めない。
- ターゲット本体への変更、push、PR、merge、ランタイム有効化は、明示的に依頼された別作業とする。

## Prompt制御研究の設計原則

- **最優先は、意図しない動作を正しい条件判断へ誘導することではなく、その動作へ至るpermissionまたはdependencyの辺を閉じることとする。** 誤経路をprompt準拠のまま実行でき、モデルが条件を正しく判定した場合だけ回避できる制御は、品質KPIや成功率が高くても機序成立としない。誤経路の実行不能性を確認する前に、条件、順序、自己判定、ticket、ownership labelまたは処理手順を追加しない。
- `OBJECTIVE_INVARIANCE`: prompt制御の分析、Candidate設計および評価では、明示された利用者要求またはその要求が指定する一意なrepository authorityから、`task_objective := target改善系列 / required effect / preserved effect / artifact間relation`を実行前にbindし、task completionまで保持する。比較基準、制御原文のsource、実装の直接の親および失敗反例の役割を分離し、ある役割のCandidateを別の役割へ昇格させない。分析result、Candidateの成否、比較上の利便性または実装方法は、局所predicate、methodおよびallowed deltaだけを変更でき、`task_objective`を別目的へ置換、縮小または別系列へ移動できない。`derived_operation_ready := task_objective内の未完了predicateがbind済み ∧ requested resultがそのpredicateを直接bind可能 ∧ target改善系列、required effect、preserved effectおよびartifact間relationを保持`とし、trueの場合だけ派生する分析、設計、probe、Candidate作成または評価を発行する。falseの派生operationは発行対象へ入れず、task全体を停止したり、すでに固定済みの目的を利用者へ再確認したりせず、同じ`task_objective`を満たす別のpermissionまたはdependency境界へ分解し直して作業を継続する。
- review制御の現行再設計は、Candidate214で実証したpacket構築後のreviewer再read閉鎖と別containerの必要観測を保持する。同Candidateでもrootへの初回whole-source deliveryは閉じていなかったため、過剰遮断だけでなく最初のsource取得を、実行前に一意なowner、carrier、read permissionおよびobservable output境界で再設計する。Candidate215からCandidate222までの条件付き判断、必要性の自己分類、ticket、ownership宣言、producer別集合、output labelまたはobservation viewは、誤経路を閉じなかった反例として扱い、次Candidateの親または追加条件の材料にしない。必要な正常経路の合法なcarrierをpromptで固定できない案は、閉鎖を弱めず`candidate_not_created`として棄却する。これは問題の検討終了を意味しない。問題を未解決の設計課題として残し、read対象の粒度、owner、packet構築、source bootstrap projectionおよびobservable output境界を分解し直して、必要reviewを完遂できる別案の検討を続ける。現行方針は`docs/candidate214-route-closure-recontrol-direction.md`、delivery境界の再監査は`docs/review-carrier-bootstrap-authority-audit.md`を参照する。
- 保存済みresultまたはtraceからprompt制御上の原因を分析し、その分析から制御文、Candidate、再構成または次案を導く作業では、着手前に`docs/prompt-control-design-principles.md`の全文を読む。文書の所在を知っていること、過去Candidateからリンクされていること、または一部の原則を記憶していることを読了の代わりにしない。
- 成功runと失敗runの比較から次の制御を検討する場合は、同文書の「成功動作を実行手順へ転記せず、誤経路の到達可能性を閉じる」を分析から提案へ移る前に適用する。成功時のtool順、判断順またはmodel stepを、そのまま新しい実行義務へ変換しない。
- Candidate bundleまたはCandidate本文を作成する場合は、同文書の`Candidate作成前の検討gate`を満たした設計記録を先に固定する。評価resultの記録、品質採点またはKPI集計だけを行い、次の制御案を導かない作業には、この追加読了を必須化しない。

## 共通のアーティファクト境界

- アーティファクトが存在することと、評価済み、採用済み、release済み、本体反映済みであることを混同しない。
- baseline、candidate、release、evaluation result、approval、projectionを別の状態とゲートとして扱う。
- `PROMPT_ONLY_COMPARISON`: 同一のprompt改善系列では、固定済みのケース、fixture、TaskSpec、oracle、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingおよび集計方法をCandidate間で再利用し、事前に宣言したprompt identityだけを実験変数とする。固定試験のresultを次Candidateのprompt設計へ使ったことだけを理由に、新しいケース、set、profile条件または採点規則を作らない。blindまたは未見であることは別の証拠属性であり、固定条件でのprompt比較可能性と混同しない。評価契約の欠陥またはtask objectiveの変更によってprompt以外を変える場合は別の評価系列とし、変更前後の差をprompt効果として比較しない。
- シークレット、クレデンシャル、非公開の生の実行ログ、一時worktreeをcommitしない。

## 内部メモの扱い

内部の作業メモは、判断と進行状況を整理するためだけに使う。利用者への説明や質問、作業計画、要約、リポジトリ内の文書へそのまま流用しない。依頼、根拠、現在の状況を理解し直し、それぞれの目的と読み手に合う形で内容を最初から組み立てる。人が読む内容は自然な日本語で表し、正確な区別や参照に必要な用語、識別子、ファイル名だけを後から加える。
利用者への説明では、内部の状態名や識別子を並べた省略表現を避け、何が済み、何が未完了で、次に何をするのかを、助詞と述語を補った自然な日本語の文として書く。

会話、利用者向け説明、質問、作業計画、要約、PRの題名・本文、リポジトリ内の文書は、別の言語を明示的に指定されない限り、自然な日本語で書く。英語は、制御の正確な対応関係を保つために必要な識別子、状態値、スキーマ項目、コマンド、API名、製品名、ファイル名に限る。工程、役割、判断、状態、成果物を表す一般語は日本語で記し、日本語文へ不要な英単語を混在させない。既存の履歴アーティファクト、固定済み原文、機械的互換性を保つ必要がある値は、この表記規則だけを理由に書き換えない。

## 比較試験の実行前ゲート

- 保存済みresultを基準に品質、トークン、経過時間、採用可否を比較する試験では、評価スロットを一件でも発行する前に基準resultを一意にbindし、宣言したprompt identity以外の互換条件が完全一致することを証明するpreflight receiptを保存する。
- 一項目でも不一致、未固定、未確認があれば、評価スロットを一件も発行しない。不一致の値と理由を報告して停止する。実行後に不一致を発見して結果を参考値へ降格する進め方を禁止する。
- 試験ごとに実行環境を最適化しない。保存済み基準resultと比較する場合は、その基準で固定したLayer 1を再利用する。
- 照合する互換条件の内訳、preflight command、Layer 1再利用、atomic run経路、並列上限の固定値は`evaluations/AGENTS.md`を正本とする。

## 共通の変更規律

- 一つの変更では一つの判断または一つの`アーティファクト単位`を扱う。この項の`変更`と`アーティファクト単位`は、ケース、プロファイル、セット、rating contract、プロンプトバンドル、release、resultなど評価アーティファクトとプロンプトアーティファクトの変更単位を指す。gitのcommit、branch、PRの粒度を定める規則ではなく、docsとdescriptorだけの変更にこの単位規則を適用しない。
- 依頼が要求しないアーティファクトを変更しない。
- 既存アーティファクトと周辺経路を破壊しない。
- 正本と履歴を区別する。
- 履歴アーティファクトを現在解釈へその場で書き換えない。
- プロンプト変更と評価条件変更を同じ比較単位へ混ぜない。
- ルートの`README.md`は入口と要約に限定し、詳細な履歴やCandidate全系譜を戻さない（配下READMEの詳細一覧は対象外）。
