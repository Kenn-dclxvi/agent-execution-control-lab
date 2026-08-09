# Candidate169 修正判定命題と証拠役割の閉包設計

> **位置づけ**: 破棄済み旧設計系列の履歴Candidate／現行設計へ継承しない

## 結論

Candidate169はCandidate168を直接の親とし、`REPAIR_CONTRACT_ADMISSION`の修正必要性判定を、判定対象となる命題と、その命題を直接証明できる証拠役割の対応まで含むpredicateへ置き換える。固定済み七ケース、TaskSpec、allowed read、oracle、rating contractは変更しない。

Candidate168は、現在の違反と必要な修正後条件の立証責任を導入して修正不要ケースを10 / 10通過させた。一方、判定不能ケースでは4 / 10しか正しく停止できなかった。許可された同じ入力から、「実際の事象が起きたか」「手順と意味的に整合するか」「公開表現として根拠強度が適切か」という非同値な命題を選べてしまい、選んだ命題に対しては具体的矛盾を構成できたためである。

Candidate169の変更軸は一つだけとする。

```text
repair_decision_evidence_closed :=
    repair_decision_proposition_ready
    ∧ proposition_evidence_admissibleな直接根拠だけで
      satisfactionまたはviolationと必要なpostconditionを立証可能
```

## 親Candidateと保持する境界

- 親Candidateは`the-caption-3ce91a4-repair-evidence-burden-r1`とする。
- Candidate168 targeted評価は35 / 35 valid、Score `4 / 1 = 29 / 6`だった。
- 修正不要の意味的整合ケースは10 / 10通過したため、より良い表現を修正理由にしない立証責任は保持する。
- 判定不能ケースは、修正4件、正しい停止4件、誤った`no_repair_required` 1件を含み、判定命題の選択と証拠役割の混同が残った。
- cleanとperturbedのproducer routing、先行評価の情報封鎖、既存の三つの終端状態は保持する。

## 一つの変更軸

Candidate168の`REPAIR_CONTRACT_ADMISSION`を、次の命題・証拠対応を含む同名predicateへ置き換える。

### 1. 修正判定命題を先に固定する

```text
repair_decision_proposition :=
    TaskSpecのrequired outcome、repair criterion、stop condition、
    preservation constraintを共同で満たし、
    その真偽が現在artifactの修正要否を決める一つの命題

repair_decision_proposition_ready :=
    非同値な別命題を選ぶとterminal dispositionまたは許されるactionが
    変わる余地がない
```

局所的なcriterion句だけを取り出して、TaskSpec全体が要求する命題を別の命題へ置き換えない。複数の非同値な命題が残り、それぞれが異なる終端状態または操作を導く場合は、証拠を評価する前に`unavailable`とする。

### 2. 証拠の役割を固定する

```text
evidence_role :=
    normative_authority | current_artifact | event_observation | provenance

proposition_evidence_admissible :=
    resultのevidence_roleがrepair_decision_propositionの真偽を
    直接bindできる
```

各役割が直接証明できる範囲を次のように限定する。

- `normative_authority`は、要求される手順、期待状態または意味的制約を証明する。過去または実行時に実際に起きた事象を証明しない。
- `current_artifact`は、現在内容と、そのartifactが何を主張しているかを証明する。自身が記述する事実の真偽を証明しない。
- `event_observation`は、観測対象の実行、応答、状態または事象が実際にどうだったかを証明する。
- `provenance`は、旧版、差分、変更履歴または由来を証明する。旧表現の正しさや、現在主張の真偽を証明しない。

同じファイルが複数の情報を含む場合も、resultが直接観測した役割ごとに扱う。役割を越えた推論で不足する観測を補完しない。

### 3. 主張強度の調整との境界

TaskSpecのrequired outcomeが、許可された証拠に合わせて公開表現または主張強度を調整することを明示している場合は、「その表現が証拠強度に適合するか」を`repair_decision_proposition`にできる。

一方、TaskSpec全体が記述対象の事実が正しいかを要求し、直接観測がなければ停止するよう定めている場合、criterionに観測強度、根拠、説明などの語が含まれることだけを理由に、命題を公開表現の支持可能性へ変換しない。事象の直接根拠が欠けているときは、弱い表現への変更も、現在表現の追認も行わず`unavailable`とする。

### 4. 三つの終端状態

