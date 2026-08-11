# Candidate176 設計判断前提の反証設計 第13版

## 結論

Candidate176はCandidate175を直接親とし、明示規範predicateとの矛盾に加え、固定一般設計の必要前提を許可済み具体的事実が直接反証する経路を追加する一軸の改訂とする。

実装へ渡すsemantic designの正本は [candidate176-decision-premise-counterexample-review-packet-r13.md](candidate176-decision-premise-counterexample-review-packet-r13.md) とする。packet identityはSHA-256 `aac076e57ae2a093753444f9ce70d6bbb67038c4378e53c3472f5a97ea925cda`である。

## Identity

- candidate number: Candidate176
- design identity: `candidate176-decision-premise-counterexample-design-r13`
- prompt identity: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- direct parent: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- changed target: root `AGENTS.md`
- changed axis: 明示された設計判断前提の具体的反証
- evaluation status: `design_adversarial_review_passed / not_implemented / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 実装条件

1. Candidate175のreview要否、permission前停止、operation admission、producer分離、semantic projection、manifest、root非代行、一般設計admissionを維持する。
2. Candidate173の規範矛盾経路を維持する。
3. `concrete_counterexample_established`を、規範矛盾経路と判断前提反証経路の論理和にする。
4. 判断前提反証は、一件以上の`fact_supports`を使用できる。各supportはmanifest成功観測または先行固定contract / authority列挙の一形式だけを持つ。
5. 非明示前提、列挙、省略、open境界、名称またはより安全な設計の可能性から反例を作らない。
6. 判断前提、直接否定、design effectは独立reviewerが判定し、rootは固定source、support、receipt、provenance、snapshotのidentity bindingだけを行う。
7. 反例成立後は無関係なmanifest欠落で失効させない。反例不成立時だけmissingを`unavailable`へ使う。
8. fixture、case、期待terminalまたは既知対象名による分岐を追加しない。

## 変更前監査

第13版のsemantic packetを、一般仕様とCandidate175 promptだけを許可入力とする独立実行へ渡した。結果は`no_counterexample_found`であり、実装、Target評価、過去監査、会話履歴は渡していない。

## 初回評価

- first gate: 変更しないADR9 r2を各N=5
- second gate: ADR9全件通過時だけStandard14を各N=5
- model / reasoning / Agent/runtime/CLI / permission: Candidate175の対応する保存済みresultと同一
- Candidate175の既存runは再実行せず、Candidate176の不足runだけを発行する
- 失敗runはvalidのまま保持し、試験、oracle、rating contractを変更しない
