# Candidate168 修正必要性の立証責任設計

> **位置づけ**: 破棄済み旧設計系列の履歴Candidate／現行設計へ継承しない

## 結論

Candidate168はCandidate167を直接の親とし、`REPAIR_CONTRACT_ADMISSION`を、修正可能性ではなく修正必要性の立証を要求するpredicateへ置き換える。固定済み七ケース、TaskSpec、allowed read、oracle、rating contractは変更しない。

Candidate167は、情報封鎖とproducer routingを成立させた一方で、現在内容を支持する根拠の欠如、より安全または明確な代替表現の構成可能性、過去差分にある旧表現を、欠陥と修正後条件の根拠として受け入れた。その結果、修正不要ケースで明確化のための変更を行い、判定不能ケースで保守的な表現変更を行った。

Candidate168の変更軸は一つだけとする。

```text
repair_contract_ready :=
    current violationが許可済み直接根拠で立証済み
    ∧ 各required postconditionがそのviolationの解消に必要と立証済み
```

## 親Candidateと観測済み誤経路

- 親Candidateは`the-caption-3ce91a4-prechange-repair-contract-admission-r1`とする。
- Candidate167 targeted評価は35 / 35 validだったが、Score `4 / 1 = 21 / 14`でquality gateを通過しなかった。
- 修正不要ケースでは、現在内容が判定条件を意味的に満たしていても、より明示的または完全な説明を作れることを修正理由にした。
- 判定不能ケースでは、raw evidenceが許可範囲にないことを現在表現の欠陥とみなし、過去差分にある弱い表現を修正後条件として採用した。
- cleanとperturbedのproducer routingおよび先行評価の情報封鎖は成立していたため、担当選択ではなく、同じproducerが用いる修正必要性の判定境界を変更対象にする。

## 一つの変更軸

Candidate167の`REPAIR_CONTRACT_ADMISSION`を、次の立証責任を持つ同名predicateへ置き換える。

### 1. 非機械判定の初期状態

非機械的な意味判断が必要な修正操作は、rootが担当選択前に`no_repair_required`を先取りせず、まず`unobserved`へ結び付ける。先行評価の有無からproducerを一つ選び、そのproducerだけが終端状態を返す。

### 2. 現在の違反の立証

```text
repair_violation_proven :=
    許可済み直接根拠が、現在artifactとbind済みrepair criterionの
    具体的な矛盾または必須効果の欠落を観測している
```

次の事実だけでは`repair_violation_proven=true`にしない。

- 現在の主張を支持する根拠がallowed readに存在しないこと。
- 現在より安全、明確、詳細または完全な表現を構成できること。
- 過去差分、旧版または既存例に別の表現があること。
- より広いrepository authorityの内容を現在artifactが逐語的に再掲していないこと。
- 修正要求または先行評価が存在すること。

TaskSpecが「指定された完全な証拠集合に支持根拠が存在しないこと」自体を欠陥として明示した場合だけ、その完全性と不在を直接観測した結果を違反の根拠にできる。閲覧範囲が完全な証拠集合であると結び付けられない場合、支持根拠の欠如は真偽も欠陥も確定しない。

### 3. 修正後条件の必要性

```text
repair_postconditions_proven :=
    全required postconditionが、立証済みviolationを解消するために必要
    ∧ repair criterionを越える改善を含まない
```

具体的な矛盾が立証されていない状態で、安全そうな表現、以前の表現、一般的なベストプラクティスから修正後条件を構成しない。判定条件をすでに満たす意味的に同等な表現へ、用語一致、明確化、補足または全authorityの再掲を要求しない。

### 4. 三つの終端状態

- `no_repair_required`: 許可済み直接根拠が、現在artifactはbind済みrepair criterionを満たすと示す。意味的に同等な表現を認め、より良い表現の余地を修正理由にしない。
- `ready`: `repair_violation_proven=true`かつ`repair_postconditions_proven=true`である。
- `unavailable`: `no_repair_required`も、違反と必要な修正後条件の両方も立証できない。支持根拠の欠如、より安全な代替案、過去の文言だけが得られた場合を含む。

## 消す判断点

- 「根拠がないため強い表現を弱める」という推測修正。
- 「より分かりやすくできるため修正する」という編集上の改善。
- 過去差分の旧表現を修正後の正解として扱う判断。
- producer選択前にrootが非機械判定を`no_repair_required`へ確定する判断。

## 新たに増える判断点

- TaskSpecが証拠集合の完全性と、支持根拠の不在自体を欠陥として明示しているか。
- 各修正後条件が、立証済みの具体的違反を解消するために必要か。

この二点は、ケース名、対象文書、特定語句、期待terminalへ依存しない。文書、設定、コード、構造化アーティファクトの修正操作へ共通に適用する。

## 非目標

- 固定済みケース、TaskSpec、allowed read、oracle、rating contractの変更。
- 特定のケースID、見出し、語句またはpathによる分岐。
- 根拠に基づく主張強度の管理一般を禁止すること。TaskSpecが証拠集合と不在時の処置を明示した別操作では、そのrequired outcomeを適用する。
- 独立reviewerの常時起動、reviewerによる実装、変更後レビューの追加。
- Standard14、採用、release、projectionの同時判断。

## 評価と停止条件

1. Candidate167を親に、root `AGENTS.md`の`REPAIR_CONTRACT_ADMISSION`だけが変わるfull bundleを作成する。
2. 固定済み七ケースのLayer 1を再利用し、prompt identity以外の条件をpreflightで照合する。
3. Candidate168だけを各ケース`N=5`で実行し、既存のoracleとratingで採点する。
4. 35 / 35 valid、35 / 35 Score `4`、全mechanism条件成立の場合だけ次段階を検討する。
5. 一件でも不成立なら、ケースや評価条件を変更せず、結果を保存してStandard14前で停止する。

## 状態

`design_complete / fixed_cases_unchanged / one_axis_repair_evidence_burden / candidate_materialized / targeted_35_of_35_valid / score4_29 / score1_6 / quality_gate_failed / standard14_not_started`
