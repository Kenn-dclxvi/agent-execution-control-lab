# P002 VCC6 cost再進入原因監査

> [!IMPORTANT]
> **状態**: `completed / saved_trace_only / vcc6_unchanged / quality_preserved / mechanism_preserved / tokens_reduced / elapsed_regressed / model_generation_cost_isolated / duplicate_plan_rebinding_edge_identified / p002_not_adopted`
>
> 本書は保存済みVCC6 resultとprivate traceを読む原因監査である。新しい評価slot、Case、rating、runtime、Candidate、releaseまたはprojectionは作成していない。

## 結論

P002の経過時間増加は、validation commandの実行時間、command output量またはterminal response量の増加では説明できない。P002ではP001比でinput tokenが10.35%減った一方、生成output tokenが76.26%、reasoning tokenが57.53%増え、30組の対応run差では経過時間差との相関がそれぞれ`0.849`、`0.806`だった。

P002固有のprompt差には、既に`VALIDATION_PLAN`へ固定した順序、method、pass conditionおよびstop dependencyを、`VALIDATION_CARRIER_CODEX`の開始前にcarrier inputへ項目別に再bindする依存がある。同じblockの直前文は固定済みplan全体を一つのcarrier identityへ既にbindしているため、この項目別bindingはplanの意味をcarrier admission用に再構成できる重複辺である。

次の設計対象は、carrier、validation commandまたはterminal projectionの削除ではない。固定済みplan identityを構成fieldへ再分類、再構成または再bindするpermissionを閉じ、plan identityをそのままcarrierへ渡す関係である。必要なterminal evidence、documented result fieldおよびterminal schemaだけは、planと別責任のterminal projection contractとして開始前bindingを維持する。

## 固定した目的とアーティファクト関係

`task_objective`は次へ固定した。

- target改善系列: portable full-agent validation carrierのcost回復。
- required effect: VCC6でP002が成立させたvalidationの品質、途中result ingress閉鎖、依存先fail-fast、同一continuation identityおよびterminal一回投影を維持する。
- preserved effect: P001のvalidation以外の共通意味、81 primitive coverage、一枚の`AGENTS.md`配送およびplatform block分離を変えない。
- artifact間relation: P001を実装の直接基準、P002を成立効果とcost失敗の反例、C147をportable系列の比較参照、VCC6を変更しない固定benchmarkとして扱う。

P002はVCC6の事前cost gateに失敗したため、次Candidateの直接親または全文継承元にしない。

## 一次証拠

- result: [`vcc6-p001-p002-n5-comparison-r1`](../evaluations/targets/codex-validation-carrier-conformance/results/vcc6-p001-p002-n5-comparison-r1.json)
- result content identity: `eee1d9269290d908fdda5a4eeaf7ee1cbf3cfb88ecddb1380254b39060cb2cc1`
- comparison registration: [`vcc6-p001-p002-n5-comparison-registration-r1`](../evaluations/targets/codex-validation-carrier-conformance/registrations/vcc6-p001-p002-n5-comparison-registration-r1.json)
- fixed benchmark policy: [`vcc6-fixed-benchmark-policy-r1`](../evaluations/targets/codex-validation-carrier-conformance/registrations/vcc6-fixed-benchmark-policy-r1.json)
- P002 N=1で再利用した6 runのprivate root: `/Volumes/SN7100/_verification/codex-validation-carrier-p002-heldout-r1-n1-r1`
- paired N=5で新規発行した54 runのprivate root: `/Volumes/SN7100/_verification/vcc6-p001-p002-n5-r1`

private rootからは各runの`codex-events.jsonl`、`execution-observation.json`およびfixtureの`.carrier-events.log`だけを読み、raw traceはリポジトリへ転記していない。resultが持つ各evidenceのbytesとSHA-256は変更していない。

## 集計方法

60件のlogical slotを`arm / case_id / iteration`で対応付け、各`codex-events.jsonl`の`turn.completed.usage`、完了した`command_execution`、`agent_message`、`file_change`と、resultの`elapsed_seconds`を集計した。

- tokenと経過時間の主判定値は登録済みresultを使用した。
- `output_tokens`と`reasoning_output_tokens`は原因診断であり、第4のKPIまたは独立gateにしていない。
- 相関は30組の`P002 - P001`対応差に対するPearson相関であり、因果効果量として扱わない。
- Case固有literal、oracleまたはexpected resultをprompt設計入力へ使っていない。

## 全30 run合計

