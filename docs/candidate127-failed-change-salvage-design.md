# Candidate127 failed-change salvage設計

## 結論

Candidate127はCandidate125を直接親とし、root `AGENTS.md`の`RECOVERY`だけを置換する。artifact変更が実際に失敗した後、失敗resultから不一致の変更単位を特定でき、変更未適用を確認でき、独立した必要変更が残る場合だけ、一回のmachine reworkでその必要変更を救済する`failed_change_salvage_ready`を一つの追加predicateとする。

Candidate126の`change_input_ready`は継承しない。最初のartifact変更前に全criterionや全change inputを再確認するgateは追加せず、初回成功経路を変えない。

## Identityと作成前gate

- candidate number: Candidate127
- prompt identity: `the-caption-3ce91a4-failed-change-salvage-r1`
- direct parent: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- changed target: root `AGENTS.md`
- changed rule: `RECOVERY`
- changed axis: failed artifact change salvage
- evaluation status: `not_evaluated`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 基準状態の最短正常経路

Candidate125のF04成功runは、`App.tsx`を終端まで取得し、`const hasAuditKey = true;`だけを`funds.some(...)`へ変更した。開始状態ですでに正しい`colSpan={hasAuditKey ? 7 : 6}`は変更せず、指定された`npm ci`、lint、buildを順に成功させた。

保存済みcompatible poolでは、F04の成功25件がこの必要変更だけを行いscore `4`だった。初回artifact変更が成功するこの経路はCandidate127で変更しない。

## 保存traceで確認した一つの誤経路

Candidate125の2026-08-01追加runでは、F04の5件がscore `2`になった。

- `fd0343d8198f433ea1377536b741980e`
- `24520644defc4c9bbd286ebe1220fa67`
- `aaea372253ff44e3a99e029b3f9df141`
- `1664ae1804354e14806eecb6bf904c67`
- `fd11349c90264ed29699065248723057`

5件すべてのmodel-visible continuation resultには、必要変更前の`const hasAuditKey = true;`と、開始状態ですでに正しい`colSpan={hasAuditKey ? 7 : 6}`が含まれていた。最初のatomic patchは、正しい`hasAuditKey`変更と、現在内容にない`colSpan={7}`または同等の不要hunkを混ぜたため全体が失敗した。

さらに5件すべてが、許可された一回のreworkでも`colSpan={6}`等の不要hunkを残した。二回目もatomic failureとなり、正当性が失われていない`hasAuditKey`変更、Node validation、最終成果がすべて未実施になった。

## C126と異なる問題設定

Candidate126は最初のartifact変更前に全変更単位のcurrent-content operandをexact bindする`change_input_ready`を追加した。F04初段N=5はstale hunk 0 / 5だったが、2件が開始状態ですでに充足したF04-C2の再確認を必要条件として読み、必要な`hasAuditKey`変更も行わず停止した。

Candidate127は初回patchの完全な防止を目的にしない。実際のfailure resultで不一致単位と変更未適用が確定した後だけ、失敗した単位を捨て、failure前から正当性が成立していた独立変更を救済する。よってC126が増やした変更前の停止判断を持たない。

## 追加する一つのpredicate

`failed_change_salvage_ready := artifact変更invocationがnon-success ∧ resultがtarget artifactへの変更未適用を示す ∧ failure resultから不一致の変更単位を特定可能 ∧ failure前に未充足criterion / target / current contentへbind済みで、不一致単位へ依存しない変更単位が一件以上残る`

`failed_change_salvage_ready=true`かつTaskSpecのmachine rework残数が一回以上の場合だけ、machine reworkを一回消費し、残った独立変更単位だけを次のartifact変更へ発行する。不一致単位、それへ依存する単位、failure前にcurrent contentへbindされていない単位は失効する。

salvageでは追加read、repository search、別target、別methodへの切替え、推測によるpreimage補完、失効単位の再構成を行わない。salvage変更が成功した場合は既存の`VALIDATION_PLAN`へ進む。false、部分適用が不明、独立変更が残らない、またはrework残数がない場合は既存TaskSpecの停止条件を維持する。

## 消す判断点と増える判断点

消す判断点は、artifact変更失敗後に、不一致が確定した変更単位を推測で書き換えて同じreworkへ残すかどうかである。

増える判断点は`failed_change_salvage_ready`のtrue / falseだけである。判定入力は実際のartifact変更resultとfailure前に受領済みのcontent evidenceに限定する。初回変更前のread、criterion再監査、change input監査、hunk数制限は増やさない。

## 非目標

- patch tool、atomic apply、executor、Codex CLI、adapter、runtime hookの変更
- 最初の誤patchを必ず防止すること
- machine rework上限を増やすこと
- failure後に追加evidenceを取得すること
- 正当に相互依存する複数変更単位を一部だけ適用すること
- Candidate126の`change_input_ready`を継承または微修正すること
- Candidate127の採用、release、本体投影

## Targeted evaluation gate

Candidate127だけを先に実行する。model、reasoning、CLI、runtime、permission、rating、fixture、TaskSpec、token accounting、executor条件はCandidate125 compatible条件へ固定し、prompt identityだけを変更する。profileの`max_workers`は`24`、初段はF04 `N=5`とする。

### F04 N=5

- quality: score `4`が5 / 5
- outcome: 必要な`hasAuditKey`変更が5 / 5
- preservation: `colSpan`変更が0 / 5
- recovery: 初回artifact変更が失敗したrunでは、最初のreworkで独立した必要変更を適用する
- recovery: 不一致または未bindの変更単位をreworkへ残さない
- evidence: artifact変更失敗後の追加readが0件
- validation: `npm ci`、lint、buildが5 / 5で成功

一件でもscore `3`以下、必要変更なし、`colSpan`変更、二回目のrework、failure後の追加read、required validation未実施があれば停止する。

F04 N=5を通過した場合だけ、F02 / F07を各N=5で実施し、正当に必要な複数変更単位をfailureなしの通常経路で抑止しないことを確認する。両caseを通過した場合だけStandard14 N=5へ進む。
