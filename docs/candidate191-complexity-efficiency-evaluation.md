# Candidate191 複雑性・効率評価

> **結果**: `M8_completed / materially_larger_than_C147 / KPI_recorded / Standard14_mechanism_failed_reassessed / M9_not_ready`

## 結論

Candidate191はC147より明確に複雑で、Standard14とADR9のall-agent token中央値も高い。初回静的監査では増加部分を責務競合または安全に削除できる重複とは判定しなかったが、後続のケース別trace再集計により、C147の変更前共同発行を9 / 14ケースで退行させた機序不一致が判明した。

C147比ではroot `AGENTS.md`が`10,772 → 17,989 bytes`、`+7,217 bytes`、`+67.00%`となった。条項は`13 → 19`、明示的な`:=`定義は`9 → 28`である。これは小さな増加ではない。ただし、Candidate190で独立`OWNER_ROLE`を統合後削除した結果、Standard14の8件でowner metadataを不要review producerへ昇格した。今回残る境界の再記述を、同じ「重複削除」の形で圧縮する根拠はない。

Candidate191は変更せず、最適化Candidateも作らない。後続の[Standard14コスト機序再判定](candidate191-standard14-cost-mechanism-reassessment.md)によりM9 readyを撤回し、共同発行とconsumerなし開始観測の原因分析へ戻す。将来修正する場合は新しいprompt identityとし、影響するADR9・Standard14 gateを再実施する。

## 静的複雑性

| 指標 | C147 | Candidate191 | 差 |
|---|---:|---:|---:|
| 文字数 | 7,090 | 12,301 | `+5,211`（`+73.50%`） |
| UTF-8 bytes | 10,772 | 17,989 | `+7,217`（`+67.00%`） |
| top-level条項 | 13 | 19 | `+6`（`+46.15%`） |
| 明示`:=`定義 | 9 | 28 | `+19`（`+211.11%`） |
| 明示有限state domain | 1 | 5 | `+4` |
| state literal延べ数 | 3 | 15 | `+12` |

stateは構文上明示された有限domainだけを数えた。C147の`required_predicate_state`に対し、Candidate191ではそれに加えて`review_requirement`、`review_execution_permission`、observationの`terminal state`、review judgement result kindを持つ。boolean predicateのtrue/falseや散文中の`nonterminal`は水増しを避けるため数えていない。

19条項は共通execution core 12条項とreview固有7条項に分かれる。状態遷移の競合ownerは0件と判定した。owner metadata非権限化は`PRODUCER_BINDING`、`OWNER_ROLE`、`REVIEW_REQUIREMENT`から参照されるが、前者は一般producer選択、`OWNER_ROLE`はmetadataの非権限性、`REVIEW_REQUIREMENT`はreview適用と非適用時の効果を所有する。これは同じ遷移の複数所有ではなく、Candidate190の実失敗を閉じる接続guardである。

## Candidate191の3 KPI

| 評価系列 | run | quality中央値 | all-agent token中央値 | elapsed中央値 |
|---|---:|---:|---:|---:|
| ADR9 r2全9ケース N=5 | 45 | 100.0 | 1,410,389 | 921.670秒 |
| ADR05・ADR07・ADR09 N=20 | 60 | 100.0 | 550,016.5 | 373.550秒 |
| Standard14全14ケース N=5 | 70 | 100.0 | 1,875,286 | 932.726秒 |

M6は3ケース一組、M5は9ケース一組、M7は14ケース一組のiteration中央値なので、系列間の絶対値を比較しない。それぞれの登録result内の3 KPIをそのまま記載した。

## 互換系列内の記述比較

