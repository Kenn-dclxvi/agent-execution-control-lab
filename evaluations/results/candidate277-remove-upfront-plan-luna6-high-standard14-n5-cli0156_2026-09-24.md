# Candidate277 事前方針文削除・Standard14計測報告

## 結果

GPT-6 Luna High・Standard14・N=5で70 / 70件が有効、除外0件、全件Score `4`だった。C276の5行目を削除しても、C276に対するコストは下がらず、品質中央値を保った一方でトークン中央値と経過時間中央値が増加した。単一N=5の結果なので、5行目の因果効果を確定したとは言えない。

## 条件と証跡

- Candidate: `the-caption-3ce91a4-execution-control-no-upfront-plan-r1`（SHA-256 `2c7db261dffb9d45407433175e9c50208203d71c69fdd01095eb6d03010499ca`）
- 直接親 / 主比較: C276 result `9c659e7e0e0847beb97051fd23d92d94`
- Free参考比較: 保存済みControl-Free result `71a8231c6cc048d0a522aaa43d3a91b6`（再実行なし）
- 共通compatibility key: `d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`。preflightは70 slotを許可、C276と同一Layer 1・同一評価条件を使用。
- runtime: Codex CLI 0.156.1 / GPT-6 Luna High / all-agent token accounting v1
- Quality contract: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- C277 result: `6ae61524a1e34f8b8e97c677e0ad985d`
- 執行: 70 / 70 valid、除外0。品質採点可能70 / 70、Score `4`が70件。

## 全体中央値

| 指標 | C277 | C276 | C277 − C276 | Control-Free | C277 − Free |
|---|---:|---:|---:|---:|---:|
| 品質 / 100 | 100.00 | 100.00 | 0.00 pt | 92.86 | 7.14 pt |
| all-agent total_tokens | 2,659,295 | 2,525,590 | 133,705 (+5.29%) | 3,141,404 | -482,109 (-15.35%) |
| elapsed_seconds（秒） | 1,028.22 | 925.10 | 103.12 (+11.15%) | 1,043.65 | -15.43 (-1.48%) |

## Control-Freeとのケース別内訳

各ケースの中央値をN=5から算出した。差分率は`(C277 / 比較側 − 1) × 100`。負数はC277が少ないことを示す。C276との全ケース差分は同じJSONに記録した。

| ケース | C277 score | C277 tokens / 秒 | Free score | Free tokens / 秒 | tokens差 | elapsed差 | C276比 tokens / elapsed |
|---|---:|---:|---:|---:|---:|---:|---:|
| `TC-A01-LATENT-MODE-POLICY` | 4×5 | 96,718 / 37.5 | 0×5 | 443,240 / 98.2 | -78.2% | -61.8% | +29.8% / +51.8% |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 4×5 | 213,227 / 71.4 | 4×5 | 311,131 / 76.2 | -31.5% | -6.3% | -4.1% / -4.9% |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 4×5 | 198,508 / 68.6 | 4×5 | 228,850 / 66.0 | -13.3% | +3.9% | -18.5% / +2.0% |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 4×5 | 504,753 / 158.0 | 4×5 | 429,669 / 97.9 | +17.5% | +61.3% | +32.6% / +70.1% |
| `TC-F03-ATOMIC-CONTEXT-CLEANUP` | 4×5 | 157,970 / 77.2 | 4×5 | 207,635 / 71.1 | -23.9% | +8.6% | -20.0% / -14.3% |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 4×5 | 286,019 / 86.2 | 4×5 | 307,990 / 79.0 | -7.1% | +9.1% | +22.1% / +15.1% |
| `TC-F05-CLARIFY-UNITS-MODE` | 4×5 | 32,304 / 28.1 | 4×5 | 33,043 / 31.0 | -2.2% | -9.4% | -0.6% / +8.8% |
| `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | 4×5 | 51,597 / 35.5 | 4×5 | 77,502 / 32.5 | -33.4% | +9.3% | +0.5% / +12.1% |
| `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | 4×5 | 250,786 / 81.9 | 4×5 | 247,341 / 73.4 | +1.4% | +11.7% | +9.5% / +28.5% |
| `TC-F07-CANONICAL-V4-RUNNER` | 4×5 | 222,385 / 69.3 | 4×5 | 233,194 / 82.5 | -4.6% | -16.0% | -7.6% / -28.6% |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 4×5 | 159,361 / 68.9 | 4×5 | 173,869 / 66.6 | -8.3% | +3.4% | +2.3% / +11.2% |
| `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | 4×5 | 302,417 / 93.7 | 4×5 | 160,487 / 54.2 | +88.4% | +72.8% | +52.2% / +32.3% |
| `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | 4×5 | 194,166 / 64.6 | 4×5 | 216,802 / 90.2 | -10.4% | -28.4% | -9.3% / -12.6% |
| `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | 4×5 | 119,839 / 59.1 | 4×5 | 79,447 / 52.3 | +50.8% | +13.0% | +48.6% / -23.3% |

## 判定

C276比で品質中央値は100点を維持したが、all-agent token中央値は5.29%増、elapsed中央値は11.15%増えた。Free比では品質中央値が7.14ポイント高く、token中央値は15.35%少ない一方、elapsed中央値は1.48%少ない。したがって、この削除でC276のコスト増加が解消したという仮説は支持されない。Freeとの差は参考位置づけで、5行目単独の因果推定には使わない。

採用・release・runtime projection・本体反映はこの評価から判断していない。

## 保存先

- [C277 result](candidate277-remove-upfront-plan-luna6-high-standard14-n5-cli0156_2026-09-24.json)
- [品質audit](candidate277-remove-upfront-plan-luna6-high-standard14-n5-quality-audit-r1.json)
- [C277対C276比較](candidate277-candidate276-luna6-high-standard14-n5_2026-09-24.json)
- [C277対Control-Free比較](candidate277-control-free-luna6-high-standard14-n5_2026-09-24.json)
- [Freeケース別内訳](candidate277-control-free-case-breakdown-luna6-high-standard14-n5_2026-09-24.json)
- [設計記録](../../docs/candidate277-remove-upfront-plan-design.md)

注: execution sealのworkspace圧縮と採点用view作成は完了した。Codex project config cleanupはseal receiptでwarning（unexpected pruned workspace path）になったが、run validity、採点、result登録には影響していない。
