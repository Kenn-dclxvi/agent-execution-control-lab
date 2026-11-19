# agent-execution-control-lab

THE-CAPTIONの開発課題を使い、AIエージェントへの指示が成果の品質、実行経路、費用、所要時間にどう影響するかを調べるリポジトリです。

## THE-CAPTIONのSTD14計測結果

Freeはルートに実行指示を置かない比較条件です。C319はルートに6行の汎用指示を、C324は5項の実行制御を置きます。各条件でディレクトリごとの指示を使います。C324は2026年11月18日に正式リリースし、個人用Codexの共通指示に適用しました。[C319の本文](prompts/releases/the-caption-3ce91a4-unconfirmed-location-search-release-r1/files/AGENTS.md.txt)・[C324の本文](prompts/releases/the-caption-3ce91a4-without-investigation-rule-release-r1/files/AGENTS.md.txt)・[C324のリリース記録](prompts/releases/the-caption-3ce91a4-without-investigation-rule-release-r1/README.md)

各行は同じ14課題を5回ずつ実行した70件です。実測トークン数は、各試験で記録した全エージェント分の使用量です。トークン数・費用・時間は、14課題分の合計を5組作ったときの中央値です。実行環境やモデルが異なる行には、それぞれの実行条件で観測した値を載せています。

「A02 自力／満点」は、起動先を聞き返さずに特定して修復へ進んだ件数と、周辺への影響・検証まで含めて4点だった件数です（各5件）。A02にはv15の行動基準を適用し、ほかの13課題は登録時の点数を用いています。[採点契約](evaluations/rating-contracts/README.md)・[A02の再採点記録](evaluations/results/a02-r2-behavioral-rescore-v1.md)

| 実行環境 | モデル・推論設定 | 条件 | 点数分布（70件） | A02 自力／満点 | 実測トークン数（参考値） | API換算費用（USD） | 実行時間（秒・参考値） |
|---|---|---|---|---:|---:|---:|---:|
| Codex CLI | GPT-6.2 Sol Low | Free | 4点64件・2点1件・0点5件 | 5／4 | 2,363,259 | 0.9397 | 615.97 |
| Codex CLI | GPT-6.2 Sol Low | C324 | 4点70件 | 5／5 | 1,719,316 | 0.6918 | 477.95 |
| Codex CLI | GPT-6.2 Astra Low | Free | 4点67件・0点3件 | 5／5 | 1,859,240 | 2.4488 | 974.80 |
| Codex CLI | GPT-6.2 Astra Low | C324 | 4点70件 | 5／5 | 1,525,168 | 2.1173 | 590.28 |
| Codex CLI | GPT-6.1 Sol Low | Free | 4点69件・0点1件 | 5／5 | 2,218,847 | 0.9344 | 636.90 |
| Codex CLI | GPT-6.0 Astra Low | Free | 4点67件・3点1件・0点2件 | 5／4 | 2,256,298 | 6.1484 | 634.75 |
| Codex CLI | GPT-6.1 Terra Low | Free | 4点67件・0点3件 | 5／5 | 2,198,845 | 0.4336 | 410.50 |
| Codex CLI | GPT-6.1 Terra medium | Free | 4点67件・0点3件 | 5／5 | 2,656,589 | 0.5033 | 382.51 |
| Codex CLI | GPT-6.1 Terra high | Free | 4点67件・0点3件 | 5／5 | 2,749,764 | 0.5044 | 442.42 |
| Antigravity CLI | Gemini 4 Neon Low | [Free](evaluations/results/20e70e57abd9480dbc4bc14726077cf6.json) | 4点65件・0点5件 | 5／5 | 1,635,453 | 2.7718 | 1,567.13 |
| Antigravity CLI | Gemini 4 Neon Low | [C324](evaluations/results/42c68b19f02844a1a33102b68b16d335.json) | 4点70件 | 5／5 | 1,077,967 | 2.3655 | 1,259.13 |
| Antigravity CLI | Gemini 4 Argon Low | [Free](evaluations/results/free-c319-gemini4-argon-low-standard14-n5_2026-11-11-free-result.json) | 4点70件 | 5／5 | 1,690,292 | 1.2285 | 986.48 |
| Antigravity CLI | Gemini 4 Argon Low | [C319](evaluations/results/free-c319-gemini4-argon-low-standard14-n5_2026-11-11-c319-result.json) | 4点70件 | 5／5 | 1,101,751 | 0.9981 | 898.23 |
| Antigravity CLI | Gemini 4 Hydrogen Low | [Free](evaluations/results/free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-free-result.json) | 4点64件・1点1件・0点5件 | 5／5 | 1,580,374 | 0.9427 | 939.71 |
| Antigravity CLI | Gemini 4 Hydrogen Low | [C319](evaluations/results/free-c319-gemini4-hydrogen-low-standard14-n5_2026-11-16-c319-result.json) | 4点69件・0点1件 | 5／5 | 1,113,666 | 0.8121 | 775.66 |
| Claude Code | Sonnet 5.5 Low | [Free](evaluations/results/be6db20a751a4c7f92fc905ebba9773e.json) | 4点65件・0点5件 | 5／5 | 859,525 | 0.6997 | 249.24 |
| Claude Code | Sonnet 5.5 Low | [C319](evaluations/results/c319-four-models-standard14-n5_2026-10-15.md) | 4点70件 | 5／5 | 786,811 | 0.6321 | 264.53 |
| Claude Code | Opus 5.5 Low | [Free](evaluations/results/616b1cf5c6ed46e8bc40f0a36f944cb2.json) | 4点69件・0点1件 | 5／5 | 750,215 | 1.2731 | 269.41 |
| Claude Code | Opus 5.5 Low | [C319](evaluations/results/c319-four-models-standard14-n5_2026-10-15.md) | 4点70件 | 5／5 | 712,222 | 1.1275 | 257.93 |
| Claude Code | Fable 5.1 Low | Free | 4点65件・0点5件 | 5／5 | 1,425,105 | 4.3717 | 558.25 |
| Claude Code | Fable 5.1 Low | [C319](evaluations/results/c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11-fable51-same-price-comparison.json) | 4点70件 | 5／5 | 1,198,335 | 3.7826 | 480.39 |
| Claude Code | Fable 5.2 Low | [Free](evaluations/results/free-claude-fable52-low-standard14-n5-cli2317_2026-11-10-completed.md) | 4点67件・0点3件 | 5／5 | 1,145,815 | 4.0235 | 468.65 |
| Claude Code | Fable 5.2 Low | [C319](evaluations/results/c319-claude-fable52-low-standard14-n5-cli2317_2026-11-11.md) | 4点70件 | 5／5 | 814,023 | 3.0694 | 391.29 |

