# Candidate122 prechange evidence wave closure設計

## 結論

Candidate122はCandidate119を直接親とする。停止したCandidate120とCandidate121は継承しない。

Candidate119で成立したvalidation predicate / exact command method境界を保持する。TaskSpecが同じ未解決predicateを共同で決めるexact target setを列挙済みの場合だけ、変更前content evidenceを一つのinvocationへ閉じ、そのterminal resultを`edit-ready`または`terminal stop`にする`prechange_evidence_wave_ready`一変更軸を`EVIDENCE_GATE`へ追加する。

## Identityと状態

- candidate number: Candidate122
- prompt identity: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`
- direct parent: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`
- non-parent: `the-caption-3ce91a4-implementation-edit-ticket-closure-r1` / `the-caption-3ce91a4-evidence-request-scope-closure-r1`
- changed target: root `AGENTS.md`
- changed axis: exact target setに対する変更前content evidence waveの発行とterminal closure
- evaluation status: `standard14_evaluated / token_target_passed / quality_gate_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate119とする。Candidate119はA02の変更後validation-method探索を0 / 5件へ減らした。この成立部分を保持する。
2. Candidate121はA02のimplementation bind後・変更前再入を0 / 5件、token中央値を`143,419`まで改善したが、変更後method探索が1 / 5件再発した。Candidate121を親にしない。
3. Candidate107 / Candidate118 / Candidate121のF02各5 traceを[`Candidate121 F02 evidence route分析`](candidate121-f02-evidence-route-analysis.md)で対応付けた。変更前evidence bytes中央値は`53,938 / 110,667 / 41,410`、token中央値は`173,000 / 256,931 / 209,379`だった。bytes削減だけではC107水準へ戻らない。
4. 最初のtarget数だけでもtokenの高低を分離できない。4 targetを最初に読んだrunにC107最小`135,285`、C118低値`172,226`、C118 / C121高値が共存した。
5. evidence invocation数だけでも分離できない。C121最高値`260,556`は変更前evidence 2件、低値`171,805`は6件だった。
6. C121はlocatorを独立resultとしてmodelへ返す二段階routeを追加した。agent message数中央値はC107 / C118の5から6へ増えた。exact target setがTaskSpecで列挙済みのF02では、locator identityを独立resultにする必要性を保存traceから確認できない。
7. 追加する一変更軸は、`prechange_evidence_wave_ready := spec_ready ∧ TaskSpecが同じ未解決predicateを共同で決めるexact target setを列挙済み ∧ target全件がadmission済み ∧ result受領後の判断がedit-readyまたはterminal stopへ限定済み`である。
8. `prechange_evidence_wave_ready=true`なら、exact target setのcontent evidenceを一つのinvocationで取得する。locator identityを独立resultとして返さず、複数の変更前content invocationへ分割しない。
9. そのterminal resultで変更predicateと保持constraintをbindできれば、未発行evidenceを失効させてartifact変更を発行する。bindできなければ、観測した具体的なmissing / unreadable / contradiction / unsatisfied constraintをterminal dispositionとして停止する。一般的安全確認またはmethod確認として次waveを開かない。
10. TaskSpecがexact target setを列挙していない場合、またはtargetが同じpredicateを共同で決めない場合はfast pathを適用せず、Candidate119のdefault-deny admissionと一件ずつの追加evidence条件を維持する。
11. Candidate50の一般read batchingはA02 costを拡大した。Candidate122は順序非依存read一般へ適用せず、TaskSpec列挙済みexact target set、同一predicate、terminal dispositionの三条件をすべて要求する。
12. A系またはF系固有path、symbol、tool名、byte閾値、executor、wrapper deadlineはpromptへ追加しない。

## 初回targeted gate

初回評価はA01 r2 / A02 r2 / F01 r3 / F02 r1各`N=5`、Rating v14、`gpt-5.6-sol` Medium、CLI `0.146.0`、profile上の`M=24`へ固定する。

quality / mechanism gateは次とする。

- execution: `20 / 20 valid`
- quality: score `4` × 20
- A01: required value待ち5 / 5、変更0 / 5、test 0 / 5
- A02: canonical成果5 / 5
- A02: implementation bind後・最初のartifact変更前のcommand再入0 / 5
- A02: artifact変更後・最初のvalidation前method探索0 / 5
- F01: required command evidence完備5 / 5、command protocol違反0件
- F02: TaskSpec列挙済みexact target setを同一predicateへbind 5 / 5
- F02: 最初のartifact変更前のcontent evidence invocation 1件以下 5 / 5
- F02: locator-only result後の別content invocation 0 / 5
- F02: content evidence terminal result後の追加read 0 / 5
- F02: focused / full required validation完備5 / 5

cost gateは次とする。

- A02 token中央値: Candidate119の`149,154`以下
- F02 token中央値: Candidate107の`173,000`以下
- いずれも満たさない場合、mechanism成立とcost未達を分離して停止する

qualityまたはmechanismが一件でも崩れた場合は停止する。全gate通過時だけA02 / F02の拡張試験とStandard14を別判断する。

## 期待と逆の結果になった場合

- exact target setをbindしてもcontent evidenceが複数invocationへ分かれた場合、このpredicateは発行routeを制御できていないため停止する。
- one-wave routeが成立してF02 costだけ未達の場合、bytes、target数、invocation数を追加でprompt制約せず、同一event sequence内のtoken分散として停止する。
- A02の変更前再入または変更後method探索が再発した場合、fast pathの非適用条件が既存境界を保持していないため停止する。
- 一部runだけで成立した場合、文言の微修正を続けず、成立 / 不成立traceの発行前state差が観測できる場合だけ別Candidateを検討する。

## 非目標

- Candidate121のlocator identity条件の微修正
- Candidate120のedit ticket labelの微修正
- 全readのbatch化またはread回数の一般上限
- byte cap、temporary file、output受領後projection、result classification
- validation nonterminal返却自体の抑止
- executor、dispatch、rating contractの変更
- release、runtime projection、THE-CAPTION本体反映

## 評価結果

20 / 20件はvalidかつscore `4`だった。F02の変更前content evidenceはliteralな一つのinvocationとして4 / 5件だったが、4 invocationのrunも同じmodel stepから発行され、途中判断のない一つのcontent waveとしては5 / 5件で成立した。F02 token中央値`124,719`は事前目標`173,000`を下回った。詳細は[`targeted評価結果`](../evaluations/results/candidate118-candidate122-prechange-evidence-wave-closure-v14-medium-a01-a02-f01-f02-atomic-n5-cli0146_2026-07-31.md)を正本とする。

後続の[`Standard14各N=5`](../evaluations/results/candidate118-candidate122-prechange-evidence-wave-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)はtoken中央値`1,403,840`でCandidate107目標を通過したが、F04の1件がincomplete bounded contentをterminal missingと誤分類してscore `2`となった。後続証拠により現在状態を`quality_gate_failed / stopped`へ更新する。targeted resultの20 / 20 score `4`は履歴として保持する。
