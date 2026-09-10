# agentic chat正常経路の実現可能性監査 r8

## 結論

r4–r7で残った固定toolとworker carrierの二経路は、評価対象外のruntime変更を加えず、固定TaskSpec、MCP tool identity、repository fixtureおよび既存trace projectionの範囲で一つの正常経路へbindできる。新しいcapability probeを一件だけ作成できる。

## 固定tool identity

r4のmodel-visible inputは短い`fetch_branch_counter_hours`を指定した。一方、0.146.0の既定MCP namespaceとリポジトリ内の既存contractは`mcp__<server>__<tool>`形式であり、このserverの完全identityは`mcp__branch_hours__fetch_branch_counter_hours`となる。r4 runnerのsynthetic test自身もこの完全identityを期待していた。

したがってr4のcall 0件を、固定toolがmodelから利用不能という証拠へ昇格させない。r8はmodel-visible TaskSpecとtrace oracleの両方を完全identityへbindする。非prefix公開設定は使わず、runtime既定の名前を変更しない。

## worker carrier

r3–r7は駐車場資料本文をrootのmodel-visible inputへ含めたため、root最終回答がworker resultへ依存していなかった。r8では資料本文を固定fixture fileとして評価workspaceへmaterializeし、root inputには相対pathだけを載せる。

- root: fixture fileのread禁止、packet構築、result binding、最終集約だけを担当
- worker: `fork_turns=none`で起動し、packetで許可されたfixture pathだけをread
- packet: task identity、allowed read path、質問、返却形式だけを含み、資料本文とtool recordを含めない
- oracle: root read 0件、worker read 1件以上、worker terminal result、root finalへの直接対応を別々に判定

rootとworkerは同じworkspace permissionを持つが、TaskSpec上のread permissionはproducer別に一意である。rootがfileを読めばprompt準拠の別正常経路ではなく明示違反となり、traceで検出できる。workerが読まなければ必要resultを合法に生成できない。

## r8の境界

r8はr3のcombined capability taskを置き換える新identityであり、r4–r7の失敗prompt、短いtool名、root-visible資料本文、JSON構文そのものを成果とするpacket条件を継承しない。保持するのはexact 0.146.0 runtime、モデル、reasoning、persisted session、write-once、retryなし、安全なprojectionおよび各diagnosticで確認済みのtrace selectorである。

合格した場合だけagentic target登録前設計を更新できる。失敗した場合は同じidentityを再試行せず、結果が示したpermissionまたはdependency境界だけを未解決として保持する。
