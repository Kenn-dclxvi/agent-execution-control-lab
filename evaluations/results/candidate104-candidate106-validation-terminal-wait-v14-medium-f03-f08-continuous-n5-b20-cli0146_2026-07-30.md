# Candidate104 / Candidate106 validation terminal待機 Rating v14 Medium F03・F08 N=5 B20

## 結論

Candidate104とCandidate106を、F03正対象とF08負の対照について各20 batch、各batch `N=5`でmatched実行した。両promptの新規slotは各batchの同一global queueへ入れ、設定上の並列上限は`M=24`へ固定した。

両promptとも200 / 200件がvalid・rateable・score `4`で、excluded attemptは0件だった。品質gateは通過した。

一方、F03のfocused validation完了からfull validation完了までに途中messageを挟まなかったのはCandidate104の89 / 100に対し、Candidate106は99 / 100だった。Candidate106の残る1件はfocused validationがexit code `0`でterminalになり、同じwrapper内でfull validationを開始した後、wrapperのnonterminal返却とfull validationのterminal resultの間に進捗messageを挟んだ。失敗回復ではなく、Candidate106が閉じる対象経路の再発である。

事前に固定したzero-regression gateに従い、Candidate106を`targeted_f03_f08_b20_evaluated / quality_gate_passed / route_stability_gate_failed / cost_no_significant_difference / stopped`とする。Standard14 B20、採用、release、runtime projection、本体反映へ進めない。

## 実行条件

| 項目 | 固定値 |
| --- | --- |
| cases | `TC-F03-ATOMIC-CONTEXT-CLEANUP/r2`、`TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1` |
| prompt | Candidate104 / Candidate106 |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / Python | Codex CLI `0.146.0` / Python `3.14.5` |
| repetition | 各prompt・各case `N=5 × B20 = 100 run` |
| execution | 両prompt共通global queue、設定上の`M=24` |
| token | all-agent `total_tokens` v1 |
| compatibility key | `ebc96293b130a4b62fcc79248f6c31856980154d3c4684bd35d250df0ca11f3a` |

profileは[`Candidate104 F03/F08`](../profiles/candidate104-staged-evidence-admission-v14-reasoning-medium-f03-f08-global-m24-n5-cli0146-r1.json)と[`Candidate106 F03/F08`](../profiles/candidate106-compact-validation-terminal-wait-v14-reasoning-medium-f03-f08-global-m24-n5-cli0146-r1.json)である。prompt identity以外のcomparison conditionsは同一である。

## 品質結果

| prompt | valid / rateable | score 4 | excluded attempt |
| --- | ---: | ---: | ---: |
| Candidate104 | `200 / 200` | `200 / 200` | `0` |
| Candidate106 | `200 / 200` | `200 / 200` | `0` |

各batchはF03とF08を5件ずつ含む。20 / 20 batchで、両promptとも10 / 10件がscore `4`だった。

## F03機構結果

| 診断 | Candidate104 | Candidate106 |
| --- | ---: | ---: |
| focused validationを1回実行 | `100 / 100` | `100 / 100` |
| full validationを1回実行 | `100 / 100` | `100 / 100` |
| required validation間のmessageなし | `89 / 100` | `99 / 100` |
| agent message数中央値 | `5` | `5` |
| command数中央値 | `8` | `8` |

Candidate106の違反はBatch 15、run `db37cda875434f2abb2bf64d5c20c232`である。focused pytestはexit code `0`だった。同じcustom exec wrapperは続けて`bash scripts/dev/main_verify.sh`を開始したが、outerに明示した`yield_time_ms=1000`により`Script running with cell ID`をmodelへ返した。そのnonterminal返却後、full validationのterminal resultより先に「focused gate以降は同じ検証票内で進行中」とするmessageを返した。

したがって、Candidate106は経路頻度を11件から1件へ減らしたが、実行票をterminalまで閉じる制御を全件では成立させなかった。