- `no_repair_required`: `proposition_evidence_admissible`な許可済み直接根拠が、現在artifactについて判定命題の充足を示す。
- `ready`: 同じく適格な直接根拠が判定命題の違反を示し、全required postconditionがその違反の解消に必要と立証される。
- `unavailable`: 判定命題が一つに定まらない、命題に対応する直接根拠が欠ける、または充足と違反・必要条件のいずれも立証できない。

Candidate168の立証責任は維持する。より安全、明確、詳細または完全な代替を構成できること、支持根拠が見つからないこと、旧表現があることだけでは`ready`にしない。

## 設計時の反証監査

この表は候補promptへ埋め込む分岐ではなく、一般predicateが固定済みTaskSpecを矛盾なく処理できるかを実装前に確認するための監査である。

| 操作の種類 | TaskSpec全体から固定される命題 | 必要な証拠役割 | 一般則が導く状態 |
| --- | --- | --- | --- |
| 手順との意味的対応を確認する修正 | 現在内容が要求された手順・意味制約を満たすか | `current_artifact` + `normative_authority` | 充足を直接確認できれば`no_repair_required` |
| 文書内部の具体的不整合を直す修正 | 現在内容が同じartifact内の固定済み条件と矛盾するか | `current_artifact`、必要に応じて`normative_authority` | 違反と必要条件を直接確認できれば`ready` |
| 過去の実行事象を述べる主張の正否を確定する修正 | 記述された事象が実際に起きたか | `current_artifact` + `event_observation` | 事象観測が欠ければ`unavailable` |

この対応を成立させるためにケースID、対象path、特定語句または期待terminalが必要になるなら、設計不成立としてCandidateを実装しない。

## 消す判断点

- TaskSpec全体より局所criterionを優先し、事実の正否を表現の支持可能性へ読み替える判断。
- normative authorityから過去または実行時の事象が実際に起きたと推定する判断。
- current artifactの記述を、その記述自身の真実性の証拠として循環利用する判断。
- provenanceにある旧表現を、旧表現の正しさまたは修正後の正解として扱う判断。
- 直接観測がない事実主張を、弱い表現への変更で解決したとみなす判断。

## 新たに増える判断点

- TaskSpec全体から、修正要否を決める命題が一つに定まるか。
- 受領resultの証拠役割が、その命題の真偽を直接bindできるか。
- TaskSpecが要求するのが事実の正否か、証拠に適合した表現強度か。

これらは、ケース名、対象文書、特定語句、期待terminalに依存しない。コード、設定、文書、構造化アーティファクトの修正要否判定へ共通に適用する。

## 非目標

- 固定済みケース、TaskSpec、allowed read、oracle、rating contractの変更。
- 特定のケースID、見出し、語句またはpathによる分岐。
- 証拠に基づく主張強度の調整一般を禁止すること。
- 欠けたevent observationを得るため、forbidden inputや未許可pathを読むこと。
- 独立reviewerの常時起動、reviewerによる実装、変更後レビューの追加。
- Standard14、採用、release、projectionの同時判断。

## 評価と停止条件

1. この設計の反証監査を終えてから、Candidate168を親に`REPAIR_CONTRACT_ADMISSION`だけが変わるfull bundleを作成する。
2. 候補実装後に構造試験と全回帰試験を完了する。Target評価を設計または実装の入力に使わない。
3. 固定済み七ケースのLayer 1を再利用し、prompt identity以外の条件をpreflightで照合する。
4. Candidate169だけを各ケース`N=5`で実行し、既存のoracleとratingで採点する。ケース、TaskSpec、allowed read、oracle、ratingを評価結果に合わせて変更しない。
5. 評価結果への候補側の対策は、この一般設計から導ける場合だけ許す。試験固有の条件は追加しない。
6. 35 / 35 valid、35 / 35 Score `4`、全mechanism条件成立の場合だけStandard14を検討する。
7. 一件でも不成立なら結果を保存する。命題・証拠対応を適用しても同じ曖昧性が残る場合は、model-visibleなTaskSpecとoracleの対応が一意でない可能性を結論に含め、局所規則の追加を停止する。

## 状態

`design_complete / fixed_cases_unchanged / one_axis_repair_decision_evidence_closure / candidate_materialized / targeted_35_of_35_valid / score4_30 / score1_5 / quality_and_mechanism_gates_failed / standard14_not_started`
