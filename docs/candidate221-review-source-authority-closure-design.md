# Candidate221 review source authority closure 設計

## 状態

- `creation_gate_fixed`
- `candidate_created`
- `evaluation_not_started`
- direct base: `Candidate147`

## 結論

Candidate221は、Candidate214で閉じたpacket投影元の再readとrootによるreviewer-owned値の先行観測を維持しながら、rootがreviewer packetを構築する権限と、reviewerが未投影のcurrent valueを直接観測する権限を、TaskSpecが発行前に固定した構造targetへ分離する。

閉じる辺は次の一つである。

```text
model-visible / read allowed / target artifact
  -> rootがreview用container全体を取得
  -> packet配送禁止のreviewer observation valueもrootへ配送
```

rootはTaskSpecがpacket配送を直接許可したtargetとroot-owned変更・検証targetだけをexact regionとして読める。finite evidence manifestが独立review producerの直接観測targetへ固定し、packet配送を許可していないregionはreviewerだけが読める。whole container、owner混在region、ownerまたはcarrierが一意でないtargetは発行しない。

## 直接baseと反証入力

直接baseはCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`とする。Candidate214からCandidate220までの本文は継承しない。

- Candidate214はpacket投影元再readを6回から0回、root先読みを1件から0件へ減らしたが、container全体を閉じて4件を`unavailable`にした。
- Candidate215は非重複regionを開いたが、packet投影時のregion固定をmodel判断へ残し、必要・不要readが揺れた。
- Candidate220はobservable output closureを宣言しても、root whole-container resultがADR03からADR06の20 / 20に残った。

これらは成功時のread順を示す親ではなく、権限辺と過剰遮断の反証である。

## 一次入力で固定したownerとcarrier

ADR9 r2全9ケースのTaskSpecは、`design-admission.json`内のmodel-visible fieldを列挙し、reviewer packetへ配送できるものを「semantic projection、境界、authority、必要なnormative contract、必須scope、manifest」に限定する。review contractは独立producer identity、finite evidence manifest、各observationのexact structural target、root substitution禁止を固定する。

このため発行前に次を一意化できる。

| value class | owner | carrier | read permission |
|---|---|---|---|
| packet配送が明示されたsemantic / boundary / authority / normative contract / scope / manifest | rootが構築、reviewerが消費 | packet | rootはexact targetだけ |
| packet配送が許可されずfinite manifestが直接観測targetへ固定したcurrent inventory / contract等 | reviewer | direct observation result | reviewerはexact targetだけ |
| artifact変更・required validationのroot-owned value | root | root result | rootはexact targetだけ |
| history / untrusted prior result / root予想 | なし | なし | readまたはpacket配送禁止 |

ADR03、ADR05、ADR06でC214が遮断した必要値はfinite manifestのexact inventory / contract targetへ固定され、packet許可集合には入らない。したがってrootへwhole-container outputを返さず、reviewerが直接観測できる。

## Candidate作成前の検討gate

1. 基準prompt setはCandidate147。最短正常経路はrootがTaskSpec-declared packet projectionだけをexact readし、reviewerがpacketと未充足のexact direct observationだけでterminal resultを返す経路。
2. 誤経路はCandidate220のADR03からADR06全20 runで観測したroot mixed-owner whole-container admission。
3. TaskSpecの一般read許可、Candidate147 `EVIDENCE_GATE`のtarget artifact許可、`DECISION_BOUNDARY`の共同発行許可がroot whole-source readを合法にするため、promptのproducer別evidence authorityが必要。
4. `PRECHANGE_REVIEW`と`REVIEW_SOURCE_AUTHORITY`を追加する。前者はreview resultとeffect、後者はroot packet projection、root operation target、reviewer direct observationの発行権限だけを持つ。
5. source availabilityからroot whole readへ至る辺を削除し、exact structural targetごとのproducer権限へ置換する。成功runのtool順は転記しない。
6. 増える判断は、TaskSpecが直接固定したtargetがpacket projection、root operation、reviewer observationのどれに属するかと、region overlapだけ。case、field、selector、期待terminalの対応表は追加しない。
7. ADR9 r2全9ケース各N=5で45 / 45 Score 4、terminal、artifact境界、reviewer cardinality、required command、result admission / effectの全件一致を要求する。
8. root whole-container / mixed-owner resultは20 / 20から0件、packet source再readとroot reviewer-owned prereadは0件を維持し、ADR03からADR06の必要direct observationを20 / 20、ADR07 / ADR09のpaired-only routeを各5 / 5と想定する。
9. 品質または上記機序が一件でも外れたら有効runを保持して停止する。repair rerun、ADR9 N=20、Standard14、採用、release、projectionへ進めない。permission分離の成立確認なので対象権限違反はzero-toleranceとする。

## 同一Candidateで扱う理由

root whole-source権限だけを削除するとpacket constructionが不能になり、reviewer direct observationだけを開くとroot先読みと投影元再readが残る。packet projection、root operation、reviewer observationの三集合とoverlap denyは、一つのproducer別source authorityを完全にする分離不能な境界である。

## 非目標

- Candidate215からCandidate220までの条件、ticket、work itemまたはoutput closureの継承
- 特定tool、selector、read回数、model stepまたは成功時判断順の固定
- case、field、scope、observation identityの本文埋込み
- ADR9のTaskSpec、case、fixture、schemaまたはoracle変更
- executor、CLI、adapter、runtime hookまたは外部wrapper変更

## 参照

- [Prompt制御の検討原則](prompt-control-design-principles.md)
- [Candidate214経路閉鎖の再制御方針](candidate214-route-closure-recontrol-direction.md)
- [Candidate214 ADR9結果](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate220 ADR9結果](../evaluations/results/candidate220-review-observable-output-closure-adr9-r2-n5_2026-08-14.md)
