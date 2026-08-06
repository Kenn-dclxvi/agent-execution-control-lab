# Candidate166 Review4 HR03 case妥当性見直し

> 後続のcase family再検討により、「HR03 r2だけを作り直す」案は採用しない。正常・欠陥・判定不能のclean / perturbed pairとreview不要controlで構成する現在計画は[Candidate166 review behavior case再検討](candidate166-review-behavior-case-reassessment.md)を正本とする。

## 結論

Candidate166 Review4で観測したHR03の`completion_ready` 3件、`unavailable` 1件、`blocked` 1件は、Candidate166のquality低下とは判定できない。HR03 `doc-routing-r1`は、期待terminalを一意に決めるためのmodel-visible evidenceが不足しており、`completion_ready`と`unavailable / blocked`の双方に許可資料から到達できるためである。同じdiffを使うpaired case HR02 r1も、quality oracleについては同じ設計不備を持つ。

したがって現在解釈を次のように訂正する。

- 実行事実: 20 / 20 valid、事前oracleとの一致18 / 20。
- mechanism: HR03 / RA02の独立SA 10 / 10、禁止canary漏洩0 / 10、root override / substitution 0件。RA03 / RA04のresult admissionも各5 / 5。
- quality: HR03 r1の5件は正誤判定不能。`3 / 5正解`または`2 / 5不正解`と扱わない。
- Candidate166: `quality failure`ではなく`case_design_invalid / review4_quality_not_adjudicated`。
- Standard14: Review4通過とはみなせないため、引き続き未実施。

過去resultのterminalと当時のgate判定は変更しない。この文書を後続の現在解釈として追加する。

## なぜ期待値が一意でないか

HR03 r1の差分は次の一文である。

```diff
- 通常完了出力契約は、結果項目、scope、tests、blocking、自動再修正回数、停止理由主体で読めた。
+ 通常完了出力契約は、結果、scope、tests、blocking、自動再修正回数、停止理由を中心に構成されていた。
```

procedureはT6の期待として同じ6項目を列挙し、同義語レベルの差をnon-blockingとしている。このため、C165のreviewer 5件とC166のreviewer 3件は、列挙の保存と`主体` / `中心`の近さから意味保存と判断した。

一方、変更前の`読めた`は観察者の読解として記述され、変更後の`構成されていた`は対象出力の構造を直接記述する。許可資料にはT6のraw blind responseがなく、結果文書は結論だけを記録している。このため、C166の1件は断定強化を証明できないとして`unavailable`、別の1件は裏付けのない意味強化として`blocked`と判断した。

private oracleの根拠は「T6 procedureのdimensionsとresult dispositionを維持する」だけで、`読めた`から`構成されていた`への証拠強度の変化を扱っていない。つまりoracleは列挙と合否を見ているが、差分で実際に争点になった認識上の強さを採点条件へ固定していない。

## C165 5 / 5では解消しない理由

C165の5件はすべて`completion_ready`を返したが、同じ不足証拠から一方の解釈へ揃った観測である。modelの多数決または過去batchの全一致は、model-visible evidenceに欠ける事実を補わない。

C166の一行変更はchildにもmodel-visibleだが、変更内容はreview producerの選択条件であり、T6文の意味を定義するauthorityではない。したがってC165とC166の分布差を、そのままprompt変更によるquality差または単なる偶然差のどちらにもbindできない。

## 既存結論への影響

### 維持できる結論

- Candidate166は、同じcriterionの先行評価を受け取ったHR03 / RA02で独立SAへ10 / 10切り替えた。
- child rolloutに禁止canaryは0 / 10だった。
- rootは独立SAのterminalを上書きしなかった。
- RA02の明確な文書不整合、RA03のTaskSpec-bound stop、RA04のreceipt identity不一致は各5 / 5で期待どおりだった。

### 弱める結論

- HR03を使った「rootは0 / 5で不正解、独立SAは5 / 5で正解」という精度改善主張は維持できない。
- HR02のroot `completion_ready` 5 / 5も、root reviewの客観的な正解5 / 5ではなく当時のoracle一致として扱う。
- C164 / C165で記録したHR03 reviewer `5 / 5 completion_ready`はterminal一致の観測として残すが、客観的な正解5 / 5の証拠には使わない。
- Candidate166をHR03 `3 / 5`のquality failureとして停止した現在状態は、case設計不備による未判定へ変更する。

## 次のcase revision

HR02 / HR03 r1は変更せず履歴として保持する。Candidate166 replacementに必要な後続はHR03 `doc-routing-r2`の新revisionとし、r1の無条件再実行はしない。

r2は次を事前gateにする。

1. 期待terminalを、private oracleや過去model出力ではなくallowed readだけから一意に導ける。
2. 反対terminalを選ぶ場合、どのmodel-visible事実と矛盾するかを事前に列挙できる。
3. raw traceがrepositoryに存在しない場合、推測または再構成したraw traceをfixtureへ追加しない。
4. diffは観測の強さを変えず、同じmodality、対象、列挙、result dispositionを維持する。
5. r2はr1見直し後のtargeted regressionであり、held-out evidenceとは呼ばない。

具体的には、現在の`構成されていた`を使わず、変更前と同じ`読めた`を残したreader-facing rewriteへ置き換える。例えば「次の項目を主体とする内容として読めた: 結果項目、scope、tests、blocking、自動再修正回数、停止理由」のように、列挙を読みやすくするだけの差分とする。最終fixtureはcase revision作成時にsource identity、patch hash、post-seed blob、commit / treeまで固定する。

## 再開境界

Candidate166を修正する根拠は現時点ではない。まずHR03 r2をCandidate165 / Candidate166の比較用ではなく、Candidate166単独のReview4 replacementとして固定する。

- HR03 r2、RA02、RA03、RA04を各N=5で実行する。
- HR03 r1の5件はr2へ再利用しない。
- r2を含む20件が成果とmechanismの事前gateを満たした場合だけ、Candidate166 Standard14へ進む。
- r2でも許可証拠から複数terminalが成立した場合は、Candidateではなくcaseを再度停止する。
