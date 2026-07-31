# Candidate116 outcome / implementation boundary設計

## 結論

Candidate116はCandidate108を直接親とし、`SPEC`と`EVIDENCE_GATE`を一つの変更軸として置換する。

`SPEC`は利用者が観測するrequired outcome valueだけを確定する。target artifact、canonical path、module、command、implementation methodは、TaskSpecがそれ自体を成果として要求しない限りimplementation choiceとし、未固定でも`spec_ready=false`にしない。

`EVIDENCE_GATE`は`spec_ready=false`なら未固定outcomeをclarificationへ返して停止する。`spec_ready=true`になった後だけ、targetとrepository authorityを読み、implementation choiceを解決する。

## Identityと状態

- candidate number: Candidate116
- prompt identity: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed rules: `SPEC` / `EVIDENCE_GATE`
- single change axis: required outcome確定とimplementation choice解決の境界分離
- bundle SHA-256: `339f3f1153739e4dbafb288d16c3756b098d717a3d2563e50e3bd63fc7234d72`
- evaluation status: `targeted_a01_a02_f01_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_improved / elapsed_near_flat_slightly_higher / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate108とする。Candidate114 / 115は停止済みの診断証拠であり継承しない。
2. 最短正常経路は、required outcome valueが未固定なら開始状態確認後にclarificationへ停止し、固定済みならtargetとrepository evidenceからimplementation choiceを解決して成果を作る経路である。
3. 保存済み誤経路は二つで一つのtradeoffを示す。Candidate114 A02の1件はcanonical entrypointをoutcome valueとして扱って誤停止した。Candidate115 A01の4件はimplementation authority許可を一般read permissionへ広げ、未固定modeのまま実装した。
4. TaskSpecとrepository stateは両caseで十分だが、現行promptはoutcome authorityとimplementation authorityを同じ文で扱うため、モデルが境界を入れ替え得る。
5. 置換する一軸は、`SPEC`をoutcomeだけのboundary、`EVIDENCE_GATE`をoutcome確定後のimplementation boundaryにすることである。
6. 消す判断点は、canonical path未固定を利用者への質問へ昇格する分岐と、一般read permissionを未固定outcomeの決定委譲へ変換する分岐である。
7. 新たに増えるlabel、case固有path、authority whitelist、tool名、回数、token・時間閾値、Executor制御は0件である。`implementation choice`は既存`METHOD`が扱う実装手段を説明する直接語であり、新しい状態labelにしない。
8. 初回評価はA01 r2 / A02 r2 / F01 r3各N=5とする。A01で未固定outcome停止、A02でcanonical implementation探索、F01で通常の成果変更を確認する。
9. quality gateは15 / 15件score `4`とする。mechanism gateはA01の変更・試験0件、A02のcanonical成果5 / 5、F01のrequired validation完了5 / 5とする。
10. 一件でも崩れた場合は停止する。通過前にStandard14へ進めない。

## 非目標

- A01 / A02固有の分岐または例示
- authority selectorのTaskSpec schema追加
- implementation methodの固定
- Executor、validation wrapper、dispatchの変更
- 採用、release、runtime projection、本体反映

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 15件
- direct KPI reference: 保存済みCandidate108同case atomic N=5

Candidate108は再実行せず、新しいCandidate116の15 slotだけを一つのglobal queueへ入れる。

## 評価結果

targeted 15 / 15件と、単独M=24で実行したStandard14不足分55 / 55件はscore `4`だった。A01は5 / 5件が開始状態確認だけでclarificationへ停止し、A02は5 / 5件がcanonical成果へ到達したため、境界分離のmechanismは成立した。

Standard14ではtargetedの15 runを再利用し、不足55 runだけを追加した。Candidate108比の集約中央値はtoken `-9.26%`、elapsed `+0.25%`だった。tokenは改善し、elapsedはほぼ同水準で僅かに長い。評価とmechanism gateは通過し、採用は別判断として未決定である。

先行する二つの55-run campaignはcontrollerが重なってhost全体のM=24を超えたためKPIから除外した。正規一次結果は、汚染runを含まないisolated registryで単独実行した[`Candidate108 / Candidate116 Standard14 atomic N=5`](../evaluations/results/candidate108-candidate116-outcome-implementation-boundary-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)を正本とする。
