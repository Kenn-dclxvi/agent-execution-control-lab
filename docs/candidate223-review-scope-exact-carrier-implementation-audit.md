# Candidate223 review scope exact carrier 実装監査

## 判定

`implementation_passed / evaluation_completed_failed_stopped`

## 固定したCandidate

- prompt identity: `the-caption-3ce91a4-review-scope-exact-carrier-r1`
- direct base: `the-caption-3ce91a4-result-effect-scope-r1`
- bundle SHA-256: `85473ee6fc8d50c1e9946b2fb4d328fae68a260ade5380e9c32501ed2fbd9320`
- changed target: `AGENTS.md`だけ

Candidate147の既存条項を保持し、`PRECHANGE_REVIEW`と`REVIEW_SCOPE_CARRIER`だけを追加した。Candidate214からCandidate222までのprompt本文は継承していない。

TaskSpec r13とcase r4には`review-scope-carrier-contract/v2`を追加した。fixtureの意味、oracle、期待terminal、rating、runtime、permissionおよびexecutor条件はr2から維持し、missing paired evidenceは追加していない。

## 静的検証

- bundle verificationはmanifest記録と同じSHA-256で成功した。
- Candidate147から変更したbundle targetは`AGENTS.md`だけだった。
- Candidate本文にcase ID、observation ID、scope ID、具体的field名またはtool順を含めていない。
- 9ケースのseed patchは固定target commitからmaterializeし、宣言commitと9 / 9件一致した。
- Candidateとr4 caseのfocused testは21件成功した。
- `git diff --check`は成功した。

この静的監査は必要review完遂を証明しない。後続ADR9 r4 N=5では、root exact projection 45 / 45、scope外reviewer read 0件を確認した一方、必要reviewerは28 / 30件に留まったため、品質・機序とも不通過だった。

## 参照

- [Candidate223設計](candidate223-review-scope-exact-carrier-design.md)
- [方向監査](candidate223-review-scope-exact-carrier-direction-audit.md)
- [ADR9 r4 N=5結果](../evaluations/results/candidate223-review-scope-exact-carrier-adr9-r4-n5_2026-08-14.md)
