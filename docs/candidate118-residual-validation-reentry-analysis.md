# Candidate118 residual validation reentry分析

## 結論

Candidate118で残ったStandard14のtoken増加は、Candidate118が追加したA02のimplementation bind terminal closureより、F02 / F03 / F06を中心とする変更後validationのnonterminal返却とmodel再入で説明するのが、保存済みtraceと過去試験に最も整合する。

ただし、現在保存されているprompt解決策をCandidate118へそのまま適用して採用候補にはできない。Candidate109はF03で対象経路とcostを改善したが、outer yieldというexecutor方法をpromptへ指定したため`prompt_design_boundary_failed`で停止済みである。Candidate110 / Candidate111のprompt境界は、terminal前model再入を確実には閉じなかった。

executor側のsuccess deliveryと透過interception probeは原因層を切り分ける過去の参考証拠であり、このrepositoryで実装または採用する候補ではない。したがって、現時点では新しいprompt Candidateを作らない。再開するのは、Candidate118の互換な保存traceで、modelが発行時点に観測できる条件だけにより同じ再入を閉じられる新しいprompt判断点が確認された場合に限る。

## Candidate118で見えた残差

Candidate116 / Candidate118 Standard14の選択済み各70 runを比較した診断値は次のとおりである。これらは3 KPIではなく、token差の帰属を調べるためのtrace診断である。

| 診断 | Candidate116 | Candidate118 | 差 |
| --- | ---: | ---: | ---: |
| token合計 | `7,990,833` | `8,743,556` | `+752,723`（`+9.42%`） |
| input token合計 | `7,835,316` | `8,592,753` | `+757,437`（`+9.67%`） |
| output token合計 | `155,517` | `150,803` | `-4,714`（`-3.03%`） |
| completed command | `604` | `593` | `-11` |
| root `wait` call | `4` | `22` | `+18` |

token増分はinput側にあり、outputとcommand件数は増えていない。case別token合計差はF02 `+241,050`、F03 `+226,480`、F06 `+145,107`である。この3 caseだけで`+612,637`となり、全増分の`81.4%`を占める。3 caseではmodel stepが合計14件増え、そのうち12件は追加されたwaitに対応した。

代表traceでは、validation wrapperがcell ID付きnonterminal resultを返した後、同じvalidationのterminal resultを得るためにmodelが再入した。F06では長い検証outputの後にdiff / statusを再取得する経路もあった。一方、F02 / F03の変更前commandはCandidate118で増えていない。Candidate118のprompt本文増分だけでも、上記のcase集中とstep増を説明できない。

以上から、原因候補を「validation成功rawの大きさ」だけに狭めない。直接観測された残差は、validation ticketがterminalになる前のmodel返却、その後のwait-only再入、および再入後に長い既存contextを再投入する経路である。

## 過去試験による裏付け

| 試験 | 保存済み観測 | 現在の判断 |
| --- | --- | --- |
| Candidate106 → Candidate107 Standard14 | token中央値`1,704,606 → 1,523,137`（`-10.65%`）。Candidate107はCandidate108よりwaitが少ない | costの下限を示すが、F03の長期試験でouter deadline違反が4 / 100件あり`stopped` |
| Candidate107 → Candidate108 Standard14 | wait `3 → 23`、token中央値`+15.75%`。token合計増分の`99.7%`はinput | terminal後だけ判断する規則でも、nonterminal返却を許すとwait再入costが残ることを支持 |
| Candidate108 → Candidate109 F03 `N=5` | terminal前model再入0 / 5、token`-15.97%`、elapsed`-16.43%` | 経路とcostは改善したが、outer yield最大値をpromptへ指定したため誤った設計層で停止 |
| Candidate108 → Candidate110 F03 `N=5` | terminal前model再入なし2 / 5 | 抽象的なdecision boundaryだけではexecutor返却を強制できない |
| Candidate108 → Candidate111 F03 `N=5` | terminal前model再入なし3 / 5。再入あり群のtoken中央値は再入なし群より`+16.50%` | model returnの抽象条件でも短時間returnの選択は残る |
| Success-silent delivery F02 `N=5` | token中央値`-17.86%`、合計`-21.60%` | 単一caseでは成功したが一般化不可 |
| Pytest exact allowlist F06 matched A/B `N=5` | model-visible output合計`-64.47%`に対し、model再入`22 → 31`、token中央値`+41.76%` | output抑制だけでは再入costを解決しない。wrapper方式は停止 |
| runtime shim / CLI hook probe | runtime shimはallowlist外Pythonの`sys.executable`を変更。CLI 0.146.0のhookはtool output置換を提供しない | 原因層の参考証拠。外部executor対応はこのrepositoryの候補範囲外 |