後続の保存rollout分析では、Candidate104 / Candidate106の途中message全12件がouter `yield_time_ms=1000`と`Script running with cell ID`返却を伴い、短時間yieldなしの157件は途中message0件だった。詳細は[`Candidate106 F03 B20 short-yield経路分析`](../../docs/candidate106-f03-b20-short-yield-route-analysis.md)を参照する。

## KPI比較

各値は20個のbatch内`N=5`中央値の中央値である。差は`Candidate106 - Candidate104`である。

| scope | KPI | Candidate104 | Candidate106 | 差 |
| --- | --- | ---: | ---: | ---: |
| F03 | token | `113,938.0` | `114,046.5` | `+108.5`（`+0.10%`） |
| F03 | elapsed | `80.803`秒 | `82.618`秒 | `+1.815`秒（`+2.25%`） |
| F08 | token | `121,772.0` | `115,591.5` | `-6,180.5`（`-5.08%`） |
| F08 | elapsed | `80.677`秒 | `78.356`秒 | `-2.321`秒（`-2.88%`） |
| F03 + F08 | token | `245,911.5` | `234,746.5` | `-11,165.0`（`-4.54%`） |
| F03 + F08 | elapsed | `161.876`秒 | `161.380`秒 | `-0.496`秒（`-0.31%`） |

対応する20 batch中央値をpairとする二側正確Wilcoxon符号付順位検定を行った。tieには平均順位を使い、符号割当てを全列挙した。各scopeのtokenとelapsedを一つのfamilyとしてHolm補正し、`alpha=0.05`とした。

| scope | KPI | 対応差中央値 | raw p | Holm p | 判定 |
| --- | --- | ---: | ---: | ---: | --- |
| F03 | token | `-107.0` | `0.621513` | `0.697620` | 有意差なし |
| F03 | elapsed | `+3.520`秒 | `0.348810` | `0.697620` | 有意差なし |
| F08 | token | `-3,438.0` | `0.430433` | `0.860867` | 有意差なし |
| F08 | elapsed | `-1.790`秒 | `0.474905` | `0.860867` | 有意差なし |
| F03 + F08 | token | `-7,337.5` | `0.474905` | `0.949810` | 有意差なし |
| F03 + F08 | elapsed | `+2.080`秒 | `0.595819` | `0.949810` | 有意差なし |

したがって、F03でもF08でもCandidate106のcost差は統計的に確認できない。Standard14 N=5で観測したF08 token `+9.87%`は、今回のB20では方向が反転しており、固定的なprompt流入costとは支持されない。

## F08負の対照

F08では両promptともagent message数中央値`5`、command数中央値`13`だった。Candidate106の変更対象であるrequired validation間の待機はF08では発火しない。B20でtoken・elapsedの有意な悪化も観測しなかった。

この結果から、Candidate106の停止理由はF08へのcost流入ではなく、F03のzero-regression gateを1件満たさなかったことである。

## Result identity

- Candidate104 bundle SHA-256: `b25d13fb2f9d598adfae2359bd5cfbcef2591731d07e9165b1f9b3fc83e036b0`
- Candidate106 bundle SHA-256: `127e4246b1c0443c53b44aebcbda31cc3e63cf2a1a640769f47ee77adc8661e1`
- Batch 1 result ID: C104 `3a9ac2df8c3d41048c108b014b4df0df`、C106 `46e8df88d69a417c8ff6733caea48fa5`
- Batch 20 result ID: C104 `d5eb950127df4d6797be4dd9e3b34359`、C106 `2c7f993c7a0a4608b784d8c54e71c085`
- campaign summary SHA-256: `6d4b912b51dd43e7551f84afc6de20c214fc8e484d1d0234af699daa5889ab0c`
- analysis v2 SHA-256: `1914e51cd00ab87682fa1a70472a985455fc280819f1b0bd9213bad67a3e2bfa`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate104-candidate106-validation-terminal-wait-v14-medium-f03-f08-continuous-n5-b20-cli0146-20260730-r1`

raw run evidenceと20 batchの全result IDはverification checkoutへ保持し、このrepositoryへcommitしない。
