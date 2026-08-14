# Candidate224 review source exclusive authority 設計

## 状態

- `creation_gate_fixed`
- `candidate_created_and_evaluated`
- `quality_failed_mechanism_failed_stopped`
- direct base: `Candidate147`
- evaluation input: `ADR9 r2 unchanged`

## 目的

必要な独立reviewを完遂しながら、review開始前にrootが複数recipient用valueを含むsource全体を受領する経路と、reviewerがpacketで受領済みの値をsourceから再取得する経路を同時に閉じる。

試験のfield、期待terminal、成功runのtool順またはcase別read集合から制御を組み立てない。先に一般的なreview operationのowner、carrier、read permissionおよびobservable outputを固定し、変更していないADR9 r2は後続の観測にだけ使う。

## C214から保持する境界

Candidate214から保持するのは本文ではなく、次の局所境界である。

- packetへ実際に配送したsource valueへreviewerが別selector、部分抽出または別commandで再到達できない。
- packet sourceと重ならない別containerの必要観測を一律に閉じない。
- rootはreviewerのjudgementまたはterminal resultを補完しない。

Candidate214のcontainer全体閉鎖は、同じcontainer内にあるpacket非配送の必要値まで遮断したため保持しない。後続監査で判明したroot初回whole-source deliveryも成立済み境界として扱わない。

## 閉じるpermission edge

従来は、一般の`EVIDENCE_GATE`が`target artifact`またはimplementation choiceのためのsource readをrootへ許可し、その上へreview専用のview条件を追加していた。このため、review source全体を一般repository evidence operationへ含める経路が残った。

Candidate224では、pre-review sourceを一般repository evidence operationの対象から除外する。review terminal前のsource accessは、次の二operationだけに限定する。

```text
root packet projection operation
  -> rootが受領できるのはTaskSpecがpacket配送を直接許可した有限projectionだけ

reviewer observation operation
  -> bind済みreview producerだけがfinite manifestのexact targetを直接受領する
```

source container、ancestor、複数recipient用valueを含む共同output、target artifactという一般名および将来の変更・validationは、どちらのoperationにもsource全体を追加するauthorityを与えない。

## prompt-only carrier

promptが新しいtask valueやcase別対応表を作るのではない。TaskSpecがすでに固定した二つの有限集合を、source readより前にresult recipientへbindする。

- `root_packet_projection`: reviewer packetへliteral配送を直接許可されたvalue projectionと、そのprovenance、review applicability、required scopeおよびmanifest descriptor。
- `reviewer_observation_targets`: finite evidence manifestのexact targetのうち、root projectionと同一、祖先、子孫または重複しないtarget。

root projectionはsource containerを入力として扱う実装であっても、observable outputが上記projectionだけに閉じる場合に限り許可する。source全体または除外対象を含むoutputを受領してから選別する経路は許可しない。

reviewer observationは一つのexact targetと一つのreviewer recipientへbindする。rootはそのtool resultを受領せず、reviewerはroot projectionと重なるtargetをsourceから再取得しない。finite manifestのtarget帰属を将来の必要性、owner宣言、ticketまたは読後分類で変更しない。

## 正常経路

1. rootはreview applicabilityとpacketに許可された有限projectionだけを受領する。
2. review不要ならreview operationを作らない。permission deniedならreviewerとartifact変更を発行せず`unavailable`にする。
3. reviewが必要で許可されている場合、rootは受領済みprojectionだけからpacketを構築する。
4. 独立reviewerはpacketと、同producerだけへ許可されたmanifest exact observationからterminal resultを返す。
5. admissible `no_counterexample_found`だけが対応するartifact変更を開く。`counterexample_found`と`unavailable`は対応変更だけを停止する。

これは成功runの実行順を義務化するものではない。各repository evidence invocationの前に、operation identity、producer、result recipient、exact output境界および重複禁止が固定されていることを要求するdependency構造である。

## Candidate作成前gate

1. 目的は必要reviewの完遂であり、Scoreや試験通過ではない。
2. Candidate147をdirect baseとし、Candidate214からCandidate223までの本文を親にしない。
3. pre-review sourceを一般`EVIDENCE_GATE`の`target artifact`権限から除外する。
4. root whole-source output、mixed-recipient output、reviewer-owned value outputおよび受領後の選別を許可するoperation classを残さない。
5. reviewerはroot projectionと重なるsource region、container全体、ancestorまたはmanifest外targetを取得できない。
6. packet非配送でmanifestに固定されたexact targetは、同じcontainerであることだけを理由に遮断しない。
7. ownerとrecipientの割当てを必要性、期待result、ticket、自己申告またはsource読取後の分類で変更しない。
8. root projectionまたはreviewer targetをsource read前に有限・排他的に固定できなければpermissionを広げず`unavailable`にする。
9. case identity、fixture field、selector、tool、read回数または期待terminalをCandidate本文へ埋め込まない。
10. TaskSpec、case、fixture、oracle、rating、runtime、permissionおよびexecutor条件を変更しない。

上の全件を満たすため、Candidate147の一般`EVIDENCE_GATE`へpre-review sourceの専用authority優先を組み込み、`PRECHANGE_REVIEW`と`REVIEW_SOURCE_EXCLUSIVE`を追加するCandidate作成を許可する。

## 停止条件

変更していないADR9 r2で、必要review欠落、root whole-source delivery、root reviewer-owned value delivery、reviewerによるroot projection再取得、whole-source read、manifest外read、result admission不一致またはresult effect不一致が一件でもあれば停止する。

試験結果に合わせてTaskSpec、case、fixture、oracleまたはCandidate本文を修正再実行しない。

## 非目標

- TaskSpecまたは評価入力へのcarrier追加
- case別scope-to-observation対応表
- runtime、tool adapter、executorまたはwrapperの変更
- 採用、releaseまたはprojection

## 動的結果

変更していないADR9 r2の45件では、必要reviewerは30 / 30で起動したが、必要なreview判断は28 / 30だった。root mixed-owner admissionはpacket case 20 / 20、reviewer direct observationは9 / 20であり、この設計が想定した排他的source authorityは成立しなかった。

同じcontainerからroot packet literalとreviewer observationを取得するr2の構造では、promptでprojectionを宣言してもrootのwhole-output能力を閉じられない。C214のcontainer閉鎖を弱めず正常carrierを開くには入力またはruntime側の排他的carrierが必要だが、今回の許可範囲には含まれない。次Candidateを作成せず未解決として保持する。

- [Candidate224 ADR9 r2 N=5結果](../evaluations/results/candidate224-review-source-exclusive-authority-adr9-r2-n5_2026-08-14.md)
