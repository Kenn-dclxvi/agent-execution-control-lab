# Candidate113 explicit authority delegation設計

## 結論

Candidate113はCandidate108を直接親とし、`EVIDENCE_GATE`一規則だけを置換する。

未固定のrequested outcome valueをrepository authorityから解決する経路は、TaskSpecがその値の決定をrepository authorityへrequired constraintとして明示した場合だけ開く。一般的なread permissionや「既存authorityを必要範囲で読む」というallowed-read constraintは、値の決定を委ねた根拠にしない。

これはtool call数や読取り順を指定する制御ではない。未固定値を解決するauthority evidence identityのadmission条件を、model-visibleなTaskSpecへbindする境界制御である。

## Identityと状態

- candidate number: Candidate113
- prompt identity: `the-caption-3ce91a4-explicit-authority-delegation-r1`
- direct parent: `the-caption-3ce91a4-validation-ticket-terminal-closure-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_GATE`の置換
- bundle SHA-256: `6524aab28cc7b5af48bbc093695ba9bdefbdf6d3e1b945420654ec2eeb13bffe`
- evaluation status: `targeted_a01_a02_evaluated / quality_gate_passed / descriptive_cost_lower / authority_admission_not_demonstrated / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準prompt setはCandidate108とする。Candidate112は停止済みであり継承しない。
2. 基準状態での最短正常経路は、TaskSpec明示の開始状態とtarget artifactを確認し、requested outcome valueが未固定でauthorityへの明示委譲もない場合に、一度のclarification resultでterminalにする経路である。
3. 保存済み誤経路はCandidate108 A01 r2 N=5の3 runとCandidate112 A01 r2 N=5の3 runである。target artifactから現在値と未固定valueを判定した後も、直接関連testまたはrepository-wide authorityを追加探索した。
4. Candidate108 A01の2 runは、開始状態とtarget artifactだけでscore `4`のclarification resultへ到達した。追加探索はquality成立に必要ではない。
5. Candidate108の`EVIDENCE_GATE`は「repository authorityへ委ねられている」を直接観測可能なTaskSpec predicateとして定義していない。A01の一般的なallowed-read constraintを値決定の委譲と解釈する分岐が残る。
6. 置換するpredicateは`authority_delegated`一つとする。TaskSpecがrequested outcome valueをrepository authorityから決めることをrequired constraintとして明示した場合だけtrueとする。
7. 消す判断点は、一般的なread permissionまたはallowed-read constraintを根拠に、不存在かもしれない値決定authorityを探索する分岐である。
8. 新しいtool名、path allowlist、回数、token、時間閾値、Executor制御は追加しない。
9. A02は「canonical targetはrepository authorityと現行entrypoint実体を根拠に決める」と明示するため、`authority_delegated=true`のpositive controlとして保持する。
10. 初回評価はA01 r2とA02 r2の各N=5とする。10 / 10件のscore `4`を必須とする。A01ではtarget artifactが別authorityを明示しない限り、値決定のためのtest・repository-wide authority探索が0件であることをmechanism gateとする。A02ではcanonical成果への到達を必須とする。
11. quality、A01 mechanism、A02 canonical成果のいずれかが崩れた場合は停止する。通過前にStandard14へ進めない。

## 変更する規則

```text
authority_delegated := TaskSpecがrequested outcome valueをrepository authorityから決めることをrequired constraintとして明示
```

requested outcome valueが未固定かつ`authority_delegated=true`の場合だけ、その値をbindするauthority invocationを許可する。一般的なread permissionまたはallowed-read constraintは、このpredicateをtrueにしない。

`authority_delegated=false`で許可済みresultが未固定valueを示した場合は、追加探索を開かずclarification resultとして変更前evidence operationをterminalにする。

## 非目標

- tool call、shell grouping、並列発行、model return回数の直接指定
- Executor、validation wrapper、outer yieldの変更
- case固有pathまたはevidence whitelistの追加
- TaskSpec、Evaluation set、fixture、rating、model、reasoning、CLI、permissionの変更
- 採用、release、runtime projection、THE-CAPTION本体反映

## 初回試験

- cases: A01 r2 / A02 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: 各`N=5`
- profile上の並列上限: `M=24`
- ready slot: 10件
- direct reference: Candidate108の保存済み同case atomic N=5

初回gateを通過する前にStandard14 profileを作らない。

## 評価結果

初回試験は10 / 10件がscore `4`だった。固定schemaの合算中央値はCandidate108比でtoken`-26.28%`、elapsed`-18.90%`だった。

一方、A01でtarget artifact確認後に追加authority探索なしでclarificationへ到達したrunは0 / 5だった。4件は明示委譲なしでauthority探索へ進み、1件はtarget artifactを確認せず直接clarificationへ進んだ。狙ったauthority admission境界は成立していないため、Standard14へ進めず停止する。詳細は[`Candidate113 targeted結果`](../evaluations/results/candidate108-candidate113-explicit-authority-delegation-v14-medium-a01-a02-atomic-n5-cli0146_2026-07-31.md)を正本とする。
