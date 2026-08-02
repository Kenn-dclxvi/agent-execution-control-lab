# Candidate134 syntactic lexeme continuation設計

## 結論

Candidate134はCandidate128を直接親とし、`EVIDENCE_GATE`のcontinuation request predicateだけを置換する。Candidate131とCandidate133は停止済みの診断証拠として使い、継承しない。

変更軸は、未解決criterionから意味的なanchor集合を作ることではない。TaskSpec原文に現れるcode-shaped lexemeを構文規則で全件抽出し、その同一target内の完全一致contentを一回のcontinuation resultの先頭へ必ず置く。これにより、exact語があるのにanchor集合を空とみなす判断を削除する。

## Identity

- candidate number: Candidate134
- prompt identity: `the-caption-3ce91a4-syntactic-lexeme-continuation-r1`
- direct parent: Candidate128 `the-caption-3ce91a4-required-effect-closure-r1`
- diagnostic predecessors: Candidate131、Candidate133。停止済みであり継承しない
- changed rule: `EVIDENCE_GATE`
- changed axis: continuation lexeme集合の構文的確定
- unchanged: TaskSpec、Evaluation set、`SPEC`、`RECOVERY`、`VALIDATION_PLAN`、`METHOD`を含む他の全rule

## 作成前gate

作成前のStandard14全14件監査は[`TaskSpec lexeme authority監査`](candidate133-task-spec-lexeme-authority-audit.md)を正本とする。

### 基準prompt set

Candidate128を基準とする。単一editable targetが全未解決変更criterionを所有し、初回contentだけでは変更predicateをbindできない場合に限り、同targetへ一回のcriterion-complete continuationを許可する。

### 最短正常経路

Candidate131 F04 N=29の28件は、TaskSpecまたは初回contentのexact語を使って`App.tsx`内の一致箇所と周辺contentを直接取得し、必要変更と3 validationを完了した。

### 保存済み誤経路

- Candidate131 run `e3907d1b47534d05aa19bb6721bf4374`はexact語を受領済みでも全残存contentを選び、配送切詰め後にscore `2`で停止した。
- Candidate133 run `0b5d191ec8974e84ba74abd10c0f543d`はTaskSpecにexact語があっても変更前anchorを使わず、`App.tsx`を順に全量取得した。

両者はanchorの不存在ではなく、anchor集合を意味的に確定する判断がfalse側へ倒れた例である。

### 既存入力だけでは防げない理由

TaskSpecには`audit_match_key`と`colSpan`が明記されている。しかしCandidate131の`criterion_anchor_ready`とCandidate133の`observed_anchor_set`は、その語を未観測criterionへbind可能なanchorと分類する追加判断を要求した。TaskSpecの語を増やしても、この分類判断が残る限り同じ分岐を防げない。

## 置換する一つのpredicate

```text
criterion_code_lexeme_set :=
  各未観測criterionのTaskSpec原文にそのまま現れるASCII tokenのうち、
  criterion IDを除き、
  `_`、`.`、`/`のいずれかを含むもの、または
  小文字から大文字への切替えを含むcamelCase / PascalCase tokenの全件集合

continuation_scope_complete :=
  一つのinvocationのresultで、
  criterion_code_lexeme_setが非空なら最初に
  全memberの同一target内の全完全一致箇所と各周辺contentを直接返し、
  memberのいずれかがtarget内で一致しない場合だけ
  同一targetの全未取得contentを終端まで後続させる
  ∨ 集合が空なら同一targetの全未取得contentを終端まで返す
```

抽出は語の意味、criterionとの関連性、実装方法を判定しない。synonym、TaskSpecにない語、repository-wide searchを加えない。F04では`audit_match_key`と`colSpan`が集合へ入り、両方がtarget内で一致するため全残存content fallback条件は成立しない。

## 消す判断点と増える処理

消す判断点は、TaskSpec中のexact語がidentifier、property、key、labelとしてcriterionへbind可能かという意味分類である。

増える処理は、文字形に基づく集合抽出と各memberの完全一致有無の確認である。これは入力文字列とtargetの一致結果だけで決まり、owner、importance、relevanceを新たに判定しない。

新しいinvocation、continuation回数、target、authority readは増やさない。TaskSpecへ新しいfieldも追加しない。

## 既存制御との分離

- Authority: Candidate116 / Candidate118由来の境界を維持する。
- Evidence coverage: Candidate134の変更対象とする。
- Effect stateとClosure: Candidate128の`required_effects_closed`を維持する。
- Dependency: TaskSpec明示関係とrequired effect集合を維持する。
- Change construction: 新predicateを追加しない。
- executor、CLI、adapter、runtime hook、report delivery: 変更しない。

promptへcase名、特定path、`audit_match_key`、`colSpan`、固定command、固定context幅を入れない。

## 初段F04 N=5 gate

model `gpt-5.6-sol`、reasoning `medium`、CLI `0.146.0`、Rating v14、M=24で、Candidate128とprompt以外の互換条件を機械照合してからCandidate134の不足5 runだけを発行する。

- valid / rateable: 5 / 5
- score `3`以下: 0 / 5
- criterion code lexemeのdirect content: 5 / 5
- 全残存content fallback: 0 / 5
- locator-only独立result: 0 / 5
- staleまたは未観測preimageを持つ変更: 0 / 5
- 必要なartifact変更と3 validation完備: 5 / 5

一件でもscore `3`以下、direct lexeme content欠落、全残存content fallback、必要変更またはvalidation欠落があれば停止する。追加24件、F02、F07、Standard14、採用以降へ進めない。

N=5を通過した場合だけ、同じpoolへ24件を追加してN=29 stabilityを確認する。

## 評価結果

F04 N=5はscore `4 / 3 = 4 / 1`だった。direct lexeme contentは5 / 5だったが、全target content fallbackが3 / 5、criterion外の語を混ぜた集合が2 / 5で発生した。

score `3`の1件は`audit_match_key`と`colSpan`を直接取得した一方、両箇所が参照する既存`hasAuditKey`定義を観測できず、同名定義を追加してlintを失敗させた。buildは未実行だった。

事前条件に従いCandidate134を`quality_gate_failed / mechanism_gate_failed / result_registered / stopped`とする。追加24件、F02、F07、Standard14へ進めない。詳細は[`F04 N=5 result`](../evaluations/results/candidate128-candidate134-syntactic-lexeme-continuation-v14-medium-f04-atomic-n5-cli0146_2026-08-02.md)を正本とする。

## 結論表

| 項目 | Candidate133 | Candidate134案 |
| --- | --- | --- |
| anchor集合 | 意味的にbind可能なobserved anchor | 文字形に一致する全TaskSpec lexeme |
| 空判定 | modelの意味分類を含む | 原文の構文だけで決まる |
| TaskSpec変更 | なし | なし |
| continuation回数 | 1回 | 1回、変更なし |
| 親 | C128 | C128 |
| Point 3〜6 | C128を維持 | C128を維持 |
