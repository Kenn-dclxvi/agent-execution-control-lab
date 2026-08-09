# Candidate172 実装前設計 admission 設計

## 結論

Candidate172はCandidate147を直接親とし、一般設計の境界ごとに敵対的レビューの要否を決め、受入可能な結果が揃うまで成果物変更を許可しない`DESIGN_ADMISSION`を一軸で追加する。

レビューは、設計が探索由来の開いた境界へ依存し、必須検証が反例を見逃し得て、その反例が一般設計を変える場合だけ必要とする。契約または先行repository authorityが有限領域を閉じ、必須検証が全memberと関係を網羅する境界では起動しない。

## Identity

- candidate number: Candidate172
- prompt identity: `the-caption-3ce91a4-preimplementation-design-admission-r1`
- direct parent: `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）
- changed target: root `AGENTS.md`
- changed axis: 一般設計のreview要否とartifact変更許可を結ぶ`DESIGN_ADMISSION`
- evaluation status: `not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. 基準プロンプトはCandidate147の固定バンドル`51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`とする。
2. 基準状態の最短正常経路は、仕様と境界台帳を完成し、閉じた境界ならreviewを起動せず設計をadmitし、`implementation_bound`成立後に変更と必須検証を完了する経路である。
3. 保存済み45件では、閉じた境界でもreviewを10 / 10件起動した。review必須の20件では9件でreviewを起動せず、起動した11件も具体的反例を返せず`unavailable`となった。
4. Candidate147は一般的なproducer、evidence、implementation bind、result effect scopeを持つが、一般設計の境界分類、review要否、review結果の受入条件をartifact変更許可へ結ぶpredicateを持たないため、この誤経路を既存制御だけでは防げない。
5. 追加する変更軸は`DESIGN_ADMISSION`一つとする。
6. この制御は、permissionがあるという理由だけでreviewを起動する判断、review必須時にrootが判定を代行する判断、具体的反例にもmanifest全件成功を要求する判断、未admit設計から変更する判断を除く。
7. 新たに増える判断点は、境界ごとの四条件、review permission、packet readiness、三つのreview dispositionの受入、一般設計のadmissionである。特定case、fixture、期待terminalによる分岐は増やさない。
8. 品質維持は、実装前に固定済みの9ケースを各5件実行し、全45件で点数4と機序条件の双方を確認する。
9. 一件でも点数3以下、期待経路不一致、情報封鎖違反、未admit設計からの変更、または計測不能があれば停止し、Standard14へ進まない。

## 追加するpredicate

まず`design_contract_ready`を、required outcome、permission、保持条件、成果物間関係、未確定値の有無から判定する。次に`general_design_ready`を、全required outcomeと設計要素の対応、変更対象の一般条件、正本と責任境界、保持挙動と成果物間関係、停止またはfallback条件、全boundary decisionの記録から判定する。契約不足は一般設計とreviewを開始せず既存`SPEC`の確認経路へ戻し、一般設計または台帳不足はreviewを起動せず`unavailable`とする。

各`boundary decision`について次を判定する。

```text
boundary_requires_adversarial_review :=
  design_relies_on_boundary
  ∧ closure_source=autonomous_exploration
  ∧ repository authorityが対象領域を閉じていない
  ∧ required_validation_coverage=non_exhaustive
  ∧ 反例があっても必須検証が成功し得る
  ∧ 反例への対応が一般設計の境界変更を必要とする
```

全境界を分類でき、該当境界がなければ`not_required`とする。一件でも該当すれば`required`、設計または台帳不足で判定できなければ`unavailable`とする。

`required`の場合だけ独立review操作を一件作る。permission否定は操作作成、producer binding、packet構築・配送より先に適用する。permissionが許可されていること自体はreview要否を成立させない。

review結果の受入は次のように非対称にする。

- `counterexample_found`は、対象境界、契約根拠、具体的反例、設計への影響が結び付けば受け入れる。反例が成立した時点でmanifestの残りを成功させる必要はない。
- `no_counterexample_found`は、全対象境界、必須review scope、manifest全件の成功receiptが完全一致する場合だけ受け入れる。
- `unavailable`は、許可範囲で不足した根拠へ結び付く場合だけ受け入れる。

`not_required`または受入可能な`no_counterexample_found`だけが一般設計をadmitする。`counterexample_found`は設計をrejectし、`unavailable`はadmitしない。一般設計をadmitした後だけCandidate147の`implementation_bound`へ接続して成果物変更を許可する。

## 汎用性

このpredicateはファイルmembershipに限らず、適用条件、authority、ownership、停止、fallback、非影響を前提にするconsumer境界へ同じ形で適用する。閉包を設計者の探索量や既存試験件数から推定せず、先行契約またはrepository authorityと網羅検証の組へ結び付ける。

## 非目標

- 固定済みTarget評価、oracle、rating contract、合否条件の変更
- case ID、fixture名、既知の期待terminalによる分岐
- すべての非機械的判断へのreview追加
- review結果をrootが再生成または再採点すること
- Candidate167からCandidate169の修正契約制御の継承
- executor、CLI、tool adapter、runtime hook、外部wrapperの変更
- release、採用、THE-CAPTION本体への反映

## 初回評価

- cases: TC-ADR01からTC-ADR09、各N=5
- design contract: `design_revision_7`
- targeted evaluation: `preimplementation-adversarial-design-review-targeted-evaluation-design-r10`
- model / reasoning: 基準resultと同一
- direct reference: Candidate147の保存済み45件
- prompt以外の互換条件: Candidate147と完全一致

既存Candidate147の45件は再実行しない。Candidate172の不足45件だけを発行する。試験はCandidate実装前に固定済みの版をそのまま使い、結果に合わせて変更しない。
