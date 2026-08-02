# Candidate132 observed preimage change construction設計

## 結論

Candidate132はCandidate131を直接親とし、`EVIDENCE_GATE`へ`change_preimage_ready`だけを追加する。artifact変更operationがcurrent contentとの一致を要求する削除行、置換前文字列、contextを、変更箇所について最新のadmission済みcontentに実在するexact valueへbindしてから変更を発行する。

C126の`change_input_ready`は継承しない。全criterionの充足状態を変更前に完全再監査する条件と、発行予定patchのpreimage確認を分離する。未bind operandを持つ変更単位だけを除き、独立してreadyな変更単位は止めない。

## Identity

- prompt identity: `the-caption-3ce91a4-observed-preimage-change-construction-r1`
- direct parent: Candidate131 `the-caption-3ce91a4-criterion-anchor-continuation-r1`
- diagnostic predecessor: Candidate126。停止済みであり継承しない
- changed rule: `EVIDENCE_GATE`
- changed axis: observed preimage change construction
- unchanged: Candidate131のcriterion anchor coverage、Candidate128の`RECOVERY`、他の全rule

## 作成前gate

### 最短正常経路

Candidate131 F04 N=5は5 / 5件でcriterion anchorの周辺contentを直接取得し、全件score `4`だった。発行する変更が一行でも複数式でも、変更箇所の現在値を受領済みcontentから使い、required validationへ進む。

### 保存済み誤経路

Candidate125 compatible poolのF04 5件は、正しい`hasAuditKey`変更と、現在内容に存在しない`colSpan={7}`、`py-24`を前提とする変更単位を同一patchへ入れた。stale preimageによりpatch全体が失敗し、score `2`になった。

Candidate126は`change_input_ready`によりstale operandと`colSpan`変更を0 / 5へ抑えた。しかしF04 N=5の2件、先行発行N=20全体の8件で、全criterionを再確認できないことを理由に必要な`hasAuditKey`変更も止めた。少なくとも5件はcontinuation deliveryの切詰めを停止理由にした。

Candidate131は同じF04でdirect anchor content 5 / 5、全未取得content fallback 0 / 5を成立させた。したがってPoint 5では、coverageを再変更せず、発行予定operationのpreimageだけを対象にする。

## Predicate

```text
change_preimage_ready :=
  発行予定artifact変更operationがcurrent artifactとの一致を要求する
  削除行 / 置換前文字列 / contextの全operandが、
  そのoperationで変更する箇所について
  最新のadmission済みcontent evidenceに現れるexact valueへbind済み
```

追加予定の新しいcontentはpreimageではない。falseの場合は、受領済みevidenceだけから未bind operandを要求する変更単位だけを除いて再構成する。false自体を追加read、全criterion再監査、artifact変更全体の停止条件にしない。

## 既存制御との分離

- Point 2 Evidence coverage: Candidate131の`criterion_anchor_ready`
- Point 3 Effect state: Candidate128の`required_effects_closed`
- Point 4 Dependency: 新predicate不要。TaskSpecとeffect closureを維持
- Point 5 Change construction: Candidate132の`change_preimage_ready`
- Point 6 Closure / recovery: Candidate128の`RECOVERY`

patch tool、atomic apply、executor、CLI、adapter、runtime hookは変更しない。hunk数、特定path、case名、固定commandをpromptへ入れない。

## F04 N=5 gate

model `gpt-5.6-sol`、reasoning `medium`、CLI `0.146.0`、Rating v14、M=24で、Candidate131とprompt以外の互換条件を機械照合してから不足5 runだけを発行する。

- valid / rateable: 5 / 5
- score `3`以下: 0 / 5
- direct anchor content: 5 / 5
- staleまたは未観測preimageを持つ変更単位: 0 / 5
- required artifact変更と3 validation完備: 5 / 5
- `change_preimage_ready=false`だけを理由にした追加readまたはfalse stop: 0 / 5

一件でもscore `3`以下、stale preimage、必要変更抑止、validation欠落があれば停止する。F02、F07、Standard14、採用、release、本体反映へ進めない。

## 評価結果

F04 N=5はscore `4 / 2 = 4 / 1`となり、事前条件に従って停止した。staleまたは未観測preimageを持つ変更は0 / 5で、必要な`hasAuditKey`変更は5 / 5だった。一方、1件が全残存contentを取得して配送切詰めに遭い、正しい一行変更後も未観測の`colSpan` effectを未充足と判定して3 validationを開始しなかった。

`change_preimage_ready`はstale変更抑止には成功したが、Candidate131のdirect anchor routeを5 / 5から4 / 5へ悪化させ、false stopを1 / 5へ再発させた。現在状態は`quality_gate_failed / result_registered / stopped`である。詳細は[`F04 N=5 result`](../evaluations/results/candidate131-candidate132-observed-preimage-change-construction-v14-medium-f04-atomic-n5-cli0146_2026-08-01.md)を正本とする。
