# Candidate147リリース

## 結論

Candidate147を採用し、公開版`the-caption`へ投影した。

release状態は`projected`、runtime projectionは`projected`である。Candidate147と内容が同一のrelease snapshotであり、prompt本文は変更していない。

## 識別情報

- release identity: `the-caption-3ce91a4-result-effect-scope-release-r1`
- source candidate: `the-caption-3ce91a4-result-effect-scope-r1`
- source candidate commit: `b62063b7be57853318d17a154363e4b39a55144d`
- bundle SHA-256: `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`
- content relation: Candidate147と同一内容
- Candidate147から変更したtarget: なし

## 採用根拠

- Standard14 N=100は1,400 / 1,400件がscore `4`
- score `3`以下、excluded attempt、controller error、command protocol violationは0件
- targeted F01 / F02 / F03は15 / 15件で狙った`result_effect_scope`が成立
- Candidate145 N=5比でtoken中央値`-9.17%`、elapsed中央値`-23.13%`
- Candidate147 N=100の集約中央値はCandidate125 N=5参照値付近であり、費用増加を回収した

品質、安定性、狙った制御機構、費用回収を別々に確認した。費用は統計的な優越ではなく、Candidate145で生じた増加をCandidate125付近へ戻したという判断である。

## 未解決risk

- 結果はRating v14、Medium、CLI `0.146.0`、固定Standard14 N=100の範囲に限定する。
- Candidate125より統計的に低token・短elapsedとは主張しない。
- F06ではauthority追加readが21 / 100件残った。quality failureではないが、完全に除去したとは扱わない。
- Candidate manifestのtarget commit・treeは公開移行前の記録であり、公開版では解決しない。投影時は公開版のbaselineを別に固定する。

## 投影結果

- public repository: [`Kenn-dclxvi/the-caption`](https://github.com/Kenn-dclxvi/the-caption)
- PR: [#13](https://github.com/Kenn-dclxvi/the-caption/pull/13)
- baseline / rollback identity: `3b6013e0850d0f9ebbec72e534c0b644602ca880`
- merge commit: `3119a91d3fad63180884f80ac6b742fbae328afe`
- 実効変更: root `AGENTS.md`一つ
- required validation: `bash scripts/dev/verify_change_set.sh`、`382 passed in 7.12s`
- public CI: Secret Scan `gitleaks` success
- post-merge照合: 実効変更1 / 1、manifest target 15 / 19
- 保持したtarget drift: `docs/AGENTS.md`、`docs/how-to/index.md`、`docs/reference/project-contexts/the-caption.txt`、`src/AGENTS.md`
- 本番運用checkout `/Users/kenn/repos/the-caption`は更新していない。今回のterminalはpublic repository `main`への公開である
- 正本: [`projection.json`](projection.json)

## 状態

| lifecycle | state |
| --- | --- |
| evaluation | `standard14_n100_evaluated / quality_stability_gate_passed / mechanism_gate_passed / aggregate_cost_recovered` |
| adoption | `adopted` |
| release | `projected` |
| runtime projection | `projected` |

## 根拠

- [Candidate147採用判断](../../../docs/candidate147-adoption-decision.md)
- [Standard14 N=100 result](../../../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [F06 N=100 result](../../../evaluations/results/candidate147-result-effect-scope-v14-medium-f06-atomic-reuse-n100-cli0146_2026-08-02.md)
- [Targeted F01 / F02 / F03 result](../../../evaluations/results/candidate145-candidate147-result-effect-scope-v14-medium-f01-f02-f03-atomic-n5-cli0146_2026-08-02.md)
- [Candidate147設計](../../../docs/candidate147-result-effect-scope-design.md)
- [Candidate147 manifest](../../candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
