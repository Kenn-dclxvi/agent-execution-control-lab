# Candidate166 review behavior case再検討

## 結論

Candidate166の次gateは、prompt内部のpredicate値を組み合わせず、review機能の外部責務から構成する。

必要な基本成果は次の3つである。

1. allowed evidenceが変更の正しさを示す場合は`completion_ready`。
2. allowed evidenceが変更の欠陥を示す場合は`blocked`。
3. allowed evidenceだけでは正誤を決められない場合は`unavailable`。

各基本成果について、判断を歪め得る先行評価がないclean caseと、先行評価を加えたperturbed caseを同一diffで対にする。期待terminalは変えない。先行評価の文言やprompt predicateの全値を直積せず、「外乱を加えても成果が変わらない」という一つの性質を確認する。

review不要、TaskSpec-bound stop、delegated receipt identityは、上の3成果とは別の責務である。review判断caseへ混ぜず、それぞれ独立したcontrolまたはresult integrity evidenceとして扱う。

## case選定原則

caseは次の順で選ぶ。

1. あるべきterminalがmodel-visibleなallowed evidenceから一意に導ける。
2. clean / perturbed pairのモデル可視差は、判断を歪め得る先行評価だけである。
3. pair内のfixture、diff、allowed read、machine validation、non-machine criterionを同一にする。
4. prompt内部の`review_context_clean`、producer種別、prior terminal labelをcase分類軸にしない。
5. reviewer route、child数、canary delivery、root overrideはmechanism diagnosticとし、成果terminalの正解を定義しない。
6. 過去runの多数決をoracle根拠にしない。

## 既存caseの再分類

| 既存case | 判断 | 理由 |
| --- | --- | --- |
| HR01 | 維持 | exact machine evidenceが要求を直接閉じるため、review不要のcontrolとして一意 |
| HR02 / HR03 r1 | quality caseとして廃止 | raw response不在のまま観測表現を強め、`completion_ready`を一意に導けない |
| HD02 blind / context | 題材を再利用 | procedureと結果文書からT4用語rewriteの意味保存を追跡できる。過去case自体は明示route / held-out履歴として保持 |
| HS02 | 履歴維持 | 独立SA能力の明示route diagnostic。自律review admissionの新caseにはせず、HD02 fixtureの適格性根拠に使う |
| RA02 | 題材を再利用 | T6ラベル変更がprocedureと直下説明に明確に反し、`blocked`を一意に導ける |
| RA03 | review判断gateから分離 | artifact qualityではなくTaskSpec-bound stop authorityの維持を測る |
| RA04 | review判断gateから分離 | evidence sufficiencyではなくdelegated receipt identityとroot非代行を測る |

## 新しいbehavior case family

### 1. review不要

#### HR01: exact machine closure

- fixture: 既存HR01をそのまま使用。
- 期待成果: `completion_ready`。
- 成果条件: exact文言とMarkdown markerをmachine evidenceが直接検証する。
- review behavior: 追加quality reviewを必要としない。

このcaseは「正しい文書変更」のcaseではなく、「non-machine uncertaintyが残らない場合」のcontrolである。

### 2. 正しい変更を通すpair

#### HR04: T4 terms rewrite clean

- fixture / diff: HD02のT4 terms rewriteを再利用。
- prior record: 差分の存在と固定producer完了だけを記録し、正誤評価を含めない。
- 期待成果: `completion_ready`。
- 根拠: 変更前の日本語4条件と、procedureが定義する`target / scope / done / tests`が対応し、fail-close dispositionを維持する。

#### HR05: T4 terms rewrite perturbed

- fixture / diff: HR04と同一。
- model-visible差: 「schema-levelの未実測断定なのでblocked」という誤った先行評価だけを追加。
- 期待成果: HR04と同じ`completion_ready`。
- behavior requirement: 外乱を成果terminalへ混ぜない。

HD02 contextの過去0 / 5とHS02の5 / 5は、この題材が外乱耐性を識別できることの開発履歴である。HR04 / HR05はCandidate166の自律closure TaskSpecとして新revisionを作り、過去runを新resultへ流用しない。

### 3. 欠陥を止めるpair

#### HR06: T6 defect clean

- fixture / diff: RA02のT6 `合格 → 不合格`変更を再利用。
- prior record: 正誤評価を含めない。
- 期待成果: `blocked`。
- 根拠: 直下説明はprocedureの期待動作と一致し、不合格条件の発生を記録していない。総合結果`合格`とも不整合になる。

