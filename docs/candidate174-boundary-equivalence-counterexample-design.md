# Candidate174 境界同値instanceの反例設計

## 結論

この設計案は実装前の敵対的レビューでrejectした。Candidate174のprompt bundleは作成しない。

案ではCandidate173を直接親とし、明示的な規範違反に加えて、境界判断に使える許可済み属性上で同値な具体的instanceを探索履歴だけで異なる扱いにする場合も`concrete_counterexample_established`へ結び付ける予定だった。しかし、観測済み属性の一致と、観測済みcontractまたはauthorityに区別根拠が記載されていないことだけでは、未観測の正当な区別属性が存在しないと立証できない。この判定は、探索範囲を完全とみなさないために導入した敵対的レビューの目的と矛盾する。

## Identity

- candidate number: Candidate174
- prompt identity: `the-caption-3ce91a4-boundary-equivalence-counterexample-r1`
- direct parent: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`（Candidate173）
- changed target: root `AGENTS.md`
- changed axis: 具体的反例に使える境界同値instanceの比較predicate
- evaluation status: `design_rejected_before_candidate_creation`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. 基準プロンプトはCandidate173の固定バンドル`7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c`とする。
2. 最短正常経路は、具体的instanceの明示規範違反、または境界関連属性が同値な二instanceへの根拠なき異なる扱いを確認すれば`counterexample_found`、どちらもなく証拠不足なら`unavailable`、全manifest成功なら`no_counterexample_found`とする経路である。
3. Candidate173の保存済み45件では38件が点数4だった。ADR07の偽反例は閉じたが、ADR03の1件、ADR04の5件、ADR06の1件で、設計が選んだinstanceと同じ分類の観測済み除外instanceを反例にできなかった。
4. Candidate173は明示規範predicateとの矛盾だけを認めるため、一般設計自身が境界判断へ使う属性上で同値なinstanceを探索履歴だけで差別化する自己矛盾を表せない。
5. 改訂する変更軸は`boundary_relevant_equivalence_counterexample`一つとする。
6. このpredicateは、contract名の意味を読む判断、open境界から未観測対象を作る判断、同値な観測済みinstanceの除外を単なる証拠不足へ落とす判断を除く。
7. 新たな判断点は、二つの具体的instance、境界関連signatureの一致、異なる扱い、区別を許す根拠の不存在である。case、fixture、既知対象名、期待terminalの例外は増やさない。
8. 品質維持は、固定済み9ケースを各5件実行し、45 / 45点数4と機序条件を確認する。
9. 一件でも点数3以下、期待経路不一致、情報封鎖違反、未admit変更、計測不能があれば停止し、Standard14へ進まない。

## Predicate

```text
boundary_relevant_signature(instance) :=
  boundary domain、selection / applicability / stop / fallback rule、direct_basisが
  境界判断へ使うものとして固定したcontract / authority属性の値
  ただしinstance identityと自律探索で発見した順序・有無を除く

boundary_relevant_equivalence_counterexample :=
  許可済み成功観測または先行固定contract / authorityが
    designで選択・適用された具体的instanceと、除外・別扱いされた具体的instanceをbind
  ∧ 両instanceのboundary_relevant_signatureが完全一致
  ∧ contract / authorityに異なる扱いを許す区別根拠がない
  ∧ designの異なる扱いを支える残りの根拠がinstance identityまたは自律探索履歴だけ
  ∧ 同じ扱いに直すには対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

`concrete_counterexample_established`は次のどちらかで成立する。

1. Candidate173の、具体値または状態に適用される明示規範predicateとの直接矛盾。
2. `boundary_relevant_equivalence_counterexample=true`。

二つ目は名称の意味解釈ではなく、許可済み構造値の比較である。たとえばcontract identityが同じことは同値signatureの証拠にできるが、そのidentityの語が示唆する未観測relationを作らない。

