# Candidate119 validation predicate / method boundary設計

## 結論

Candidate119はCandidate118を直接親とし、validation readinessの一変更軸だけを置換する。

TaskSpecまたはcommand evidence protocolが要求するvalidation predicate、順序、個別pass条件、stop条件がbind済みなら、TaskSpec未指定のexact commandは未固定のvalidation identityではなくexecution methodとして扱う。exact commandを探すことだけを理由にrepository evidenceを追加せず、既に受領したTaskSpec、適用中instruction、target evidenceの範囲でmethodを選び、validation実行票へbindする。

Candidate118のrequired outcome / implementation choice境界、implementation bind後の変更前evidence terminal closure、cell ID付きnonterminal result後のwait-only制御は変更しない。

## Identityと状態

- candidate number: Candidate119
- prompt identity: `the-caption-3ce91a4-validation-predicate-method-boundary-r1`
- direct parent: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed axis: `validation_predicate_ready`によるvalidation predicate / exact command method境界
- evaluation status: `targeted_a01_a02_f01_evaluated / quality_gate_passed / postchange_method_boundary_passed / prechange_terminal_closure_failed / a02_cost_target_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate118とする。Candidate118のA02 `N=20`は20 / 20件がscore `4`で、implementation bind後・最初のartifact変更前のevidence再入は0 / 20件だった。この制御を親として保持する。
2. 基準状態の最短正常経路は、Candidate118 A02 iteration 2、run `24c2ce13affc4919bf8fb8f12d35a2b9`である。canonical implementationをbindして`run.sh`を変更した後、repository探索を追加せず、shell syntax、既存test、diff、statusを実行してscore `4`へ到達した。all-agent tokenは`133,737`だった。
3. 保存済み誤経路はCandidate118 A02 iteration 1 / 3 / 4 / 5である。4 / 5件がartifact変更後、最初のvalidation commandより前にtests、`tests/AGENTS.md`、pytest設定またはtest runnerを追加探索した。tokenは`224,977`から`316,128`だった。
4. 同じ追加探索はCandidate107 A02にも2 / 5件存在した。したがって新規事象とは扱わない。Candidate118では発生率が4 / 5へ偏り、case中央値がCandidate107の`125,559`から`226,321`へ増えた分布差を対象にする。
5. A02 TaskSpecは「shell syntax、既存test、最終diff」というvalidation predicateを要求するが、`pytest -q`または`pytest tests/ -v`等のexact commandを成果値として固定しない。repository authorityはcanonical implementationを解決できるが、TaskSpec未指定のexact command探索を必須にはしない。
6. 現行`VALIDATION_CLOSURE`は`validation_set_ready`へexact commandの事前bindを要求し、`EVIDENCE_GATE`はartifact変更後に確定可能なvalidation identity探索を`VALIDATION_PLAN`へ委ねる。一方、`METHOD`はTaskSpec未指定手段をexecutorが選ぶとする。この重なりが、predicate成立後もexact command確認のためrepository探索を開く判断点を残す。
7. 置換する一つの変更軸は、`validation_predicate_ready`を導入し、TaskSpecまたはcommand evidence protocolがexact commandを明示したvalidationだけcommandの事前bindを要求することである。未指定commandは`METHOD`としてvalidation実行票を発行する時点で選択してbindする。
8. 消す判断点は、validation predicate、順序、pass条件、stop条件がbind済みであるにもかかわらず、exact commandがTaskSpec未指定という理由だけでrepository evidenceを追加する分岐である。
9. 新たに増える判断点は、TaskSpecまたはcommand evidence protocolがexact commandを明示しているかの一件である。これは実行前のmodel-visible入力から判定する。明示command、required validation、fail-fast、個別exit判定は弱めない。
10. A02固有path、pytest command、read回数、token閾値、tool名、wrapper deadline、executor制御はpromptへ追加しない。evidence output cap、temporary file projection、read batchingも追加しない。
11. 初回評価はA01 r2 / A02 r2 / F01 r3各`N=5`とする。quality gateは15 / 15件score `4`とする。
12. mechanism gateは、A01の変更・test 0 / 5、A02のcanonical成果5 / 5、implementation bind後・変更前evidence再入0 / 5、artifact変更後・最初のvalidation command前のvalidation-method探索0 / 5、F01のrequired command evidence完備5 / 5とする。
13. cost gateはA02 token中央値をCandidate118の`226,321`未満かつC81以降のcase最小CandidateであるCandidate107の`125,559`以下とする。前者だけを満たし後者を満たさない場合はmechanism成立とcost目標未達を分離して停止し、A02 `N=20`またはStandard14へ進めない。
14. qualityまたはmechanismが一件でも崩れた場合は停止する。全gate通過時だけA02を互換atomic runで`N=20`へ拡張し、Candidate118の二つのclosureを同時に要求する。

## 置換する変更軸

`VALIDATION_CLOSURE`のreadinessを次へ置換する。

```text
validation_predicate_ready := artifact変更完了 ∧ TaskSpec-required validationのpredicate / order / individual pass condition / stop conditionが全件bind済み ∧ TaskSpecまたはcommand evidence protocolがexact commandを明示したvalidationだけそのcommandがbind済み
```

`validation_predicate_ready=true`で、exact commandがTaskSpec未指定の場合、その未固定状態をmissing validation identityとしてrepository evidenceの開放条件にしない。既に受領したTaskSpec、適用中instruction、target evidenceの範囲から`METHOD`として選択し、validation実行票の発行時にcommandへbindする。

TaskSpecまたはcommand evidence protocolがexact commandを明示する場合は、従来どおりそのcommandをrequired validationとしてbindする。commandを抽象predicateへ読み替えたり、別methodへ置換したりしない。

## 非目標

- Candidate118のrequired outcome / implementation choice境界の変更
- implementation bind後の変更前evidence terminal closureの変更
- validation nonterminal返却またはouter deadlineの抑止
- evidence resultのscope、byte数、projection、batching制御
- case固有commandまたはpathのprompt固定
- executor、dispatch、rating contractの変更
- Candidate118の採用判断
- release、runtime projection、THE-CAPTION本体反映

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 15件
- direct parent reference: 保存済みCandidate118同case atomic `N=5`
- case cost target: Candidate107 A02中央値`125,559`

Candidate118は再実行しない。Candidate119の不足15 slotだけを発行する。targeted quality、mechanism、costの全gateを通過する前にA02 `N=20`拡張profileまたはStandard14 profileを作らない。

## 評価結果

15 / 15件はvalidかつscore `4`だった。A02の変更後・最初のvalidation前method探索はCandidate118の4 / 5件から0 / 5件へ減り、token中央値は`226,321`から`149,154`へ下がった。一方、implementation bind後・変更前command再入が1 / 5件発生し、Candidate107のcase目標`125,559`以下にも届かなかった。事前停止条件に従いA02 `N=20`とStandard14へ進めず、Candidate119を停止する。詳細は[`評価結果`](../evaluations/results/candidate118-candidate119-validation-predicate-method-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md)を正本とする。
