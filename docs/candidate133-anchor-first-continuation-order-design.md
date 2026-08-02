# Candidate133 anchor-first continuation order設計

## 結論

Candidate133はCandidate128を直接親とし、`EVIDENCE_GATE`のcontinuation request predicateだけを置換する。Candidate131は停止済みの診断証拠として使い、継承しない。

変更軸は、未観測criterion全体にanchorが揃ったかを先に一括判定することではない。TaskSpecまたはadmission済みcontentに既に現れるexact anchor集合を、同じ一回のcontinuation resultの先頭scopeへ必ず置く。その後、anchorを持たない未観測criterionが残る場合だけ、同一targetの未取得contentを続ける。

## Identity

- candidate number: Candidate133
- prompt identity: `the-caption-3ce91a4-anchor-first-continuation-order-r1`
- direct parent: Candidate128 `the-caption-3ce91a4-required-effect-closure-r1`
- diagnostic predecessor: Candidate131。停止済みであり継承しない
- changed rule: `EVIDENCE_GATE`
- changed axis: anchor-first ordering inside the single continuation result
- unchanged: `SPEC`、`RECOVERY`、`VALIDATION_PLAN`、`METHOD`を含む他の全rule

## 作成前gate

### 最短正常経路

Candidate131 F04 N=29の28件は、TaskSpecまたは初回content中の`identifier / property / key / literal label`を使って同一target内の一致箇所と周辺contentを直接取得した。anchor語とcontext幅は複数あったが、全件が必要なcurrent contentを得て、一行変更と3 validationを完了した。

### 保存済み誤経路

run `e3907d1b47534d05aa19bb6721bf4374`は初回contentで`audit_match_key`と`const hasAuditKey = true;`を受領していた。それでもCandidate131の`criterion_anchor_ready`をtrue側へbindせず、`sed -n '261,$p'`で全残存contentへ直行した。配送切詰め後に`colSpan`を確認できず、変更0件、validation 0 / 3でscore `2`となった。

Candidate131 N=29のstaleまたは未観測preimageを持つ変更は0件だった。したがってPoint 5のchange constructionは変更しない。Candidate132の`change_preimage_ready`も継承しない。

## 置換する一つのpredicate

```text
observed_anchor_set :=
  TaskSpecまたはadmission済みcontentに既に現れ、
  同一targetの未観測criterionへbind可能な
  完全一致可能identifier / property名 / key / literal labelの集合

continuation_scope_complete :=
  一つのinvocationのresultで、
  observed_anchor_setが空でなければ最初に
  全memberの同一target内の全一致箇所と各周辺contentを直接返し、
  その後に限り、anchorを持たない未観測criterionが残る場合だけ
  同一targetの全未取得contentを終端まで返す
```

`observed_anchor_set`が空の場合はCandidate128の全未取得content fallbackを維持する。集合が空でない場合、全criterionがanchor-readyかという別の一括判断でdirect部分を失効させない。locator identityだけを独立resultにせず、direct部分とfallback部分を別invocationへ分割しない。

## 消す判断点と増える判断点

消す判断点は、exact anchorが一件以上model-visibleでも、全未観測criterionにanchorが揃ったかを先に再分類し、false側でanchorをすべて捨てる判断である。

新しいread、result round、continuation回数は増やさない。一回のcontinuation result内の順序だけを増やす。入力はTaskSpecと既に受領したcontentに限定し、synonym、未観測名、repository-wide searchをanchorへ加えない。

## 既存制御との分離

- Authority: Candidate116 / Candidate118由来の`SPEC`とauthority boundaryを維持する。
- Effect stateとClosure: Candidate128の`required_effects_closed`を維持する。
- Dependency: TaskSpec明示関係とrequired effect集合を維持する。
- Change construction: 新predicateを追加しない。
- report delivery: 変更しない。制御対象はmodel-visibleなrequest順序だけである。

executor、CLI、adapter、runtime hook、特定path、case名、固定command、固定context幅をpromptへ入れない。

## 初段F04 N=5 gate

model `gpt-5.6-sol`、reasoning `medium`、CLI `0.146.0`、Rating v14、M=24で、Candidate128とprompt以外の互換条件を機械照合してからCandidate133の不足5 runだけを発行する。

- valid / rateable: 5 / 5
- score `3`以下: 0 / 5
- 初回contentでobserved anchorが一件以上あるrun: direct anchor部分をcontinuation resultの先頭へ置く 5 / 5
- 全残存contentへ直接進む: 0 / 5
- locator-only独立result: 0 / 5
- staleまたは未観測preimageを持つ変更: 0 / 5
- 必要なartifact変更と3 validation完備: 5 / 5

一件でもscore `3`以下、anchor部分欠落、全残存contentへの直行、必要変更またはvalidation欠落があれば停止する。F02、F07、Standard14、追加24件、採用以降へ進めない。

N=5通過時だけ、同じpoolを追加24件でN=29へ拡張する。N=29でも同じ停止条件を適用する。

## 評価結果

F04 N=5は5 / 5件がscore `4`だったが、anchor-first continuationは4 / 5件だった。1件は変更前にanchor検索を行わず、`App.tsx`の全残存contentを二段階で取得した。変更・validation後の最終`rg`は変更前mechanismの証拠にしない。

事前条件に従い、現在状態を`quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とする。追加24件、F02、F07、Standard14へ進めない。詳細は[`F04 N=5 result`](../evaluations/results/candidate128-candidate133-anchor-first-continuation-order-v14-medium-f04-atomic-n5-cli0146_2026-08-01.md)を正本とする。

## 結論表

| 項目 | Candidate131 | Candidate133案 |
| --- | --- | --- |
| direct anchorの開放 | 全未観測criterionがanchor-ready | observed anchor集合が空でなければ必ず先頭 |
| anchorのないcriterion | 全体をfull fallbackへ切替え得る | anchor部分の後だけfull fallbackを同一resultへ続ける |
| continuation回数 | 1回 | 1回、変更なし |
| 親 | C128 | C128 |
| Point 3〜6 | C128を維持 | C128を維持 |
