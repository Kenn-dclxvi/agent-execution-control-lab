# Candidate126 criterion-bound change input設計

## 結論

Candidate126はCandidate125を直接親とし、root `AGENTS.md`の`EVIDENCE_GATE`だけを置換する。artifact変更の各変更単位を、未充足の変更criterionと、直前に観測したcurrent contentへbindしてから発行する`change_input_ready`を一つの追加predicateとする。

patchのhunk数は制限しない。必要な複数hunkは許可し、開始状態ですでに充足済みのcriterionへ向けた変更単位と、観測していない現在値を一致条件にする変更単位だけを発行対象から除く。

## Identityと作成前gate

- candidate number: Candidate126
- prompt identity: `the-caption-3ce91a4-criterion-bound-change-input-r1`
- direct parent: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- changed target: root `AGENTS.md`
- changed axis: criterion-bound change input admission
- evaluation status: `not_evaluated`
- adoption: `not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 基準状態の最短正常経路

Candidate125のF04成功runは、`App.tsx`の必要範囲を終端まで取得し、未充足のF04-C1だけを次の変更へ変換した。

1. `const hasAuditKey = true;`を観測する。
2. `colSpan={hasAuditKey ? 7 : 6}`が開始状態ですでにF04-C2を満たすことを観測する。
3. `hasAuditKey`だけを`funds.some(...)`へ変更する。
4. 指定された`npm ci`、`npm run lint`、`npm run build`を順に実行する。

保存済みcompatible poolでは、F04の成功25件がこの必要変更だけを行いscore `4`だった。

## 保存traceで確認した一つの誤経路

2026-08-01のCandidate125 Standard14追加runでは、F04の5件が同じ誤経路でscore `2`になった。run IDは次のとおりである。

- `fd0343d8198f433ea1377536b741980e`
- `24520644defc4c9bbd286ebe1220fa67`
- `aaea372253ff44e3a99e029b3f9df141`
- `1664ae1804354e14806eecb6bf904c67`
- `fd11349c90264ed29699065248723057`

5件すべてで、model-visible resultには現在の`colSpan={hasAuditKey ? 7 : 6}`と`py-20`が含まれていた。しかし最初のatomic patchは、正しい`hasAuditKey` hunkと、現在内容に存在しない`colSpan={7}`および`py-24`を前提とする不要なhunkを一つにした。後者のpreimage不一致によりpatch全体が適用されず、retryでも観測値ではない`colSpan={6}`を推測して再失敗した。

その結果、5件すべてで許可pathの変更、`npm ci`、lint、buildが未実施になった。一次diagnosticはverification campaignの`batch-n030/quality-audit.json`とsealed execution evidenceに保持し、現在解釈は[`Candidate125 N=100追試停止結果`](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md)へ記録する。このpoolはcase別30件を登録済みだが、N=30のselection receiptと集約resultは未作成であるため、正式なN=30 resultとは扱わない。

## 既存入力だけでは防げない理由

TaskSpecはF04-C1とF04-C2を明示し、`App.tsx`だけを編集可能pathにしている。Candidate125の`EVIDENCE_GATE`は必要contentを終端まで取得し、実装判断へ進むところまで閉じる。しかし、artifact変更を構成する各単位が未充足criterionだけを扱うことと、変更operationが一致を要求するcurrent contentを観測値へbindすることは要求していない。

情報不足、fixture drift、executor failureではない。誤った2個目のhunkを発行する判断は、modelが変更前contentを受領した後のmodel-visibleな選択であり、prompt制御の対象である。atomic applyの全体失敗は結果を増幅したが、executorの変更を解決策にしない。

## 追加する一つのpredicate

`change_input_ready := artifact変更の各変更単位が未充足の変更criterionへbind済み ∧ current artifactとの一致をoperationが要求する全operandが最新のadmission済みcontent evidenceのexact valueへbind済み ∧ 開始状態ですでに充足済みのcriterionに変更単位がない`

ここで変更単位とは、一つのhunkに限定しない。patchでは削除行、context、置換前文字列など、適用時に現在内容との一致が必要な部分をcurrent-content operandとする。追加する新しい内容は開始状態に存在しないため、current-content operandには含めない。

`change_input_ready=true`の場合だけartifact変更を発行する。falseの場合は、受領済みevidenceだけから不要または未bindの変更単位を除いて再構成する。`change_input_ready=false`自体を追加readの開放条件にせず、既存`EVIDENCE_GATE`のadmission条件を維持する。

## 消す判断点と増える判断点

消す判断点は次の二つである。

1. 開始状態ですでに充足済みのcriterionも念のため変更するか。
2. 観測していない現在値を推測して変更operationの一致条件に使うか。

増える判断点は`change_input_ready`のtrue / falseだけである。criterionの充足状態とcurrent contentはTaskSpecと許可済みresultから直接観測できる。新しいrepository read、tool回数、hunk数、行数、token、時間閾値、case固有whitelistは追加しない。

## 非目標

- patch tool、atomic apply、executor、Codex CLI、adapter、runtime hookの変更
- hunkを常に一つへ制限すること
- 正当な複数fileまたは複数hunk変更の禁止
- model-invisibleなseed patch、oracle、graderによる変更内容の指定
- Candidate125の既存runをCandidate126の品質証拠として再利用すること
- Candidate126の採用、release、本体投影

## Targeted evaluation gate

Candidate固有gateはCandidate126だけを先に実行する。model、reasoning、CLI、runtime、permission、rating、fixture、TaskSpec、token accounting、executor条件はCandidate125 compatible条件へ固定し、prompt identityだけを変更する。profileの`max_workers`は`24`を維持する。

### F04 N=5

- quality: score `4`が5 / 5
- mechanism: 観測していないpreimageを含む変更単位が0 / 5
- mechanism: 開始状態で充足済みのF04-C2へ向けた変更単位が0 / 5
- mechanism: 未充足のF04-C1へbindした変更が最初のartifact変更operationで適用されるrunが5 / 5

### F02 / F07 N=5

- quality: 両caseともscore `4`が5 / 5
- preservation: 必要な複数変更単位をhunk数だけで抑止しない
- F02 preservation: Candidate125のexact-target content waveを5 / 5で維持する
- overhead: `change_input_ready`確認だけを理由に変更前evidence invocationを追加しない

F07は二つのrequired artifactを一貫して変更する`TC-F07-DEPENDENCY-PROVENANCE-PAIR`を使用する。

## 停止条件

次のいずれか一件でexpanded evaluationへ進まず停止する。

- score `3`以下
- 観測していないcurrent-content operandの発行
- 開始状態ですでに充足済みのcriterionへ向けた変更単位の発行
- 正当に必要な複数変更単位の抑止
- `change_input_ready`だけを理由にした追加read
- F02 exact-target content waveの回帰

targeted gateをすべて通過した場合だけStandard14 N=5を別段階で実施する。C125の中断済みN=50 partial batchはC126へ混ぜず、C125 poolの未完了execution provenanceとして保持する。
