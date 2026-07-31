# Candidate116 outcome / implementation boundary Rating v14 Medium A02 N=20

## 結論

Candidate116のA02を、既存atomic run 5件を再利用し、不足15件だけを追加して`N=20`へ拡張した。20 / 20件がvalid・rateable・score `4`で、canonical implementationとrequired validationを完了した。

一方、repository authorityと変更内容を明示的にbindした後、最初のartifact変更より前に追加commandへ再入する経路を5 / 20件で観測した。追加commandは合計7件で、既存5件では0件、新規15件では5件だった。開放条件となる`missing / unreadable / bind済みvalueまたはconstraintとの具体的矛盾 / allowed path内で充足不能 / 適用中instructionによる別authorityの明示`は、5件の再入前に観測していない。

この結果はCandidate116の品質失敗または採用判断ではない。次Candidateの作成根拠となる、変更前evidence operationのterminal境界に限定したmechanism診断である。

## Identity

- prompt identity: `the-caption-3ce91a4-outcome-implementation-boundary-r1`
- bundle SHA-256: `339f3f1153739e4dbafb288d16c3756b098d717a3d2563e50e3bd63fc7234d72`
- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- Evaluation set: `the-caption-standard14-r1` r1
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI: `0.146.0`
- Python: `3.14.5`
- permission: `approval_policy=never / sandbox=workspace-write`
- profile上の並列上限: `M=24`
- sample count: `N=20`
- atomic pool key: `71b41aa4790543a87477e22d67ad0ade05d55f840cde058c1b3740bc2a42d948`
- result ID: `5b891a79a63c48afad354388d2789af1`
- compatibility key: `68cb73405c97b19a021aabdb777b615f630d5dda2b3a2246d824e7947aae1a34`
- excluded attempt: 0件

内部campaign pathには準備時の作業呼称`b20`が残る。このpathはwrite-once履歴identityとして変更しない。正式な試行回数表記と結果解釈は`N=20`とする。

## KPI

| 指標 | Candidate116 A02 N=20 |
| --- | ---: |
| valid / rateable / score `4` | 20 / 20 |
| quality中央値 | 100.00 |
| token中央値 | 210,913.5 |
| elapsed中央値 | 86.232秒 |

## Mechanism判定

bind時点は、最初のfile changeより前のmodel messageが次の全項目を固定した時点とした。

1. canonical targetが`src.app.entrypoints.v4_daily_main`である。
2. `run.sh`の明示的な`v4|v`分岐が旧`daily_main`を参照することが故障原因である。
3. implementation dispositionが、そのmodule指定だけの置換である。
4. 周辺routingを保持する。

そのbind messageと最初のfile changeの間にcommand resultを一件でも受領した場合を、bind後・変更前再入とした。artifact変更後のvalidation identity探索は別operationとして集計対象から除外した。

| source | run数 | bind後・変更前再入 | command数 |
| --- | ---: | ---: | ---: |
| 既存atomic run | 5 | 0 | 0 |
| 新規不足run | 15 | 5 | 7 |
| 合計 | 20 | 5（25.00%） | 7 |

違反5件のrun IDは次のとおりである。

- `3b75281267c249b3bd774cff67cd848a`: 3 command
- `78771534961e4a04bf8f1146f9990f4a`: 1 command
- `c3d1e57427a641e59d1331d28548640c`: 1 command
- `e64d323eb65e4cae89cb6181309c91af`: 1 command
- `eaa1faa6aa7a4ef9a57f09a7a097d6b8`: 1 command

5件はいずれもbind済みtargetを変更しなかった。後続readは、既に引用したauthorityやentrypoint実体の再確認、または変更後に確定可能なvalidation identityの探索だった。

## 判断

Candidate116の`EVIDENCE_GATE`には、許可済みresultで変更predicateを判定できた時点で変更前evidence operationをterminalにする規則が既にある。しかし同一identity・互換条件の`N=20`で5件再現したため、semantic auditだけでなく保存traceにbindした次Candidate作成根拠が成立した。

次CandidateはCandidate116を直接親とし、C117の`implementation_authority_delegated`を継承しない。新しいauthority admission条件を追加せず、Candidate116の既存terminal句を、bind済み状態から未発行readを失効させartifact変更へ遷移する一つのpredicateへ置換する。

## 状態

- evaluation: `a02_n20_evaluated / quality_gate_passed / implementation_bind_terminal_route_reproduced`
- Candidate116 adoption: `not_decided`のまま
- release: `not_created`
- runtime projection: `not_projected`
- THE-CAPTION本体反映: 未実施
