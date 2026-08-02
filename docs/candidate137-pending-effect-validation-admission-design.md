# Candidate137 pending-effect validation admission設計

## 結論

Candidate137はCandidate136を直接親とし、root `AGENTS.md`の`RECOVERY`だけを置換する。変更前に観測済みの未充足effectだけを変更するCandidate136の境界を維持し、未観測effectを充足済みと推測せず、TaskSpec-required validationが変更後状態を直接判定できる場合だけvalidationへadmitする。

変更軸は検索語、read回数、command、case固有symbolではない。全effectの充足をvalidation開始前に要求していたCandidate128の二値closureを、`validationへ進める状態`と`完了できる状態`へ分ける。

## Identity

- candidate number: Candidate137
- prompt identity: `the-caption-3ce91a4-pending-effect-validation-admission-r1`
- direct parent: `the-caption-3ce91a4-effect-local-change-admission-r1`（Candidate136）
- changed target: root `AGENTS.md`
- changed label: `RECOVERY`
- evaluation status: `not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. 基準prompt setはCandidate136とする。最短正常経路は、観測済み未充足effectだけを変更し、未観測effectを変更せず、TaskSpec-required validationがその変更後状態を直接判定した後にだけ全effectをclosedへbindする経路である。
2. 保存済み誤経路はCandidate136 F04 run `b187a52f5b834503b8f9da0d6cb72b53`である。必要な一行変更は成功したが、別effectが未観測だったためrequired validationを開始せずscore `3`となった。Candidate132にも同じ変更後false stopが1 / 5件ある。
3. F04 TaskSpecは二つのsource behaviorを静的確認するrequired validationを明示する。Candidate119由来の`VALIDATION_PLAN`はpredicateが固定済みならexact commandをmethodとして選べる。一方、Candidate128由来の`required_effects_closed`がそのvalidation前に全effectの証明を要求し、直接observerへ進む経路を遮断する。
4. 置換軸は`pending_effect_validation_admitted`、`required_effects_validation_ready`、validation resultを入力に含む`required_effects_closed`の一つの状態遷移である。
5. 消す判断点は、観測済み未充足effectを正しく変更した後、未観測effectを推測でclosedにするか、required observerを発行せず停止するかという二分岐である。
6. 増える判断点は、TaskSpec-required validationがpending effectを変更後artifact上で直接判定するかの一件である。一般的なtest、lint、build、diff、statusまたは他effectの成功を直接判定へ読み替えない。
7. F04 N=5で全件score `4`、必要変更5 / 5、充足済みeffect変更0 / 5、initial patch failure 0 / 5、required validation完備5 / 5、pending effect observer経路が発生した場合はvalidation前false stop 0件を要求する。
8. prompt、case、fixture、TaskSpec、rating、model、reasoning、CLI/runtime、permission、executor挙動、token accountingをCandidate136の互換条件へ固定し、profileの`max_workers=24`を維持する。
9. score `3`以下、未観測effectの推測変更、direct observerを持たないpending effectでのvalidation開始、validation result前の完了、または既存stop conditionを越えた追加read / 追加変更が一件でもあれば停止する。

## 保存挙動からの導出

Candidate125は開始状態で充足済みのeffectを不要な変更へ戻し、F04の登録済み30 run中5件をscore `2`にした。Candidate126、Candidate129、Candidate131は完全性を変更前gateへ置き、未観測effectが観測済み未充足effectの変更まで止めるfalse stopを観測した。

Candidate136はこの二つを分離した。未観測effectを変更せず、別の観測済み未充足effectを5 / 5で変更した。しかしCandidate128のclosureを維持したため、正しい部分変更後もpending effectを直接確認するrequired validationへ進めなかった。

したがって次の制御点はcontent取得方法ではない。変更admission、validation admission、terminal closureの位置関係である。

## 置換する状態遷移

```text
pending_effect_validation_admitted(effect) :=
  prechange stateがunobserved
  ∧ artifact変更resultがそのeffectを所有するcontentを変更していない
  ∧ TaskSpec-required validationが変更後artifact上のeffectを直接判定する
  ∧ pass conditionとstop conditionがbind済み

required_effects_validation_ready :=
  各effectが applied / prechange satisfied / pending observer admitted のいずれか

required_effects_closed :=
  各effectが applied / prechange satisfied / direct validation passed のいずれか
```

- 観測済み未充足effectが残る場合はvalidationへ進まず、既存reworkまたは停止を使う。
- 未観測effectへdirect observerがなければ停止する。
- pending effectを推測で変更しない。
- direct observerのnon-successから追加read、別method、追加変更を開かない。
- 全effectがclosedになるまで完了しない。

## 既存制御との関係

- C94 / C95のoperation開始前`spec_ready`: 変更しない。
- C125のsingle-target continuation: 変更しない。
- C136のeffect-local initial change admission: 維持する。
- C119由来のvalidation predicate / method境界: 維持する。
- C71 / C81由来のvalidation result closure: 維持する。
- C76のfinal-state observer: 設計証拠として参照するが継承しない。C76はvalidation間のtarget-version順序を扱い、本candidateはpending effectを直接判定できるvalidation admissionを扱う。

## 汎用性と非目標

適用対象は、複数required effectの一部が未観測で、観測済み未充足effectを変更済みかつ、TaskSpec-required validationが未観測effectの変更後状態を直接判定できるimplementationである。言語、拡張子、target数、hunk数、case ID、symbol名をpredicateへ含めない。

次は非目標とする。

- outcome valueが未固定のclarification task
- read-only reviewまたはboundary disposition
- direct observerを持たないpending effectの楽観的完了
- 特定lexeme、検索command、read範囲、出力配送方法の固定
- executor、adapter、runtime hook、外部wrapperの変更
- validation failure後の新しいrework経路

## 初回評価gate

初回はF04 N=5、M=24だけを実施する。score `3`以下が一件でも出た時点で停止し、F02、F07、追加24件、Standard14へ進めない。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| score `3`以下 | 0 / 5 |
| 必要な未充足effect変更 | 5 / 5 |
| 充足済みまたは未観測effectの変更 | 0 / 5 |
| initial patch failure | 0 / 5 |
| required validation完備 | 5 / 5 |
| direct observerなしpending effectでのvalidation開始 | 0 / 5 |
| validation result前の全effect完了判定 | 0 / 5 |