GPT-6.2 Lowでは、C324の満点がSolでFreeより6件、Astraで3件多くなりました。A01ではFreeのSolが5件、Astraが3件、変更先が未確定のまま進んで0点でした。C324では両モデルとも5件すべてで開始状態だけを確認し、変更先を利用者に質問しました。FreeのSolに残るA02の失点は、明示的な空引数の扱いを変えた1件です。AstraのFreeは11月19日の再計測結果です。[AstraのFree再計測](evaluations/results/free-astra62-low-standard14-n5_2026-11-19.md)

C324のSolは登録時のv14で68件が4点、2件が1点でした。この2件は引数なしの場合だけ `shift` を省き、正規の起動先・周辺経路を保って検証も完了したため、v15では4点です。[C324のSol実行記録](evaluations/results/c324-sol62-low-standard14-n5_2026-11-18.md)・[C324のAstra実行記録](evaluations/results/c324-astra62-low-standard14-n5_2026-11-18.md)

Gemini 4 Neon LowのA02は、保存済みの証跡をv15で確認し、FreeとC324の両方で5件すべてが4点でした。Freeの0点5件はすべてA01で、C324は全70件が4点でした。14課題分のAPI換算費用の中央値は、Freeの2.7718 USDからC324の2.3655 USDへ14.66%下がりました。[Neon Lowの比較報告](evaluations/results/free-c324-gemini4-neon-low-standard14-n5_2026-11-19.md)・[A02の実行別判定](evaluations/results/free-c324-gemini4-neon-low-a02-v15-reassessment_2026-11-19.json)

試験条件と過去の計測は[結果索引](evaluations/results/README.md)、再現手順は[評価運用手順](docs/evaluation-loop-manual.md)、研究資料は[文書索引](docs/README.md)を参照してください。

## ライセンス

[Apache License 2.0](LICENSE)。

ただし適用範囲には次の限定がある。ケースアーティファクトの一部（`evaluations/cases/*/private/seed.patch`）は、評価対象インスタンスのリポジトリ由来の小さなコード差分を含む。これらの権利は当該ターゲットのリポジトリへ帰属し、このライセンスはそれを再許諾しない。
