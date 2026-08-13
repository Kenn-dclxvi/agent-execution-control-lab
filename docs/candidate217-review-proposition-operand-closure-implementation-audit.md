# Candidate217 review proposition operand closure 実装監査

## 状態

- `candidate_created`
- `static_verification_passed`
- `ADR9_r2_N5_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- `adoption_not_decided`
- `release_not_created`
- `projection_not_performed`

## Candidate identity

| 項目 | 値 |
|---|---|
| Candidate | Candidate217 |
| prompt identity | `the-caption-3ce91a4-review-proposition-operand-closure-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `627c8e27541e0b6ab96129e19121def1a43a289d903222d8260d52cf66507056` |
| root `AGENTS.md` SHA-256 | `9c39c9d9030e1484426498226d763b8cc21fbcfa8c53ea19ab2555f46dba2cc2` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `ADR9_r2_N5_completed / quality_failed / mechanism_failed / stopped` |

## 実装範囲

Candidate147のfull bundleを直接基盤とし、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはCandidate147と同一である。

artifact変更前reviewをC147上へ再構成し、`REVIEW_INPUT_CLOSURE`として次の一軸を追加した。

1. required review propositionのdirect operandを、他入力を固定したとき値の違いが命題またはallowed terminal kindを変え得るpredicate dependencyとして固定する。
2. admission済みcurrent operandはpacket receipt、未admitでterminalを分け得るoperandはfinite manifest observationへexactly one bindingを持たせる。
3. bindingの欠落または二重化があればreviewerを起動せず、供給不能な必須operandを`unavailable`へbindする。
4. packet済みoperandをreview evidence consumerへ戻さず、packet constructionやclosure確認のための新規readとroot先読みを禁止する。

## 持ち込まなかった制御

- case別のoperand表、field / scope / target / observation対応
- value equalityや期待terminalからのoperand推定
- 成功runのtool順、read順、判断順またはpacket文面
- executor、adapter、runtime hookまたは外部wrapper変更
- Candidate216をprompt親とする系譜

Candidate216は、既取得operand再取得14回、7 runと必須operand欠落1 runの保存証拠、およびprojection conflict・誤paired read・root prereadを0件にできた反証だけに使った。

## 静的検証

- `verify_bundle()`が成功した。
- manifestのbundle SHA-256再計算値が一致した。
- Candidate147との差分targetは`AGENTS.md`だけだった。
- 非変更targetは18件だった。
- root本文にcase identity、固定path、固定field / scope / observation identityまたは期待dispositionを含めていない。
- direct operand、exactly one binding、admitted operandのpacket固定、未admit operandだけのobservation、closure前reviewer起動禁止を固定した。
- bundle identity snapshotへCandidate217を追記した。

## 動的評価で判明した制約

静的検証では、admission済みoperandをpacketへ含める制御自体の整合しか確認できなかった。ADR9 r2 N=5では、TaskSpecが値をmodel-visible fixed inputとしながら、その値をreviewer packetの許可項目に含めない経路を観測した。この場合、C217のpacket必須化とobservationへの再分類禁止は同時に満たせない。

このため、静的検証通過を動的な機序成立へ昇格しない。次の設計ではoperand closureより前に、packetへ合法的に投影できる値とreviewerが直接観測すべき値の所有権を分ける必要がある。

## 参照

- [Candidate217作成前設計](candidate217-review-proposition-operand-closure-design.md)
- [Candidate217方向監査](candidate217-review-proposition-operand-closure-direction-audit.md)
- [Candidate217 manifest](../prompts/candidates/the-caption-3ce91a4-review-proposition-operand-closure-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate217 ADR9結果](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
