# Candidate278 C277残存規則削除・Standard14計測報告

## 結果

GPT-6 Luna High・Standard14・N=5で70 / 70件が有効、除外0件、採点可能70 / 70件で全件Score `4`だった。C277と比べ品質中央値は同じ100点で、all-agent `total_tokens`中央値は132,774（+4.99%）、`elapsed_seconds`中央値は56.89秒（+5.53%）増えた。これは同条件の一回のN=5比較であり、三規則の個別効果や一般的な因果を示すものではない。

## 条件と証跡

- Candidate: `the-caption-3ce91a4-execution-control-heading-only-r1`（Candidate278、bundle SHA-256 `9bf39dfe87d6315c199226c62d8fbf9eae359b16c3436d8229b8c08f842f9108`）
- 直接親 / 比較基準: C277 result `6ae61524a1e34f8b8e97c677e0ad985d`
- 共通compatibility key: `d72f0ae2d2d945c77bfab3ee51284db2dc8011fbc3072d096ecc3ca041fa304e`。事前照合receiptは70 slotを許可し、C277の固定条件・Layer 1を再利用した。
- 実行条件: GPT-6 Luna High、Codex CLI 0.156.1、Standard14 14ケース×5回、all-agent token accounting v1
- C278 result: `b4287d35640041e7bdf1e12ad1559e4b`
- 実行: 70 / 70 valid、除外0、採点可能70 / 70、Score `4`が70件
- 実行証拠archive: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate278-execution-control-heading-only-luna6-high-standard14-n5-cli0156-20260924-r1/compact/execution-evidence.tar.zst`（SHA-256 `066ac09f4cef05dcb408848ecdefc5f6e311340657aa5588fd933b6e0657b03d`）

## C277との全体中央値

| 指標 | C278 | C277 | C278 − C277 |
|---|---:|---:|---:|
| 品質 / 100 | 100.00 | 100.00 | 0.00 pt |
| all-agent `total_tokens` | 2,792,069 | 2,659,295 | 132,774 (+4.99%) |
| `elapsed_seconds` | 1,085.11 | 1,028.22 | 56.89 (+5.53%) |

## 判定範囲

この試験ではC277のroot `AGENTS.md` 3行目以降に残っていた三規則をまとめて削除した。差を個別規則へ帰属せず、経路の観測は診断情報として扱う。Standard14 N=5の品質は維持されたが、tokenとelapsedの中央値はいずれも増加した。採用・release・runtime projection・本体反映は判断していない。

## 保存先

- [C278 result](candidate278-execution-control-heading-only-luna6-high-standard14-n5-cli0156_2026-09-24.json)
- [品質audit](candidate278-execution-control-heading-only-luna6-high-standard14-n5-quality-audit-r1.json)
- [C277比較](candidate277-candidate278-luna6-high-standard14-n5_2026-09-24.json)
- [設計記録](../../docs/candidate278-remove-remaining-rules-design.md)
