# C319・Fable 5.2 low・THE-CAPTION STD14 N=5の完了結果（2026-11-11）

C319を全14課題、各5回の計70件で実行し、採点・集計・正式な評価result登録まで完了した。**70件すべてが4点だった。** 同じ実行条件のFreeは67件が4点、A01の3件が0点であり、C319ではその3件に相当する失点が今回のN=5では出なかった。

## Freeとの比較

| 指標 | Freeの中央値（最小〜最大） | C319の中央値（最小〜最大） | 中央値の変化 |
| --- | ---: | ---: | ---: |
| 品質（0〜100） | 92.86（92.86〜100.00） | 100.00（100.00〜100.00） | +7.69% |
| 費用（API単価換算、USD） | 4.0235（3.8479〜4.1334） | 3.0694（2.8885〜3.3445） | -23.71% |
| 経過時間（秒） | 468.65（440.38〜474.51） | 391.29（380.08〜439.38） | -16.51% |
| 生のトークン（参考） | 1,145,815（1,118,226〜1,185,813） | 814,023（793,751〜895,167） | -28.96% |

各値は、1反復の14課題分を合算・集計した値から求めた5反復中央値である。品質は中央値で7.14ポイント上がり、費用は23.7%減、経過時間は16.5%減、生のトークンは29.0%減だった。品質の変化は、Freeの5反復の幅の上限と一致する。費用、時間、生のトークンのC319中央値はFreeの5反復の最小値より低かった。

経過時間は各runの時間を合計した値であり、並列待ち行列全体の所要時間や利用上限解除までの待ち時間を含まない。費用は固定したAPI単価表による換算で、契約プランの実請求額ではない。生のトークンはキャッシュ読み取り、書き込み、出力などを含む保存済み使用量であり、利用上限に達するまでの件数と同一視しない。

[公式の比較記録](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-free-comparison.json)は、FreeとC319を同じ単価表`api-standard-2026-11-10`で使用量の内訳から数え直したもの。比較元は[Freeの完了結果](free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed.md)。

## 全70件のトークン合計

途中の質問に対しては、双方で5件揃っていた10課題、計50件でC319が24.3%少ないと報告した。全14課題、70件が揃った合計は次のとおりで、C319が増えていたわけではない。

| 条件 | 70件の総トークン |
| --- | ---: |
| Free | 5,732,898 |
| C319 | 4,151,889 |

C319の70件合計はFree比27.6%少なかった。[使用量の内訳と参照元](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-token-comparison.json)を保存した。この合計と上表の「14課題分の5反復中央値」は異なる集計である。利用上限の制約でC319は3回、Freeは2回に分けて発行した。分割と計測時刻は実行履歴として残し、トークンや時間の補正は加えていない。

## 課題別の点数

| 課題 | C319の点数分布 |
| --- | --- |
| A01-LATENT-MODE-POLICY | 4点×5 |
| A02-REPOSITORY-RESOLVABLE-V4-ROUTING | 4点×5 |
| F01-DOMAIN-DUPLICATE-ASSET-KEY | 4点×5 |
| F02-CROSS-LAYER-HISTORY-DATE-BOUND | 4点×5 |
| F03-ATOMIC-CONTEXT-CLEANUP | 4点×5 |
| F04-WEB-AUDIT-COLUMN-VISIBILITY | 4点×5 |
| F05-CLARIFY-UNITS-MODE | 4点×5 |
| F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY | 4点×5 |
| F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT | 4点×5 |
| F07-CANONICAL-V4-RUNNER | 4点×5 |
| F07-DEPENDENCY-PROVENANCE-PAIR | 4点×5 |
| F08-CANONICAL-CLI-REFERENCE-SYNC | 4点×5 |
| F10-ENTRYPOINT-INVENTORY-REVIEW | 4点×5 |
| F10-MONTHLY-FORMAT-TEST-REVIEW | 4点×5 |

A01も5件すべて4点、A02およびF課題もすべて4点だった。この固定STD14、N=5の範囲での観測であり、未評価の課題やモデルへの一般化、採用、リリース、本体反映を意味しない。Candidate本文の変更や新しい制御の設計は行っていない。

