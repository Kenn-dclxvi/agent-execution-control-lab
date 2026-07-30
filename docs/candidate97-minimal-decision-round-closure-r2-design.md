# Candidate97 minimal decision round closure r2設計

## 結論

r1の長い列挙を廃止し、Candidate81の`DECISION_BOUNDARY`へ二つの閉包条件だけを追加する。

1. 追加invocationには、新たに判明した必要evidenceの事前bindingを要求する。
2. terminal resultがある同一invocationの理由なし再発行を禁止する。

## Identityと状態

- candidate number: Candidate97
- revision: r2
- prompt identity: `the-caption-3ce91a4-decision-round-closure-r2`
- direct parent: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- changed target: root `AGENTS.md`
- changed rule: `DECISION_BOUNDARY`
- evaluation status: `targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 作成根拠

C81 F02 100 runは全件score `4`だが、agent message 7件以上の15 runはelapsed下位25%へ一件も入らず、full gateを2回実行した5 runのelapsed中央値は`126.322`秒だった。既存規則は相互非依存invocationの同時発行を要求するが、wave後にinvocationを追加できる条件とterminal result再利用を明示していない。

r1はinspectionとcompletionの具体例を規則本文へ列挙しすぎた。r2は結果から必要な制御だけを残し、TaskSpec、read対象、validation集合、completion evidenceを新たに定義しない。

## Prompt変更

Candidate81の`DECISION_BOUNDARY`一規則だけを置換する。

- waveを分けられるのは、先行resultが未発行invocationの4値を変え得る場合だけとする。
- 既知の相互非依存invocationは従来どおり一waveから発行する。
- wave後の追加invocationには、新たに判明した必要evidenceを先にbindする。
- terminal resultがある同一invocationは、result失効または`RECOVERY`なしに再発行しない。

## 非目標

- inspectionまたはcompletion commandの列挙
- TaskSpec、repository authority、required validationの変更
- command数、message数、token数の上限
- stdout配送またはexecutorの変更
- 採用、release、本体反映

## F02 gate

- F02 r1、Rating v14、Medium、CLI `0.146.0`
- candidate-only `N=5`、`M=5`
- score `4`: 5 / 5
- required command evidence: 5 / 5
- full gate一回: 5 / 5
- terminal validation後の同一full gate再発行: 0 / 5
- reason bindingなしの追加read: 0 / 5

いずれかを満たさなければ停止する。通過した場合だけ保存済みC81 resultとKPIを比較する。

## F02評価結果

2026-07-30にCandidate97 r2だけを`N=5`、`M=5`で実行した。5 / 5件がscore `4`で、focused gateとfull gateは各run一回だった。一方、全5件がfull gate成功後に別の`git status` commandを発行し、completion decision-round closureは0 / 5だった。inspection commandも3件から12件に分布し、同一model stepの一waveへ閉じた一次証拠を取得できなかった。

事前gateに従い、現在状態を`targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。詳細は[`F02 result`](../evaluations/results/candidate81-candidate97-decision-round-closure-r2-v14-medium-f02-n5-cli0146_2026-07-30.md)を正本とする。
