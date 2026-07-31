# Candidate118 / Candidate122 prechange evidence wave closure Rating v14 Medium Standard14 atomic reuse N=5

## 結論

Candidate122は正式なStandard14 token目標へ到達したが、品質gateで停止する。

Standard14 14 case × 5件は70 / 70 valid、score `4 / 2 = 69 / 1`だった。token中央値は`1,403,840`で、目標としたCandidate107の`1,523,137`を`119,297`（`7.83%`）下回った。elapsed中央値も`823.020秒`でCandidate107を`122.476秒`（`12.95%`）下回った。

一方、F04の1件は最初の`App.tsx`取得範囲に表描画部分が含まれなかった後、C122のone-wave terminal条件を理由に追加readを行わず停止した。required成果と3つのNode validationが欠落し、Rating v14 score `2`となった。したがって、aggregate quality中央値`100.000`やtoken目標達成を採用根拠にしない。

現在状態は`standard14_evaluated / token_target_passed / elapsed_below_candidate107 / quality_gate_failed / f04_incomplete_content_false_stop / result_registered / stopped`とする。採用、release、runtime projection、本体反映へ進めない。

## Identityとcoverage

- Candidate122 prompt: `the-caption-3ce91a4-prechange-evidence-wave-closure-r1`
- bundle SHA-256: `5b7525ec265ea10f207a3b23f0bbf749f677554aad1c2fa0c5beae0c41e0d2d3`
- profile: `candidate122-prechange-evidence-wave-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- reference Candidate118 result: `ed8862d5b6af472da4247d39ef80075f`
- Candidate122 pool: `a37730ec2c09e294e3364f6cfb50bf539bf8f522dc14eabe1e94e734b7a46384`
- reused atomic runs: A01 / A02 / F01 / F02各5件、計20件
- newly executed atomic runs: 残り10 case各5件、計50件
- execution: 新規50 / 50 valid、excluded 0
- Candidate122 selection: `e86445de03d246a58982b3ae6e07cf8e`
- Candidate122 analysis: `4933531a14b8472cb7ebef4dee13f3b3`
- Candidate122 result: `761ee9908f0046e0a448abed4aad8a89`
- execution archive SHA-256: `64af97fbe62b16fcc4acc62fc578f080d0db3e6b1d5f82d9fc05670eec9bcb85`
- final compact archive SHA-256: `4c96ac7326ac244ef569b32554b718dc27804fca2562930c6670d6e8ff027fbd`

## KPI

| 比較 | quality中央値差 | token中央値差 | elapsed中央値差 |
|---|---:|---:|---:|
| Candidate122 - Candidate107 | `0.000` | `-119,297`（`-7.83%`） | `-122.476秒`（`-12.95%`） |
| Candidate122 - Candidate118 | `0.000` | `-314,885`（`-18.32%`） | `-18.627秒`（`-2.21%`） |

quality中央値差`0.000`は、70件中1件のscore `2`を隠す。quality gateは件数で判定し、不通過である。

## F04失敗の事実

失敗runは`996248c6c2e54f259281a4804ac278fa`である。

1. 開始identity、root `AGENTS.md`、`App.tsx` 1〜320行、`package.json`、`package-lock.json`を一つのcommandで取得した。
2. `App.tsx`の表描画と`colSpan`は取得範囲外だった。
3. agentは「追加の変更前evidence取得は許可されない」と判断した。
4. `App.tsx`を変更せず、`npm ci`、`npm run lint`、`npm run build`を実行せずterminalにした。

これはenvironment failureではない。TaskSpecの開始状態は正常で、必要fileもread可能だった。C122が`prechange_evidence_wave_ready=true`のresultでpredicateをbindできない場合を、取得範囲の不足とrepository上の`missing / unreadable`に分けずterminal stopへ閉じたことが直接原因である。

## 成功traceとの比較

F04の成功4件のうち3件は、最初のbounded `sed`で表部分が範囲外だった後、同じ`App.tsx`の後半を追加readしてから変更した。残る1件は最初の1〜260行だけで故障点を確定し、既存の共通boolean構造を保持して変更した。

| 経路 | 件数 | quality |
|---|---:|---:|
| 初回bounded contentだけで変更predicateをbind | 1 | score `4` |
| 初回範囲不足を同じtargetのcontinuation readで補完 | 3 | score `4` |
| 初回範囲不足をterminal missingと誤分類 | 1 | score `2` |

C107のF04 5件は全件score `4`で、必要に応じて後半rangeまたは`rg -C`で`hasAuditKey / Audit Key / colSpan`を補足した。よって、C107との差は「追加readが常に不要」ではない。必要criteriaの未観測を、target不存在やread不能と同じ停止理由へまとめないことがC122に不足している。

## 次仮説

次候補はC122をそのまま採用せず、C122を直接親としてincomplete contentだけを扱う。

`prechange_wave_complete := admission済みtargetの取得成功だけでなく、変更predicateと保持constraintに必要なTaskSpec criterionがresult内で観測済み`

`prechange_wave_complete=false`かつtargetが存在しread可能で、未観測criterionと同じtargetの未取得rangeまたはsymbol locatorを一意にbindできる場合だけ、そのtargetへのcontinuation evidenceを一件許可する。新しいtarget、一般的安全確認、method探索は開かない。`missing / unreadable / contradiction / unsatisfied constraint`は従来どおり停止する。

初回gateはF04とF02各`N=5`を最低範囲とする。F04 5 / 5 score `4`とfalse stop 0 / 5、F02 5 / 5 score `4`、content wave 5 / 5、token中央値`173,000`以下を同時に要求する。