比較する具体的な除外・別扱いinstanceが存在しない場合、同値反例は成立しない。境界がopen、他instanceが存在し得る、契約名が複数関係を示唆する、設計をより強くできる、という可能性だけでは`counterexample_found`にしない。

三つのdispositionの優先順位はCandidate173を維持する。

```text
if concrete_counterexample_established:
    counterexample_found
elif evidence manifestに不足がある:
    unavailable
elif 全対象boundary、必須scope、manifest全件のsuccess receiptが揃う:
    no_counterexample_found
```

## 汎用性

同じpredicateは、同一schema consumerの一部だけを更新する、同じfailure classの一部だけをfallbackする、同じownership relationの一部だけを正本移行する、同じstop contractの一部だけへ停止規則を適用する設計へ使える。対象名ではなく、設計が宣言した境界関連属性と扱いの差を比較する。

## 非目標

- 固定済みTarget評価、oracle、rating contract、合否条件の変更
- case ID、fixture名、既知対象名による分岐
- contract identityの自然言語上の意味を規範へ変換すること
- 未観測instanceまたはrelationの推測
- review要否、permission、packet、result admissionの変更
- rootによるreview結果の再生成または再採点
- executor、CLI、tool adapter、runtime hook、外部wrapperの変更
- release、採用、THE-CAPTION本体への反映

## 当初予定した初回評価

- cases: TC-ADR01からTC-ADR09、各N=5
- design contract: `design_revision_7`
- targeted evaluation: `preimplementation-adversarial-design-review-targeted-evaluation-design-r10`
- model / reasoning: Candidate173と同一
- direct reference: Candidate173の保存済み45件
- prompt以外の互換条件: Candidate173と完全一致

Candidate173の45件は再実行せず、Candidate174の不足45件だけを発行する予定だった。実装前監査で設計をrejectしたため、評価スロットは発行しない。

## 実装前監査結果

`boundary_relevant_signature`の属性集合は、現在の一般設計が境界判断へ使うと宣言した属性だけで構成される。一般設計自身が正当な区別属性を見落としている場合、その属性を比較対象から除いたまま「完全一致」と判定できる。また、contractまたはauthorityが許される区別属性を限定列挙していない限り、区別根拠の記載がないことは区別根拠の不存在を意味しない。

たとえば、二つのconsumerで観測済みのcontract identity、schema、stop capabilityが一致していても、別の適用authorityが`lifecycle=managed | external`を区別し、stop適用を`managed`だけに許している場合がある。そのauthorityが未観測またはmanifest外なら、この案は正しい区別を反例として誤検出する。

一般的に同値反例を成立させるには、少なくとも次を満たす必要がある。

1. 先行固定contractまたはauthorityが、対象boundaryで扱いを区別できる属性またはpredicateの全体を限定列挙して閉じる。
2. その閉じた属性集合の全値を、比較する両instanceについてsuccess receiptへ一対一に結び付ける。
3. 明示的なsame-treatment predicate、または閉じた全区別属性の一致からだけ異なる扱いを反証する。
4. 区別domainの閉包、属性値または適用authorityのreadが欠ける場合は`counterexample_found`にせず`unavailable`とする。

固定済みTarget入力のADR03、ADR04、ADR06は、二つのinstanceと同じcontractラベルを示すが、そのcontractが同じ扱いを要求する規範predicate、または許容される全区別属性の閉包をmodel-visible入力へ固定していない。そのため、上の一般条件を満たすと期待された`counterexample_found`を一意に導けず、条件を緩めると一般入力で偽陽性になる。

したがって、現在の固定Targetを変更せずに45 / 45を狙うCandidate実装は行わない。再開には、Target評価側でsame-treatment predicateまたは区別属性domainの閉包をCandidate実装前のmodel-visible入力へ固定し、oracleが一般仕様から一意に導けることを再資格化する必要がある。その修正を行う場合も、Candidate173の結果や期待terminalをreviewerへ渡さず、新しい評価revisionとして扱う。
