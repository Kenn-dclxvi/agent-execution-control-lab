# Candidate114 spec-ready evidence phase boundary設計

## 結論

Candidate114はCandidate108を直接親とし、`EVIDENCE_GATE`一規則だけを置換する。

`spec_ready=false`の間は、TaskSpec、明示された開始状態、およびTaskSpecが未固定valueの決定元として要求する一意なrepository authorityだけをadmitする。target artifact、一般read-only path、targetへ適用されるinstructionは`spec_ready=true`の後に開く。

新しいsemantic label、case固有whitelist、tool回数、token・時間閾値は追加しない。既存の`spec_ready`が担当する仕様確定と、`EVIDENCE_GATE`が担当する変更前証拠取得の順序を一つにする。

## Identityと状態

- candidate number: Candidate114
- prompt identity: `the-caption-3ce91a4-spec-ready-evidence-phase-boundary-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`の置換
- bundle SHA-256: `c6cd2756a8a1a5b192ed6eb5f17dc380bd884873c23c3f190d9974fc09c757dd`
- evaluation status: `targeted_a01_a02_f01_evaluated / a01_mechanism_passed / quality_gate_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 保存traceの再分析

ControlFreeRepositoryのA01 Medium N=5は5 / 5件が未固定modeを質問せず、source、test、変更、validationへ進んでscore `0`だった。このtraceはrootの仕様確定境界を全削除できないことを示す。Rating v13、異なるprompt identityのためKPI比較には使わず、挙動の対照だけに使う。

Candidate104 A01 N=5は5 / 5件がscore `4`だった。1件は開始状態だけを確認してclarificationへ到達した。残る4件はtarget sourceを読んだ後、3件がtest、1件がgit historyへ進んでからclarificationした。

Candidate108 A01の保存済みN=5も5 / 5件がscore `4`だったが、追加test・authority探索なしの正常経路は1 / 5だった。Candidate113ではauthority admission条件を追加しても、target確認後に追加探索なしでclarificationへ到達したrunは0 / 5だった。4件が明示委譲なしでauthority探索へ進み、1件だけtargetを読まず直接clarificationした。

したがって、削除対象はauthorityの意味定義ではない。`spec_ready=false`でもtargetを初期admissionすることで、current value、option set、test expectationをrequested outcome valueの手掛かりとして追う分岐が開く点を対象にする。

## 作成前gate

1. 基準prompt setはCandidate108とする。Candidate112、Candidate113は停止済みであり継承しない。
2. 最短正常経路は、TaskSpecと開始状態から未固定requested outcome valueを確認し、一意なrepository authorityがTaskSpecから要求されていなければclarification resultでterminalにする経路である。
3. 保存済み誤経路はCandidate108 A01 N=5の4 runである。target artifactを確認した後にtestまたはrepository authorityを追加探索した。
4. Candidate108の1 runとCandidate104の1 runは追加探索なしでscore `4`へ到達しており、誤経路の追加evidenceは品質成立に必要ではない。
5. ControlFreeRepositoryは5 / 5件が未固定valueを質問せず実装したため、仕様確定境界の全削除はできない。Candidate113はauthority条件の追加でrouteを変えられなかったため、同条件を詰めない。
6. 置換するpredicateは`EVIDENCE_GATE`一つとする。既存`spec_ready`のfalse / trueを、仕様確定evidenceとtarget evidenceのphase境界として使う。
7. 消す判断点は、requested outcome valueが未固定のままtargetを読み、そのcurrent value、option set、test expectationから追加evidenceを探す分岐である。
8. 新たに増えるlabel、case固有path、tool名、例外、回数、token・時間閾値、Executor制御は0件である。
9. 初回評価はA01 r2、A02 r2、F01 r3の各N=5とする。A01でclarification、A02でrepository authorityによる仕様確定、F01で明示済み仕様から通常変更へ進めることを確認する。
10. quality gateは15 / 15件score `4`とする。mechanism gateはA01でtarget / test / historyを開かずclarificationへ到達すること、A02とF01で必要成果とrequired validationを完了することとする。
11. qualityまたはmechanism gateが一件でも崩れた場合は停止する。通過前にStandard14へ進めない。

## 非目標

- authorityの新しい意味分類
- 再入、tool call、shell grouping、並列発行の直接指定
- Executor、validation wrapper、dispatchの変更
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
- direct reference: Candidate108の保存済み同case atomic N=5

15 slotは一つのglobal queueへ入れる。Candidate108は保存済みrunを再利用し、不足runだけを発行する。

## 評価結果

A01は5 / 5件がscore `4`で、target・test・history・authority探索なしにclarificationへ到達した。A02は4 / 5件、F01は5 / 5件がscore `4`だった。A02の1件がauthority path未記載を理由に誤停止したためquality gate不通過とし、Standard14へ進めず停止した。詳細は[`Candidate114 targeted結果`](../evaluations/results/candidate108-candidate114-spec-ready-evidence-phase-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md)を正本とする。