この系列は、C118の残差と同じevent sequenceを複数の独立した試験で支持する。一方で、現在利用可能な実装が品質、機構、設計層、costの全gateを同時に満たしたことは示していない。

## prompt-only目標token KPI

compatibility key `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`を持つRating v14、Medium、CLI 0.146.0、Standard14各`N=5`の一次resultを確認した。

| prompt | score 4 | token中央値 | 状態上の注意 |
| --- | ---: | ---: | --- |
| Candidate98 | `70 / 70` | `1,869,862` | 後続比較の基準 |
| Candidate104 | `70 / 70` | `1,748,721` | quality / targeted gate通過 |
| Candidate105 | `70 / 70` | `1,760,978` | terminal return不完全 |
| Candidate106 | `70 / 70` | `1,704,606` | 長期route stability gate失敗 |
| Candidate107 | `70 / 70` | `1,523,137` | 最小値だがouter deadline gate失敗、`stopped` |
| Candidate108 | `70 / 70` | `1,763,098` | mechanism通過、採用未判断 |
| Candidate116 | `70 / 70` | `1,599,779` | C118の直接比較相手、A02残差あり |
| Candidate117 | `70 / 70` | `1,792,124` | reentry spilloverで`stopped` |
| Candidate118 | `70 / 70` | `1,718,725` | A02 mechanism通過、token regression |

この互換集合の最小値はCandidate107の`1,523,137`である。Candidate118との差は`-195,588`、Candidate118から見た必要削減率は`11.38%`である。

Candidate107の比較はexecutor条件をCandidate106と固定し、promptだけを変更したものである。`all-agent token`はrootと起動されたWorkerを含むが、外部executor treatmentを含むという意味ではない。したがって`1,523,137`は、C118の品質とA02 mechanismを維持する次のprompt-only採用候補が到達を目指すtoken KPIとする。

Candidate107自体のouter deadline gate失敗は、この目標値を無効にしない。失敗が示すのはCandidate107の制御をそのまま採用できないことであり、同じ固定executor条件でpromptだけによりこのcost水準へ到達可能だった事実は残る。次候補は、quality、C118のA02 terminal closure、validation route stabilityをすべて維持したうえで、この値以下を目標にする。

## このrepositoryで次の採用候補を作るgate

次の候補は、次を事前に満たすprompt変更軸が保存traceから確認された場合だけ作る。

1. Candidate118 prompt、TaskSpec、fixture、rating、model、reasoning、permissionを維持する。
2. 変更するpredicateは、明示input、repository authority、model-visibleなmachine-bound resultから発行時点に判定できる一つに限定する。
3. wrapper、yield、wait、tool adapter、runtime hookなどのexecutor方法をpromptへ指定しない。
4. F02 / F03 / F06で、狙ったprompt判断がterminal前model再入を減らしたことをcandidate traceへbindする。
5. targeted gate通過後のStandard14で70 / 70 score `4`、Candidate118のA02 bind後・変更前再入0件を維持する。
6. Standard14 token中央値はCandidate107の`1,523,137`以下をprompt-only目標KPIとし、token合計もCandidate118より減らす。

現在の保存traceでは、Candidate110 / Candidate111がこのprompt-only境界を確実に成立させていない。新しいmodel-visible判断点も観測されていない。したがってcandidate bundleと評価profileを作らず、`prompt_control_not_demonstrated / candidate_not_created`で停止する。外部executor対応はこのrepositoryのbacklogへ追加しない。

## 一次参照

- [`Candidate116 / Candidate118 Standard14`](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [`Candidate106 / Candidate107 Standard14`](../evaluations/results/candidate106-candidate107-validation-wrapper-reentry-closure-v14-medium-standard14-atomic-n5-cli0146_2026-07-31.md)
- [`Candidate107 / Candidate108 Standard14`](../evaluations/results/candidate107-candidate108-validation-ticket-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [`Candidate108 / Candidate109 F03`](../evaluations/results/candidate108-candidate109-validation-ticket-outer-wait-closure-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md)
- [`Candidate110 F03`](../evaluations/results/candidate110-validation-ticket-decision-boundary-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md)
- [`Candidate111 F03`](../evaluations/results/candidate111-validation-ticket-model-return-boundary-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md)
- [`Success-silent delivery F02`](../evaluations/results/candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md)
- [`Success delivery executor F06 A/B`](../evaluations/results/candidate81-success-delivery-executor-ab-v14-medium-f06-n5_2026-07-29.md)
- [`Pytest allowlist success delivery設計`](pytest-allowlist-success-delivery-design.md)
