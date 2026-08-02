# Candidate131 criterion anchor continuation設計

## 結論

Candidate131はCandidate128を直接親とし、`EVIDENCE_GATE`のcontinuation request predicateだけを置換する。各未観測criterionに、TaskSpecまたはadmission済みcontentで直接観測した完全一致可能なanchorがある場合は、その全anchorの全一致箇所と周辺contentを一つのinvocationで直接返す。anchorがないcriterionが残る場合だけ、同一targetの全未取得contentを終端まで要求する。

ここでanchorとは、検索位置だけを返すlocatorではない。identifier、property名、key、literal labelのように、既にmodel-visibleで、同一target内のcontentへ完全一致できる語である。synonymや未観測名を推測して追加しない。

## Identity

- prompt identity: `the-caption-3ce91a4-criterion-anchor-continuation-r1`
- direct parent: `the-caption-3ce91a4-required-effect-closure-r1`（Candidate128）
- diagnostic predecessor: Candidate130。停止済みであり継承しない
- changed rule: `EVIDENCE_GATE`
- changed axis: criterion anchorからdirect content requestへのbind
- unchanged: `SPEC`、`OWNER_ROLE`、`RECOVERY`、`VALIDATION_PLAN`、`METHOD`を含む他の全rule

## 作成前gate

### 基準prompt setと最短正常経路

基準はCandidate128である。一つのeditable targetが全未解決criterionを所有し、初回contentで必要箇所が未観測なら、同targetへの一回のcriterion-complete continuationを許可する。必要contentを受領したら未充足effectだけを変更し、Candidate128のrequired-effect closureとvalidationへ進む。

### 保存traceで確認した誤経路

Candidate130 F04 N=5は5件すべてが初回resultで`hasAuditKey = true`と`audit_match_key`を観測し、TaskSpecでは`colSpan`もmodel-visibleだった。それでも5 / 5件が`sed -n '261,$p'`で全未取得contentを選び、focused取得は0 / 5だった。3件はcontinuation deliveryの切詰め後に変更とrequired validationを開始せず、score `1`になった。

Candidate107の同case成功traceでは、3 / 5件が`hasAuditKey / Audit Key / colSpan`の全一致箇所と周辺contentを一回で直接取得した。5 / 5件がscore `4`だった。この保存差から、直接観測済み語を具体的なrequest scopeへbindする経路が実行可能だと確認した。

### 既存制御との重複

- Candidate121: locator identityを独立resultにしてからcontentを取得した。decision roundとcostが増えたため戻さない。
- Candidate124: continuationを一回へ制限したが、bounded rangeがcriterionを覆わず2 / 5件で停止した。
- Candidate125 / Candidate128: criterion-complete fallbackを保持する。anchorがない場合は全未取得contentを終端まで取得できる。
- Candidate130: `symbol identity`がidentifier以外のproperty名やliteral labelを確実に含まず、具体的なanchor集合とrequest identityの接続もなかった。Candidate131はこのpredicateを置換し、並置しない。
- report deliveryの切詰め自体はpromptで制御しない。Candidate131が制御するのは、model-visibleな選択であるrequest scopeだけである。
- effect state、change admission、failed-change recovery、required-effect closureはPoint 3以降または既存controlの責務であり、この変更軸へ混ぜない。

## 置換するpredicate

```text
criterion_anchor_ready :=
  各未観測criterionに対し、
  TaskSpecまたはadmission済みcontentで直接観測した
  完全一致可能なidentifier / property名 / key / literal labelが一つ以上あり、
  そのcriterionと同一targetへbind済み

continuation_scope_complete :=
  criterion_anchor_ready=trueなら、
  全anchorの同一target内の全一致箇所と各周辺contentを
  一つのinvocationで直接返す
  OR
  criterion_anchor_ready=falseの場合に限り、
  同一targetの全未取得contentを終端まで覆う
```

anchorのlocator identityだけを独立resultとして返さない。完全一致が複数ある場合は一箇所へ絞らず、同一target内の全一致箇所を取得する。

## 消す判断点と増える判断点

消す判断点は、検索に使える語を受領済みでも、それをprogram symbolと分類できるかを再判断し、具体化済みの全未取得contentへ流れる分岐である。

増える判断点は`criterion_anchor_ready`のtrue / falseだけである。入力はTaskSpecと受領済みcontentへ限定する。repository-wide search、別target、二回目のcontinuation、locator-only round、case固有pathや固定commandは追加しない。

## 非目標

- executor、CLI、adapter、runtime hook、report deliveryの変更
- F04固有のpath、名前、commandをpromptへ入れること
- Candidate130の継承
- effect state、変更単位、recovery、validation controlの同時変更
- N=5だけによる採用、release、runtime projection

## 初段評価gate

初段はF04 r2だけをN=5、model `gpt-5.6-sol`、reasoning `medium`、CLI `0.146.0`、Rating v14、`M=24`で実行する。Candidate128 / Candidate130とprompt以外のatomic compatibility条件を機械照合してから不足5 runだけを発行する。

通過条件は全て満たすこととする。

- valid / rateable: 5 / 5
- score `3`以下: 0 / 5
- criterion anchorから全一致箇所の周辺contentを一回で直接取得: 5 / 5
- 全未取得content fallback: 0 / 5
- locator-only独立result: 0 / 5
- required artifact、`npm ci`、lint、build完備: 5 / 5

一件でもscore `3`以下、全未取得content fallback、locator-only独立result、必要変更またはrequired validation欠落があれば停止する。F02、F07、Standard14、採用、release、本体反映へ進めない。

## 評価結果

後続の[`F04 N=5`](../evaluations/results/candidate128-candidate131-criterion-anchor-continuation-v14-medium-f04-atomic-n5-cli0146_2026-08-01.md)は5 / 5件がscore `4`だった。direct anchor contentは5 / 5、全未取得content fallback、locator-only独立result、false stopは各0 / 5で、Point 2の初段N=5 gateを通過した。iteration 1で観測した共通上流変更と下流3式変更の差はdependency / change construction監査へ分離する。

後続の[`F04 N=29 stability`](../evaluations/results/candidate131-criterion-anchor-continuation-v14-medium-f04-atomic-reuse-n29-cli0146_2026-08-01.md)は既存5件を再利用し、追加24件でscore `4 / 2 = 23 / 1`、合計`28 / 1`となった。1件がexact anchorを受領済みでも全残存content fallbackを選び、配送切詰め後に変更とvalidationを開始しなかった。stale preimageは0 / 29だったが、Point 2 stability gate不通過のためCandidate131を停止する。
