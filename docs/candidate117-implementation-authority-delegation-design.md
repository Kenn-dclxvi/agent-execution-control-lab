# Candidate117 implementation authority delegation設計

## 結論

Candidate117はCandidate116を直接親とし、`EVIDENCE_GATE`一規則だけを置換する。

Candidate116のrequired outcomeとimplementation choiceの境界分離は維持する。その上で、repository authorityからimplementation choiceを解決する経路は、TaskSpecがそのchoiceの決定をrepository authorityへrequired constraintとして明示した場合だけ開く。

これはpath、tool、読取り回数、実行順を固定する制御ではない。一般的なread permissionをauthority探索の開始根拠へ変換する判断点を消し、TaskSpecが明示したimplementation authorityだけをadmissionへbindする。

## Identityと状態

- candidate number: Candidate117
- prompt identity: `the-caption-3ce91a4-implementation-authority-delegation-r1`
- direct parent: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`の置換
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate116とする。Candidate113は停止済みの診断証拠であり継承しない。
2. 最短正常経路は、required outcomeが未固定なら開始状態確認後にclarificationへ停止し、固定済みでTaskSpecがimplementation authorityを明示するならtarget artifactとそのauthorityからchoiceを解決して成果を作る経路である。
3. 保存済み誤経路はCandidate116 A02 N=5とする。5 / 5件はscore `4`だったが、4 / 5件が変更前にrepository-wide検索または広いfile listを取得した。A02 token中央値はCandidate107の`125,559`に対して`240,098`だった。
4. Candidate107からCandidate116までのA02 token増加`417,657`のうち`414,182`、`99.17%`はinput tokenだった。Candidate116の変更前tool出力はN=5合計`356,381`文字で、Candidate107の`141,366`文字より`152.10%`多かった。
5. Candidate113 A02は同じTaskSpecの明示authorityを`authority_delegated`へbindし、5 / 5件score `4`、token中央値`150,160`、model step合計`27`だった。一方、A01のauthority admissionは0 / 5で成立せず停止した。Candidate116はA01を`spec_ready=false`で5 / 5停止できているため、outcome境界を戻さずimplementation側だけへ明示委譲を置く。
6. TaskSpecはA02でcanonical targetをrepository authorityと現行entrypoint実体から決めることをrequired constraintとして明示する。ただしCandidate116の`EVIDENCE_GATE`は、明示委譲と一般的なread permissionをimplementation authorityのadmission条件として分離していない。
7. 置換するpredicateは`implementation_authority_delegated`一つとする。`spec_ready=true`かつTaskSpecが未解決implementation choiceをrepository authorityから決めることをrequired constraintとして明示した場合だけauthority evidenceを開く。
8. 消す判断点は、一般的なread permissionまたはallowed-read constraintを根拠に、未解決choiceへbindしていないrepository evidenceを探索する分岐である。
9. 新しいlabel参照は`EVIDENCE_GATE`内の`implementation_authority_delegated`一つである。case固有path、authority whitelist、tool名、読取り回数、token・時間閾値、Executor制御は追加しない。
10. 初回評価はA01 r2 / A02 r2 / F01 r3各N=5とする。quality gateは15 / 15件score `4`、mechanism gateはA01の変更・試験0件、A02のcanonical成果5 / 5、F01のrequired validation完了5 / 5とする。
11. qualityまたはmechanismが一件でも崩れた場合は停止する。成立しても、Candidate116比で対象3 caseのtokenとelapsedが両方低下せず、A02のmodel stepまたはtool-result再入が減らない場合はStandard14へ進めない。

## 変更する規則

```text
implementation_authority_delegated := TaskSpecが未解決のimplementation choiceをrepository authorityから決めることをrequired constraintとして明示
```

`spec_ready=false`ではCandidate116と同じく開始状態確認以外を開かない。`spec_ready=true`の後も、一般的なread permissionまたはallowed-read constraintだけではimplementation authorityを開かない。

## 非目標

- required outcomeとimplementation choiceの境界変更
- A01 / A02固有の分岐または例示
- path whitelist、tool call、shell grouping、並列発行、model return回数の指定
- validation wrapper、Executor、dispatchの変更
- TaskSpec、Evaluation set、fixture、rating、model、reasoning、CLI、permissionの変更
- 採用、release、runtime projection、THE-CAPTION本体反映

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 15件
- direct reference: 保存済みCandidate116の同case atomic N=5

Candidate116は再実行しない。Candidate117の不足15 slotだけを一つのglobal queueへ入れる。targeted gateを通過する前にStandard14 profileを作らない。
