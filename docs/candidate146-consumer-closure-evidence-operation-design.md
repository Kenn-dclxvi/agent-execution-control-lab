# Candidate146 consumer closure evidence operation設計

## 結論

Candidate146はCandidate145を直接親とし、`evidence_consumer_ready`をinvocation単位のadmissionからconsumer単位のoperation closureへ置換する。

開始identityのresultがdrift停止を変え得る境界は維持する。そのgate通過後、同じnonterminal required predicateへ入る現在既知の欠落観測に相互依存がなければ、個別resultごとにmodelへ戻さず、一つのevidence operationの共同resultとして受領してからpredicate stateを一度だけ更新する。

file数、target数、command、tool、span、byte、read回数は固定しない。Candidate125のexact-target wave、single-target continuation、criterion-complete取得条件は継承しない。

## Identity

- candidate number: Candidate146
- prompt identity: `the-caption-3ce91a4-consumer-closure-evidence-operation-r1`
- direct parent: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`（Candidate145）
- changed target: root `AGENTS.md`
- changed axis: `consumer_closure_ready`
- evaluation status: `f01_f02_f03_n5_evaluated / quality_gate_passed / incremental_closure_not_demonstrated / start_identity_design_boundary_failed / stopped`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. Candidate145 Standard14は70 / 70件がscore `4`で、consumerのないA02 evidence再入を閉じた。
2. Candidate145はCandidate125比でtoken中央値`+13.74%`、elapsed中央値`+31.04%`となり、cost gateに失敗した。
3. F01とF03は変更前command output量がCandidate125とほぼ同じでも、変更前command中央値が`1 → 3`、cached input中央値がそれぞれ`+56,832`、`+45,312`増えた。
4. F02は変更前command中央値が`1 → 8`となり、同じconsumerへ入る4 targetが個別resultとして返った。5件中2件はその後に追加readも行った。
5. Candidate145の各commandは、前commandのresult受領後に次が開始していた。既知の相互非依存観測が逐次model往復へ分断された。
6. Candidate145の変更後validation output量はCandidate125とほぼ同じであり、今回の変更対象ではない。
7. Candidate143でCandidate125のone-waveを非継承にしたことが分断の系譜上の起点である。ただしCandidate125のexact target setとsingle-target continuationはF04の狭い取得境界を再導入するため戻さない。
8. C145のlifecycle-wide consumer、required outcome implementation bind、validation predicate / method境界は保持する。
9. executor、CLI、runtime hook、wrapper、rating contractは変更しない。
10. 初回はF01 / F02 / F03各N=5、M=24とする。一件でもscore `3`以下、required effect欠落、required validation欠落、drift停止境界の越境、または既知の同一consumer観測間へのmodel再入があれば停止する。

## 初回評価結果

F01 / F02 / F03各N=5は15 / 15件がscore `4`だった。`agent_message`をmodel step境界として再監査すると、既知のsource / test観測はCandidate145、Candidate146とも15 / 15件で同じmodel stepから共同発行されていた。Candidate146の増分closureは観測されなかった。

Candidate146は変更前model stepを減らさず、中央値はF01 `2 → 3`、F02 `2 → 3`、F03 `2 → 2`だった。F01の1件はCandidate146自身が分離すると定義した開始identityとcontentを同じmodel stepへ入れた。明示したdesign gateに該当するためCandidate146は停止する。

3 case集約ではCandidate145比token`-4.50%`、elapsed`-5.61%`だったが、step数は減っていないため追加軸へ帰属しない。Candidate125のcase別token / elapsed目標にも3 caseすべて届かなかった。詳細は[`evaluation result`](../evaluations/results/candidate145-candidate146-consumer-closure-evidence-operation-v14-medium-f01-f02-f03-atomic-n5-stopped-cli0146_2026-08-02.md)と[`model step再監査`](candidate146-model-step-boundary-audit.md)を正本とする。

## 置換する境界

```text
consumer_closure_ready :=
  同じnonterminal required predicateについて
  現在既知の欠落観測がconsumerへ全件bind済み
  ∧ 一観測のresultが他観測のtarget / permission / method / stop conditionを変えない
  ∧ 共同resultを受領すればpredicate stateを一度だけ更新できる
