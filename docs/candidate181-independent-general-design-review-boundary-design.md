# Candidate181 独立一般設計review境界の設計

> 状態: `design_complete / adversarial_review_passed / candidate_implemented / implementation_audit_passed / target_evaluation_failed / candidate_stopped`

## 結論

Candidate181はCandidate147を直接の親とし、自律探索から作った一般設計を実装へ渡す前に、独立reviewが必要か、誰のどの終端結果で受入可否を変えられるかを一つの境界として追加する。Candidate180を含む後続Candidateの本文、構造、結果schemaは継承しない。保存済みの失敗は、境界から除くべき判断を特定する観測証拠としてだけ使う。

制御対象はreview工程ではない。rootが独立producerの代わりに反例を意味判定する経路と、独立producerの結果を受ける前に一般設計を実装へ渡す経路を閉じる。readの順序、回数、tool、packet形式、field集合、locator、record identityは固定しない。

## Candidate作成前gate

1. 基準prompt setはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。
2. 最短正常経路は、要求と適用中authorityが変更効果を閉じた一つの具体対象へ限定している場合に、独立reviewを作らずC147の`implementation_bound`から変更へ進む経路である。
3. 保存済みの誤経路はCandidate180 ADR9 r2 N=5である。ADR03〜ADR06は必要reviewer起動3 / 20、ADR07はreviewer 5 / 5でも完了0 / 5、ADR09はreviewer起動2 / 5だった。
4. Candidate147はoperation producerとresult effectを閉じるが、自律探索から作った一般設計について独立した反証producerを要求する条件を持たない。Candidate180はroot側の直接反例判定と未来全域の閉包要求を加えたため、独立性を失い過剰停止した。
5. 追加するpredicateは`independent_general_design_review_admitted`だけとする。
6. このpredicateは、rootが具体的反例を確定する判断点、証拠取得成功をreview operation作成条件にする判断点、未来の全実例の不存在証明を`no_counterexample_found`へ要求する判断点を除く。
7. 新しい判断は、提案設計の意味上の変更効果が規範で閉じた対象を越えるか、固定した独立review resultを現在設計へ受け入れられるかだけである。case分岐、取得手順、結果形式は増やさない。
8. 品質保持対象は、閉じた単一対象、authorityによる有限列挙、owner語列だけを含む通常作業、permission否定、具体的反例、反例なしの完全review、必要観測が成立しないreviewである。
9. 情報封鎖した敵対的設計reviewで一般入力の反例が一件でも成立すればCandidateを作らない。`no_counterexample_found`の場合だけC147からbundleを作る。

## reviewを必要とする境界

`normative_boundary`を、要求または適用中authorityがchange effectまたは保持constraintを要求する対象、状態、関係とする。`semantic_effect_boundary`を、提案設計が実際に観測可能な判断を変える対象、状態、関係とする。共通関数を使うだけで効果が明示対象へ閉じる場合は後者を広げず、共有既定動作または全域規則により規範対象外の判断も変える場合はその範囲を含める。

次が共同で成立する場合だけ`independent_general_design_review_required=true`とする。

1. 規範が閉じた一つの具体値を越える共通判断を要求するか、semantic effectが閉じた規範対象を越える。
2. その一般判断に必要な対象集合、関係、区別または設計前提のいずれかが、要求、適用中authorityまたは許可済みの変更前resultで閉じていない。
3. 現在設計をその境界へ適用してよいかを独立producerが反証できる、明示規範、保持constraint、設計が明示した必要事実、または許可済み観測がある。

第3条件は具体的反例の成立をrootへ判定させない。独立producerが判定する規範predicateと事実の入力が存在することだけを固定する。rootが反例らしい事実を既に見ていても、一般設計の受入可否を変える意味判定は独立reviewへ残す。

一条件でも成立しなければreviewを作らない。ただし条件の入力が未固定、未終端または到達不能ならfalseへ落とさず`unavailable`とする。artifact変更後validationの予定は変更前のreview要否を閉じない。

## 独立operationと情報境界

reviewが必要なら、新しいreview operationのTaskSpecへnon-rootの独立producer roleをconstraintとして固定する。利用者が特定execution identityを要求した場合はそれをbindし、未指定ならpermission内でexecutorが一つのnon-root identityをpredicate前に選ぶ。owner語列をproducer指定へ読み替えず、permission否定またはproducer不在なら`unavailable`とする。producer、terminal、sender、rootの役割はCandidate147の`PRODUCER`、`TERMINAL`、`OWNER_ROLE`、`ROOT`を使う。

review operationを作るために必要なのは、反証対象と許可境界が固定されていることである。必須観測の成功はoperation作成条件にしない。観測targetがmissing、unreadableまたはnon-successでも、その状態を独立producerへ帰属可能に渡せるならreview operationを起動し、producerが`unavailable`を終端結果として返す。rootがpacket不完成を理由にreviewerを省略して同じ`unavailable`を代行しない。

