# Candidate176 設計判断前提の反証設計 第3版

## 結論

Candidate176はCandidate175を直接親とし、固定一般設計の判断を成立させる明示的な事実前提が、許可済みの具体的事実で直接否定された場合を`counterexample_found`へ加える一軸の改訂とする。

実装へ渡すsemantic designの正本は、情報封鎖用packet [candidate176-decision-premise-counterexample-review-packet-r3.md](candidate176-decision-premise-counterexample-review-packet-r3.md) とする。packet identityはSHA-256 `44ce752bb7191d015c8268c69397ec34aa2af8b4d036ea1d9e33a1ba84b7df71`である。実装は監査通過済みpacketのpredicateとschemaだけを使用し、本書の履歴・状態または監査結果をpromptへ流用しない。

## Identity

- candidate number: Candidate176
- design identity: `candidate176-decision-premise-counterexample-design-r3`
- semantic packet identity: `sha256:44ce752bb7191d015c8268c69397ec34aa2af8b4d036ea1d9e33a1ba84b7df71`
- prompt identity: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- direct parent: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- changed target: root `AGENTS.md`
- changed axis: 明示規範への違反とは別に、設計判断を支える固定事実前提の具体的反証を判定する経路
- evaluation status: `design_not_audited / not_implemented / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 第2版からの一般修正

1. 判断前提の証拠源を`manifest_observation`と`prior_fixed_enumeration`の型付き論理和にした。前者だけにmanifest success receipt、後者だけに先行authorityの列挙receiptを要求する。
2. `counterexample_found`を`normative`と`decision_premise`の排他的schemaにし、各経路の必須fieldと禁止fieldを固定した。
3. 判断前提経路のboundary、premise provenance、dependency、scope、snapshot、evidence source、全receiptを起動前descriptorと完全一致させるresult admissionを固定した。
4. 情報封鎖監査へ本書全体を渡さず、履歴、状態、先行findingを含まないsemantic packetだけを渡す。

## 作成前gate

1. 基準プロンプトはCandidate175の固定バンドル`251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`とする。
2. Candidate175のreview要否、permission前停止、review operation仕様、明示producer binding、allow-list semantic projection、packet identity、三つのdisposition、一般設計admissionは変更しない。
3. 変更軸はsemantic packetの`decision_premise_counterexample_established`追加だけとし、既存の規範矛盾経路との型付き論理和で`concrete_counterexample_established`を構成する。
4. 情報封鎖した独立監査は、一般仕様、Candidate175の現行prompt、semantic packetの3入力だけで行う。本書、初版、第2版、監査記録、Target評価、実装は渡さない。
5. 監査が`counterexample_found`または`unavailable`なら実装しない。`no_counterexample_found`の場合だけCandidate bundleを作成する。
6. 固定済みADR9 r2とStandard14は変更しない。実装後はADR9各N=5を先に実行し、全件通過した場合だけStandard14各N=5を実行する。

## 変更前監査の判定範囲

semantic packet末尾の`Adversarial audit criterion`をcriterionとする。独立reviewerは、一般入力での偽陽性、偽陰性、任意の`unavailable`、証拠源の混同、descriptorとの値不一致、snapshotまたはscopeの後付け、open-worldの不当な閉包、Candidate175との矛盾、root代行またはcase固有分岐を確認する。

監査resultはsemantic packet identity、確認範囲、具体的反例の有無へbindする。反例がある場合は、入力、誤経路、正しい経路、一般修正を返す。`no_counterexample_found`だけを実装admissionに使う。

## 監査通過後の初回評価

- first gate: ADR9 r2、TC-ADR01からTC-ADR09、各N=5
- second gate: Standard14、各N=5
- model / reasoning / Agent/runtime/CLI / permission: Candidate175の対応する保存済みresultと同一
- direct reference: Candidate175の保存済みADR9 N=5およびStandard14 N=5
- prompt以外の互換条件: 対応するCandidate175 resultと完全一致

Candidate175の既存runは再実行しない。Candidate176の不足runだけを発行する。ADR9とStandard14は変更せず、失敗runをvalidのまま保持し、結果に合わせた再試行またはケース修正を行わない。
