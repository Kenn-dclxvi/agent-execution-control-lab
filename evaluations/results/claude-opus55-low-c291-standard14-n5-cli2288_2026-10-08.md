# C291のClaude Code Opus 5.5 low・Standard14 N=5計測（2026-10-08）

2026-10-08。利用者の指示で、C291をOpus 5.5の推論設定`low`で、全14ケース各5回、計70件測った。Opus 5.5のlowで測った保存済みの結果はなく、比較相手を持たない単独の計測である。**有効70件すべてが4点だった。品質中央値100、全エージェントトークン中央値877,620、経過時間中央値276.49秒。** 除外と再試行は0件だった。

## 条件

[C291 mediumのプロファイル](../profiles/c291-claude-opus55-medium-standard14-n5-cli2288-r1.json)から、次の3点だけを変えた（[今回のプロファイル](../profiles/c291-claude-opus55-low-standard14-n5-cli2288-r1.json)）。

- 推論設定を`low`にした。
- 起動時のプラグイン一覧を、実際の環境（`cc-plugin-telemetry@builtin`だけ）に合わせた。利用中のアカウントは組織に属さないため、`cc-plugin-sec-default@builtin`は読み込まれない。
- 利用者の判断で、契約プランを条件から外した。認証の条件は「claude.aiでのログイン、APIキーなし」だけである。

Claude Code 2.1.288、`claude-opus-5-5`、評価コード、採点契約、ケース、fixture、TaskSpecはmedium系列と同じである。評価セットとfixtureは、C280で固定したLayer 1を写して使った。発行前に1回だけ実際に起動し、起動時の環境がプロファイルと一致することを確かめた（[発行前の記録](claude-opus55-low-c291-standard14-n5-cli2288_2026-10-08-preflight.json)）。

C291のidentityは`the-caption-3ce91a4-validation-call-exit-r1`、bundle SHA-256は`08f2c5533dba68e004d1fb75cbbaf04aa34e69e36eff9e0b420bfad811f69a8e`である。日本時間2026-10-08 04:23:39〜04:26:31に一つの計画を実行した。発行は14件ずつの波を順に待つ方式（`wave_barrier`）で、medium系列の`global_queue`とは異なる。

## 結果

| 条件 | 4点 | 品質中央値 | 全エージェントトークン中央値 | 経過時間中央値 |
| --- | ---: | ---: | ---: | ---: |
| C291 low（今回） | 70 / 70 | 100.00 | 877,620 | 276.49秒 |

中央値は、14ケースを合算した各反復の値を5回分集計した値である。参考として、C291 medium（[計測記録](claude-opus55-c291-standard14-n5-cli2288_2026-10-08.md)）はトークン中央値1,143,211だった。ただし、推論設定、プラグイン一覧、発行方式、時刻、アカウントが異なり、互換キーも異なるため、両者の差をプロンプトや推論設定の効果としては比較しない。

## 機序の診断

[診断](claude-opus55-low-c291-standard14-n5-cli2288_2026-10-08-mechanism-diagnostics.json)は、[C290・C291のN=5診断](c290-c291-standard14-n5_2026-10-08-mechanism-diagnostics.json)と同じ抽出で集計した。

| 条件 | ルートの本文がツール出力に現れたrun | `src`の本文 | `tests`の本文 | 検証の呼び出し | 失敗した呼び出し | 終了コードのずれの候補 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C291 low | 8 / 70 | 28 | 15 | 69 | 0 | 0 |

lowでも、ルートの本文の再取得はmediumと同じく0件にはならなかった。検証の呼び出しの終了コードのずれは0件だった。

## 登録の記録

計測全体を[登録結果](7e868f2502c24a2eac3c09cd99388e42.json)として記録した。その前に、ランを1件ずつ登録しようとして、ケースごとの1ケースだけのプールが14個、登録簿に作られた。登録簿は追記専用のため残っているが、どの結果からも参照していない。このため、登録結果からラン単位の索引への取り込み（`import-result`）は、既存の記録と食い違って行えなかった。比較相手のない系列のため、ラン単位の集計は作っていない。

採用、追加反復、release、本体反映は行っていない。

## 一次アーティファクト

- [登録結果](7e868f2502c24a2eac3c09cd99388e42.json)・[品質監査](claude-opus55-low-c291-standard14-n5-cli2288_2026-10-08-quality-audit.json)
- [発行前の記録](claude-opus55-low-c291-standard14-n5-cli2288_2026-10-08-preflight.json)・[機序の診断](claude-opus55-low-c291-standard14-n5-cli2288_2026-10-08-mechanism-diagnostics.json)
