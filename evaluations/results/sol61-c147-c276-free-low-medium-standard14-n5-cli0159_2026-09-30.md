# GPT-6.1 SolのC147・C276・Control-Free比較（2026-09-30）

Standard14の14ケースを各5回、C147・C276・Control-Freeの推論設定low／mediumで計測した。6条件の計420件が有効で、各実行の専用`CODEX_HOME`に個人の指示ファイルがなく、開始時の設定ファイルが空であることを全件確認した。認証情報と固定したモデル一覧だけを渡し、ユーザー設定、rules、メモリーを無効にした。

| プロンプト | 推論設定 | Score 4 | 得点分布 | 品質中央値 | 全エージェントトークン中央値 | 所要時間中央値 |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| C147 | low | 70 / 70 | 4: 70件 | 100.00 | 1,493,465 | 739.33秒 |
| C147 | medium | 69 / 70 | 4: 69件、2: 1件 | 100.00 | 1,493,212 | 875.66秒 |
| C276 | low | 70 / 70 | 4: 70件 | 100.00 | 1,870,011 | 916.38秒 |
| C276 | medium | 70 / 70 | 4: 70件 | 100.00 | 2,263,288 | 1124.57秒 |
| Control-Free | low | 65 / 70 | 4: 65件、0: 5件 | 92.86 | 2,186,315 | 1034.67秒 |
| Control-Free | medium | 65 / 70 | 4: 65件、0: 5件 | 92.86 | 2,592,002 | 1251.60秒 |

C147 mediumのScore 2は依存関係の宣言と固定ファイルを更新するケースの1件。FreeのScore 0は両設定ともA01の5件で、禁止された試験操作を実行したためだった。
各中央値は14ケースを合算した反復ごとの値を5回分集計したもの。トークンは子エージェントを含む全エージェントの使用量であり、所要時間は既存の総所要時間指標を保持した。

## 条件の固定と個人指示の除外

モデルは`gpt-6.1-sol`、CLIは署名とハッシュを確認して保存した`0.159.0`、並列上限は24、採点はRating v14に固定した。既存のControl-Free GPT-6 Sol結果から固定された第1層だけを再利用し、ケース、fixture、TaskSpec、採点基準は変更していない。同じ推論設定の3条件はプロンプト以外の互換キーが一致する。lowとmediumは推論設定が異なる別の比較条件として扱う。

各実行は新しい専用`CODEX_HOME`を使い、`AGENTS.md`と`AGENTS.override.md`は作成せず、開始時の`config.toml`は0バイトとした。終了時の設定にはCLIが自動生成した当該作業場所の`trust_level=trusted`だけがあり、個人の設定や追加指示がないことも全件確認した。認証情報は実行終了後に削除した。通常利用の個人設定は変更していない。実行記録から全420件のモデル、CLI版、プロンプトハッシュと隔離状態を検証した。

CLI 0.156.1による初回試行はサービス側でモデルを拒否され、有効結果0件だった。発行を停止して証拠を別保存し、今回の品質・トークン・所要時間へ含めていない。0.159.0の独立した接続確認では応答と使用量を取得してから全6条件を開始した。

## 保存した比較

新しい6条件内だけで比較する。旧GPT-6結果とはモデルとCLIが異なるため、同一条件の比較値として扱わない。固定Standard14・各5回の観測であり、採用、release、本体反映を示さない。

- [C147とControl-Freeのlow比較](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c147-free-low-comparison.json)
- [C276とControl-Freeのlow比較](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c276-free-low-comparison.json)
- [C147とControl-Freeのmedium比較](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c147-free-medium-comparison.json)
- [C276とControl-Freeのmedium比較](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c276-free-medium-comparison.json)
- [C276とC147のlow比較](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c276-c147-low-comparison.json)
- [C276とC147のmedium比較](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c276-c147-medium-comparison.json)

一次集計は[機械可読記録](sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30.json)。非公開の事前照合、実行記録、隔離証拠、個別run索引と選択結果は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/sol61-c147-c276-free-low-medium-standard14-n5-20260930-r2`に保存した。
