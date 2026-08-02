# Candidate129 unsatisfied-effect change admission設計

## 結論

Candidate129はCandidate128を直接親とし、root `AGENTS.md`の`EVIDENCE_GATE`だけを置換する。Candidate128の`required_effects_closed`と失敗後reworkは変更しない。初回artifact変更へ入れられるのを、admission済み変更前resultの観測済みcurrent contentが未充足と示すrequired effectだけに限定する`change_effect_admitted`を一つのpredicateとする。

## Identityと作成前gate

- candidate number: Candidate129
- prompt identity: `the-caption-3ce91a4-unsatisfied-effect-change-admission-r1`
- direct parent: `the-caption-3ce91a4-required-effect-closure-r1`
- changed target: root `AGENTS.md`
- changed rule: `EVIDENCE_GATE`
- changed axis: initial artifact changeへ入れるrequired effectのadmission
- evaluation status: `targeted_f04_n5_evaluated / quality_gate_failed / stopped`
- adoption: `not_adopted`
- release: `not_created`
- runtime projection: `not_projected`

## 基準の最短正常経路

一つのeditable targetについて、初回content resultで未観測のrequired effectがあれば、Candidate125由来の一回のcriterion-complete continuationを維持する。受領済みresultが、あるeffectを開始状態から充足済み、別のeffectを未充足と示した場合、未充足effectだけを一回のartifact変更へ入れる。全required effectが閉じた後は、Candidate128の`VALIDATION_PLAN`へ進む。

F04では、`hasAuditKey`のdata依存性だけを変更し、開始状態ですでに条件連動している`colSpan`を保持する経路である。

## 保存traceで観測した誤経路

同じF04 r2 comparison block `78ce2e9758d3bb7a85925c44ef29c71b4459275e92f0d385e0bde3b9b609e65c`をraw rolloutで再集計した。

| prompt | initial apply failure | 件数 |
| --- | ---: | ---: |
| Candidate108 | 0 / 5 | 5 |
| Candidate116 | 0 / 5 | 5 |
| Candidate118 | 0 / 5 | 5 |
| Candidate122 | 0 / 5 | 5 |
| Candidate124 | 0 / 5 | 5 |
| Candidate125 | 22 / 30 | 30 |
| Candidate127 | 5 / 5 | 5 |
| Candidate128 | 4 / 5 | 5 |

Candidate125の30件では、22件のfirst patchが`hasAuditKey`に加えて`colSpan`変更を含み、22件すべてがpreimage不一致で失敗した。残る8件はfirst patchへ`colSpan`を含めず、initial apply failureはなかった。失敗22件では、開始状態の正しい`colSpan={hasAuditKey ? 7 : 6}`がmodel-visible resultに存在した。

Candidate128 result文書の「初回失敗3 / 5」はmechanism集計値である。raw rolloutを再監査すると、run `f50df5eae57a40ae95774bda89428efe`にも`apply_patch verification failed`があり、実数は4 / 5だった。この後続再監査は過去resultをin-place再採点せず、本設計の診断証拠として分離する。

## 上昇点と原因境界

同じcomparison blockではCandidate124までinitial apply failureは0件で、Candidate125から増えた。Candidate125は、`single_change_target_ready`を「一targetが全未解決変更criterionを所有する」と定義し、`continuation_scope_complete`なrequest identityを変更発行条件へ接続した。

保存traceでは、開始状態ですでにrequired effectを満たすcurrent contentを受領しても、そのeffectを「一targetが所有する変更criterion」としてfirst patchへ再生成した。TaskSpecのcriterion列挙、target ownership、request scopeが、current contentの未充足証拠なしに変更単位をadmitする経路になっていた。

TaskSpec、repository authority、repository stateは正しいcurrent contentを提供していたため、evidence不足やexecutor failureではない。promptがcriterion ownershipからartifact変更単位へのadmissionを制御する層である。

## 置換する一つのpredicate

`change_effect_admitted(effect) := admission済みprechange resultの観測済みcurrent contentが、そのTaskSpec required effectを未充足と示す`

