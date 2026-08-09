# Candidate173 具体的反例の判定設計

## 結論

Candidate173はCandidate172を直接親とし、敵対的reviewの三つの結果を分ける`concrete_counterexample_established`を`DESIGN_ADMISSION`内へ追加する一軸の改訂とする。

許可済み根拠で実在と契約違反を直接確認できた反例は、その後に別のmanifest欠落が見つかっても`counterexample_found`として保持する。一方、境界がopenであること、名称が関係を示唆すること、未観測対象が存在し得ることだけでは具体的反例を成立させない。

## Identity

- candidate number: Candidate173
- prompt identity: `the-caption-3ce91a4-concrete-counterexample-adjudication-r1`
- direct parent: `the-caption-3ce91a4-preimplementation-design-admission-r1`（Candidate172）
- changed target: root `AGENTS.md`
- changed axis: 敵対的review dispositionを分ける具体的反例の立証責任と優先順位
- evaluation status: `not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. 基準プロンプトはCandidate172の固定バンドル`99474ab061becfe205d8e1646e6032dc024d5bb29cc09563201ce9658457c212`とする。
2. 最短正常経路は、reviewerが許可済み根拠を確認し、具体的反例が成立すれば即座に`counterexample_found`、成立せずmanifest全件成功なら`no_counterexample_found`、成立せず判定に必要な根拠が不足すれば`unavailable`を返す経路である。
3. Candidate172の保存済み45件では、40件が点数4だった。ADR04の2件とADR05の1件は具体的反例を構成できたのに別manifest欠落を`unavailable`へ優先し、ADR07の2件はopen境界と契約名から未観測関係を推測して`counterexample_found`とした。
4. Candidate172は`counterexample_found`にmanifest全件成功を要求しないが、具体的反例の成立条件、missing evidenceとの優先順位、名称からの推論禁止を固定していないため、二つの解釈が残る。
5. 改訂する変更軸は`concrete_counterexample_established`一つとする。
6. このpredicateは、成立済み反例を無関係な証拠欠落で失効する判断と、open境界または語名だけから未観測対象・関係を実在扱いする判断を除く。
7. 新たな判断点は、反例candidateの実在根拠、直接の規範根拠、一般設計との矛盾、design effectの四点である。case、対象名、fixture、期待terminalの例外は増やさない。
8. 品質維持は、実装前から固定済みの9ケースを各5件実行し、45 / 45点数4と機序条件を確認する。
9. 一件でも点数3以下、期待経路不一致、情報封鎖違反、未admit変更、計測不能があれば停止し、Standard14へ進まない。

## Predicate

```text
concrete_counterexample_established :=
  許可済みの成功観測または先行固定contract / authorityの明示列挙が、具体的な入力、状態、consumer、成果物関係または失敗経路をbind
  ∧ contract_basisが、その具体的instanceに適用される規範predicateを明示
  ∧ その具体値または状態に対する固定一般設計の扱いが規範predicateとの矛盾を直接示す
  ∧ 対応に対象集合、一般条件、正本、所有、停止またはfallbackの変更が必要
```

次は実在根拠または規範根拠にしない。

- 境界またはauthorityが対象領域を閉じていないこと
- 未観測member、consumer、relation、failureが存在し得ること
- identity、項目名、分類名、契約名が関係や義務を示唆すること
- 設計をより強くできること

open境界はreview要否を成立させるが、それ自体は反例ではない。契約名またはラベルは、対応する規範predicateと具体的instanceが許可済み根拠に明記されている場合だけ`contract_basis`になる。

reviewerは、許可済みの成功観測または先行固定contract / authorityの明示列挙から`concrete_counterexample_established`を判定する。成立した場合は`counterexample_found`を終端結果とし、後続または別manifest項目のmissing、unreadable、non-success、receipt欠落でその結果を失効させない。

成立しない場合に限り、全manifest成功なら`no_counterexample_found`、反例有無の判定を変え得る許可根拠が不足すれば`unavailable`とする。つまり三つの結果は次の順で排他的に決まる。

```text
if concrete_counterexample_established:
    counterexample_found
elif evidence manifestにmissing / unreadable / non-success / receipt欠落がある:
    unavailable
elif 全対象boundary、必須scope、manifest全件のsuccess receiptが揃う:
    no_counterexample_found
```

## 既存制御との関係

- Candidate172のreview要否、permission前停止、producer分離、packet情報封鎖、identity照合、artifact変更許可は維持する。
- `counterexample_found`と`no_counterexample_found`の証拠負担が非対称であることも維持する。
- 今回はreview要否やmanifest自体を変えず、三つのdispositionを分ける反例predicateだけを固定する。

## 汎用性

同じpredicateは、未探索consumer、暗黙fallback、ownership越境、failure分類、成果物間関係の反例へ適用できる。具体的なinstanceと規範違反が成立した場合は追加の完全性証明を待たず設計をrejectし、単なる未知可能性だけではrejectしない。

## 非目標

- 固定済みTarget評価、oracle、rating contract、合否条件の変更
- case ID、fixture名、既知対象名による分岐
- review要否の四条件の変更
- manifest対象またはrequired scopeの削減
- rootによるreview結果の再生成または再採点
- Candidate167からCandidate169の修正契約制御の継承
- executor、CLI、tool adapter、runtime hook、外部wrapperの変更
- release、採用、THE-CAPTION本体への反映

## 初回評価

- cases: TC-ADR01からTC-ADR09、各N=5
- design contract: `design_revision_7`
- targeted evaluation: `preimplementation-adversarial-design-review-targeted-evaluation-design-r10`
- model / reasoning: Candidate172と同一
- direct reference: Candidate172の保存済み45件
- prompt以外の互換条件: Candidate172と完全一致

Candidate172の45件は再実行しない。Candidate173の不足45件だけを発行する。Target評価は一切変更せず、結果対応も本書の一般predicateへ限定する。
