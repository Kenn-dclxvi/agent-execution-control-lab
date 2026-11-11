# FreeとC319 — Gemini 4 Argon Low、STD14 N=5

2026-11-11に、FreeとC319をそれぞれSTD14の14ケースで5回ずつ計測した。**本試験140件の実行、全エージェントの使用量確定、採点、集計、結果登録、最小容量保存、復元照合、作業コピー削除まで完了した。** 基盤確認として別途承認された単独実行1件と親子実行1件は、成績に含めない。

## 結果

各指標は14ケース合計の5反復に対する中央値で、括弧内は最小〜最大。品質は満点を100%とした値である。経過時間は各ケースで測った時間を足す。費用は[固定した標準API単価表](../price-tables/api-standard-2026-11-11.json)による換算額である。

| 指標 | Free | C319 | 中央値の差率 |
| --- | ---: | ---: | ---: |
| 品質 | 100.00%（98.21〜100.00） | 98.21%（98.21〜100.00） | -1.79% |
| 費用 | 1.2285051 USD（1.1791145〜1.2934928） | 0.9980612 USD（0.9273750〜1.0410728） | -18.76% |
| 経過時間 | 986.484 秒（895.204〜1,133.070） | 898.225 秒（754.862〜911.607） | -8.95% |
| 参考トークン数 | 1,690,292（1,516,752〜1,793,044） | 1,101,751（1,030,921〜1,226,030） | -34.82% |

70件の点数分布は、Freeが4点69件・3点1件、C319が4点67件・3点3件だった。3点はいずれもA02の「抽象的な試験成果を示す証拠」の不足で、Freeの第2反復、C319の第2・第3・第4反復に該当する。保存された[同一条件での比較](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-comparison.json)は5反復、対応する条件群1組を確認した。この固定STD14内の結果として扱い、採用や未評価条件への一般化は行わない。

## 固定した条件

- Gemini 4 Argon Low（`gemini-4-argon-low`）、推論設定`low`、Antigravity CLI `1.5.5`。実行ファイルと設定のSHA-256を固定した。
- [Freeのプロファイル](../profiles/free-gemini4-argon-low-standard14-n5-agy155-20261111-r1.json)と[C319のプロファイル](../profiles/c319-gemini4-argon-low-standard14-n5-agy155-20261111-r1.json)は同じ実行条件を持ち、既存のプロンプト識別値だけが異なる。
- 固定済みSTD14 r1のLayer 1を複製し、各70スロットの発行前確認を保存した。一つの待ち行列、並列上限24、既存のCPU使用率による発行制御を共通にした。
- [成果品質の採点契約](../rating-contracts/outcome-terminal-state-evidence-antigravity-collector-v1.json)はv14のケース規則を維持する。
- [計測基盤と実行手順](../../docs/gemini-argon-standard14-measurement.md)に、認証・個人設定・使用量・コマンド証拠の境界を記載した。

## 証跡の再収集

最初の収集では85件が有効、55件が計測失敗として除外された。50件は長いツール出力の省略を処理できず、5件は終了済みツールの`ERROR`状態を未完了と扱ったためである。モデルの実行自体はすべて終了していた。

[保存記録の照合処理](../../scripts/antigravity_saved_evidence.py)と[完全出力の再収集処理](../../scripts/recollect_antigravity_commands.py)で、会話・ステップ番号・モデル識別値・使用量・ツールの実行時刻を照合した。元の除外記録は変更せず、Freeの30件とC319の25件について、復元した証拠を持つ有効記録を追記した。[55件の再収集記録](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-recollection.json)は、元の記録のSHA-256、完全出力のSHA-256、処理コードのSHA-256、元の実測経過時間、追加のモデル呼び出しが0件であることを保持する。

選択した各70件は、発行した70サンプルと一対一で対応する。証跡の再収集でモデルを再実行せず、元の経過時間と使用量を使った。登録結果の`excluded_attempts`は選択した有効記録を対象とするため、最初の55件の除外履歴は再収集記録と保存済みの元の試験記録から確認する。

今後の実行用に[アダプタv2](../../scripts/run_antigravity_evaluation_v2.py)へ同じ収集修正を接続した。今回の140件は元のアダプタと保存記録の再照合による計測であり、v2による追加のモデル試験は実施していない。モデルに渡す課題文の同一性はテストで確認した。

## 一次アーティファクトと完了記録

### Free

登録ID: `819891d6b5c24e6494defe50381ea2f0`。内容SHA-256: `3a5aa92e371360bcbd5e1da0693f7e1a6efa8ec9788b7b2d52bee924c76d8d40`。

[登録結果](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-result.json)、[選択](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-selection.json)、[集計](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-analysis.json)、[採点](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-quality-audit.json)、[発行前確認](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-preflight.json)、[保存・復元照合・後片付けの完了記録](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-complete.json)。

### C319

登録ID: `3cb465b8be0d47dabc76418ec7a66be4`。内容SHA-256: `f5a570b713b2f166543eef4a9a5e596552971ca03f4bb4fbc80b0846374d5a45`。

[登録結果](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-result.json)、[選択](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-selection.json)、[集計](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-analysis.json)、[採点](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-quality-audit.json)、[発行前確認](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-preflight.json)、[保存・復元照合・後片付けの完了記録](free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-complete.json)。

両試験の`complete.json`は`status: complete`で、保護入力の不変確認と、全195個の作業コピー（元の140個と再収集用55個）の削除を確認した。共通環境と固定済みLayer 1の正本は保持した。
