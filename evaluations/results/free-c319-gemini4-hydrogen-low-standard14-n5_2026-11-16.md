# FreeとC319 — Gemini 4 Hydrogen Low、STD14 N=5

2026-11-16にFreeとC319をSTD14 r1の14ケースで5回ずつ、各70件・合計140件計測した。**実行、全エージェントの使用量確定、採点、集計、結果登録、最小容量保存、復元照合、作業コピー削除まで完了した。** 別途承認された基盤確認1件は成績に含めない。

## 結果

各指標は14ケース合計の5反復中央値、括弧内は最小〜最大。品質は満点を100%とした値である。経過時間は各ケースで測った時間を足す。費用は[固定単価表](../price-tables/api-standard-2026-11-16.json)による標準API換算額である。

| 指標 | Free | C319 | 中央値の差率 |
| --- | ---: | ---: | ---: |
| 品質 | 92.86%（87.50〜92.86） | 100.00%（92.86〜100.00） | +7.69% |
| 費用 | 0.9427266 USD（0.8694248〜0.9618518） | 0.8121325 USD（0.7666737〜0.9177800） | -13.85% |
| 経過時間 | 939.711 秒（839.178〜1,047.576） | 775.659 秒（726.217〜798.905） | -17.46% |
| 参考トークン数 | 1,580,374（1,418,787〜1,755,755） | 1,113,666（1,035,678〜1,379,668） | -29.53% |

点数分布はFreeが4点64件・1点1件・0点5件、C319が4点69件・0点1件だった。Freeの0点5件とC319の0点1件はいずれもA01で、変更後の値が未確定のままの変更と試験操作が採点理由に記録されている。Freeの1点1件はF10 Monthly第4反復で、所定の指摘要素の不足が採点理由に記録されている。C319の品質中央値100%と、A01に0点を1件観測したことを区別する。

[同一条件の比較](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-comparison.json)は5反復と条件群1組の対応を確認した。この固定STD14内の観測として扱い、採用や未評価条件への一般化は行わない。

## 固定条件と基盤対応

- モデルは`gemini-4-hydrogen-low`、推論設定`low`、Antigravity CLI `1.5.9`。実行ファイル、設定、コードのSHA-256を固定した。
- [Freeのプロファイル](../profiles/free-gemini4-hydrogen-low-standard14-n5-agy159-20261116-r1.json)と[C319のプロファイル](../profiles/c319-gemini4-hydrogen-low-standard14-n5-agy159-20261116-r1.json)は同じ条件を持ち、既存のプロンプト識別値だけが異なる。
- 固定済みLayer 1を複製して各70スロットの発行前照合を保存した。一つの待ち行列、並列上限24、既存のCPU使用率による発行制御を共通にした。
- 親と全子会話でHydrogen Lowのモデル識別値1527を照合し、他モデルを推定で計数しない。CLI 1.5.9の途中の子通知と完了記録を区別する。
- [既存の採点契約](../rating-contracts/outcome-terminal-state-evidence-antigravity-collector-v1.json)とケース、課題文、成果品質の規則を維持した。
- [基盤の説明](../../docs/gemini-hydrogen-standard14-measurement.md)に確認実行、単価、使用量の定義と保存条件を記載した。全テスト2,128件と2,209件の補助検証が成功した。

## 保存記録の再照合

最初の収集は各69件が有効で、FreeのA01とC319のF02各1件が記録の終端状態の照合で除外された。Freeの記録には引数不正で終了したツール呼び出しの`INVALID`状態があり、C319の記録にはDB上は完了している背景コマンドの表示が`RUNNING`のまま残っていた。

[再照合用の収集器](../../scripts/antigravity_completed_tasks.py)と[追記処理](../../scripts/recollect_antigravity_background_tasks.py)は、親子の使用量、固定したツール・権限、同一会話・ステップのDB上の完了状態、完全出力の参照先と終了コードを照合する。完全出力に日時がある場合は、コマンドの開始が外側のツール呼び出しと一致し、終了がその呼び出し区間内にあることを要求する。コマンド出力本文にある成功の文字列を終了状態に使わない。失敗したコマンドの終了コードもそのまま保持する。

元の除外記録、実測時間、使用量、サンプルの識別子を保持し、[再収集記録](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-recollection.json)を持つ有効な証拠を各1件追記した。モデルの追加実行は0件で、選択した各70件は最初に発行した70サンプルに一対一で対応する。再照合されたFreeのA01は0点、C319のF02は4点だった。登録結果の`excluded_attempts`は選択した有効記録を対象とし、元の除外履歴は再収集記録と保存済みの原記録から確認する。

実測時のコードは各試験の`execution-source/`、再照合時のコードは`recollection-source/`に保存し、プロファイルと再収集記録のコード識別値から追跡できる。実行中のコードを変更せず、再照合は140件のモデル実行が終了した後に行った。

## 一次アーティファクトと完了記録

### Free

登録ID: `c590ee051ae8473793eb190ef9401294`。内容SHA-256: `13509f97ca543ec9a40ec9bca0891fcaffa91945f73656f2ddf643cea8d25328`。

[登録結果](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-result.json)、[選択](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-selection.json)、[集計](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-analysis.json)、[採点](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-quality-audit.json)、[発行前確認](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-preflight.json)、[保存・復元照合・後片付けの完了記録](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-complete.json)。

### C319

登録ID: `3afd369b4447446e8101b4dfb60e700b`。内容SHA-256: `7661d55f60aef77d90f77d63bc01c53c162410be58f313fba47bd2669ffb106c`。

[登録結果](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-result.json)、[選択](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-selection.json)、[集計](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-analysis.json)、[採点](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-quality-audit.json)、[発行前確認](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-preflight.json)、[保存・復元照合・後片付けの完了記録](free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-complete.json)。

両試験の`complete.json`は`status: complete`で、保護入力の不変確認と142個の作業コピー（元の140個と再照合用2個）の削除を確認した。共通環境と固定済みLayer 1の正本は保持した。
