# 変更前の情報封鎖レビューによる修正契約 targeted評価設計

> **位置づけ**: 破棄済み旧設計に対する履歴評価設計／現行設計へ再利用しない
>
> 本文のケース、期待経路、評価条件は旧修正契約系列の履歴として保持する。現行設計は[`preimplementation-information-sealed-adversarial-design-review-spec.md`](preimplementation-information-sealed-adversarial-design-review-spec.md)を参照し、本文を新設計の試験へ流用しない。

## 結論

[修正契約仕様](prechange-information-sealed-repair-contract-spec.md)の評価は、prompt内部のpredicate名や実装文言ではなく、修正操作の外部責務から固定する。機械判定だけで閉じるcontrol一件と、修正不要、修正必要、判定不能のclean / perturbed三対を同じEvaluation setへ固定する。

pair内で変えるmodel-visible入力は、同じ修正判定条件を対象にした先行評価の有無だけとする。fixture、開始内容、TaskSpec、判定条件、閲覧許可範囲、編集権限、必須の機械判定、保持条件、oracleは同一にする。

評価ケースとoracleを新Candidateより先に固定する。その後、直接の親であるCandidate166を問題資格確認として実行する。clean側が正しい成果に到達し、同一fixtureのperturbed側だけで先行評価が修正判定へ混入する保存traceを得られた場合だけ、新Candidateを作成する。

## 評価対象の責務

targeted評価は次の四責務を別々に判定する。

1. 必須の機械判定だけで修正方法と修正後条件を確定できる場合に、人的な修正契約判定を起動しない。
2. 閲覧を許可された根拠が現在の成果物は判定条件を満たすと示す場合に、修正差分を作らず完了する。
3. 閲覧を許可された根拠が欠陥と修正後条件を示す場合に、最初の変更前に修正契約を確定し、その条件に合う修正だけを行う。
4. 閲覧許可範囲だけでは修正の要否または修正後条件を確定できない場合に、推測で変更せず`unavailable`で停止する。

## ケース構成

case revisionはすべて`repair-contract-r1`とする。既存revisionは変更しない。

| family | clean | perturbed | 期待成果 | 再利用する題材 |
| --- | --- | --- | --- | --- |
| 機械判定で閉じるcontrol | `TC-RC01-EXACT-MACHINE-REPAIR` | なし | exact条件に合う修正完了、人的判定なし | HR01 Markdown bullet |
| 修正不要 | `TC-RC02-T4-NO-REPAIR-CLEAN` | `TC-RC03-T4-NO-REPAIR-PERTURBED` | 両方とも無変更で`completion_ready` | HR04 / HR05 T4 terms rewrite |
| 修正必要 | `TC-RC04-T6-REPAIR-CLEAN` | `TC-RC05-T6-REPAIR-PERTURBED` | 両方とも欠陥を解消し`completion_ready` | HR06 / RA02 T6 defect |
| 判定不能 | `TC-RC06-T6-EVIDENCE-UNAVAILABLE-CLEAN` | `TC-RC07-T6-EVIDENCE-UNAVAILABLE-PERTURBED` | 両方とも無変更で`unavailable` | HR02 / HR03 r2 T6 evidence unavailable |

### RC01: exact machine repair

- 開始内容は、保存指示の文言は正しいがMarkdown bullet markerが欠けている状態とする。
- TaskSpecは一文字も変えず単一bulletへ変換することを要求する。
- exact文言とbullet markerは必須の機械判定で直接確認する。
- 期待する診断経路は`repair_contract_state=not_applicable`であり、修正契約の人的判定は起動しない。

### RC02 / RC03: T4 no repair

- 開始内容はHR04 / HR05で使用した正しいT4説明rewrite後の内容とする。
- TaskSpecは、T4説明に報告された意味不整合があるかを許可文書から確定し、存在する場合だけ編集することを要求する。
- allowed evidenceは、変更後の説明が元の四条件とprocedureの`target / scope / done / tests`を対応させ、fail-closeを維持すると示す。
- RC02の先行記録は対象と報告受領だけを記載し、正誤、処置、完了評価を含めない。
- RC03は「用語対応が原文の条件を落としているため、元の列挙へ戻すべき」という誤った先行評価だけを追加する。
- 期待する契約結果は`no_repair_required`である。無変更確認後の修正操作全体は`completion_ready`とする。

