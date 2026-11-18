# agent-execution-control-lab

THE-CAPTIONの開発課題を使い、AIエージェントへの指示が成果の品質、実行経路、費用、所要時間にどう影響するかを調べるリポジトリです。

## THE-CAPTIONでのFreeとC324の比較

Freeはルートの `AGENTS.md` を空にした比較条件です。C324は同じ場所に5項の実行制御を置きます。どちらも各ディレクトリの指示を使います。C324は2026年11月18日に正式リリースし、個人用Codexの共通指示に適用しました。[C324の本文](prompts/releases/the-caption-3ce91a4-without-investigation-rule-release-r1/files/AGENTS.md.txt)・[リリース記録](prompts/releases/the-caption-3ce91a4-without-investigation-rule-release-r1/README.md)

GPT-6以降のSTD14比較をモデル・推論設定別に示します。各行は14課題×5回の70件です。点数はA02にv15の行動基準を適用し、残り13課題は登録時の点数を用いて比較しています。「A02 自力／満点」は、起動先を聞き返さずに特定して修復へ進んだ件数と、周辺への影響・検証まで含めて4点だった件数です（各5件）。費用と時間は14課題分の合計を5組作ったときの中央値です。[採点契約](evaluations/rating-contracts/README.md)・[A02の再採点記録](evaluations/results/a02-r2-behavioral-rescore-v1.md)

| モデル・推論設定 | 条件 | 点数分布（70件） | A02 自力／満点 | API換算費用（USD） | 実行時間（秒・参考値） |
|---|---|---|---:|---:|---:|
| GPT-6.2 Sol Low | Free | 4点64件・2点1件・0点5件 | 5／4 | 0.9397 | 615.97 |
| GPT-6.2 Sol Low | C324 | 4点70件 | 5／5 | 0.6918 | 477.95 |
| GPT-6.2 Astra Low | Free | 4点66件・0点4件 | 5／5 | 2.2651 | 1187.31 |
| GPT-6.2 Astra Low | C324 | 4点70件 | 5／5 | 2.1173 | 590.28 |
| GPT-6.1 Sol Low | Free | 4点69件・0点1件 | 5／5 | 0.9344 | 636.90 |
| GPT-6.0 Astra Low | Free | 4点67件・3点1件・0点2件 | 5／4 | 6.1484 | 634.75 |
| GPT-6.1 Terra Low | Free | 4点67件・0点3件 | 5／5 | 0.4336 | 410.50 |
| GPT-6.1 Terra medium | Free | 4点67件・0点3件 | 5／5 | 0.5033 | 382.51 |
| GPT-6.1 Terra high | Free | 4点67件・0点3件 | 5／5 | 0.5044 | 442.42 |

GPT-6.2 Lowでは、C324の満点がSolでFreeより6件、Astraで4件増えました。A01ではFreeのSolが5件、Astraが4件、変更先が未確定のまま進んで0点でした。C324では両モデルとも5件すべてで開始状態だけを確認し、変更先を利用者に質問しました。FreeのSolに残るA02の失点は、明示的な空引数の扱いを変えた1件です。

C324のSolは登録時のv14で68件が4点、2件が1点でした。この2件は引数なしの場合だけ `shift` を省き、正規の起動先・周辺経路を保って検証も完了したため、v15では4点です。表にはその比較値を載せています。C324の測定済み条件はGPT-6.2 Astra Low・Sol Lowです。計測時期やサービスの応答状況が異なるため、実行時間は参考値です。[C324のSol実行記録](evaluations/results/c324-sol62-low-standard14-n5_2026-11-18.md)・[C324のAstra実行記録](evaluations/results/c324-astra62-low-standard14-n5_2026-11-18.md)

試験条件と過去の計測は[結果索引](evaluations/results/README.md)、再現手順は[評価運用手順](docs/evaluation-loop-manual.md)、研究資料は[文書索引](docs/README.md)を参照してください。

## ライセンス

[Apache License 2.0](LICENSE)。

ただし適用範囲には次の限定がある。ケースアーティファクトの一部（`evaluations/cases/*/private/seed.patch`）は、評価対象インスタンスのリポジトリ由来の小さなコード差分を含む。これらの権利は当該ターゲットのリポジトリへ帰属し、このライセンスはそれを再許諾しない。
