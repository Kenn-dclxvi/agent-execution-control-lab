# P001 THE-CAPTION Standard14投影設計

> [!IMPORTANT]
> **作成時状態**: `candidate_precreation_gate_fixed / p001_canonical_bytes_preserved / c147_nonroot_surface_preserved / standard14_n5_not_started / adoption_not_decided`

## 結論

P001をStandard14で直接評価するため、P001本体を変更せず、THE-CAPTION用の投影bundleを別identityで作る。投影bundleはCandidate147のprompt bundleを比較基準とし、root `AGENTS.md`だけをP001の固定bytesへ置換する。root以外の18 target、TaskSpec、fixture、case、oracle、rating、runtimeおよびtoken accountingは変更しない。

P001の正本は`portable-semantic-c147-portable-full-agent-r1`のまま保持する。Standard14 resultは、実際に配送した投影bundle identityへbindし、P001単体bundleのresultとして登録しない。

## Candidate作成前gate

1. **比較基準と正常経路**: 基準はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`である。正常経路は、固定済みStandard14 TaskSpec、root実行制御、THE-CAPTION固有の局所instructionおよびrepository authorityを読み、許可された実装、検証、終了へ進む経路である。
2. **実測した問題経路**: 固定Layer 1の代表fixtureへP001単体bundleだけを重ねると、C147 bundleが空化する`docs/glossary.md`、`docs/orchestration-process.md`、`docs/prompt-guide.md`および`prompts/*.md`四件がTHE-CAPTION元内容のまま残る。root以外に7 targetの差が生じ、P001 root一枚の差へKPIを帰属できない。
3. **問題を許す境界**: P001単体bundleはroot `AGENTS.md`だけを列挙するため、bundle適用処理は未列挙targetを変更しない。TaskSpec、repository authorityおよびfixtureは、この配送前のprompt集合差を閉じない。
4. **変更範囲**: C147 bundleの19 targetを保持し、root `AGENTS.md`だけをSHA-256 `3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3`のP001本文へ置換する。P001本文、C147の非root target、file modeおよびsymlink targetは変更しない。
5. **閉じる問題経路**: 投影bundleへ全targetを明示することで、未列挙のTHE-CAPTION元promptが残る経路をなくす。モデルの判断順に依存せず、root以外の有効prompt surfaceをC147とbyte一致させる。
6. **維持する正常経路**: THE-CAPTION固有の局所instruction、空化済みlegacy prompt、symlinkおよびrepository authorityはC147と同じcarrierで届く。P001は自己完結したroot一枚として配送し、component readを要求しない。
7. **追加costと対象外影響**: 新しい条件、label、判断、tool順および例外はprompt本文へ追加しない。比較対象となる実効差はroot本文の10,772 bytesから10,781 bytesへの置換だけである。静的9 bytes差だけで効率を判定しない。
8. **評価条件**: `the-caption-standard14-r1`の14 Caseを各N=5で実行し、C147の登録済み互換result `f7baeadc5bd44399ac13cc0e0a8aff48`を比較基準とする。modelは`gpt-5.6-sol`、reasoningは`medium`、Codex CLIは`0.146.0`、Pythonは`3.14.5`、permissionは`workspace-write / never`、設定上の並列上限は24、token accountingはall-agent v1とする。品質、all-agent `total_tokens`、`elapsed_seconds`を記録し、tool順やread回数は原因診断に限定する。
9. **停止条件**: 投影bundleのroot以外がC147と一件でも不一致、P001 root bytesが不一致、preflightのprompt identity以外に不一致、slot coverageが14 Case × 5でない、実行がinvalid、採点不能または必要KPI欠落なら停止する。有効な低品質runは再実行せず保持する。評価成立を採用、releaseまたはruntime projectionへ昇格させない。

## identity境界

| 役割 | identity | 扱い |
| --- | --- | --- |
| portable正本 | `portable-semantic-c147-portable-full-agent-r1` | P001。本文bytesとportable semantic結果の正本 |
| Standard14比較基準 | `the-caption-3ce91a4-result-effect-scope-r1` | C147の保存済み互換resultを再利用 |
| Standard14投影bundle | `p001-the-caption-standard14-projection-r1` | 実際にTHE-CAPTION fixtureへ配送し、Standard14 resultをbindするidentity |

投影bundleの合格はP001のplatform非依存性一般を証明しない。THE-CAPTION Standard14上で、C147非root surfaceを固定したroot置換の結果だけを示す。

## 評価結果と現在状態

Standard14の14項目各N=5は70 / 70件が`valid`かつScore `4`だった。一方、Candidate147との互換比較では、14項目集約中央値のall-agent `total_tokens`が`+113.73%`、`elapsed_seconds`が`+17.04%`となり、両方とも増えた。現在状態は`standard14_n5_completed / quality_gate_passed / aggregate_cost_both_higher / cost_regression / p001_canonical_unchanged / adoption_not_decided`とする。N=20へ自動拡張せず、採用、releaseおよびruntime projectionも行わない。一次証拠は[`P001 THE-CAPTION投影 Standard14 N=5評価`](../evaluations/results/p001-the-caption-standard14-projection-n5_2026-08-18.md)と登録result `e8bb0207c8014e5bac8d79ec2cf74bf4`である。

## 参照

- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
- [`Portable full-agent kernel直接比較設計`](portable-full-agent-kernel-direct-comparison-design.md)
- [`P001 bundle`](../evaluations/targets/portable-instruction-semantic-conformance/prompts/candidates/portable-semantic-c147-portable-full-agent-r1/)
- [`C147 bundle`](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/)