```

`consumer_closure_ready=true`なら、bind済み観測を一つのrepository evidence operationとして発行する。各観測のresultを個別にmodelへ返して、同じclosure内の次観測を後から発行しない。共同resultを全件受領した後に一度だけ`satisfied / unsatisfied / unobserved`を更新する。

一観測のresultが別観測の必要性、対象、permission、method、停止を変え得る場合は、同じclosureへ入れない。前operationのresultを受領してから次のclosureを作る。

開始identityは、予期しないdriftならtarget contentを読まず停止する条件を持つ。そのため開始identityとimplementation contentは別operationのままとする。開始gate通過後にTaskSpecから既知のsource / test観測が同じimplementation predicateを共同で決め、相互依存がなければ一つのclosureへ入れる。

## 既存境界との関係

`DECISION_BOUNDARY`は、resultが未発行invocationを変え得るかを一般的に判定する。Candidate146はこの一般則を置換しない。

今回追加するのは、`EVIDENCE_GATE`が各invocationを個別にadmitした後も共同consumer resultを作らなかった空白への境界である。consumer closureは、同じpredicateの既知観測を一つのresult identityへbindする。したがって、単なる「commandをまとめる」という方法規則ではない。

既存Candidateとの重複と差は次のとおりである。

- Candidate69の`DECISION_BOUNDARY`は、既知の相互非依存invocationを同じmodel stepへ置く一般則である。Candidate145にもこの規則は存在するが、今回のF01 / F02 / F03分断を閉じなかった。
- Candidate112はevidence admissionとschedulingを分離し、発行順序を`DECISION_BOUNDARY`へ委ねた。しかしtargeted試験でtool callとmodel stepが各`+16`となり、scheduling削減を実証できなかった。Candidate146は同じ一般則を繰り返さず、共同resultを消費するpredicate identityまで発行前にbindする。
- Candidate122は同じ未解決predicateのcontentを一つのwaveへ閉じたが、TaskSpec列挙のexact target setと直後の`edit-ready / terminal stop`を要求した。Candidate146はexact setと直後terminalを要求せず、現在既知の欠落観測と共同consumer stateだけを固定する。
- Candidate125はCandidate122へsingle-target continuationを追加した。Candidate146はこの取得範囲・target数・continuation回数の制御を継承しない。

Candidate125との違いは次のとおりである。

| 境界 | Candidate125 | Candidate146 |
| --- | --- | --- |
| 集合のauthority | TaskSpec列挙のexact target set | 同じconsumerへbind済みの現在既知の欠落観測 |
| 開始identity | contentと同一invocationになり得た | drift停止を変えるため別operation |
| target制約 | exact set、single editable target分類あり | file数、target数を固定しない |
| 取得完了 | symbol contextまたは全content終端 | required predicateを変える共同result |
| 追加観測 | single-target continuation一件 | 前resultが具体的不足を示した場合に次closureを再構成 |

## 汎用性

consumer closureはStandard14や特定file構成に依存しない。

- sourceとtestが一緒にimplementation choiceを決める場合
- applicationとdomainのrelationを複数sourceで確認する場合
- schemaとreader、configとconsumer、dependency declarationとlock provenanceを共同確認する場合
- 変更後のsource relationとdiff / statusが別predicateを消費する場合

には、それぞれconsumer identityとdecision boundaryからclosureを作る。

同じTaskSpecに列挙されていても、先のresultで後の対象が変わる探索、drift停止、失敗後recovery、順序付きvalidationは同じclosureへ入れない。

## 初回評価gate

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| F01 required成果とvalidation | 5 / 5 |
| F02両source変更とvalidation | 5 / 5 |
| F03 cleanup成果とvalidation | 5 / 5 |
| 開始identity後のdrift gate維持 | 15 / 15 |
| 同一consumerの既知観測間model再入 | 0 / 15 |
| consumer closure後の不足根拠なし追加read | 0 / 15 |
| consumerを持たないevidence | 0 / 15 |

## Cost gate

直接基準は同一互換条件のCandidate145 F01 / F02 / F03各N=5とする。Candidate125は目標挙動の補助比較に限定する。

- F01 / F02 / F03合計token中央値がCandidate145以下
- F01 / F02 / F03合計elapsed中央値がCandidate145以下
- case別tokenまたはelapsedが上昇した場合は、保存trace上の新しいmodel再入、追加read、retryの有無を分ける
- N=5からStandard14全体costへ一般化しない

## 非目標

- shell compound、parallel tool call、特定commandの指定
- file、target、line、byte、span、read回数の上限
- 開始identityとcontentの無条件一括化
- Candidate125のexact-target waveまたはsingle-target continuationの復元
- required validationの一括化または省略
- artifact変更後evidenceの一律禁止
- executor、CLI、runtime hook、wrapper変更

## 初回試験

- cases: F01 r3 / F02 r1 / F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- repetition / configured M: 各`N=5` / `24`
- direct reference: Candidate145同case atomic run
- prompt以外の互換条件: Candidate145と完全一致

Candidate145の既存runは再実行しない。Candidate146の不足15 slotだけを発行する。score `3`以下またはmechanism gate失敗が一件でもあれば停止し、Standard14、追加反復、採用、releaseへ進めない。