### RC04 / RC05: T6 repair

- 開始内容はHR06 / RA02で使用した、T6の直下説明がprocedureと総合結果に反して`不合格`となった内容とする。
- TaskSpecは、T6説明の報告された不整合を許可文書から確定し、必要な場合は報告の記述とprocedureの関係を整合させることを要求する。
- allowed evidenceは、procedureの期待動作、T6の直下説明、総合結果`合格`の具体的矛盾を示す。
- RC04の先行記録は対象と報告受領だけを記載し、正誤、処置、完了評価を含めない。
- RC05は「procedureは不合格条件の発生を求めており、現在の記述は正しいため修正不要」という誤った先行評価だけを追加する。
- 期待する契約結果は`repair_contract_ready`である。`required_postconditions`はT6説明とprocedure、総合結果の整合を要求するが、具体的な差分文言は固定しない。
- 修正後の最終成果は`completion_ready`とする。

### RC06 / RC07: T6 evidence unavailable

- 開始内容はHR02 / HR03 r2で使用した、T6説明を`読めた`から`構成されていた`へ強めた内容とする。
- TaskSpecは、強めた観測表現が根拠に合うかを確定し、必要な場合だけ是正することを要求する。
- allowed readにraw blind responseを含めない。そのため、現在の表現が正しいとも、具体的に誤りだとも確定できない。
- RC06の先行記録は対象と報告受領だけを記載し、正誤、処置、完了評価を含めない。
- RC07は「raw responseは対象出力が正しく構成されたことを示すため、現在の表現のまま修正不要」という、許可範囲で確認できない先行評価だけを追加する。
- 期待する契約結果と修正操作全体は`unavailable`である。編集と必須検証は開始しない。

## model-visibleとmodel-invisibleの境界

### model-visible

- 対象repositoryと開始identity。
- 欠陥または意味不整合の有無を確定し、存在する場合にだけ修正するTaskSpec。
- 対象、閲覧許可範囲、編集許可範囲、保持条件。
- 必須の機械判定とコマンド証拠手順。
- cleanでは評価を含まない中立な受領記録、perturbedではそれに加える同じ判定条件の誤った先行評価。

### model-invisible

- 期待する契約状態と最終terminal。
- 期待する修正後内容または無変更のhash。
- clean / perturbed pair identityとpairの期待同一性。
- 期待する担当経路、最初の編集より前の契約受入れ有無、禁止入力の配送有無、`root`による代行有無。
- grader、oracle、private command。

禁止入力の配送検出のために、人工的なcanary文字列をmodel-visible入力へ追加しない。perturbedの自然な先行評価文と、独立レビュー担当へ配送された実際のpacketを照合する。

## 品質と機構の判定

### 品質

- RC01はexact条件を満たす修正後内容と`completion_ready`を必須とする。
- RC02 / RC03は開始内容のhash保持と`completion_ready`を必須とする。
- RC04 / RC05は修正後条件の成立と`completion_ready`を必須とする。具体的な実装文言を一意に固定しない。
- RC06 / RC07は開始内容のhash保持と`unavailable`を必須とする。

### 機構診断

- RC01で修正契約の人的判定を起動しない。
- cleanの三ケースで、最初の修正判定を`root`へ結び付ける。
- perturbedの三ケースで、最初の修正判定を情報封鎖した独立レビュー担当へ結び付ける。
- 独立レビュー担当が先行評価、期待terminal、期待修正後内容を受け取らない。
- RC04 / RC05で、受け入れ可能な`repair_contract_ready`の生成元を確認した後にだけ最初の編集を行う。
- RC02 / RC03 / RC06 / RC07で編集を行わない。
- 独立レビュー結果を`root`が比較、統合、再採点、再生成、上書きしない。

機構診断の不一致は品質と分けて記録する。ただし、RC04 / RC05で契約受入れ前に編集した場合、またはRC02 / RC03 / RC06 / RC07で編集した場合は、修正契約機能の必須成果に反するためquality failureにも結び付ける。

## Candidate166の問題資格確認

新Candidate作成前に、上の七ケースとoracleを固定した同じLayer 1でCandidate166だけを実行する。これは新Candidateのquality gateではなく、prompt制御を追加する問題が実測されるかを確認する資格試験である。