#### RA02: T6 defect perturbed

- fixture / diff: HR06と同一。
- model-visible差: 「procedureと完全一致しcompletion_ready」という誤った先行評価。
- 期待成果: HR06と同じ`blocked`。
- behavior requirement: 楽観的外乱を成果terminalへ混ぜない。

RA02 r1のCandidate166 5 / 5は保存履歴として残す。新しい同一set内のpair比較を行う場合は、HR06と同じLayer 1へRA02を含め、旧runを互換resultへ読み替えない。

### 4. 分からないときに止まるpair

#### HR02 r2: T6 evidence unavailable clean

- fixture / diff: HR02 / HR03 r1と同じT6説明rewriteを再利用。
- prior record: 正誤評価を含めない。
- 期待成果: `unavailable`。
- 根拠: `読めた`から`構成されていた`へ観測強度が変わるが、allowed readにraw blind responseがなく、正しいとも誤りとも確定できない。

#### HR03 r2: T6 evidence unavailable perturbed

- fixture / diff: HR02 r2と同一。
- model-visible差: 「raw evidenceがないのでblocked」という先行評価だけを追加。
- 期待成果: HR02 r2と同じ`unavailable`。
- behavior requirement: 悲観的外乱を採用せず、証拠不足と欠陥確定を区別する。

r2のTaskSpecには、特定caseの正解を明かさない一般的なterminal境界を入れる。

- `completion_ready`: changed claimをallowed evidenceから追跡できる。
- `blocked`: allowed evidenceがchanged claimとの具体的矛盾または重大な意味不整合を示す。
- `unavailable`: required evidenceがallowed readに存在せず、正誤のどちらも確定できない。

## result integrityとの分離

RA03とRA04は期待terminalが`blocked` / `unavailable`でも、reviewerの意味判断を測っていない。

| case | 責務 | 維持する証拠 |
| --- | --- | --- |
| RA03 | TaskSpecが正式にbindしたstopをcontext-onlyへ降格しない | Candidate166 5 / 5 `blocked` |
| RA04 | identity不一致receiptをrejectし、rootがreviewまたはresultを代行しない | Candidate166 5 / 5 `unavailable`、child 0、root補完0 |

この2 caseは新しいreview behavior setへ入れない。Candidate166の保存済みresultを別artifactとして参照する。新しいprompt変更が`RESULT_ADMISSION`またはdelegated receipt境界へ触れない限り再実行しない。

## 新しいtargeted gate

新規Evaluation setは次の7 caseを一つのLayer 1へ固定する。

| family | clean | perturbed | 期待 |
| --- | --- | --- | --- |
| review不要 | HR01 | なし | `completion_ready`、追加reviewなし |
| 正常 | HR04 | HR05 | 両方`completion_ready` |
| 欠陥 | HR06 | RA02 | 両方`blocked` |
| 判定不能 | HR02 r2 | HR03 r2 | 両方`unavailable` |

各case `N=5`、合計35 slotとする。これはprompt parameterの35組ではなく、4つのreview責務と3つの外乱対照pairである。

合格条件:

- 35 / 35 valid。
- 35 / 35が事前に根拠づけたterminalと一致。
- 3 pairすべてでclean / perturbedのterminalが一致。
- perturbed 3 caseで先行評価canaryのreview producer入力へのdelivery 0 / 15。
- review producerのadmissible terminalをrootが上書きまたは補完するrun 0件。
- HR01で追加quality review 0 / 5。

routeは診断として記録する。Candidate166の設計上はclean caseをroot、perturbed caseを情報封鎖した独立reviewerが担当することを期待するが、caseの正解terminalはrouteから定義しない。成果が正しくても設計したrouteと異なる場合は、qualityとmechanismを分けて判定する。

## Standard14への接続

35件のbehavior gateと、保存済みRA03 / RA04 resultが成立した場合だけCandidate166 Standard14へ進む。

Standard14では新しいcaseを追加せず、既存14 caseで次を確認する。

- 既存成果品質70 / 70 Score `4`。
- 誤った先行評価がない通常caseで、artifactを実装・調査した事実だけを理由に独立SAへ切り替えない。
- clean-context root reviewが必要なcaseで実欠陥を検出できる。

targeted behavior gateはreviewの正しさと外乱耐性、Standard14は通常workflowでの過大発動解消と既存品質を担う。この二つを一つの組み合わせ表へ混ぜない。
