# Candidate124 incomplete content continuation設計

## 結論

Candidate124はCandidate122を直接親とする。Candidate123は継承しない。Candidate122で成立したexact-target content waveとvalidation method境界を保持し、初回resultが「対象なし」ではなく「同じread可能targetの必要範囲が未観測」である場合だけ、同じtargetへの限定continuationを一度許可する。

変更predicateは複数条件を持つが、変更軸は`incomplete content continuation`一つである。一般的な追加調査を再開する制御ではない。

## Identityと状態

- candidate number: Candidate124
- prompt identity: `the-caption-3ce91a4-incomplete-content-continuation-r1`
- direct parent: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`
- changed target: root `AGENTS.md`
- changed axis: incomplete contentとterminal absenceの分類、および同一target限定continuation
- evaluation status: `targeted_a01_a02_f01_f02_f04_evaluated / quality_gate_failed / stopped`
- release: `not_created`
- runtime projection: `not_projected`

## 保存traceで確認した誤経路

根拠の正本は[`Candidate122 Standard14 result`](../evaluations/results/candidate118-candidate122-prechange-evidence-wave-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)とする。

1. F04失敗run `996248c6c2e54f259281a4804ac278fa`は`App.tsx`を正常にreadした。
2. 初回取得範囲1〜320行には、TaskSpecが要求した表描画と`colSpan`が含まれなかった。
3. C122は追加の変更前evidenceを禁止したため、取得範囲不足を`missing`と同じterminal dispositionにした。
4. artifact変更と3つのrequired validationを実行せず、score `2`となった。
5. C122のF04成功4件中3件とC107のF04成功5件は、必要な場合に同じtargetの後続rangeまたはsymbol周辺だけを補足してscore `4`だった。

既存TaskSpecと最初のresultだけでは、未観測criterionがtarget不存在なのか取得範囲外なのかをC122の二分岐で表現できない。この不足がfalse stopを生んだ。

## 置換する制御

`prechange_wave_complete := admission済みtargetの取得がsuccess ∧ 変更predicateと保持constraintに必要なTaskSpec criterionがresult内で観測済み`

`bounded_content_continuation_ready := prechange_evidence_wave_ready ∧ prechange_wave_complete=false ∧ targetの存在とread可能性が初回resultで確認済み ∧ 未観測criterionがTaskSpecから特定済み ∧ そのcriterionを同じtargetの未取得rangeまたはsymbol locatorへ一意にbind可能 ∧ continuation未発行`

`bounded_content_continuation_ready=true`の場合だけ、同じtargetの未取得rangeまたは未観測symbol周辺へcontinuation evidenceを一件許可する。continuationは未観測criterionだけを返す。新しいtarget、repository-wide search、一般的安全確認、implementation method探索を開かない。

continuation resultを受領した後は、変更predicateと保持constraintをbindしてartifact変更へ進むか、具体的な`missing / unreadable / contradiction / unsatisfied constraint`で停止する。二回目のcontinuationは許可しない。

初回resultですでにtargetの不存在、read不能、bind済みconstraintとの矛盾、allowed path内での充足不能を観測した場合は、C122どおり停止する。単なる範囲不足をこれらへ読み替えない。

## 変更により消す判断点と増える判断点

消す判断点は、「必要criterionが初回resultにない」という事実だけでtargetをterminal missingにする判断である。

増える判断点は一つである。初回result後に、`targetはread可能だがcriterionだけが未観測`か、`targetまたはconstraintが実際にterminal disposition`かを判定する。

## 初回targeted gate

初回評価はA01 r2 / A02 r2 / F01 r3 / F02 r1 / F04 r2各`N=5`、Rating v14、`gpt-5.6-sol` Medium、CLI `0.146.0`、profile上の`M=24`へ固定する。A01 / A02 / F01 / F02はC122で成立した経路の保持確認、F04は修正対象の確認である。

- execution: `25 / 25 valid`
- quality: score `4` × 25
- F04: false stop 0 / 5
- F04: 初回bounded contentでcriterion未観測のrunは、同じ`App.tsx`への限定continuationがちょうど1回、または初回resultだけで変更predicateを正しくbind
- F04: artifact変更と`npm ci` / `npm run lint` / `npm run build`のrequired evidence完備5 / 5
- F02: exact target set content wave 5 / 5
- F02: content後の一般追加read 0 / 5
- F02: token中央値`173,000`以下
- A01: required value待ち5 / 5、artifact変更・test 0 / 5
- A02: canonical成果5 / 5、変更後validation method探索0 / 5
- F01: required command evidence完備5 / 5

品質または対象mechanismが一件でも崩れた場合は停止する。全gate通過時だけ、保存済みatomic runを再利用してStandard14の不足caseを実行するかを別判断する。

## 期待と逆の結果になった場合の停止条件

- read可能targetの範囲不足を再びterminal missingとする
- continuationを二回以上発行する
- continuationで新しいtargetまたは一般探索を開く
- F02のcontent waveまたはcost targetを崩す
- A01 / A02 / F01の既存品質・mechanismを崩す
- 25件中一件でもscore `4`未満

## 非目標

- read回数、file数、bytesの一般上限または一般下限
- unknown targetの推測
- repository-wide searchの許可
- Candidate123のpreterminal result round制御の修正または継承
- executor、Codex CLI、tool adapter、runtime hook、外部wrapperの変更
- 採用、release、runtime projection、THE-CAPTION本体反映

## 評価結果

[`Rating v14 Medium A01 / A02 / F01 / F02 / F04各N=5`](../evaluations/results/candidate122-candidate124-incomplete-content-continuation-v14-medium-a01-a02-f01-f02-f04-atomic-n5-cli0146_2026-07-31.md)は25 / 25 valid、score `4 / 2 = 23 / 2`だった。F04の2件は一度のcontinuationを620行で終え、未観測criterionをなお取得できず停止した。F02も追加content readが2 / 5件へ再発し、token中央値`188,908`で目標を超えた。事前停止条件に従いCandidate124を`stopped`とし、Standard14へ進めない。