| 観測値 | P001 | P002 | 差 | 読み方 |
| --- | ---: | ---: | ---: | --- |
| all-agent `total_tokens` | 1,787,262 | 1,617,954 | -169,308（-9.47%） | 登録済みKPI。P002が減少 |
| `elapsed_seconds` | 806.972 | 893.449 | +86.477（+10.72%） | 登録済みKPI。P002が退行 |
| input tokens | 1,769,263 | 1,586,229 | -183,034（-10.35%） | input固定費の増加ではない |
| output tokens | 17,999 | 31,725 | +13,726（+76.26%） | 生成側の追加処理と対応 |
| reasoning output tokens | 7,730 | 12,177 | +4,447（+57.53%） | 生成側の追加処理と対応 |
| command完了数 | 45 | 46 | +1 | command数だけでは全体差を説明しない |
| command output bytes | 430,935 | 431,235 | +300（+0.07%） | raw command output量はほぼ同じ |
| terminalを含むagent message bytes | 14,545 | 13,240 | -1,305（-8.97%） | 最終応答の大型化ではない |
| `.carrier-events.log` bytes | 735 | 735 | 0 | Caseごとのvalidation実行記録量は同じ |

対応run差と経過時間差の相関は、output tokens `0.849`、reasoning output tokens `0.806`、command数`0.551`、command output bytes `0.069`だった。P002 arm内でも経過時間とoutput tokensの相関は`0.984`、reasoning output tokensは`0.892`だった。

## Case別の対応差

| Case | elapsed差 | total token差 | output token差 | reasoning差 | command数差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| VCC-H01 | -27.802秒 | -11,505 | -128 | +71 | -1 |
| VCC-H02 | +17.210秒 | -47,434 | +3,750 | +1,234 | +2 |
| VCC-H03 | +36.660秒 | -919 | +3,072 | +945 | -1 |
| VCC-H04 | +47.879秒 | -15,396 | +4,044 | +1,262 | +3 |
| VCC-H05 | -29.676秒 | -104,296 | +616 | +69 | -2 |
| VCC-H06 | +42.206秒 | +10,242 | +2,372 | +866 | 0 |

required validationがないH01では時間も短縮した。nonterminal continuationを持つH05も、P001の大きなinput再入削減が生成増を上回って短縮した。一方、通常success、terminal failure、dependency停止および必要fieldだけのterminal projectionを扱うH02、H03、H04、H06では生成量と時間がともに増えた。H06はcommand数差が0でも42.206秒増えたため、追加commandだけを原因または次の制御対象にしない。

## prompt上の未閉鎖辺

P002は次の三段階を持つ。

1. `VALIDATION_PLAN`がrequired validation、順序、個別method、pass condition、stop dependencyおよびterminal条件を固定する。
2. `VALIDATION_RESULT_CLOSURE`がplan全体と必要なmethod bindingをready条件にする。
3. `VALIDATION_CARRIER_CODEX`の第一文が固定済みplan全体を一つのcarrier execution identityへbindした後、第二文が同じvalidation identity、method、pass condition、stop dependencyをcarrier inputへ再び項目別にbindする。

第三段階の後半だけが、固定済みplanをcarrier用の別表現へ再構成できるdependency edgeである。これは次の二責任を一つへ混ぜている。

- 既に完了したplan semanticsをcarrierへ渡す責任。
- terminal evidence、documented result fieldおよびterminal schemaが観測可能かをcarrier開始前に閉じる責任。

前者はimmutableなplan identityを直接渡せば足りる。後者はP002の過剰投影防止に必要なので削除せず、独立したterminal projection contractとして保持する。

## 棄却した次案

- success runのcommand順、引用形式またはread有無をpromptへ転記する。
- Case別にcarrierを使うかモデルへ選ばせる。
- H02、H03、H04、H06だけを特別扱いする。
- terminal schema、必要evidenceまたはcapability preflightを削除して短くする。
- Codex CLI、tool adapter、runtime wrapperまたはVCC6 Caseを変更する。
- elapsedだけを再計測する、P002へ追加Nを発行する、またはP002をStandard14へ進める。

いずれも、成功手順の固定、自己分類、必要な正常境界の削除、prompt以外の変数変更、または固定済み停止条件の回避になるため採用しない。

## 次の許可範囲

次に許可するのは、P001を直接親とし、validation functional blockを一差分で置換するP003の作成前設計と静的反例監査である。P003 bundle、Profile、dispatch planおよび評価slotは、次を確認するまで作成しない。

1. immutable plan identityを直接渡すrouteで、項目別再bindがprompt準拠で実行不能になる。
2. terminal evidence、documented result field、terminal schemaおよび7 capabilityの開始前bindingを維持する。
3. fail-fast、continuation、terminal一回投影およびcarrier後fallback禁止を維持する。
4. VCC6のCase、fixture、TaskSpec、oracle、rating、runtime、token accountingおよび集計方法を変更しない。