| 系列 | 比較相手 | token差 | elapsed差 | 境界 |
|---|---|---:|---:|---|
| Standard14 N=5 | C147 | `+427,660`（`+29.54%`） | `+80.183秒`（`+9.41%`） | 同じStandard14互換条件。ただしC147は訂正ADR9機序不通過 |
| Standard14 N=5 | C176 | `+225,727`（`+13.68%`） | `-25.661秒`（`-2.68%`） | 同じcompatibility key。C176の訂正機序監査は別途不通過 |
| ADR9 r2 N=5 | C176 | `+176,560`（`+14.31%`） | `+56.243秒`（`+6.50%`） | 同じcompatibility key。quality resultと訂正機序を一組で解釈 |
| ADR05・07・09 N=20 | Candidate190 | `-40,681.5`（`-6.89%`） | `-5.544秒`（`-1.46%`） | 同じ3ケース互換系列。Candidate190のM6は履歴上機序通過 |

Candidate191はC147より長く、Standard14のtokenとelapsedも高い。したがって「長文化してもruntime costは増えていない」とは言えない。一方、Candidate190から`OWNER_ROLE`を復元したCandidate191は、M6ではtokenとelapsedがともにわずかに低い。prompt bytesだけでruntime costを説明できないことも同時に確認できる。

## producer・command・recovery

| 評価系列 | review producer / child session | machine-bound command | nonzero result | 真正protocol違反 | environment recovery |
|---|---:|---:|---:|---:|---:|
| ADR9 r2 N=5 | 30 / 30 | 302 | 26 | 0 | 0 |
| ADR05・07・09 N=20 | 60 / 60 | 510 | 43 | 0 | 0 |
| Standard14 N=5 | 0 / 0 | 562 | 1 | 0 | 0 |

command件数は保存済みall-agent command evidenceの成功resultとnonzero resultを合算し、訂正監査でcollector誤検出と確定した記録を除いた。repository evidence、変更、validationを全runで完全に区別するlifecycle labelは保存されていないため、これはevidence invocationだけの純数ではなくmachine-bound command invocationの観測上限である。

ADR9のnonzero resultは主に`missing`等を表す観測結果であり、command evidence欠落やenvironment recoveryではない。Standard14の1件はA02の非必須read-only locator commandで、required validation、terminalまたはqualityへ影響していない。environment-only repairとsame required command rerunの組は3系列とも0件だった。

## 最適化系列との照合

Candidate188の`+58.47%`で問題だったのは増加率そのものではなく、C147の旧条項を削除しながら通常経路を外部の「C147由来」へ委譲し、worker contextとevidence責務を欠落・競合させた変換形式だった。Candidate191はfull bundleとして自己完結し、非変更targetを保持し、M5・M6・M7の完全性試験を通過している。

ただし、`+67.00%`のprompt量とStandard14 token `+29.54%`は採用上無視できない。安全に削除できるreview責務は0件だが、保存traceから共同発行の退行が確認された。短縮だけを目的に`OWNER_ROLE`等を統合せず、別の一変更軸として共同発行の優先関係とconsumerなし開始観測禁止を修正対象にする。

## 一次証拠

- [構造化M8監査](../evaluations/results/candidate191-explicit-review-operation-applicability-m8-complexity-efficiency-audit-r1.json)
- [Candidate191 ADR9 r2登録result](../evaluations/results/e599690689294c658b52a6a9e301697f.json)
- [Candidate191 M6登録result](../evaluations/results/43fa5e3f8fc54440ad36e849a6c91a59.json)
- [Candidate191 Standard14登録result](../evaluations/results/da6ada84ac07426d8c66dddddcb08fdc.json)
- [C147 Standard14 N=5結果](../evaluations/results/candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)
- [Standard14コスト機序再判定](../evaluations/results/candidate191-standard14-cost-mechanism-reassessment-r1.json)

## 状態

`M8_completed / complexity_materially_higher_than_C147 / C191_KPI_recorded / Standard14_token_higher_than_C147_and_C176 / Standard14_quality_passed_mechanism_failed_reassessed / no_safe_duplicate_deletion_selected / optimization_candidate_not_created / M9_not_ready / adoption_not_decided / release_not_created / projection_not_performed`
