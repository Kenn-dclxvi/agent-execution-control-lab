# Candidate118 implementation bind terminal closure設計

## 結論

Candidate118はCandidate116を直接親とし、`EVIDENCE_GATE`一規則だけを置換する。Candidate117は停止済みであり、その`implementation_authority_delegated`条件を継承しない。

許可済みresultからartifact変更を発行できるimplementation choiceがbindされた時点を、変更前evidence operationのterminal resultとする。未発行の変更前evidence invocationを失効させ、次にartifact変更を発行する。変更後に確定可能なvalidation identityの探索を、変更前evidenceの継続理由にしない。

## Identityと状態

- candidate number: Candidate118
- prompt identity: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`
- direct parent: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`のterminal句置換
- evaluation status: `targeted_a01_a02_f01_evaluated / a02_n20_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_regressed / elapsed_improved / result_registered / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate116とする。Candidate117はauthority admission条件をF系へ流入させ、Standard14 tokenを増加させた停止Candidateなので継承しない。
2. 最短正常経路は、required outcomeが固定済みなら必要なtargetとrepository authorityを読み、実行可能なimplementation choiceをbindし、変更前evidence operationをterminalにしてartifact変更へ進む経路である。
3. 保存済み誤経路はCandidate116 A02 Rating v14 Medium `N=20`とする。20 / 20件がscore `4`だったが、5 / 20件がimplementation choiceを明示的にbindした後、最初のartifact変更より前に合計7 commandへ再入した。
4. 5件の再入前に、既存`EVIDENCE_GATE`が追加evidenceを開く`missing / unreadable / bind済みvalueまたはconstraintとの具体的矛盾 / allowed path内で充足不能 / 適用中instructionによる別authorityの明示`は観測していない。
5. TaskSpecとrepository authorityは正しいcanonical targetを一意に解決できる。再入は情報不足ではなく、bind済み状態から未発行readを失効させる遷移が実行時に成立しなかったことから生じた。
6. promptは、モデルが許可済みresultと自身のbind messageから観測できる変更前operationの停止と次tool発行を制御する正しい層である。tool result配送またはruntime非観測状態を変更しない。
7. 置換するpredicateは、artifact変更を発行できるimplementation choiceのbindを変更前evidence operationのterminal resultへ変換し、未発行readを失効させる一つだけである。
8. 消す判断点は、canonical target、故障predicate、変更内容、保持constraintをbindした後も、一般的確認またはvalidation identity探索のため変更前readを継続する分岐である。
9. 新しいauthority admission label、case固有path、authority whitelist、tool名、read回数、token・時間閾値、Executor制御は追加しない。既存の追加evidence開放条件は変更しない。
10. 初回評価はA01 r2 / A02 r2 / F01 r3各`N=5`とする。quality gateは15 / 15件score `4`とする。mechanism gateはA01の変更・試験0件、A02のcanonical成果5 / 5かつbind後・変更前再入0 / 5、F01のrequired validation完了5 / 5とする。
11. qualityまたはmechanismが一件でも崩れた場合は停止する。通過時だけA02を`N=20`へ拡張し、Candidate118のbind後・変更前再入0 / 20を要求する。Candidate116 A02 `N=20`は保存済みresultを再利用し、再実行しない。
12. A02 `N=20`が0 / 20を満たす前にStandard14へ進めない。`N=20`で一件でも再発した場合は停止し、同じterminal predicateの微修正を続けない。

## 置換する規則

Candidate116の`EVIDENCE_GATE`にある次の抽象句を置換する。

```text
許可済みresultで変更predicateまたはterminal dispositionを判定できた時点で変更前evidence operationをterminalにする。
```

置換後は次の遷移を固定する。

```text
許可済みresultから、target artifact、targetへ適用中のrepository instruction、実行可能な変更predicate、保持するconstraintがbindされartifact変更を発行できる時点で、そのresultを変更前evidence operationのterminal resultとする。未発行の変更前evidence invocationを失効させ、次にartifact変更を発行する。artifact変更後に確定可能なrequired validation identityの探索はVALIDATION_PLANで行い、変更前evidence operationを再開しない。
```

既存の追加evidence開放条件はそのまま残す。許可済みresult自体が開放条件を観測した場合だけ、そのresult identityと次のevidence identityをbindして一件許可する。

## 非目標

- required outcomeとimplementation choiceの境界変更
- implementation authority admission条件の追加
- A01 / A02固有のprompt分岐または固定path例示
- implementation methodまたはvalidation commandの固定
- validation wrapper、Executor、dispatch、rating contractの変更
- Candidate116の採用判断
- release、runtime projection、THE-CAPTION本体反映

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 15件
- direct KPI reference: 保存済みCandidate116同case atomic `N=5`
- route-stability reference: 保存済みCandidate116 A02 atomic `N=20`

Candidate116は再実行しない。最初にCandidate118の不足15 slotだけを発行する。targeted gateを通過する前にA02 `N=20`拡張profileまたはStandard14 profileを作らない。

## 評価後の現在状態

宣言順どおり、targeted各`N=5`、A02 `N=20`、Standard14各`N=5`を実行した。詳細と一次数値は[`Candidate116 / Candidate118結果`](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)を正本とする。

- targetedは15 / 15件がscore `4`だった。A01の変更・試験は0件、A02のbind後・変更前再入は0 / 5件、F01のrequired validation欠落は0件だった。
- A02を互換atomic runで`N=20`へ拡張した。20 / 20件がscore `4`で、bind後・変更前再入は0 / 20件だった。Candidate116の同じ診断は5 / 20件、合計7 commandの再入だった。
- Standard14はtargeted 15 runを再利用し、不足55 runだけを単独controller・`M=24`で発行した。70 / 70件がscore `4`だった。
- Standard14集約中央値はCandidate116比でtoken `+118,946`（`+7.44%`）、elapsed `-141.224`秒（`-14.37%`）だった。品質とmechanismは通過したが、costはtradeoffであり、採用判断は固定していない。
- 保存traceではcompleted commandがCandidate116より11件少ない一方、input token合計は`+9.67%`だった。token増を横断的なcommand再入増またはprompt文字数だけへ因果帰属しない。

したがって、Candidate118を評価済み・mechanism成立とする。ただし、採用、release、runtime projection、本体反映は未実施・未判断である。
