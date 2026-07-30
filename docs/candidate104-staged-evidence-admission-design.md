# Candidate104 段階的な証拠取得の設計

## 結論

Candidate104はCandidate98を直接親とし、変更前の証拠取得を既定で閉じる`EVIDENCE_GATE`一規則だけを追加する。Candidate99からCandidate103までは失敗経路の観測証拠であり、prompt lineageには含めない。

最初の許可集合をexecutorに作らせない。TaskSpecから直接決まる開始状態、対象artifact、明示read-only path、適用中のrepository instructionだけを最初に許可する。許可済みresultが具体的な不足または矛盾を示した場合だけ、次の証拠を一件開く。

## Identityと状態

- candidate number: Candidate104
- prompt identity: `the-caption-3ce91a4-staged-evidence-admission-r1`
- direct parent: `the-caption-3ce91a4-validation-completion-sheet-r1`
- bundle SHA-256: `b25d13fb2f9d598adfae2359bd5cfbcef2591731d07e9165b1f9b3fc83e036b0`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`の追加
- evaluation status: `targeted_a02_f07_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / result_registered / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate98とする。
2. F07の最短正常経路は、checkout identity、clean status、`run.sh`を確認し、一行変更、required validation、差分確認へ進む経路である。保存済みCandidate100 iteration 4で成立している。
3. Candidate103の誤経路は、5件すべてでTaskSpecから直接決まらないrepository全体、fixture、履歴、gate実装等へ変更前探索を広げたことである。
4. F07 TaskSpecはF07-C1〜C3、正規module、開始条件、対象path、required validationを明示している。追加探索は成果値不足によるものではない。
5. Candidate99はrepository authorityを初期入力へ含め、Candidate100はdefault denyにせず、Candidate101はauthority確認を事前責務にし、Candidate102とCandidate103は初期集合をexecutorに作らせたため防げなかった。
6. Candidate57とCandidate58はauthority探索を一result一decisionへ逐次化したが、A02のcommand、model step、tokenを増やした。Candidate62はclosed read-only taskへ限定してもA02へまとめ読み方法が流入した。これらはreadの発行方法を制御しており、追加evidence identityの開放をdefault denyにはしていない。
7. 追加するpredicateは、初期許可集合と一件ずつの開放条件を固定する`EVIDENCE_GATE`一つとする。逐次化自体を効果とせず、許可集合外のevidence identityを開かないことを効果とする。
8. 消す判断点は、permissionや一般的安全確認から追加探索を作る判断である。
9. 新たに増える判断点は、許可済みresultが列挙された不足または矛盾を実際に示したかという一つである。
10. F07で不要探索を止めるだけでは過剰制御を検出できない。requested outcome valueをrepository authorityから解決するA02を同時に確認する。
11. F07は5 / 5 score `4`、広い検索なし5 / 5、履歴参照なし5 / 5を必須とする。A02は5 / 5 score `4`、clarificationなし5 / 5、repository authorityから正規routeを解決5 / 5、requested value bind後の追加authority・fixture・履歴探索0 / 5を必須とする。一件でも未達なら停止する。

## 変更する規則

```text
EVIDENCE_GATE: 変更前のevidence invocationはdefault denyとする。
最初はTaskSpec本文、TaskSpec明示の開始状態の直接観測、target artifact、
明示read-only path、target pathへ適用中のrepository instructionだけを許可する。
requested outcome valueが未固定で一意なrepository authorityへ委ねられている場合だけ、
その値をbindするauthority invocationを一件許可する。
許可済みresultで変更または停止を判断できた時点で証拠取得をterminalにする。
追加evidenceは許可済みresultが具体的な不足または矛盾を観測した場合だけ、
result identityと次のevidence identityをbindして一件許可する。
permission、allowed read、利用可能なtool、一般的安全確認は開放条件にしない。
```

## 非目標

- TaskSpec、評価case、fixture、ratingの変更
- 特定pathやcommandのroot promptへの列挙
- read回数またはtoken上限の固定
- repository authorityの利用禁止
- executorまたは開発環境による外部強制
- Candidate99からCandidate103の履歴artifactの書換え
- 採用、release、THE-CAPTION本体反映

## 評価境界

Standard14の固定Layer 1 identityを再利用し、A02 r2とF07 r2のiteration 1〜5をmodel slot発行前にcoverageへbindする。TaskSpec、fixture、rating、model、reasoning、CLI、permission、executor parameterはCandidate103と同じ値を使う。10 slotを別cycleへ分けず、設定上の`M=24`を持つ一つのglobal queueへ入れる。既存C81 resultは再実行しない。両caseのquality・mechanism gate通過前にStandard14またはB20へ進めない。
