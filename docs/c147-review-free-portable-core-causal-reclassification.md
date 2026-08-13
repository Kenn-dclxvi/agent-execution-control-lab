# C147 Review-free portable core 原因再分類

> [!IMPORTANT]
> **状態**: `superseded / M1_completion_withdrawn / functional_decomposition_reopened`
>
> 条項単位の再分類は、正の発行遷移と結果収集障壁を独立機能として分解できていなかった。現行分析は[`Candidate147 機能分解の再分析`](c147-functional-decomposition-reanalysis.md)を正とする。本文は誤ったM1完了判断の履歴として保持する。

## 結論

C147再構成の最初の単位は、Reviewを含まない共通実行制御とする。C147の13条項、条項名、順序は保持対象にしない。保持するのは、利用者が要求した成果を固定してから、必要な観測、変更、検証だけを進め、受領resultの効果を実際に依存する未完了処理へ限定する正常経路である。

Codex固有のfield名、API名、待機identity、会話継承指定、command配送方式は共通制御本文から外す。それらが担っていた意味のうち、実行環境によらず必要なものだけを、producer、input、invocation、result、dependency、completionの状態遷移として再配置する。

## 今回固定する再構成目的

一つの再構成目的は次の通りである。

> C147の成立済み正常経路を、Review responsibilityを持たず、特定実行環境の表面語にも依存しない、一意な状態遷移所有へ再構成する。

これは複数predicateを同時に変更するが、一つの構造再構成である。runtime固有語だけを先に削るとprovenanceとnonterminal closureが欠け、C147条項だけを先に統合するとruntime実装手段が新しい責任へ残るため、中間Candidateへ分割しない。

## 基準と最短正常経路