## 固定条件

- モデル：`claude-fable-5-2`、推論設定`low`
- 対象：THE-CAPTION、commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- 評価セット：`the-caption-standard14-r1`、全14課題×5反復
- C319：`the-caption-3ce91a4-unconfirmed-location-search-r1`、bundle SHA-256 `516945120d2952c0508da76e715c7ea01446f9917175a0be0c0572ccfafb450c`
- Claude Code：2.1.317、固定実行ファイルSHA-256 `577c8ac6411ef57dd741e3c491e89f57ff6f42bb835a5ac5d4f496c29f14c5d5`
- 採点契約：`outcome-terminal-state-evidence-claude-collector-v2`
- 並列上限24、CPU負荷に応じた開始制御、同じ使用量・時間の数え方
- [プロファイル](../profiles/c319-claude-fable52-low-standard14-n5-cli2317-shellenv-20261110-r1.json)、[単価表](../price-tables/api-standard-2026-11-10.json)

プロファイル全体でFreeとの差分がプロファイル識別子とプロンプト識別子だけであることを、最初の実行前および最終保存時に確認した。全課題のTaskSpec SHA-256も一致している。ケース、fixture、採点、モデル、推論設定、Agent/runtime/CLI、permission、executor挙動と集計方法は変えていない。

## 利用上限による中断と再開

第1回で5件、第2回で47件を採点・独立登録した後、いずれも利用上限のため発行を停止した。第1回と第2回の保存済みbindingで確認した除外試行は計104件。これらは品質の失敗として数えていない。[中断時の記録](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-10.md)と途中経過JSONは書き換えず保持した。

第2回は利用者の指示で11月10日19:50まで待機して不足分を再開した。再び上限に達した後は、不足18件だけの第3回計画と発行前確認記録を保存した。11月11日00:50のリセット後、利用者の再開指示を受けて00:57以降に第3回を実行した。第3回は18／18件が有効、除外0件、待ち行列全体の経過時間は59.71秒だった。前の52件は再実行していない。

各回で保管場所から固定Layer 1を複製し、プロファイル、Layer 1、発行計画、全capsuleの一致を確認した。発行許可枠は70、65、18件で、外部失敗した枠の再計画を含む。最終的に選択・登録した有効runは重複のない70件である。

## 保存した証拠

- 正式result ID：`c89ca294f9b44dbca055b30da4879aa9`、[result](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-result.json)
- [選択した70件](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-selection.json)、[KPI集計](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-analysis.json)
- [3回分の採点と証拠の要約](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-quality-audit.json)
- [発行前確認の参照とSHA-256](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-preflight.json)
- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/c319-fable52-standard14-n5-cli2317-20261110-r1`
- 一次registry：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-shellenv-r1`

生の実行ログ、認証情報、実行作業木はリポジトリへ含めていない。

## 後続のFable 5.1との同単価比較（2026-11-11）

利用者の指摘を受け、C319同士でFable 5.1と5.2の費用を、値下げと使用量に分けて確認した。両方とも70件すべて4点だった。保存済み費用の中央値は5.1が3.7826 USD、5.2が3.0694 USDで18.9%低いが、5.2の単価は入力・キャッシュ読み取り・キャッシュ書き込み・出力のすべてが5.1より20%低い。

5.2の使用量を5.1の単価で数え直した中央値は3.8368 USDで、5.1の3.7826 USDより1.4%高かった。費用低下の主因は値下げであり、使用量による費用削減とは説明できない。全70件の総トークンは5.1比で30.0%少ないが、安価なキャッシュ読み取りが5,223,421から3,415,389へ減った一方、1時間キャッシュ書き込みは590,983から614,220へ、出力は107,402から121,614へ増えていた。

[同単価比較の記録](c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-fable51-same-price-comparison.json)に単価、使用量の内訳、5反復の再計算値、参照元のSHA-256を保存した。これはモデル・CLIの版と計測時刻が異なる保存済み観測値の補足比較であり、元のresultや単価表は変更していない。同モデルのFree対C319における費用23.7%減とは別の比較である。
