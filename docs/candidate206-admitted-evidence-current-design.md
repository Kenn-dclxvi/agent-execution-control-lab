# Candidate206 admitted evidence current設計

## 結論

Candidate206はCandidate175を比較用の直接親とし、model-visible inputまたはadmission済みterminal resultに既に含まれるevidence identityを、失効するまで再利用する一関係だけを追加する。

Candidate175はADR9とStandard14の品質・機序gateを通過済みであるため、この変更の品質、機序、token、elapsedを二段階で比較できる。これはCandidate175の採用、release、projectionを意味せず、Candidate147の完成形や系譜を置き換えるものでもない。Candidate176以降の失敗系譜の機構は継承しない。

## Identity

- candidate number: Candidate206
- prompt identity: `the-caption-3ce91a4-admitted-evidence-current-r1`
- comparison direct parent: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- changed target: root `AGENTS.md`
- changed clause: `EVIDENCE_GATE`
- changed axis: `admitted_evidence_current`
- initial status: `design_ready / not_implemented / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. 比較元はCandidate175の固定bundle `251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`とする。
2. 最短正常経路は、開始inputに既に含まれるroot instructionをcurrent evidenceとして再利用し、対象pathへだけ適用される局所instruction、target artifact、固定diff、changed contentなど未観測のidentityだけを取得する経路である。
3. Candidate147 Standard14 N=100のF10 monthlyではroot `AGENTS.md`を99 / 100件が再取得した一方、再取得しなかったiteration 88もScore 4で同じmajor findingとzero driftを成立させた。99件のtoken中央値は93,597、elapsed中央値は56.639秒、非再取得1件は93,948、48.684秒だった。単独runとのKPI差は因果値に使わないが、再取得が品質成立の必要条件ではない反例になる。
4. C147由来の`EVIDENCE_GATE`は、permissionまたはallowed readを発行条件にしない。しかしmodel-visible inputまたは受領済みresultをcurrent evidenceへ移し、どの結果まで再利用するかという正の関係を固定していない。そのため、許可されたroot authorityを未観測として再取得する解釈が残る。
5. 追加する判断点は、evidence identityが現在利用可能か、そのidentityを変えるadmission済みresultがあるかの二点である。read対象の必要性、authority、permission、predicate、consumer、review要否、validation methodは変更しない。
6. path-local instructionが開始inputへ含まれない場合、target contentが未観測の場合、またはadmission済みresultが同じidentityの値を変えた場合は取得を保持する。allowed readへ列挙されただけのidentityをcurrentとは扱わない。
7. ADR9は9ケース各5件、45件すべてScore 4、Candidate175のrequired review起動、不要review 0、禁止情報配送0、未admit変更0を通過条件とする。一件でも不通過または計測不能なら停止し、Standard14を発行しない。
8. ADR9通過後だけStandard14を14ケース各5件、70件実行する。70件すべてScore 4、model-visibleで失効していないroot instructionの再取得0、必要なpath-local instruction取得の欠落0、validation・review機序の悪化0を通過条件とする。
9. KPIは保存済みCandidate175と同一条件でtokenとelapsedを比較する。品質・機序が同等以上でなければ、cost差にかかわらず採用候補にしない。品質・機序が同等でcost改善がなければ、過剰品質または無効な追加として停止する。

## 追加する関係

```text
admitted_evidence_current(evidence_identity) :=
  model-visible inputまたはadmission済みterminal resultが
    evidence_identityをrequired predicateへbind済み
  ∧ そのidentityの値を変えるadmission済みresultが未受領
```

`admitted_evidence_current=true`のidentityは、同じrequired predicateのconsumerへ再利用し、`unobserved`へ戻さず、同じidentityを取得するrepository evidence invocationを発行しない。

この関係は「rootを読まない」という対象名依存の禁止ではない。model-visible inputに含まれるroot instructionにも、先行terminal resultが返した固定diffにも同じく適用する。入力にないpath-local instructionはcurrentにならず、値を変えるadmission済みresultを受けたidentityは失効する。

## 既存制御との境界

- `EVIDENCE_GATE`のdefault deny、consumer readiness、追加evidenceの開放条件、`implementation_bound`を保持する。
- `SPEC`、`PRODUCER`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`DECISION_BOUNDARY`、`DESIGN_ADMISSION`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`を逐語的に保持する。
- Candidate175のreview operation admission、producer binding、semantic projectionを変更しない。
- Candidate176以降のcounterexample、terminal proof、structured review、projection closureその他の機構を持ち込まない。
- evidence identityをcurrentと判定することはrequired predicateの` satisfied`判定ではない。現在利用できる観測値の再利用だけを決める。

## 変更前反例監査

次を一件でも満たせない場合はbundleを作成しない。

1. model-visible root instructionを再取得対象から除外できる。
2. 開始inputにない`src/AGENTS.md`または`tests/AGENTS.md`は取得可能なままである。
3. target artifact、fixed diff、changed contentが未観測なら取得できる。
4. admission済みresultがidentityの値を変えた場合は再観測できる。
5. permissionまたはallowed readだけではcurrentにならない。
6. current evidenceをrequired predicateの成功と誤認しない。
7. review operation、validation ticket、producer bindingへ新たな順序や起動条件を加えない。
8. case ID、fixture名、対象path名または期待terminalによる分岐を含まない。

この監査を満たす実装差分が`EVIDENCE_GATE`一節だけに閉じる場合に限りCandidate206を作成する。

## 非目標

- C147、C175または他Candidateの採用再判断
- review制御の再構成
- start gate barrier、validation reentry、false-unavailable rerunの同時変更
- 評価case、oracle、rating contract、model、reasoning、CLI、permission、parallelismの変更
- executor、tool adapter、runtime hookまたは外部wrapperの変更
- releaseまたはTHE-CAPTION本体へのprojection