基準prompt setはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`である。保存済みStandard14 N=100は1,400 / 1,400件がscore `4`であり、低Score、excluded attempt、controller error、command protocol violationは0件だった。これは一般効果の証明ではなく、再構成前に保持すべき正常経路の一次基準である。

Reviewを含まない最短正常経路は次の通りである。

1. 利用者に観測可能なrequired outcomeをTaskSpecまたは一意なrepository authorityへbindする。
2. 各operationへ一つのproducerと、必要十分なinput boundaryをbindする。
3. 未解決predicateへ現在欠けている値を返せるinvocationだけを発行可能にする。
4. admitted resultだけでimplementationを一つへbindし、変更する。
5. 変更後にrequired validationを一つのplanへ固定し、個別resultを集める。
6. 全required predicateがadmitted terminal resultを持つ場合だけ完了する。
7. 途中resultは、それがtarget、permission、method、stop conditionまたはrequired inputを変える未完了operationだけへ効かせる。

## 保存traceから再構成へ持ち込む事実

| 証拠 | 今回使う事実 | 今回使わない解釈 |
|---|---|---|
| C147 Standard14 N=100 | 上記の正常経路は1,400 / 1,400 score `4`を成立させた | 13条項の文言、個数、順序が不可欠である |
| C147 F01 / F02 / F03 N=5 | resultの停止効果を局所化し、独立な許可済みreadを不要に止めない経路が15 / 15で成立した | `同一model step`という配送方式自体がprompt不変条件である |
| Candidate190 | criterion owner語列をproducer選択へ使うと不要な別executionが生じる | Review responsibilityを共通coreへ戻す |
| Candidate191〜193 | 抽象的なdispatch gateやmodel return単位の制御は、依存判定を安定させなかった | より細かいdispatch語を追加すれば解ける |
| Candidate202〜203 | Review制御をC147へ重ねると、通常経路の開始・read・producer選択へ漏れた | Reviewを共通coreの前提にする |

## C147条項の責任再分類

| C147条項 | 保持する意味 | 新しい単一owner | 取り除くもの |
|---|---|---|---|
| `SPEC` | required outcomeの固定、operation局所binding | `OUTCOME` | target pathやcommandを成果値と誤認する分岐 |
| `PRODUCER` | 一operation一producer | `PRODUCER` | `root / worker`の二分法 |
| `TERMINAL` | terminal resultが揃うまで未完了 | `COMPLETION` | session終了や進捗文による補完 |
| `CONTEXT` | 必要十分なinputと禁止input | `INPUT` | 会話turn数と継承APIの指定 |
| `EVIDENCE_GATE` | consumerのある未観測値だけを取得、変更前closure | `INVOCATION`と`IMPLEMENTATION` | lifecycle列挙と実装手段の混在 |
| `OWNER_ROLE` | owner metadataとproducer identityの分離、result provenance | `PRODUCER`と`RESULT_ADMISSION` | runtime field名と待機primitive名 |
| `ROOT` | producerでない実行がresultを再生成しない | `PRODUCER` | 特定coordinator名 |
| `INDEPENDENCE` | operationごとのpredicateとproducer | `OUTCOME`と`PRODUCER` | 別条項での同一producer規則の重複 |
| `DECISION_BOUNDARY` | result effectの局所化、真に独立な処理の非直列化 | `RESULT_EFFECT` | response / step単位の配送指定 |
| `VALIDATION_CLOSURE` | 個別判定、fail-fast、全result後の一回の完了判定 | `VALIDATION_CLOSURE` | wrapper、tool名、return timing |
| `VALIDATION_PLAN` | 変更後に検証全件を固定 | `VALIDATION_PLAN` | cell IDと専用wait方法 |
| `METHOD` | 手段とpredicate、失敗とpermissionの分離 | `METHOD` | 特定command種別への依存 |
| `RECOVERY` | environment-only repairと同一required executionの再試行 | `RECOVERY` | 固有counter名 |

## Codex固有表現の処置

次の表は旧本文や旧草案を診断するためのinventoryであり、右列の具体語を新しいcore本文へ残す許可ではない。

| 旧表現 | 処置 | portable coreで保持する意味 |
|---|---|---|
| `root` / `worker` | 削除して一般化 | bind済みproducerと、producerでないresult consumerの権限差 |
| `fork_turns=none` / 最小turn数 | 実装手段として削除 | producer inputを必要十分な範囲へ閉じ、無関係な履歴を渡さない |
| `runtime_spawn_result.task_name` / `FINAL_ANSWER.Sender` | field名を削除 | 受領resultを事前bind済みproducer identityとoperationへ対応づけられる |
| `wait` | primitive名を削除 | 同期resultだけをproducer provenanceに使わない |
| `same model step` / `modelへ戻らず` | 配送方式として削除 | resultが判断を変えないoperation間へ偽のdependencyを作らない |
| `custom exec wrapper` / `exec_command` | command配送方式として削除 | required validationを個別executionとして判定し、失敗後を発行しない |
| `validation wrapper` / `cell ID` | return schemaとして削除 | nonterminal resultを完了とせず、同じinvocationがterminalになるまで継続する |
| `environment_recovery_max` | 固有変数名を削除 | authorityへbind済みのrecovery allowanceだけを消費する |

## 制御層から除外するもの

次は新しいcoreの責任にしない。

- Reviewの要否、担当、入力routing、finding admission、finding effect。
- invocationの同時配送、responseへのreturn、非同期結果配送のatomicity。
- 特定CLI、API、tool adapter、外部wrapperの変更または要件。
- runtimeが観測できないidentityやatomicityを、prompt文だけで成立済みと宣言すること。
- 特定runtimeでの成立を別runtimeへ一般化すること。

後でReviewを検討する場合も、このcoreを直接書き換えず、明示TaskSpecが要求する別責任として接続する。接続が通常経路のproducer、inputまたはinvocation eligibilityを暗黙に変える設計は採らない。

## M1完了条件

- C147の全13条項について、保持する意味、新owner、削除する実装手段を分類した。
- Review責任を新coreのowner一覧へ含めていない。
- Codex固有表現8群を、一般化する意味と削除する表面形へ分けた。
- 正しい強制層がexecutor側である配送方式は、外部変更案へ展開せずcoreから除外した。
- Candidate bundle、評価profile、評価slotは作成していない。

次は、この分類を一意な状態遷移と制御本文へ落とすM2だけを許可する。

## 参照

- [`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- [`runtime-independent-execution-control-draft.md`](runtime-independent-execution-control-draft.md)
- [`candidate147-result-effect-scope-design.md`](candidate147-result-effect-scope-design.md)
- [`Candidate147 Standard14 N=100 result`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [`Candidate147 F01 / F02 / F03 N=5 result`](../evaluations/results/candidate145-candidate147-result-effect-scope-v14-medium-f01-f02-f03-atomic-n5-cli0146_2026-08-02.md)
- [`candidate203-m5-causal-analysis.md`](candidate203-m5-causal-analysis.md)
