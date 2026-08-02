# Candidate125 / Candidate127 failed-change salvage評価結果

## 結論

Candidate127は、C125のF04低Score経路をpromptだけで解消した。F04初段N=5は5 / 5がscore `4`だった。5件すべてで最初のatomic patchが失敗した後、不一致の不要な`colSpan`変更を捨て、独立した必要変更`hasAuditKey`だけを一回のreworkで適用した。失敗後の追加read、二回目のrework、`colSpan`変更は0 / 5だった。

非回帰確認のF02 / F07各N=5も10 / 10がscore `4`で、必要な複数artifact変更を10 / 10で維持した。続くStandard14 N=5は14 case、70 / 70がscore `4`だった。score `3`以下の停止条件は一度も発生しなかった。

一方、互換C125 Standard14 N=5比で品質中央値は同じ`100`だが、all-agent token中央値は`+57,748`（`+4.12%`）、elapsed中央値は`+58.872秒`（`+6.96%`）だった。したがって現在状態は`targeted_f04_f02_f07_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / token_regressed / elapsed_regressed / result_registered / adoption_not_decided`とする。採用、release、本体投影は別判断であり未実施である。

## Candidate identityと比較条件

- candidate: `the-caption-3ce91a4-failed-change-salvage-r1`
- bundle SHA-256: `75d37043e6efbcb91bf4e097e80f38f88e73ca7e05d42273b71c172832d2eba9`
- direct parent: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`（Candidate125）
- changed target: root `AGENTS.md`
- changed rule: `RECOVERY`
- changed predicate: `failed_change_salvage_ready`
- evaluation set: `the-caption-standard14-r1` revision `r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured max workers: `M=24`
- Standard14 reference result: `ed8862d5b6af472da4247d39ef80075f`
- Standard14 compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`

各試験は、prompt identity以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、runtime、CLI、permission、executor挙動、token accountingを実行前に機械照合した。profileの`max_workers`は全試験で`24`に固定した。

## F04 targeted N=5

- candidate pool: `4537a670c81b64d5812054ca1db691bfa94dc388030ecc8c7b6ff6e7d3f30f35`
- selection: `8709260624fe4ab79a1438c3a78debd8`
- analysis: `f28345a76e7a41678eaee88743054821`
- valid / excluded / controller error: `5 / 0 / 0`
- score分布: score `4`が5件
- token中央値: `199,058`
- elapsed中央値: `119.984秒`

| mechanism | 結果 | gate |
|---|---:|---|
| 最初のartifact変更がatomic failure | 5 / 5 | 診断対象成立 |
| failure resultが変更未適用を示した | 5 / 5 | pass |
| 一回のreworkで独立した`hasAuditKey`変更を救済 | 5 / 5 | pass |
| 最終diffが`hasAuditKey`変更だけ | 5 / 5 | pass |
| 不要な`colSpan`変更 | 0 / 5 | pass |
| failure後の追加read | 0 / 5 | pass |
| `npm ci`、lint、buildがすべて成功 | 5 / 5 | pass |

ここでいう「atomic failure」は、複数hunkを一つのpatchとして適用し、一つでも現在内容と一致しなければpatch全体が適用されない状態である。Candidate127は失敗したhunkを書き換えて再試行せず、失敗前から正当性が確定していた独立hunkだけを残した。

mechanism audit v1は同義表現一件を数えられず4 / 5としたため履歴として保存した。修正版v2は語句ではなく実際の変更結果と操作列を確認し、上表の5 / 5を確定した。

## F02 / F07 preservation N=5

- candidate pool: `370510ed744c0c913eaf62e6bb7b7a1d422946ccdbdbae8d4e76a33bc3be9424`
- selection: `218ad94878be4456b1fdf800018447ec`
- analysis: `56e1cea6b2314d14a639976388b1547c`
- result: `d6c20ff3d5d04b6c98669c943466d5ca`
- valid / excluded / controller error: `10 / 0 / 0`
- score分布: score `4`が10件
- 2 case合算token中央値: `253,184`
- 2 case合算elapsed中央値: `145.342秒`

F02は5 / 5で`src/app/v4_engine.py`と`src/domain/collection_history_updater.py`を変更した。F07は5 / 5で`requirements.in`と`requirements.txt`を変更した。必要な複数変更単位を一つに減らす誤抑止は0 / 10だった。

preservation audit v1はF02の意図された初回失敗testもcommand failureとして数え、8 / 10とした。これは品質判定ではない。修正版v2は変更pathの保存だけをmechanismとして確認し、required commandの成否はRating v14へ委ねた。Rating v14は10 / 10をscore `4`とした。

## Standard14 N=5

F04の5件とF02 / F07の10件をatomic registryから再利用した。不足55件だけを新規発行し、55 / 55 valid、excluded 0、controller error 0だった。新規55件も全件score `4`だった。

- candidate pool: `4d77f6371d0d85720a49a1cda94f8349ee8706496342972307e88cb116c34422`
- selection: `b1591318d47241b0a0e234035a5a936f`
- analysis: `91f2aa8cb5e34657aea2299e38921a4a`
- result: `a68896817ee04d2c89aea18e243ae1e1`
- run count: `70`
- case count / N: `14 / 5`
- score分布: score `4`が70件

| KPI中央値 | Candidate125 | Candidate127 | 差 | 差率 |
|---|---:|---:|---:|---:|
| quality score | 100 | 100 | 0 | 0.00% |
| all-agent total tokens | 1,401,225 | 1,458,973 | +57,748 | +4.12% |
| elapsed seconds | 846.377 | 905.249 | +58.872 | +6.96% |

比較analysisはexecution stratum `8bfe05e33d5be7c99143a918b0542a49f18cb1c5ab57bf8b8cace5fcc704e56c`でmatched、sample countは両方5である。品質維持は確認できたが、N=5のcost上昇を効率改善とは扱わない。

## 中断した準備campaign

最初のStandard14準備campaign `...20260801-r1`はevaluation slotを0件も発行せず停止した。F02 / F07の採点済み10件をatomic registryへ登録する前にdispatch planを作ったため、再利用可能な10件を不足runとして含めたからである。

write-once dispatch planとLayer 1は上書きせず、停止記録とともに保存した。10件をregistryへ登録後、別identityの`...20260801-r2`でpreflightをやり直した。r2は既存15件を再利用し、不足55件だけを発行した。

## 判断

Candidate127は、C125の低Score原因を「最初のpatchを完全に防ぐ」問題ではなく、「実失敗後に正当性が残る独立変更を救う」問題として扱った。この視点ではF04の失敗5件を5件ともscore `4`へ戻し、C126で起きた変更前false stopも避けた。

ただしStandard14 N=5ではC125よりtokenとelapsedがともに増えた。品質・mechanism gate通過と採用判断を分ける。Candidate127の採用、release、本体投影は未決定のまま保持する。

## 後続stability追試

同日、F02 → F04 → F07 dependencyの順に各caseを24件ずつN=100まで延長する追試を実施した。最初のF02追加24件でscore `4 / 2 = 22 / 2`となったため停止した。既存5件を含むF02 N=29 resultは`4 / 2 = 27 / 2`である。F02の次batch、F04、F07は未発行であり、本書のStandard14 N=5結果は履歴上書きしない。詳細は[`F02 / F04 / F07逐次N=100追試停止結果`](candidate127-failed-change-salvage-v14-medium-f02-f04-f07-sequential-atomic-n100-stopped-at-f02-n29-cli0146_2026-08-01.md)を参照する。
