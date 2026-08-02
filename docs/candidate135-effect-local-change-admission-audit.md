# Candidate135 effect-local change admission監査

## 結論

Candidate135のScore 2は、単純なhunk文字列不一致だけではない。開始状態ですでに充足していた`colSpan` effectを未充足として再び変更対象へ入れ、必要な`hasAuditKey`変更と同じ原子的patchへ結合したことが直接原因である。

既存制御との対応は三点に分かれる。

1. Effect state: Candidate128のownerである。観測済みcurrent contentから各effectを`充足済み / 未充足 / 未観測`へ個別にbindする。
2. Change admission: Candidate129が試したが、未観測effectをtarget全体の開始拒否へ波及させて3 / 5件をfalse stopした。
3. Change construction: Candidate132のglobal preimage gateはstale変更を抑止したが、Point 2・3へ干渉して停止した。

したがって次案は、新しいglobal完全性gateではない。観測済み各effectの状態を独立に固定し、`未充足`へbindできたeffectだけを変更単位へ入れるpartial ledgerが最小である。`未観測`は変更対象へ推測追加せず、別の観測済み未充足effectの変更開始も拒否しない。ただし全effect closureを推測でtrueにせず、validation開始条件はCandidate128のまま維持する。

## C135成功4件との比較

成功4件の最終diffは、すべて次の一行変更だけだった。

```diff
-  const hasAuditKey = true;
+  const hasAuditKey = funds.some((fund) => fund.audit_match_key.trim() !== "");
```

1件だけは`.trim().length > 0`を使ったが、変更単位は同じ一行である。既存のheader、row cell、`colSpan={hasAuditKey ? 7 : 6}`は変更していない。

失敗run `18c199966ac84cf79d2fbaa316120557`も、変更前に`const hasAuditKey = true;`と動的`colSpan`を含む全target contentを受領した。しかし、両方を変更する方針を立てた。空表示cellの想定文字列がcurrent contentと一致せず、正しい一行変更を含むpatch全体が原子的に失敗した。reworkでも`colSpan`を充足済みへ戻せず、変更0件で停止した。

## 既存Candidateとの重複

### Candidate128

`required_effects_closed`は変更成功・失敗後に同じeffect集合を再判定する。F04初段では、初回patch失敗4 / 5件を一回のreworkで回復し、充足済み`colSpan`を保持して未充足`hasAuditKey`だけを変更した。

C135はCandidate128を継承している。それでも1件で同じrecoveryを適用できなかった。したがってowner不足ではなく、effect stateを変更前の変更単位選択へ安定して接続できていないことが残差である。

### Candidate129

`change_effect_admitted`は充足済みeffectの初回変更を0 / 5へ抑えた。しかし、continuation切詰めで`colSpan`が未観測だった3件について、観測済み未充足`hasAuditKey`まで変更せず停止した。

失敗はpredicateの対象単位がtarget全体へ広がったことにある。次案ではeffectごとの三値状態を使い、`未観測`を別effectの変更拒否へ変換しない。

### Candidate132

`change_preimage_ready`は変更operandのexact current valueを要求し、stale preimageを0 / 5にした。一方、globalな変更前gateとしてPoint 2 coverageとPoint 3 closureへ干渉した。

次案はexact hunk文字列の完全票を新設しない。まず充足済みeffectを変更集合から除く。残った変更単位のpreimageは既存のmodel-visible contentへ従う。

## 最小predicate候補

```text
effect_prechange_state(effect) :=
  admission済みprechange contentがrequired outcomeを満たすなら satisfied
  admission済みprechange contentがrequired outcomeを満たさないと示すなら unsatisfied
  どちらにもbindできないなら unobserved

initial_change_effect_set :=
  effect_prechange_state(effect) = unsatisfied のeffectだけ
```

- `satisfied`: 保持constraint。変更へ入れない。
- `unsatisfied`: 独立した変更単位としてadmitできる。
- `unobserved`: 推測で変更へ入れない。他の`unsatisfied` effectの変更開始は拒否しない。
- validation: Candidate128の`required_effects_closed=true`まで開始しない。

このpredicateは「全effectを観測できたか」を開始gateにしない。criterion全体の完全性を要求して必要変更まで止めたCandidate126 / 129の経路を繰り返さない。

## 汎用性

対象はF04固有の`colSpan`ではなく、TaskSpecが複数required effectを持ち、その開始状態が混在するimplementationである。

- F02: 観測済み未充足effectが2つなら、両方を変更集合へ保持する。
- F04: 観測済み未充足1つ、充足済み1つなら、前者だけを変更する。
- F07 dependency: 観測済み未充足のpairなら、片方を脱落させず両方を変更する。
- 未観測effectを含む場合: 観測済み未充足effectは進められるが、全closureを推測しない。

適用domainは、required outcomeをartifact current contentから判定できるimplementationである。review、prose、境界判断、外部状態、owner判断を同じ三値ledgerへ一律に入れない。言語、拡張子、hunk数、target数はpredicateへ含めない。

## 次Candidateの境界

次Candidateを作る場合はCandidate135を直接親とし、criterion-span request authorityを保持したまま、変更前のeffect-local admissionだけを追加する。reference definition一段closureは追加しない。C135低Score runでは上流定義を含む全contentが観測済みだったため、definition closureは今回の原因ではない。

初段はF04 N=5、M=24とする。

- score `3`以下: 0 / 5。一件でも出た時点で停止する。
- criterion外lexeme混入: 0 / 5。
- `hasAuditKey`未充足effectの変更: 5 / 5。
- 開始状態で充足済みの`colSpan`変更: 0 / 5。
- initial atomic apply failure: 0 / 5。
- 未観測effectだけを理由にした観測済み未充足effectの抑止: 0 / 5。
- required validation 3件完備: 5 / 5。

F04 N=5を通過しても、TypeScript固有成功を汎用性とみなさない。次段階でF02とF07を各N=5によりpreservation確認し、その後にだけStandard14適用範囲を検討する。

## 結論表

| 論点 | 既存owner | C135での実測 | 次の扱い |
| --- | --- | --- | --- |
| request source boundary | C135 | criterion外lexeme 0 / 5 | 保持 |
| effect state | C128 | 1件で充足済みeffectを再変更対象化 | effect-local三値bindを変更前へ接続 |
| unobserved effect | C129の失敗証拠 | target全体停止へ波及させるとfalse stop | 他effectの開始拒否へ使わない |
| exact preimage | C132の失敗証拠 | global gateは他Pointへ干渉 | 新global gateを作らない |
| hunk composition | C135低Score | 必要hunkと不要hunkの結合で全体失敗 | unsatisfied effectだけを変更集合へ入れる |
| definition closure | 未採用 | C135低Scoreでは必要定義を観測済み | 今回は追加しない |
