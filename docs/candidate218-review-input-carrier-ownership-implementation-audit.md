# Candidate218 review input carrier ownership 実装監査

## 状態

- `candidate_created`
- `static_verification_passed`
- `ADR9_r2_N5_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- `adoption_not_decided`
- `release_not_created`
- `projection_not_performed`

## Candidate identity

| 項目 | 値 |
|---|---|
| Candidate | Candidate218 |
| prompt identity | `the-caption-3ce91a4-review-input-carrier-ownership-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `04c2e670eabf659b24139429246ad1e640e5162297b4fd999a0565efd8762f73` |
| root `AGENTS.md` SHA-256 | `3bfeeb58d15f8c29bc7055aef9eeb74627b810cb5e895f84d46cde59892d3862` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `ADR9_r2_N5_completed / quality_failed / mechanism_failed / stopped` |

## 実装範囲

Candidate147のfull bundleを直接基盤とし、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはCandidate147と同一である。Candidate217の`REVIEW_INPUT_CLOSURE`は継承していない。

追加した責務は次の二つだけである。

1. `PRECHANGE_REVIEW`はTaskSpecが明示した独立reviewだけを`implementation_bound`後のartifact変更前へ接続し、独立producerの三terminal resultと対応変更effectを閉じる。
2. `REVIEW_INPUT_OWNERSHIP`はrepository current value取得前に、各inputを`root_control / packet_carried / reviewer_observation / unavailable`へ排他的にbindし、reviewer-owned projectionを含むresultのroot admissionを禁止する。

## 持ち込まなかった制御

- Candidate217の「admission済みならpacket」という二値供給規則
- Candidate216以前のsource container / region名称やcase別selector
- case、field、scope、target、observationの対応表
- 成功runのtool順、read順、判断順またはpacket文面
- executor、adapter、runtime hookまたは外部wrapper変更

Candidate217はfixed input / packet carrier conflict 20件、reviewer起動前停止5件、mixed-owner root admission 20件、admission済みoperand再read12回の反証と、ADR07 paired-only 5 / 5の保持対象だけに使用した。

## 静的検証項目

- `verify_bundle()`が成功する。
- manifestのbundle SHA-256再計算値が一致する。
- Candidate147との差分targetが`AGENTS.md`だけである。
- 非変更target 18件がCandidate147と同一である。
- root本文にcase identity、固定path、固定field / scope / observation identityまたは期待dispositionを含めない。
- four-way ownership、exactly one binding、root-control非配送、reviewer-owned root admission禁止、mixed-owner whole-container非admissionを固定する。
- bundle identity snapshotへCandidate218を追記する。

## 動的評価で判明した制約

ADR9 r2 N=5では、ADR03からADR06の20 / 20 runでrootがreviewer-owned値を含むcontainer resultを取得した。19件ではreviewerも同じ値を直接観測し、少なくとも2件では禁止されたpacket配送がreviewer resultから直接確認できた。静的にownershipと非admissionを記述しても、一般`EVIDENCE_GATE`がrootのmixed-owner invocationを許可するため、resultがroot modelへ返るrouteを閉じられなかった。

したがって静的検証通過を動的な機序成立へ昇格しない。次の設計ではconsumer ownerとexact projectionをrepository evidence invocationの発行条件へbindし、owner境界を越えるresultになり得るinvocationを発行前に閉じる必要がある。

## 参照

- [Candidate218作成前設計](candidate218-review-input-carrier-ownership-design.md)
- [Candidate218方向監査](candidate218-review-input-carrier-ownership-direction-audit.md)
- [Candidate218 manifest](../prompts/candidates/the-caption-3ce91a4-review-input-carrier-ownership-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate218 ADR9結果](../evaluations/results/candidate218-review-input-carrier-ownership-adr9-r2-n5_2026-08-14.md)
