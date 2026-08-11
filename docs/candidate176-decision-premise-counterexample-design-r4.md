# Candidate176 設計判断前提の反証設計 第4版

## 結論

Candidate176はCandidate175を直接親とし、固定一般設計の判断を成立させる明示的な事実前提が、許可済みの具体的事実で直接否定された場合を`counterexample_found`へ加える一軸の改訂とする。

実装へ渡すsemantic designの正本は [candidate176-decision-premise-counterexample-review-packet-r4.md](candidate176-decision-premise-counterexample-review-packet-r4.md) とする。packet identityはSHA-256 `0d9237fe5676ee09804a5efd9ac3b46cbf9e61f1f03235a56c4a57ba63947087`である。実装は監査通過済みpacketだけを使用し、本書の履歴・状態をpromptへ流用しない。

## Identity

- candidate number: Candidate176
- design identity: `candidate176-decision-premise-counterexample-design-r4`
- semantic packet identity: `sha256:0d9237fe5676ee09804a5efd9ac3b46cbf9e61f1f03235a56c4a57ba63947087`
- prompt identity: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- direct parent: `the-caption-3ce91a4-review-operation-admission-closure-r1`（Candidate175）
- changed target: root `AGENTS.md`
- changed axis: 明示規範への違反とは別に、設計判断を支える固定事実前提の具体的反証を判定する経路
- evaluation status: `design_not_audited / not_implemented / not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 第3版からの一般修正

1. `no_counterexample_found`の前に、全判断前提descriptorについて、manifest観測または先行固定列挙の経路別receiptを一対一に要求する。
2. receiptへ具体的事実のidentityと構造化fieldを持たせ、結果の`counterexample_facts`と完全一致させる。
3. 前提predicateを不存在、普遍、boolean relation、単一値relation、基数、終端遷移へ型分けし、型別の直接否定と必須authorityを固定する。
4. 終端遷移へphase、terminality、判定horizon、相互排他性を要求し、中間的なretryまたはcontinueを終端stopの否定にしない。
5. boundary dependencyは単一要約値にせず、起動前source identityの完全一致集合として扱う。

## 作成前gate

1. 基準プロンプトはCandidate175の固定バンドル`251afdef36802c6ea3f2c4def3616288fa9054a22c028896c16418ba3e8a5061`とする。
2. Candidate175のreview要否、permission前停止、review operation仕様、明示producer binding、allow-list semantic projection、packet identity、三つのdisposition、一般設計admissionは変更しない。
3. 変更軸はsemantic packetの`decision_premise_counterexample_established`追加だけとする。
4. 情報封鎖監査は、一般仕様、Candidate175の現行prompt、semantic packetの3入力だけで行う。本書、旧版、監査記録、Target評価、実装は渡さない。
5. `no_counterexample_found`の場合だけCandidate bundleを作成する。
6. 固定済みADR9 r2とStandard14は変更しない。実装後はADR9各N=5を先に実行し、全件通過した場合だけStandard14各N=5を実行する。

## 監査通過後の初回評価

- first gate: ADR9 r2、TC-ADR01からTC-ADR09、各N=5
- second gate: Standard14、各N=5
- model / reasoning / Agent/runtime/CLI / permission: Candidate175の対応する保存済みresultと同一
- direct reference: Candidate175の保存済みADR9 N=5およびStandard14 N=5
- prompt以外の互換条件: 対応するCandidate175 resultと完全一致

Candidate175の既存runは再実行しない。Candidate176の不足runだけを発行する。ADR9とStandard14は変更せず、失敗runをvalidのまま保持し、結果に合わせた再試行またはケース修正を行わない。
