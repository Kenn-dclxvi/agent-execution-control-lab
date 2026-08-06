# click profile index

`click` target instanceのevaluation profileを引くための索引である。profile固定条件、reasoning運用基準、runtime / CLI互換、`max_workers`の規則は[`../AGENTS.md`](../AGENTS.md)を正本とする。各profileのmodel、runtime identity、permission、token accounting、set / case、rating、Nなどの実効条件はprofile JSONを正とする。

状態列は索引用の要約であり、実測値、score、KPI、停止判断は[`click results`](../results/README.md)の各一次resultを正とする。

## runtime identity

profileの`agent_environment.runtime_identity_sha256`が指す共有runtimeは次の2 revisionである。runtime構成手順、`PYTHONPATH=src`などのgate運用規則は[`../AGENTS.md`](../AGENTS.md)を正本とし、各runがどちらのrevisionを固定したかはprofile JSONを正とする。

| revision | `runtime_identity_sha256` | 備考 |
| --- | --- | --- |
| r1 | `e591efde94b1b8cf5901a8e9d71857bbc2abe1740ca9a66eea92fbe2cae13c37` | 共有venvの`pip freeze --all`出力のSHA-256 |
| r2 | `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952` | r1へ`uv==0.11.32`を追加。Std14の全runはr2へ固定 |

## 現在のprofile

| profile_id | set | Case | N | B | M | 状態 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| [`click-control-free-f01-only-global-m24-n1-r1`](click-control-free-f01-only-global-m24-n1-r1.json) | `click-f01-only-r1` | 1 | 1 | 1 | 24 | execution前停止（token accounting宣言不足、result 0件） |
| [`click-control-free-f01-only-global-m24-n1-r2`](click-control-free-f01-only-global-m24-n1-r2.json) | `click-f01-only-r1` | 1 | 1 | 1 | 24 | P1-a完了（valid 1 / 1、score 4） |
| [`click-control-free-f01-only-global-m24-n5-r1`](click-control-free-f01-only-global-m24-n5-r1.json) | `click-f01-only-r1` | 1 | 5 | 3 | 24 | P1-b / P1-c完了（3 result、valid 15 / 15、全件score 4） |
| [`click-control-free-f02-only-global-m24-n3-r1`](click-control-free-f02-only-global-m24-n3-r1.json) | `click-f02-only-r1` | 1 | 3 | 1 | 24 | 完了（valid 3 / 3、全件score 4） |
| F03 / F04 / F05 / F05-OS / F06の各`only-global-m24-n3-r1` | 対応するonly set | 各1 | 3 | 1 | 24 | 完了（各3 / 3、全件score 4） |
| `click-control-free-f07-only-global-m24-n3-r1` | `click-f07-only-r1` | 1 | 3 | 1 | 24 | 実行済み・未rating（command evidence照合不能） |
| [`click-control-free-f07-only-global-m24-n3-r2`](click-control-free-f07-only-global-m24-n3-r2.json) | `click-f07-only-r2` | 1 | 3 | 1 | 24 | 完了（3 / 3 score 4） |
| `click-control-free-f07-p-only-global-m24-n3-r1` / `r2` | 対応するonly set | 各1 | 3 | 1 | 24 | 完了（各3 / 3 score 3） |
| [`click-control-free-f07-p-only-global-m24-n3-r3`](click-control-free-f07-p-only-global-m24-n3-r3.json) | `click-f07-p-only-r3` | 1 | 3 | 1 | 24 | 完了（3 / 3 score 4） |
| F08 / F10 / F10-R / A01 / A02の各`only-global-m24-n3-r1` | 対応するonly set | 各1 | 3 | 1 | 24 | 完了（各3 / 3、全件score 4） |
| [`click-control-free-standard14-global-m24-n5-r1`](click-control-free-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-c81-full-standard14-global-m24-n5-r1`](click-c81-full-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-control-free-reasoning-medium-standard14-global-m24-n5-r1`](click-control-free-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | Medium基準完了（70 / 70、全件score 4） |
| [`click-c81-full-reasoning-medium-standard14-global-m24-n5-r1`](click-c81-full-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | Medium水平比較完了（70 / 70、全件score 4） |
| [`click-no-agents-reasoning-medium-standard14-global-m24-n5-r1`](click-no-agents-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-repository-subagents-reasoning-medium-standard14-global-m24-n5-r1`](click-repository-subagents-reasoning-medium-standard14-global-m24-n5-r1.json) | `click-standard14-r1` | 14 | 5 | 1 | 24 | 完了（70 / 70、全件score 4） |
| [`click-no-agents-reasoning-medium-f10-authority-global-m24-n5-r1`](click-no-agents-reasoning-medium-f10-authority-global-m24-n5-r1.json) | `click-f10-authority-availability-r1` | 1 | 5 | 1 | 24 | 完了（5 / 5 valid、score 1 × 5） |
| [`click-repository-authority-reasoning-medium-f10-authority-global-m24-n5-r1`](click-repository-authority-reasoning-medium-f10-authority-global-m24-n5-r1.json) | `click-f10-authority-availability-r1` | 1 | 5 | 1 | 24 | 完了（5 / 5 valid、score 4 × 5） |
| [`click-no-agents-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-no-agents-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 65 / score 1 × 5） |
| [`click-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 70） |
| [`click-c81-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-c81-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 65 / score 1 × 5） |
| [`click-c81-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1`](click-c81-repository-authority-reasoning-medium-standard14-r2-global-m24-n5-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | 完了（70 / 70 valid、score 4 × 70） |
| [`click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-r1`](click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-r1.json) | `click-standard14-r2` | 14 | 5 | 1 | 24 | CLI 0.146.0で完了（70 / 70 valid、score 4 × 65 / score 1 × 5）。CLI 0.144.0のC81とは非互換 |

`B`はprofile fieldではなく、同一profileを変更せず独立resultとして反復した回数を表す。profileの存在や表の状態要約だけを評価完了の根拠にせず、該当する一次resultで確認する。
