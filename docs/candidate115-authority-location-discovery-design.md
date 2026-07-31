# Candidate115 authority location discovery設計

## 結論

Candidate115はCandidate114を直接親とし、`EVIDENCE_GATE`のauthority location解決条件だけを明確化する。

TaskSpecがrepository authorityによるrequested outcome valueの決定を明示した場合、authorityのpathがTaskSpecに未記載であることだけではclarificationへ停止しない。allowed read内でauthority locationを解決する。TaskSpecがauthorityによるvalue決定を明示しない場合は、この経路を開かない。

## Identityと状態

- candidate number: Candidate115
- prompt identity: `the-caption-3ce91a4-authority-location-discovery-r1`
- direct parent: `the-caption-3ce91a4-spec-ready-evidence-phase-boundary-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`内のauthority location解決条件
- bundle SHA-256: `7761e2ea0e45c244c305ba782431426d62bf11c5b700ca98edfb10b6c96b8d1d`
- evaluation status: `targeted_a01_a02_evaluated / a02_mechanism_passed / quality_gate_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate114とする。
2. 最短正常経路はA01では開始状態確認後のclarification、A02ではTaskSpecが要求するrepository authorityをallowed read内で特定してtargetを変更する経路である。
3. 保存済み誤経路はCandidate114 A02 run `daf49b9bd6534ee1affcff06d04e7902`である。authority path未記載だけを理由にclarificationへ停止した。
4. 同条件のA02 4 runはauthority locationを探索し、score `4`の成果へ到達した。repository stateだけでは失敗runの解釈差を防げない。
5. 追加する条件は、TaskSpecがrepository authorityによるvalue決定を明示した場合に限り、path未記載を停止理由にしないという一条件である。
6. 消す判断点は、authority使用が明示済みなのにauthority locationの指定を利用者へ再要求する分岐である。
7. 新しいlabel、case固有path、tool名、回数、token・時間閾値、Executor制御は追加しない。authority location探索という一つの許可条件は増える。
8. 初回評価はA01 r2 / A02 r2各N=5とする。10 / 10 score `4`、A01のtarget・test・history・authority探索0件、A02のcanonical成果5 / 5を必須とする。
9. 一件でも崩れた場合は停止し、Standard14へ進めない。

## 非目標

- authorityのcase固有whitelist化
- target、tool、探索回数の指定
- Executor、validation wrapper、dispatchの変更
- 採用、release、runtime projection、本体反映

## 初回試験

- cases: A01 r2 / A02 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 10件
- KPI reference: 保存済みCandidate108同case result

Candidate114はquality gate不通過のためKPI referenceにはしない。挙動差の直接親traceとしてだけ使う。

## 評価結果

A02は5 / 5件がscore `4`へ戻った。一方、A01は4 / 5件が未確認のまま実装・試験へ進んでscore `0`となった。authority location許可が一般allowed readまで開いたため、Standard14へ進めず停止した。詳細は[`Candidate115 targeted結果`](../evaluations/results/candidate108-candidate115-authority-location-discovery-v14-medium-a01-a02-atomic-n5-cli0146_2026-07-31.md)を正本とする。
