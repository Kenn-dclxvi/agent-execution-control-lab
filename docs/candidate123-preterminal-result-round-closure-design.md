# Candidate123 preterminal result round closure設計

## 結論

Candidate123はCandidate122を直接親とする。Candidate122で成立したF02 content-wave closureとcost改善を保持し、artifact変更またはclarification停止までにresultをmodelへ返すroundを、状態に応じて0回または1回へ閉じる。

制御は一つに限定しない。同じ`preterminal result round`軸の中で、`spec_ready=false`のclarification terminalと、`spec_ready=true`のfail-closed evidence ticketを別predicateとして`EVIDENCE_GATE`へ追加する。

## Identityと状態

- candidate number: Candidate123
- prompt identity: `the-caption-3ce91a4-preterminal-result-round-closure-r1`
- direct parent: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`
- changed target: root `AGENTS.md`
- changed axis: artifact変更またはclarification停止前のmodel-visible result round closure
- evaluation status: `targeted_a01_a02_f01_f02_evaluated / quality_gate_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 根拠

保存traceの詳細は[`Candidate122 preterminal result round分析`](candidate122-preterminal-result-round-analysis.md)を正本とする。

1. A01はtoolなし2件のtoken中央値が`18,431`、開始identity resultを一度返した3件が`37,382`だった。
2. C118にも同じ二経路があり、全体中央値差はN=5内の経路比率反転である。C122固有のA01回帰ではない。
3. A02は変更前result round 1回の2件が`126,028 / 127,300`、2回の3件が`165,870 / 194,659 / 221,776`だった。
4. F02は1 roundの4件が`122,020〜125,424`、開始identityを別roundへ分けた1件が`179,543`だった。
5. F02の4 content invocationは同じmodel stepから発行され、途中判断を挟まなかった。tool invocation数ではなくmodel-visible result round数が分離要因である。
6. C118比ではA01だけが未達である。C107のcase値比ではA02だけが未達である。正式な最終目標はC107 Standard14 token中央値`1,523,137`以下であり、targeted case値は経路確認用の先行指標とする。

## 追加する制御

### clarification terminal

`clarification_terminal_ready := spec_ready=false ∧ TaskSpec本文だけで未固定required outcome valueを特定済み ∧ repository evidenceがそのvalueをbindできない ∧ artifact変更 / test / repository predicateを未開始`

`clarification_terminal_ready=true`なら、TaskSpec明示の開始identityを独立resultとして返さず、未固定required outcome valueだけをclarification resultにしてoperationをterminalにする。clarificationはartifact変更判断ではない。開始identity、target、authority、testのreadを発行しない。

### fail-closed prechange ticket

`prechange_result_round_ready := spec_ready ∧ 開始identity predicate / admission済みevidence identity / identity不一致時のstop / identity一致時に確定する変更predicateが発行前にbind済み ∧ result後の判断がedit-readyまたはterminal stopへ限定済み`

`prechange_result_round_ready=true`なら、一つのcustom exec wrapper内で開始identityを先に確認する。identityが不一致、dirty、unavailableならevidenceを発行せず、その具体的resultをterminal stopとして返す。identityが一致した場合だけ、同じwrapper内でadmission済みevidenceを個別commandとして発行し、完了済みresultをmodelへ一度だけ返す。shell compound commandへ結合しない。

返却resultで変更predicateと保持constraintをbindできれば次にartifact変更を発行する。`missing / unreadable / contradiction / unsatisfied constraint`なら具体的理由で停止する。identity successだけ、各evidence successだけ、permission確認だけをmodel return boundaryにしない。

`prechange_result_round_ready=false`ではC122のdefault-deny admissionとexact-target content-wave条件を維持し、未知targetを捏造して一括取得しない。

## 初回targeted gate

初回評価はA01 r2 / A02 r2 / F01 r3 / F02 r1各`N=5`、Rating v14、`gpt-5.6-sol` Medium、CLI `0.146.0`、profile上の`M=24`へ固定する。

quality / mechanism gateは次とする。

- execution: `20 / 20 valid`
- quality: score `4` × 20
- A01: required value待ち5 / 5、変更0 / 5、test 0 / 5
- A01: clarification前command 0 / 5
- A02: canonical成果5 / 5
- A02: artifact変更前result round 1回以下5 / 5
- A02: artifact変更後・最初のvalidation前method探索0 / 5
- F01: required command evidence完備5 / 5、command protocol違反0件
- F02: exact target set content wave 5 / 5
- F02: artifact変更前result round 1回以下5 / 5
- F02: focused / full required validation完備5 / 5

cost先行指標は次とする。

- A01 token中央値: Candidate118の`18,431`以下
- A02 token中央値: Candidate107の`125,559`以下
- F01 token中央値: Candidate107の`127,797`以下
- F02 token中央値: Candidate107の`173,000`以下

qualityまたは対象mechanismが一件でも崩れた場合は停止する。targeted gate通過時だけ、保存済みatomic runを再利用してStandard14の不足caseを実行するかを別判断する。

## 非目標

- command数、file数、content bytesの一般上限
- unknown targetの推測またはrepository-wide evidenceの無条件batch
- identity failure後のevidence取得
- shell compound commandによるexit codeまたはstop conditionの喪失
- Candidate122のF02 content-wave制御の撤回
- executor、tool adapter、runtime hook、外部wrapperの変更
- release、runtime projection、THE-CAPTION本体反映

## 評価結果

[`Rating v14 Medium A01 / A02 / F01 / F02各N=5`](../evaluations/results/candidate122-candidate123-preterminal-result-round-closure-v14-medium-a01-a02-f01-f02-atomic-n5-cli0146_2026-07-31.md)は20 / 20 validだったが、F02の1件が正常なdetached HEADをbranch identity未確定と誤分類して停止し、score `2`となった。A02の変更前result round 1回以下も3 / 5に留まった。事前停止条件に従いCandidate123を`stopped`とし、Standard14へ進めない。
