# P001 THE-CAPTION投影 Standard14 N=5評価

## 結論

P001のroot `AGENTS.md`をTHE-CAPTIONへ投影し、Candidate147の非root 18 targetをbyte一致で保持した条件で、Standard14の14項目を各5件評価した。70 / 70件が`valid`かつScore `4`だった。

一方、Candidate147との互換比較では、5回の14項目集約中央値がtoken `+113.73%`、elapsed `+17.04%`で、ともに増加した。したがって現在状態は`standard14_n5_completed / quality_gate_passed / aggregate_cost_both_higher / cost_regression / p001_canonical_unchanged / adoption_not_decided / release_not_created / runtime_projection_not_authorized`とする。N=5の差を安定傾向とは扱わず、N=20へ自動拡張しない。

## identityと互換条件

- P001正本: `portable-semantic-c147-portable-full-agent-r1`
- P001 root SHA-256: `3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3`
- Standard14投影bundle: `p001-the-caption-standard14-projection-r1`
- 投影bundle SHA-256: `a51f05a3ee64b0b4b6cf1392380de0e5e74c5111545a4e67f3f4d0358fd481f1`
- profile: `p001-the-caption-standard14-projection-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- Evaluation set: `the-caption-standard14-r1` / `r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- permission: `workspace-write / never`
- 設定上の並列上限: `M=24`
- token accounting: all-agent v1
- 比較基準: Candidate147 result `f7baeadc5bd44399ac13cc0e0a8aff48`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- P001投影result: [`e8bb0207c8014e5bac8d79ec2cf74bf4.json`](e8bb0207c8014e5bac8d79ec2cf74bf4.json)

投影bundleはC147 bundleと同じ19 targetを持ち、root `AGENTS.md`だけをP001 bytesへ置換した。P001単体bundleを直接重ねた場合に残るTHE-CAPTION元prompt 7 targetを、比較差へ混ぜていない。作成前の境界は[`P001 THE-CAPTION Standard14投影設計`](../../docs/p001-the-caption-standard14-projection-design.md)を正とする。

preflightはprompt identity以外の条件を照合し、14項目×5件の70 slot、発行済み0件、status `ready`を固定した。新規70件は272.400秒の外側実行で完了し、valid 70、excluded 0、再試行0、controller error 0だった。

## 品質

Rating v14では70 / 70件がScore `4`で、成果不成立、必須command失敗、許可外path変更および採点failureは0件だった。

owner-producer evidence不成立52件と、F04 iteration 3のcommand protocol diagnostic 4件を記録した。いずれもRating v14では診断情報であり、成果、必須commandの成功および許可範囲を満たした品質点へ混ぜていない。

## Candidate147との3 KPI比較

Candidate147も同じatomic registryから14項目×5件を新しく選択し、同じ集計器で再集計した。

| 指標 | Candidate147 | P001投影 | 差分 |
| --- | ---: | ---: | ---: |
| quality中央値 | 100.00 | 100.00 | 0.00 |
| token中央値 | 1,447,626 | 3,094,024 | +1,646,398（+113.73%） |
| elapsed中央値 | 852.543秒 | 997.840秒 | +145.297秒（+17.04%） |

項目別中央値ではtokenが12 / 14項目、elapsedが10 / 14項目で増えた。token増加率が大きいのはA02 `+241.51%`、F02 `+212.35%`、F08 `+196.28%`、F07 canonical `+152.02%`だった。elapsed増加率が大きいのはF08 `+86.69%`、F03 `+52.24%`、A01 `+38.63%`、F07 canonical `+37.56%`だった。

tokenが減ったのはF05 clarify `-2.34%`とF10 monthly `-0.64%`だけである。本文の静的差は9 bytesにすぎず、この結果は文字数短縮や特定Case内容の勝敗ではなく、同じ14操作群でP001の自然語・機能block構造を処理した実行costとして扱う。ただし、N=5だけから各項目の差を個別文や単一機序へ因果帰属しない。

## 後続の機能block別診断

同じ70 runのraw traceをmodel response、action前後、tool invocationおよびcommand outputへ分けた後続診断では、cost主因をvalidation carrier、副因をfrontier carrierへ限定した。prompt全体の長さ、worker増加、tool数またはretry増加を主因とは判定していない。診断の数値、F01〜F03のraw trace範囲および次案前の境界は[`P001 Standard14 N=5 機能block別cost診断`](../../docs/p001-standard14-n5-functional-block-cost-diagnostic.md)を正とする。

この後続診断は保存済みresultの解釈を追加するものであり、本result、P001正本、評価済み投影bundleおよびKPIを変更しない。新しいCandidateまたは評価slotも発行していない。

## 保存先と境界

raw試験rootは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/p001-the-caption-standard14-projection-v14-medium-standard14-n5-cli0146-20260818-r1`である。preflight、70件の実行証拠、quality audit、P001とC147のselection・analysis・comparison、execution seal、result登録およびfinal compactを保持する。execution archive SHA-256は`6270c975ee08bb2e5d30170993cc6ae863f771e78ad6252947f4d324bac8dec9`、final compact archive SHA-256は`35e609621a6303701565d64f3fa1b8f286b7d00a0a5730c4e3681f89f53fbe28`である。

この結果はTHE-CAPTION Standard14上のP001投影評価だけを示す。P001のportable semantic N=20結果、採用、release、他platformへの配置およびruntime projectionは変更していない。
