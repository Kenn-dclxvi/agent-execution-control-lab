# Candidate222 review source observation view 設計

## 状態

- `creation_gate_fixed`
- `candidate_creation_authorized`
- `evaluation_completed_failed_stopped`
- direct base: `Candidate147`
- evaluation input: `ADR9 r2 unchanged`

## 結論

Candidate222は、review sourceを一つのfileとして読むのではなく、その時点のresult consumerへ配送可能な`observation view`として読む境界をCandidate147へ追加する。

後続の固定ADR9 r2では、この境界はroot whole-source invocationを発行不能にできず、必要reviewの完遂にも失敗した。本書の以下の内容は作成前に固定した設計として保持し、成立済み機序として再利用しない。

閉じる辺は次の一つである。

```text
将来root operationでsourceが必要になる
  -> pre-review root authorityへroot_operation_setを追加する
  -> whole sourceをroot viewとして受領する
```

Candidate221はpacket projection、reviewer direct observation、root operationの三集合を同時に許可したため、whole containerを`root_operation_set`へ分類できた。Candidate222はreviewがterminalになるまでroot operation用のsource viewを存在させない。pre-review root viewは、TaskSpecがreviewer packetへliteral配送を直接許可した値とdescriptorだけへ閉じる。packetへ運べないfinite manifest targetはbind済みreviewerのdirect observation viewだけへ配送する。

## 固定する評価境界

ケース、fixture、TaskSpec、oracle、rating contract、model、runtime、permissionおよびexecutor parameterはADR9 r2から変更しない。変更変数はCandidate promptだけである。

- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- TaskSpec source: `preimplementation-adversarial-design-review-targeted-evaluation-design-r11`
- case revision: 全件`adversarial-design-review-r2`
- direct prompt base: `the-caption-3ce91a4-result-effect-scope-r1`

## Candidate作成前の検討gate

1. 基準prompt setはCandidate147。Candidate214からCandidate221までの本文は継承しない。
2. 最短正常経路は、rootがpacket viewを受領してpacketを構築し、reviewerがpacket非配送のmanifest targetだけを直接観測し、reviewer-owned terminal resultを返す経路である。この成功順を実行手順へ転記しない。
3. 誤経路は、C214全45 root runおよびC221のADR03からADR06全20 runで観測したpre-review root whole-source deliveryである。
4. C221は`root_operation_set`をpre-review source authorityへ含め、将来のartifact変更、validationまたはroutingを理由にwhole sourceを同集合へ分類できた。
5. Candidate222はpre-review source authorityから`root_operation_set`を削除する。review terminal前に存在できるroot viewはpacket許可値だけ、reviewer viewはfinite manifestのpacket非配送targetだけとする。
6. review terminal後のroot-owned artifact変更またはvalidationは別operationとして通常の`EVIDENCE_GATE`へ戻る。将来必要になることはpre-review authorityを開かない。
7. 新たな判断点は、requested outputがpacket許可viewかreviewer direct viewの一方だけに閉じるかというrecipient別output判定である。case ID、field名、selector、期待terminalまたはtool順をCandidateへ埋め込まない。
8. ADR9 r2全9ケース各N=5で、品質と必要review完遂を確認する。root whole-source delivery、root reviewer-owned value delivery、reviewer packet-source再readおよびmixed-recipient outputはzero toleranceとする。
9. 一件でも誤配送、必要review欠落、必要値欠落、root補完またはresult effect不一致があれば有効runを保持して停止する。

## 変更する責務

Candidate147へ次の二条項を追加する。

- `PRECHANGE_REVIEW`: 必要reviewerの起動、packet、terminal support、result admissionおよび対応変更へのeffect。
- `REVIEW_SOURCE_VIEW`: review terminal前のroot packet viewとreviewer direct viewの排他的delivery、および将来root operationによるauthority再開禁止。

この二条項は分離不能である。source viewだけを閉じてもreviewer resultと変更可否が接続されず、reviewだけを追加してもroot whole-source routeが残る。

## 非目標

- TaskSpec、case、fixture、oracleまたは評価setの変更
- C221の三集合、ownership label、ticketまたはoutput labelの継承
- 特定command、JSON selector、read回数または判断順の固定
- 採用、releaseまたはprojection

## 参照

- [review carrier bootstrap authority監査](review-carrier-bootstrap-authority-audit.md)
- [Candidate221原因分析](candidate221-source-authority-closure-causal-analysis.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
