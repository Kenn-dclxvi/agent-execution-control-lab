# Candidate131 Point 6 closure / recovery監査

## 結論

Point 6のclosure / recoveryについて、新しいCandidateは作成しない。Candidate128の`required_effects_closed`は、変更後にTaskSpecの全required effectを同じ集合で再判定し、未充足effectが残る場合だけ一回のmachine reworkへ進む。保存済みtraceでは、この制御がF02、F04、F07の部分成果を閉じている。

Candidate132のscore `2`はPoint 6の回復不足ではない。model-visibleな変更前evidenceで`colSpan`の開始状態を確認できなかったため、正しい`hasAuditKey`変更後も全required effectをclosedと証明できず停止した。これは未証明effectを充足済みと推測しない既存closureの意図した保守側動作である。

## 対象と用語

closureは、TaskSpecが要求する全effectが完了集合から落ちず、完了またはvalidation開始の前に充足を確認できる状態を指す。recoveryは、artifact変更失敗後に許可された範囲内で未充足effectを再適用する経路を指す。

監査対象は次の保存済みtraceである。

- Candidate127 F02 N=29の部分成果2件
- Candidate128 F02 / F04 / F07各N=5
- Candidate131 F04 N=5
- Candidate132 F04 N=5のscore `2` 1件

## Candidate128が閉じた三つの失敗形

Candidate128は変更単位ではなく、TaskSpecのrequired effect集合をclosureの単位にした。

- F02: 複数sourceへ分散した両effectを5 / 5で保持した。
- F04: 初回atomic変更失敗3件で、開始状態から充足済みの`colSpan`を保持し、未充足の`hasAuditKey`だけを追加readなし・一回のreworkで適用した。
- F07: direct constraintとcompiled pin provenanceのpairを5 / 5で保持した。

3 case計15件はすべてscore `4`だった。artifact数、hunk数、依存形が違っても、同じrequired-effect closureで部分成果を防いだ。

## Candidate132の停止が示す境界

Candidate132 iteration 3は、全残存contentを要求した。保存raw outputには`colSpan`があったが、model-visibleなdeliveryは途中で切れた。agentは観測できた`hasAuditKey`を正しく変更した一方、`colSpan`が開始状態から充足済みとはbindできなかった。

Candidate128のpredicateで開始状態から充足済みと扱えるのは、初回artifact変更前のadmission済みrepository evidenceへbindできるeffectだけである。raw outputに存在してもmodelが受領していないcontentを証拠にはできない。このため`required_effects_closed=false`となり、未充足effectのcurrent contentも未bindなので停止した。

この停止を回避するため、次の緩和は行わない。

- 正しい一部変更が成功したことだけで、他の未観測effectもclosedと推定する。
- lint / build成功を、TaskSpec固有の表示条件や`colSpan`値の充足証拠に読み替える。
- 変更後に追加readを開き、変更前coverageの不足を回復側で補う。
- executor、adapter、report deliveryを変更する。

これらは部分成果の成功報告、判断waveの再開、repository外制御への拡張のいずれかを招く。

## Point 2・3・5との境界

- Point 2 Evidence coverage: 開始状態で充足済みのeffectを判定できるcontentを、変更前にmodel-visible evidenceへbindする。
- Point 3 Effect state: TaskSpecの各required effectを、充足済みまたは未充足として保持する。
- Point 5 Change construction: 発行する変更のpreimageだけを確認する。全effectの充足証明には拡張しない。
- Point 6 Closure / recovery: 変更result後も同じeffect集合を落とさず、証明済みの状態だけでvalidationまたは一回のreworkを選ぶ。

Candidate132はPoint 5のpredicateを追加したことで、Candidate131で成立していたPoint 2のdirect anchor routeを5 / 5から4 / 5へ悪化させた。Point 6を緩めるのではなく、Candidate132を停止してCandidate131へ戻すのが境界を保つ対応である。

## 再開条件

次のいずれかを同じ互換条件の保存traceで観測した場合だけ、Point 6を再開する。

1. 全required effectを変更前evidenceまたは変更resultへbind済みなのに、closureがfalseとなって必要なvalidationを止める。
2. `required_effects_closed=false`かつrework可能なのに、bind済みの未充足effectを一回のreworkへ発行しない。
3. `required_effects_closed=false`のままvalidationまたは完了報告へ進む。
4. 充足済みeffectを保持できず、reworkで再び壊す。

現在の保存traceに該当例はない。六つのpointの初回監査はここで完了し、最後の成功checkpointはCandidate131、停止済み診断CandidateはCandidate132とする。
