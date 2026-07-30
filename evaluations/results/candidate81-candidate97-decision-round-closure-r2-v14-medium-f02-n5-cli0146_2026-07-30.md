# Candidate81 / Candidate97 r2 decision round closure Rating v14 Medium F02 N=5

## 結論

Candidate97 r2はF02 r1、Rating v14、Medium、Codex CLI `0.146.0`、`N=5`で5 / 5件がvalid・rateable・score `4`だった。required command evidenceも5 / 5件で揃い、focused gateとfull gateは各run一回だった。

ただし、全5 runがfull gate成功後に別の`git status` commandを発行した。inspection command数もrunごとに分散し、同一model stepの一waveへ閉じたことを保存eventから証明できなかった。事前gateに従い、状態を`targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`とする。Standard14、B20、採用、release、本体反映へ進めない。

Candidate81との正式互換比較では、Candidate97 r2のtoken中央値は`+4.72%`、elapsed中央値は`+0.31%`だった。低elapsed側への分布移動は確認できず、Candidate97 r2の最大elapsedは`130.968秒`でCandidate81の`105.121秒`を上回った。

## r1停止境界

最初に作成した`the-caption-3ce91a4-decision-round-closure-r1`は、置換後の`DECISION_BOUNDARY`が631文字だった。F02 N=5 execution開始後、terminal resultが一件も得られる前に停止した。result registryへの登録は0件であり、r1を評価結果として扱わない。

r2は具体的なinspection / completion列挙を除き、規則本文を238文字へ縮めた。r1 bundleは履歴として保持し、in-placeでr2へ変更していない。

## 固定条件

| 項目 | 固定値 |
| --- | --- |
| case | `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` |
| evaluation set | `the-caption-planning-first-f02-r1` / `r1` |
| set identity | `9de3130e4252f338cb81ce7ae91d20c1ef9ce05f734360126d9087a5d3e06b4b` |
| Rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| Codex CLI / Python | `0.146.0` / `3.14.5` |
| repetition | `N=5`、iteration `1..5` |
| effective concurrency | `M=5` |
| compatibility key | `63e6b46dac29b2657732b7d6b69826abe2f5ffff28c480ed089f4b2e1e9e650b` |

Candidate81とCandidate97 r2のprofile差はprofile IDとprompt identityだけである。TaskSpec、case revision、fixture、required validation、rating、model、reasoning、CLI、permission、executor parameter、M / Nは変更していない。

## Identity

| prompt | bundle SHA-256 | result ID | result content SHA-256 |
| --- | --- | --- | --- |
| Candidate81 | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` | `fb33b8b1f6e048babeeb770d14484501` | `c7929d8476c07731b85aa377f5fe13d1b6352b86820c5f60b239fd6eb9e7dcd6` |
| Candidate97 r2 | `07f535a6e4f4d1b13731879ccd5bddfa3856b679b39bb7a14bc7da6ea01cbc23` | `08091993bb534269bd267b6ce2ad30c0` | `275f43cc8e53f7b35ec70ab0ac462b8b7541a9b2c9a420459b22ad34cb509d17` |

Candidate97 r2 execution archive SHA-256は`5061381a2d95d9da79d92b3b27b50a5f18b31eee3f42784e1f3608a273ed2908`である。excluded attemptと再試行は0件だった。

## KPI比較

| KPI | Candidate81 | Candidate97 r2 | 差 | 変化率 |
| --- | ---: | ---: | ---: | ---: |
| all-agent token中央値 | `290,587` | `304,304` | `+13,717` | `+4.72%` |
| elapsed中央値 | `97.937秒` | `98.245秒` | `+0.308秒` | `+0.31%` |
| all-agent token合計 | `1,541,931` | `1,501,150` | `-40,781` | `-2.64%` |
| elapsed合計 | `477.880秒` | `515.058秒` | `+37.178秒` | `+7.78%` |

N=5のtargeted観測であり、有意差または一般的な効率差を主張しない。mechanism gate不通過のため、KPIを採用判断へ使わない。

## 反復別結果

| iteration | token | elapsed | command | artifact変更前command | agent message | focused gate | full gate | full gate後command |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `304,304` | `92.202秒` | 7 | 3 | 6 | 1 | 1 | 1 |
| 2 | `320,258` | `130.968秒` | 13 | 8 | 6 | 1 | 1 | 1 |
| 3 | `275,151` | `98.669秒` | 17 | 12 | 6 | 1 | 1 | 1 |
| 4 | `292,104` | `98.245秒` | 12 | 8 | 6 | 1 | 1 | 1 |
| 5 | `309,333` | `94.974秒` | 9 | 5 | 6 | 1 | 1 | 1 |

full gate後commandは全件`git status`またはそれを含むstatus / diff commandだった。各runはその理由を「許可外driftなしの最終確認」と説明しており、理由なしの再確認ではない。しかしCandidate97 r2が狙ったのは、その既知completion evidenceをvalidation後の別decision roundへ残さないことである。5 / 5件で別roundが残ったためmechanism gateは不通過である。

artifact変更前commandは3件から12件まで分布した。command eventは個別に保存されたが、Codex event schemaにはmodel response identityがないため、複数commandが同一model stepから発行されたことを一次証拠としてbindできない。mechanismが証明不能な場合も通過扱いにしない。

## 判定

- quality: `passed`（5 / 5 score `4`）
- required command evidence: `passed`（5 / 5）
- full gate再実行抑制: `observed`（0 / 5再実行）
- completion decision-round closure: `failed`（full gate後command 5 / 5）
- inspection decision-round closure: `unproven`
- lower-tail control: `not_demonstrated`
- state: `targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`

Candidate97 r2へ追記して再試験しない。追加文面でmechanismを成立させようとすると、停止したr1の長文化へ戻るためである。新しいprompt Candidateを直ちに作る根拠もない。次に再開するには、同じ短い規則でcompletion evidenceをvalidation前にbindできたfresh trace、またはpromptが生成する短い実在wrapper形式の単発証拠が必要である。

## 状態境界

- Candidate97 r1: `execution_aborted_before_terminal_result / result_not_registered / stopped`
- Candidate97 r2: `targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`
- Standard14 / B20: 未実施
- adoption / release / projection: 未実施
- Candidate81: 採用・release・projection済み基準を維持