独立producerへ渡せるのは、現在設計の意味、設計宣言境界、normative boundary、semantic effect boundary、適用規範、保持constraint、設計が明示した必要事実、起動前に固定した反証対象、必要な許可済み観測またはそのterminal state、および各入力の帰属だけである。利用者指定patch等がreview対象設計ならその意味内容は許可する。

Candidate本文、反証後の修正案または代替実装、評価case、fixture、oracle、rating、過去finding、旧Candidateの解法、無関係な履歴は渡さない。情報の役割を固定し、file、tool、提示順、件数またはschemaを固定しない。

## 独立resultの受入境界

独立producerだけが次の意味predicateを実行する。

- `counterexample_found`: 規範またはsemantic effect上、現在設計の一般判断を受ける具体的実例が設計対象から漏れるか、適用規範、保持constraintまたは設計が明示した必要事実と直接両立せず、要求を満たすには対象集合、一般条件、authority、所有、停止条件またはfallbackの変更が必要である。
- `no_counterexample_found`: 起動前に固定した全反証対象について、適用規範と設計前提、および反例の有無を変え得る許可済みevidence operationがすべてterminalかつsuccessであり、その範囲で具体的反例が成立しなかった。
- `unavailable`: 反例の有無を変え得る必要入力、evidence resultまたはproducer resultをbindできず、上の二結果のどちらにも到達できない。

`no_counterexample_found`は未来の全実例が存在しないことの証明ではない。現在設計を反証するため起動前に固定した規範、設計前提、境界上の区別と許可証拠が完全で、そのscopeに反例がないという独立resultである。設計が自己宣言した対象だけへscopeを狭めることは許さず、normative boundaryとsemantic effect boundaryから反証対象を固定する。

一件の具体的反例が成立したら、無関係な観測のmissing、失敗または未終端で`counterexample_found`を失効させない。反例が成立しない場合だけ、必要evidenceの一件でもnon-successなら`unavailable`、全件successなら`no_counterexample_found`とする。

rootが確認するのは、結果がbind済みproducerからterminal resultとして届き、現在のdesign identity、review operation identity、producer identity、result identityへbindできることだけである。反例、scope完全性または証拠の意味をrootが再判定、補完または再生成しない。

## 実装受入と効力

```text
review_gate_satisfied :=
  independent_general_design_review_required = false
  or admissible_independent_review_result = no_counterexample_found

independent_general_design_review_admitted :=
  implementation_bound
  and review_requirement_inputs_terminal
  and review_gate_satisfied
```

`counterexample_found`なら現在design identityを`blocked`にし、`unavailable`なら欠陥を確定せず現在設計を実装へ渡さない。artifact変更は`independent_general_design_review_admitted=true`の場合だけ発行する。

review要否とresultの効力は、design identity、normative boundary、semantic effect boundary、固定反証対象、反例の有無を変え得る入力へbindする。それらを変えるresultをartifact変更前に受領した場合は、依存するstateだけを失効して現在入力で判断し直す。`counterexample_found`は直接supportを変えるresultだけが失効でき、無関係な変更へ停止効果を広げない。`unavailable`の原因であるpermission、producer availabilityまたはresult配送が変わった場合は、そのstateだけを失効し新しいreview operationを作れる。

このbindingへ固定field、path、locator、record identity、列挙順または取得件数を要求しない。

## 敵対的reviewの停止条件

情報封鎖reviewerには、この文書、Candidate147制御原文、一般設計原則だけを渡す。実装、Target評価、評価case、fixture、oracle、rating、旧Candidate、保存済み評価結果、先行findingは渡さない。

reviewerは、一般入力で不要review、review漏れ、rootによる反例代行、必須観測失敗時のreview未起動、具体的反例の失効、不完全な`no_counterexample_found`、未来全域の証明要求、禁止情報依存、処理手順依存がartifact変更可否またはterminalを誤らせるかを確認する。一件でも成立すれば設計を改訂し、再reviewする。`no_counterexample_found`の場合だけCandidate bundleを作る。

## 実装後gate

設計review通過後に限り、Candidate147を直接親とする新bundleへ一つのpredicateを接続する。既存ADR9 r2のcase、TaskSpec、fixture、oracle、ratingは変更しない。最初のCandidate gateは9ケース各N=5とし、新Candidateだけを実行する。一般機序違反が一件でもあればStandard14、採用、release、projectionへ進めず、新しいCandidate identityで設計境界へ戻る。

## 情報封鎖review結果

- producer: `candidate181_adversarial_review`
- 許可入力: Candidate147制御原文、本リポジトリの一般設計原則、この設計文書
- 禁止入力: 実装、評価case、fixture、oracle、rating、保存済み評価結果、旧Candidate、先行finding、会話履歴
- terminal result: `no_counterexample_found`

固定した9観点について、artifact変更可否またはterminalを誤らせる一般入力の具体的反例は確認されなかった。この結果は設計からCandidate bundleを作ることだけを許可し、成果品質、Target評価通過、採用、releaseまたはprojectionを意味しない。