- true: そのeffectをartifact変更単位へ入れられる。
- 開始状態から充足済み: 保持constraintへbindし、変更単位へ入れない。
- current content未観測: 未充足を推測せず、変更単位へ入れない。

TaskSpecでのcriterion列挙、target ownership、`continuation_scope_complete`なrequest identityだけではtrueにしない。一回のcontinuation、複数targetのinitial content wave、Candidate128の失敗後closureは維持する。

## 消す判断点と増える判断点

消す判断点は、観測済みcurrent contentがすでに満たすeffectを「TaskSpecにcriterionとして列挙されている」「同じtargetが所有する」という理由だけで変更対象へ戻す判断である。

増える判断点は、artifact変更へ入れる各effectについて、観測済みcurrent contentが未充足を示すかという一回のadmissionだけである。全criterionの追加read、完全再監査、exact preimage文字列の別票は要求しない。

## Candidate126を継承しない理由

Candidate126の`change_input_ready`は、変更単位ごとにcriterion、target、exact current-content operandの完全bindを要求した。F04 N=20ではstale hunkを抑止した一方、8件でartifact変更を抑止し、少なくとも5件はcontinuation出力切詰めを理由に停止した。

Candidate129は全effectの完全bindを変更開始gateにしない。観測済みcurrent contentが未充足と示すeffectだけをadmitし、充足済みeffectの再生成を禁止する。未観測effectを推測で変更しない点は維持する。

## 非目標

- 中間報告、model return、tool call回数をpromptで制御すること
- patch tool、atomic apply、executor、Codex CLI、adapter、runtime hookの変更
- F04、path、symbol、具体的hunkをpromptへ埋め込むこと
- continuation回数、machine rework上限を増やすこと
- Candidate128のrecoveryを削除または弱めること
- Candidate129の採用、release、本体投影

## Targeted evaluation gate

初段はF04 r2だけをCandidate129 N=5で実行する。いきなりN=20へ進めない。model、reasoning、CLI、runtime、permission、rating、fixture、TaskSpec、token accounting、executor条件はCandidate128の保存済みF04 runと互換に固定し、profileの`max_workers`は`24`とする。

品質・mechanism gateは次のとおりとする。

- valid / rateable / score `4`: 5 / 5
- score `3`以下: 0 / 5。一件でも発生した時点で停止する。
- `hasAuditKey` required effect: 5 / 5で変更
- 開始状態から充足済みの`colSpan`: 変更0 / 5
- first patchへ充足済みeffectを含める: 0 / 5
- initial apply failure: 0 / 5
- artifact変更なしのfalse stop: 0 / 5
- Candidate128の`required_effects_closed`とrework上限違反: 0 / 5

KPIは互換なCandidate128 F04 N=5を保存基準にする。Candidate129のtokenとelapsedが両方とも高い場合、または狙ったinitial failureが一件でも残る場合は、F02 / F07 preservationとStandard14へ進めず停止する。N=5通過は一般的安定性または採用の証明にしない。

## Targeted evaluation result

2026-08-01にF04 r2 N=5を実施した。5件はすべてvalidでexcluded attemptは0件だったが、score分布は`4 / 1 = 2 / 3`となった。初回`apply_patch`失敗、充足済み`colSpan`の再変更、first patchへの充足済みeffect混入はすべて0 / 5だった。一方、3件は継続取得の出力切詰めで`colSpan`を観測できないことを理由に、観測済みの未充足`hasAuditKey` effectも変更せず停止した。

Candidate129は原因に対する抑止方向を示したが、未観測effectをtarget全体の変更開始拒否へ波及させた。事前停止条件に従いCandidate129を停止し、F02、F07、Standard14、採用、release、本体投影へ進めない。一次結果は[`Candidate128 / Candidate129 F04 N=5`](../evaluations/results/candidate128-candidate129-unsatisfied-effect-change-admission-v14-medium-f04-atomic-n5-cli0146_2026-08-01.md)を正本とする。