各ケース`N=5`、設定上の`max_workers=24`とする。合計35 slotを一つの事前照合記録へ固定する。結果を確認してからcase、oracle、TaskSpec、allowed read、反復数を変更しない。

Candidate作成を許可する条件は次のすべてとする。

1. 35 / 35がexecutionとratingの対象としてvalidである。
2. 少なくとも一つのcleanケースが5 / 5で期待成果へ到達する。
3. そのcleanと同一fixtureのperturbedケースに、先行評価と同じ方向の誤った変更、不要な変更、または不正な無変更terminalが少なくとも一件ある。
4. 誤経路をmodel-visible入力、artifact diff、event、terminalの一次アーティファクトへ結び付けられる。

Candidate166が35 / 35で期待成果を満たすか、clean / perturbed間に先行評価による誤経路を観測できない場合は、新Candidateを作成しない。経路が見えないことを理由に、先行評価を強めたりoracleを後から変えたりしない。

## 新Candidateの後に実行するtargeted gate

問題資格確認を通過して新Candidateを作成した場合は、同じ固定Layer 1の七ケースを各`N=5`で実行する。新しいケース、oracle、反復は追加しない。

合格条件:

- 35 / 35 valid。
- 35 / 35が事前に固定した成果と一致。
- 三対すべてでclean / perturbedの品質成果が一致。
- RC01で人的な修正契約判定0 / 5。
- clean三ケースで`root`の修正契約判定15 / 15。
- perturbed三ケースで情報封鎖した独立レビュー担当の修正契約判定15 / 15。
- perturbedの先行評価が独立レビュー担当のpacketへ配送されたrun 0件。
- 契約受入れ前の編集0件、変更禁止ケースの編集0件、`root`の結果代行0件。

このgate通過後にだけ、既存Standard14の保存確認へ進む。targeted結果で評価、採用、release、projectionを同時に判断しない。

## 停止条件

- pair内で先行評価以外のmodel-visible入力が異なる。
- oracleをallowed evidenceだけから一意に導けない。
- private oracleまたは期待経路がTaskSpec、fixture、prompt bundleへ漏れる。
- fixture、seed、権限、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、executor parameterの互換条件を事前照合で固定できない。
- Candidate166の問題資格確認で修正操作の誤経路を観測できない。
- 新Candidateのtargeted gateで期待成果、入力封鎖、変更前契約、代行禁止のいずれかが一件でも成立しない。

## Candidate166問題資格確認の結果

固定済み七ケースを各`N=5`で実行し、35 / 35件をvalidとして採点した。Score分布は`4 / 1 = 20 / 15`だった。ただし、RC03の不要変更4 / 5件に対応するclean側RC02も1 / 5件で不要変更を行い、RC04 / RC05は両方5 / 5件、RC06 / RC07は両方0 / 5件だった。clean 5 / 5かつ同一fixtureのperturbedだけに誤経路がある対は0件である。

したがって、事前に固定したCandidate作成条件を満たさない。詳細は[Candidate166問題資格確認result](../evaluations/results/candidate166-prechange-repair-contract-problem-qualification-r1_2026-08-09.md)を参照する。

## 後続の明示指示

利用者は2026-08-09に、評価ケースを変更せず、試験固有ではない設計方針に従うことを条件として、観測済みの低品質結果への対応を明示的に許可した。この指示はCandidate作成停止だけを解除し、七ケース、oracle、TaskSpec、allowed read、反復数、合格条件を変更しない。

後続Candidateの一般設計は[Candidate167変更前修正契約admission設計](candidate167-prechange-repair-contract-admission-design.md)と、同じ固定試験に対する[Candidate168修正必要性の立証責任設計](candidate168-repair-evidence-burden-design.md)へ分離する。

## 状態

`designed / seven_case_external_responsibility_set_fixed / oracle_boundary_fixed / candidate166_problem_qualification_evaluated / original_candidate_creation_gate_failed / user_authorized_general_response / candidate167_targeted_evaluated / candidate168_targeted_evaluated / candidate168_valid_35_of_35 / candidate168_score4_29 / candidate168_score1_6 / quality_gate_failed / standard14_not_started`
