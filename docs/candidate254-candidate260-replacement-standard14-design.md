# Candidate254の採用判断に向けたStandard14再評価設計

## 結論

現在の判断対象は既存Candidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`である。Standard14の目的はCandidate260を置換することではなく、Candidate254を正式採用できるか、採用せず追加制御を検討するかを判断することである。

Candidate147はKPI比較基準であり、改善対象ではない。Candidate260は過剰な制限が正常経路と衝突した失敗履歴であり、Candidate254の親、改善対象または置換対象ではない。Candidate260の過剰な`EVIDENCE_GATE`冒頭一段落を除いたbyte列がCandidate254と一致したことは、Candidate261という重複案を作らずCandidate254の評価へ戻る契機にすぎない。

## 改善判断

| 項目 | Candidate254 F04 N=5 | Candidate260 F04 N=5 | 現在の判断 |
| --- | ---: | ---: | --- |
| Score `4` | 5 / 5 | 5 / 5 | 品質同値 |
| C147比token中央値 | `-2.23%` | `+16.49%` | Candidate254が改善方向 |
| C147比elapsed中央値 | `-19.53%` | `-28.69%` | 両方短縮方向 |
| C147正常な結果依存経路との整合 | 4 / 5 | 4 / 5 | 同じ観測範囲 |
| 正常な結果依存readの過剰な不通過 | なし | 3件を含む | Candidate260固有差分を除外 |

Candidate254の4 / 5という機序成立率をStandard14停止条件にはしない。この機序の不成立と品質再現性の喪失は100％対応しておらず、F04の5件はすべてScore `4`だったためである。方法が変わらない別step化1件はcost診断として保持し、read範囲、回数、tool順またはmodel stepをAIへ指定する修正へ変えない。

## Standard14実行前固定

| 項目 | 固定内容 |
| --- | --- |
| 対象prompt | 既存Candidate254、bundle SHA-256 `7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52` |
| 判断対象 | Candidate254を正式採用するか、採用せず追加制御を検討するか |
| 比較基準 | 保存済みCandidate147 Standard14 N=5 result `f7baeadc5bd44399ac13cc0e0a8aff48` |
| Evaluation set | `the-caption-standard14-r1` r1、14ケース各N=5 |
| 再利用 | Candidate254の保存済みF04 5件をatomic poolへ再利用し、不足13ケース各5件だけを発行する |
| model / reasoning | `gpt-5.6-sol / medium` |
| runtime | Codex CLI 0.146.0、Python 3.14.5 |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| permission | `workspace-write / never` |
| configured M | 24 |
| token accounting | all-agent v1 |
| 品質条件 | 70 / 70 validかつrateable、70 / 70 Score `4`。個別の低Scoreを中央値で相殺しない |
| 機序の扱い | 品質と分離した診断。全件成立をStandard14停止条件にしない |
| cost判断 | 品質維持後、C147比でtokenとelapsedがともに減れば改善方向。片方が増えた場合は必要処理との対応をtrace監査し、未説明なら`unjustified_cost_regression` |
| 停止境界 | Standard14 result、品質監査、3 KPI比較を固定した時点で停止。採用、release、projectionは別判断 |

## Candidate261を作成しない理由

Candidate260から過剰な`EVIDENCE_GATE`冒頭を除いた結果はCandidate254と同一byteである。同じprompt contentへ新しいCandidate番号を付けると、内容差がないのに別案が存在するように見える。改善作業は新番号の作成ではなく、保存済みCandidate254の評価範囲を現在の判断規則で拡張する。

Standard14は70 / 70件Score `4`で品質を維持したが、Candidate147比でtoken `+6.29%`、経過時間`-4.26%`だった。token増加を必要処理として正当化できないため、Candidate254の正式採用を承認せず、追加制御の根拠を調べる側へ判断する。詳細は[Standard14 token退行原因監査](candidate254-candidate147-standard14-token-regression-causal-audit.md)へ固定する。

現在状態は`candidate254_adoption_decision_completed / duplicate_candidate261_not_created / standard14_completed / quality_passed / unjustified_token_regression / candidate254_adoption_not_approved / additional_control_evidence_not_yet_bound / release_not_created / projection_not_performed`とする。発行前の照合結果は[Standard14 N=5実行準備監査](candidate254-candidate260-replacement-standard14-n5-execution-preparation-audit.md)へ固定する。ファイル名に残る`candidate260-replacement`は作成時の誤った位置づけを示す履歴名であり、現在判断を表さない。
