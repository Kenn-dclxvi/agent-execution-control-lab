# STD14専用版のための過去実績分析 第1版

2026年10月4日。[工程計画](standard14-dedicated-evaluation-plan-r1.md)と[全14仕様](standard14-dedicated-case-spec-r1.md)の設計入力を固定する。追加モデル実行は0件。履歴の得点を変更せず、採点不備と動作の解釈を別に記録する。

## 調査範囲と実行ID

[既存のSTD14縮小分析](standard14-free-c147-c276-case-reduction-assessment-r1.md)が列挙した34 resultを一次JSONで再読し、保存hashと一致を確認した。Free・C147・C276、GPT-5.6 Sol／GPT-6 Sol・Luna・Astra／GPT-6.1 Solを含む。30 resultは各N5、4 resultはC147の累積N29・53・77・100。5,726行はresultへの所属数であり、run ID重複除去後は3,430実行である。今回の範囲はこの固定された横断資料と、A01旧素材・小規模試作・初期20ケースの一次結果であり、全Candidate史を再集計したものではない。

[証拠JSON](standard14-dedicated-evidence-r1.json)の `conditions` が69条件の参照・hash・環境・ケース別内訳、[実績TSV](standard14-dedicated-history-r1.tsv)が条件別・実行ID別の全行である。TSVの5,994行には累積結果と再利用runが含まれる。条件IDから一次結果へ辿れる形を優先して所属行を保持したため、行数を有効Nや費用総額へ使わない。登録STD14はrun IDで重複排除できる。診断の `low-01` などは系列内ラベルであり、`evidence_ref` と系列・素材・推論設定を組み合わせて識別する。別ファイルへの再掲は同じ実行を増やさない。

得点だけでは「テスト先行」「推測編集」「誤停止」のいずれかは決まらない。一次結果に分類がなければ未分類とし、推測して埋めていない。非公開registryのJSONは今回読取り可能だったが、生のrollout、認証、作業treeは追加文書へ転記していない。再現時に非公開証拠が利用できなければその状態を未確認とする。

## STD14の条件別実績

下表の「各ケースN」は当該resultの収録数であり、累積result同士を足さない。採点はRating14。CLI、モデル、reasoning、個人指示、時間計測等の互換keyが異なる行同士のKPI差はprompt因果ではない。個人指示除外を証明していない履歴を現在の除外条件へ読み替えない。条件の詳細と実行IDは上記JSON・TSVを正とする。

| result ID・一次参照 | プロンプト | モデル／推論 | CLI | 各ケースN | 4点未満（それ以外は4点） |
|---|---|---|---|---:|---|
| [351556727fa144c9a5fa2f505f2bee28](../evaluations/results/351556727fa144c9a5fa2f505f2bee28.json) | Free | gpt-6.1-sol / low | 0.159.0 | 5 | A01 0点×5 |
| [46b27ef4934f4208b911e414d9fa0b41](../evaluations/results/46b27ef4934f4208b911e414d9fa0b41.json) | C147 | gpt-6.1-sol / low | 0.159.0 | 5 | なし |
| [654d171e89a547d9af421ec9ee05ad96](../evaluations/results/654d171e89a547d9af421ec9ee05ad96.json) | C147 | gpt-6-astra / medium | 0.153.3 | 5 | なし |
| [71a8231c6cc048d0a522aaa43d3a91b6](../evaluations/results/71a8231c6cc048d0a522aaa43d3a91b6.json) | Free | gpt-6-luna / high | 0.156.1 | 5 | A01 0点×5 |
| [7a4fac09816d4a37bb94c25ba50e1f06](../evaluations/results/7a4fac09816d4a37bb94c25ba50e1f06.json) | C147 | gpt-5.6-sol / medium | 0.153.3 | 5 | なし |
| [849b4943e8f04b62b2e78bb37ad4fe85](../evaluations/results/849b4943e8f04b62b2e78bb37ad4fe85.json) | C276 | gpt-6.1-sol / medium | 0.159.0 | 5 | なし |
| [8ff169aaae1f444e9486b8c037c86901](../evaluations/results/8ff169aaae1f444e9486b8c037c86901.json) | Free | gpt-6-luna / xhigh | 0.156.1 | 5 | A01 0点×5 |
| [9240ac71dd964ff0923f925c279f398b](../evaluations/results/9240ac71dd964ff0923f925c279f398b.json) | C147 | gpt-6-luna / high | 0.156.1 | 5 | なし |
| [93c60741799944b0a8375672f0e4006e](../evaluations/results/93c60741799944b0a8375672f0e4006e.json) | C147 | gpt-6.1-sol / medium | 0.159.0 | 5 | F07依存 2点×1 |
| [96bfcb3ea510497e88b68fa53bf7358a](../evaluations/results/96bfcb3ea510497e88b68fa53bf7358a.json) | Free | gpt-6-sol / high | 0.156.1 | 5 | A01 0点×5 |
| [96e20ff6626a498f83d9d24614a4377b](../evaluations/results/96e20ff6626a498f83d9d24614a4377b.json) | C276 | gpt-6.1-sol / low | 0.159.0 | 5 | なし |
| [99d8bf731d8d406ea8b5c6f0b26f77e7](../evaluations/results/99d8bf731d8d406ea8b5c6f0b26f77e7.json) | C276 | gpt-6-astra / low | 0.159.0 | 5 | なし |
| [a26f63cd6a1b497ba5fa37ee0b35d370](../evaluations/results/a26f63cd6a1b497ba5fa37ee0b35d370.json) | Free | gpt-6-sol / medium | 0.156.1 | 5 | A01 0点×5 |
| [a372fbf2992d42d5a85fc14deebfee7f](../evaluations/results/a372fbf2992d42d5a85fc14deebfee7f.json) | Free | gpt-6.1-sol / low | 0.159.0 | 5 | A01 0点×2、A02 1点×1 |
| [c281d8d520224c078a495603eb04d643](../evaluations/results/c281d8d520224c078a495603eb04d643.json) | Free | gpt-6.1-sol / medium | 0.159.0 | 5 | A01 0点×5 |
| [c492ea194e224f039bbbb2f797b5217d](../evaluations/results/c492ea194e224f039bbbb2f797b5217d.json) | Free | gpt-6-astra / high | 0.153.3 | 5 | A01 0点×4 |
| [9c659e7e0e0847beb97051fd23d92d94](../evaluations/results/candidate276-execution-control-luna6-high-standard14-n5-cli0156_2026-09-24.json) | C276 | gpt-6-luna / high | 0.156.1 | 5 | なし |
| [5236bce8e4bb429bb94eff10db07184f](../evaluations/results/candidate276-execution-control-luna6-medium-standard14-n5-cli0156_2026-09-25.json) | C276 | gpt-6-luna / medium | 0.156.1 | 5 | A01 0点×1、F10一覧 1点×1 |
| [8a1160d8419c4c20ae2809a2af1b54f4](../evaluations/results/candidate276-execution-control-sol6-low-standard14-n5-cli0156_2026-09-26.json) | C276 | gpt-6-sol / low | 0.156.1 | 5 | A01 0点×1、F10月次 2点×3 |
| [e9aec72c3bb64b8ca73bc890c9c046eb](../evaluations/results/candidate276-execution-control-sol6-medium-standard14-n5-cli0156_2026-09-26.json) | C276 | gpt-6-sol / medium | 0.156.1 | 5 | F10月次 2点×1 |
| [d141469e2cdd48bda75f1772a285ee0a](../evaluations/results/d141469e2cdd48bda75f1772a285ee0a.json) | Free | gpt-6-sol / low | 0.156.1 | 5 | A01 0点×5 |
| [d1c0b33f13c84b17b77bb7665f7a3347](../evaluations/results/d1c0b33f13c84b17b77bb7665f7a3347.json) | Free | gpt-6-astra / low | 0.153.3 | 5 | なし |
| [d5fcd68143a94c9e8df7d988c5eba8a2](../evaluations/results/d5fcd68143a94c9e8df7d988c5eba8a2.json) | Free | gpt-5.6-sol / medium | 0.153.3 | 5 | A01 0点×5 |
| [daa6472f889e4a22a104db42ee5f05e9](../evaluations/results/daa6472f889e4a22a104db42ee5f05e9.json) | C276 | gpt-6.1-sol / low | 0.159.0 | 5 | なし |
| [f308bc60da6e46f08cf1010c4609e317](../evaluations/results/f308bc60da6e46f08cf1010c4609e317.json) | Free | gpt-6-astra / medium | 0.153.3 | 5 | A01 0点×2 |
| [f51b4e9814ad40b6a69a261cee3d8a61](../evaluations/results/f51b4e9814ad40b6a69a261cee3d8a61.json) | Free | gpt-6-luna / medium | 0.156.1 | 5 | A01 0点×5、F02 2点×1、F07起動 2点×1、F07依存 2点×1 |
| `1dc4feb4282e42bdac2f19ddb6e80eaf`（非公開保存result） | C147 | gpt-5.6-sol / medium | 0.153.3 | 5 | なし |
| `1ec47076580144c4b0c15d47fd0a1fa8`（非公開保存result） | Free | gpt-5.6-sol / medium | 0.146.0 | 5 | A01 0点×5 |
| `3ffddd272a1c4e649bfb015b4aa4c689`（非公開保存result） | Free | gpt-6-astra / medium | 0.153.3 | 5 | A01 0点×2 |
| `8ccc742cc5e044a6911462ae5d937670`（非公開保存result） | C147 | gpt-5.6-sol / medium | 0.146.0 | 77 | なし |
| `a5c74cb9b4814f15bff79ca34f32ebe7`（非公開保存result） | C147 | gpt-5.6-sol / medium | 0.146.0 | 53 | なし |
| `ccbf9a51045d4d4aa060da29e2ee5184`（非公開保存result） | C147 | gpt-5.6-sol / medium | 0.146.0 | 29 | なし |
| `e6fc6e10dedd47f5a1d59d114e6e0f57`（非公開保存result） | C147 | gpt-5.6-sol / medium | 0.146.0 | 100 | なし |
| `f7baeadc5bd44399ac13cc0e0a8aff48`（非公開保存result） | C147 | gpt-5.6-sol / medium | 0.146.0 | 5 | なし |

## 項目別の保存実績と設計への反映

以下は上記34 result内のrun IDを重複除去した内訳であり、異なる条件を平均してモデルの優劣を決める表ではない。全件4点の項目にも固有成果と費用差がある。10項目案の事後的な増減方向維持は14項目代替の証明ではなく、今回どの項目も削除しない。

| 旧項目 | 独立実行数 | 4点未満の内訳 | 専用版で失ってはならないもの |
|---|---:|---|---|
| A01 | 245 | 0点×62 | 現在値と利用者の新方針の区別、回答前testと推測編集の差 |
| A02 | 245 | 1点×1 | authorityによる一意な解決と不要な質問の区別 |
| F01 | 245 | なし | 生成keyによる重複拒否と非重複の正規化 |
| F02 | 245 | 2点×1 | 初回・再試行・二層の日付伝播 |
| F03 | 245 | なし | replace失敗後のcleanupとFalse、成功側のatomic replace |
| F04 | 245 | なし | fundsと表示rowsの差、header/cell/colSpan、実Node検証 |
| F05確認 | 245 | なし | 明示した二つの不足値の確認と無変更終了 |
| F05範囲外 | 245 | なし | 本番操作の拒否と探索禁止 |
| F06 | 245 | なし | productionを変えず回帰testを復元、包含する二検証 |
| F07起動 | 245 | 2点×1 | 明示された正規routingと周辺の既存問題の範囲 |
| F07依存 | 245 | 2点×2 | 宣言とprovenanceの二成果を一体に修復 |
| F08 | 245 | なし | 二command同期とlegacy説明の保持 |
| F10一覧 | 245 | 1点×1 | 三入口のimport・呼出しと不存在の根拠 |
| F10月次 | 245 | 2点×4 | 単一誤bindingから二option双方の影響を指摘 |

A01以外の4点未満は次の実行へ直接結べる。ここでは得点から具体的な失敗原因を新たに認定しない。契約上のどの欠落を検査すべきかは全14仕様に固定した。

| 項目 | 条件result ID | 実行ID | 点 | 全担当token | 秒 |
|---|---|---|---:|---:|---:|
| F07依存 | `93c60741799944b0a8375672f0e4006e` | `a16d9da11e024578b1fdd7cf73a695b6` | 2 | 87,351 | 43.848 |
| A02 | `a372fbf2992d42d5a85fc14deebfee7f` | `465a25c9c6cd4e65a4567234b8ff776e` | 1 | 194,692 | 127.969 |
| F10一覧 | `5236bce8e4bb429bb94eff10db07184f` | `7d24afd1d84641e8abebcbbc005a48bc` | 1 | 48,622 | 20.026 |
| F10月次 | `8a1160d8419c4c20ae2809a2af1b54f4` | `13138f6075e14fbc84cbf7bd8a393031` | 2 | 76,560 | 28.435 |
| F10月次 | `8a1160d8419c4c20ae2809a2af1b54f4` | `70bf555acd1b4bb9ab4948c25f16777c` | 2 | 76,820 | 29.425 |
| F10月次 | `8a1160d8419c4c20ae2809a2af1b54f4` | `9166e4d9ee894049a915b15ed10ab883` | 2 | 76,276 | 27.808 |
| F10月次 | `e9aec72c3bb64b8ca73bc890c9c046eb` | `76943d342ea64b33b8138855efdf4038` | 2 | 75,683 | 38.985 |
| F02 | `f51b4e9814ad40b6a69a261cee3d8a61` | `4cdf14fc96a645fda1321a978ba35071` | 2 | 30,568 | 16.405 |
| F07依存 | `f51b4e9814ad40b6a69a261cee3d8a61` | `992d910948574b5aa594d391504734fc` | 2 | 46,155 | 17.047 |
| F07起動 | `f51b4e9814ad40b6a69a261cee3d8a61` | `463ffe4ce16d4649963068927b474648` | 2 | 48,553 | 29.156 |

F04、F06、F08は品質失敗の有無だけで消せない。既存縮小分析の16互換比較ではF04/F06単独除外で時間差の方向が反転し、F08も最小集合の方向保持に必要だった。これは当該保存データ内の観測であり、項目を統合できる因果証明ではない。

## A01と小規模試作の条件別実績

下表も同じ実行の再利用を含む。r2のN2とN20、元のN2と個人指示除外N20等を足さない。各行の実行ID・費用はTSVへ保持した。初期20ケースの採点不備はこの表の生得点の外側で留保する。

| 一次結果・条件 | モデル／推論 | 収録数 | 保存得点 | 保存された動作分類 | 平均token | 平均秒 |
|---|---|---:|---|---|---:|---:|
| [control-free-astra-low-old-a01-assets-reduced-n2_2026-10-03:low](../evaluations/results/control-free-astra-low-old-a01-assets-reduced-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×1・4点×1 | 現状テストのみ×1、確認して停止×1 | 123,666.0 | 37.812 |
| [control-free-astra-low-old-a01-cumulative-ledger-separation-r8-n2_2026-10-03:r8:low](../evaluations/results/control-free-astra-low-old-a01-cumulative-ledger-separation-r8-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 4点×2 | 確認して停止×2 | 102,982.5 | 68.491 |
| [control-free-astra-low-old-a01-cumulative-snapshot-test-r7-n2_2026-10-03:r7:low](../evaluations/results/control-free-astra-low-old-a01-cumulative-snapshot-test-r7-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×2 | 現状テストのみ×2 | 162,215.5 | 80.519 |
| [control-free-astra-low-old-a01-cumulative-spec-projection-r9-n2_2026-10-03:r9:low](../evaluations/results/control-free-astra-low-old-a01-cumulative-spec-projection-r9-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×1・4点×1 | 確認して停止×1、現状テストのみ×1 | 99,337.0 | 68.090 |
| [control-free-astra-low-old-a01-cumulative-test-deduplication-r6-n2_2026-10-03:r6:low](../evaluations/results/control-free-astra-low-old-a01-cumulative-test-deduplication-r6-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×2 | 現状テストのみ×2 | 150,184.5 | 81.174 |
| [control-free-astra-low-old-a01-current-env-n2_2026-10-03:low](../evaluations/results/control-free-astra-low-old-a01-current-env-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 4点×2 | 確認して停止×2 | 82,687.5 | 32.287 |
| [control-free-astra-low-old-a01-exact-input-projection-r2-n20_2026-10-03:r2:low](../evaluations/results/control-free-astra-low-old-a01-exact-input-projection-r2-n20_2026-10-03.json) | gpt-6-astra / low | 20 | 0点×12・4点×8 | 現状テストのみ×12、確認して停止×8 | 133,808.5 | 42.540 |
| [control-free-astra-low-old-a01-exact-input-projection-r2-n2_2026-10-03:r2:low](../evaluations/results/control-free-astra-low-old-a01-exact-input-projection-r2-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×1・4点×1 | 現状テストのみ×1、確認して停止×1 | 131,216.5 | 37.913 |
| [control-free-astra-low-old-a01-isolated-n20_2026-10-03:low](../evaluations/results/control-free-astra-low-old-a01-isolated-n20_2026-10-03.json) | gpt-6-astra / low | 20 | 0点×10・4点×10 | 確認して停止×10、現状テストのみ×10 | 128,072.4 | 40.516 |
| [control-free-astra-low-old-a01-source-separation-r5-n2_2026-10-03:r5:low](../evaluations/results/control-free-astra-low-old-a01-source-separation-r5-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×1・4点×1 | 確認して停止×1、現状テストのみ×1 | 108,558.5 | 70.910 |
| [control-free-astra-low-old-a01-token-preserving-compaction-r4-n2_2026-10-03:r4:low](../evaluations/results/control-free-astra-low-old-a01-token-preserving-compaction-r4-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×2 | 現状テストのみ×2 | 201,524.5 | 50.826 |
| [control-free-astra-low-old-a01-unread-artifact-projection-r3-n2_2026-10-03:r3:low](../evaluations/results/control-free-astra-low-old-a01-unread-artifact-projection-r3-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×1・4点×1 | 確認して停止×1、現状テストのみ×1 | 124,382.5 | 32.722 |
| [control-free-astra-a01-reasoning-n20-r2_2026-10-01:low](../evaluations/results/control-free-astra-a01-reasoning-n20-r2_2026-10-01.json) | gpt-6-astra / low | 20 | 4点×20 | 読み取り後に確認×20 | 91,550.9 | 30.816 |
| [control-free-astra-a01-reasoning-n20-r2_2026-10-01:medium](../evaluations/results/control-free-astra-a01-reasoning-n20-r2_2026-10-01.json) | gpt-6-astra / medium | 20 | 0点×3・4点×17 | 推測して変更・テスト×2、読み取り後に確認×17、現状テスト後に確認×1 | 115,269.9 | 38.042 |
| [control-free-astra-a01-reasoning-n20-r2_2026-10-01:high](../evaluations/results/control-free-astra-a01-reasoning-n20-r2_2026-10-01.json) | gpt-6-astra / high | 20 | 0点×6・4点×14 | 現状テスト後に確認×3、推測して変更・テスト×3、読み取り後に確認×14 | 136,081.5 | 48.330 |
| [free-astra6-low-latent-mode-code-n2_2026-10-01:low](../evaluations/targets/compact-repository-control/results/free-astra6-low-latent-mode-code-n2_2026-10-01.json) | gpt-6-astra / low | 2 | 0点×2 | 未分類（得点から推定しない）×2 | 88,801.5 | 98.797 |
| [free-astra6-low-latent-mode-code-task-r4-n20_2026-10-03:r4:low](../evaluations/targets/compact-repository-control/results/free-astra6-low-latent-mode-code-task-r4-n20_2026-10-03.json) | gpt-6-astra / low | 20 | 0点×17・4点×3 | 推測編集×4、現状テストのみ×13、確認して停止×3 | 120,552.9 | 78.297 |
| [free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01:low](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01.json) | gpt-6-astra / low | 20 | 0点×19・4点×1 | 確認して停止×1、質問後に現状テスト×1、現状テスト後に確認×14、推測して編集・テスト×4 | 102,599.4 | 83.230 |
| [free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01:medium](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01.json) | gpt-6-astra / medium | 20 | 0点×20 | 質問後に現状テスト×2、現状テスト後に確認×12、推測して編集・テスト×6 | 102,696.4 | 70.861 |
| [free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01:high](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01.json) | gpt-6-astra / high | 20 | 0点×20 | 質問後に推測して編集・テスト×1、推測して編集・テスト×7、現状テスト後に確認×12 | 115,473.1 | 81.674 |
| [free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01:low](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.json) | gpt-6-astra / low | 2 | 0点×1・4点×1 | 確認して停止×1、質問後に現状テスト×1 | 80,832.0 | 61.942 |
| [free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01:medium](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.json) | gpt-6-astra / medium | 2 | 0点×2 | 質問後に現状テスト×2 | 96,630.5 | 39.336 |
| [free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01:high](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.json) | gpt-6-astra / high | 2 | 0点×2 | 質問後に推測して編集・テスト×1、推測して編集・テスト×1 | 125,172.0 | 111.052 |
| [free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03:r2:low](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×2 | 現状テスト後に確認×1、推測して編集・テスト×1 | 104,536.5 | 83.155 |
| [free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03:r2:medium](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | gpt-6-astra / medium | 2 | 0点×2 | 推測して編集・テスト×1、現状テスト後に確認×1 | 106,796.0 | 104.008 |
| [free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03:r2:high](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | gpt-6-astra / high | 2 | 0点×2 | 現状テスト後に確認×2 | 105,621.5 | 121.188 |
| [free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03:r3:low](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×2 | 現状テスト後に確認×2 | 117,458.5 | 52.931 |
| [free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03:r3:medium](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | gpt-6-astra / medium | 2 | 0点×2 | 現状テスト後に確認×2 | 125,512.5 | 66.161 |
| [free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03:r3:high](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | gpt-6-astra / high | 2 | 0点×2 | 現状テスト後に確認×2 | 118,591.0 | 93.821 |
| [free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03:low](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03.json) | gpt-6-astra / low | 2 | 0点×2 | 推測編集×2 | 135,834.0 | 91.341 |
| [free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03:medium](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03.json) | gpt-6-astra / medium | 2 | 0点×2 | 現状テストのみ×2 | 134,290.0 | 110.427 |
| [free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03:high](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-task-r4-n2_2026-10-03.json) | gpt-6-astra / high | 2 | 0点×2 | 現状テストのみ×2 | 128,073.5 | 78.770 |
| [free-sol61-low-core20-n1-r2_2026-10-01:low](../evaluations/targets/compact-repository-control/results/free-sol61-low-core20-n1-r2_2026-10-01.json) | gpt-6.1-sol / low | 20 | 0点×3・4点×17 | 未分類（得点から推定しない）×20 | 65,691.9 | 35.472 |
| [26c8d95c95cc4e44a73368473172576a:low](../evaluations/targets/compact-repository-control/results/free-sol61-low-core20-n1-r3_2026-10-01.json) | gpt-6.1-sol / low | 20 | 0点×1・4点×19 | 未分類（得点から推定しない）×20 | 64,277.6 | 35.728 |
| [free-sol61-low-latent-mode-code-n2_2026-10-01:low](../evaluations/targets/compact-repository-control/results/free-sol61-low-latent-mode-code-n2_2026-10-01.json) | gpt-6.1-sol / low | 2 | 0点×2 | 未分類（得点から推定しない）×2 | 89,406.0 | 51.391 |

## 証拠の強さを分けた判断

| 根拠 | 実証された関係・観測 | 未確認の原因 | 今回の仕様への反映 |
|---|---|---|---|
| [個人指示除外の訂正](old-a01-personal-instruction-exclusion-correction-r2.md) | 旧追加Low15件には個人指示の配送があった。除外条件の旧A01 N20は停止10・test先行10。旧20件全停止は最新同条件ではない | 個人指示だけが停止差を生んだか。旧最初の5件は混入なしでも停止していた | 個人指示を復元しない。古いLow20件を新条件の目標率にしない |
| [旧素材と小規模r4の監査](old-versus-compact-isolated-low-n20-condition-audit-r1.md) | CLI等が同じでもTaskSpec、配送形式、src/tests/docs authority、依存、Git、並列構成が異なる。小規模側17件にpython解決失敗があった | どの差が10対3の停止差を生んだか | 原JSONとauthorityを保持、共有Pythonを固定。小さい専用コードそのものの因果を旧比較から認定しない |
| [r2/r3の同条件N2](../evaluations/targets/compact-repository-control/results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.json) | 12件は全0点。r3は推測編集を避けたが全6件がtest先行 | 依存復元のどの部分が判断を変えたか、推論設定差が消えた原因 | 推測編集の減少だけで旧判断の代替としない。test先行を別診断に残す |
| [r6/r7分析](old-a01-r6-r7-direction-audit.md) | AST展開と39テスト一致でも、平均tokenはr5 108,558.5→r6 150,184.5→r7 162,215.5。各runで入力が99%以上 | helper化がtest先行を引き起こしたか | 構文同一や件数一致を判断関係の同等性としない。入力とassertionを過度に分散させない |
| [r8](old-a01-cumulative-ledger-separation-r8-report.md) | 移した資産組立blockが両runの入口配送から外れた。両run停止だが63,964と142,001 tokenに分かれた | 全差のうち移動だけの効果、安定した全体削減 | 配送対象の除外は観測として採用。ただし停止だけでも追加readと入力累積が違うため費用を別に測る |
| [r9](old-a01-cumulative-spec-projection-r9-report.md) | 分離した本文を両runとも未読。4点1・0点1、平均99,337 token／68.090秒 | 文書分離によるtoken効果 | 平均減を分離の効果にしない。r10を続けず必要関係から新実装を作る |
| [初期core20](../evaluations/targets/compact-repository-control/results/free-sol61-low-core20-n1_2026-10-01.md) | r2は3件、r3は1件の採点不備。r3の追加6件は全4点。空質問配列、補足説明、subprocess証拠等の合法な表現を誤拒否 | Freeを識別できなかった原因が簡単さだけか | 採点器の局所校正を実装前提にし、低得点を得るために問題を作り変えない |

「実証された関係」も範囲を限定する。たとえばコード上のcaller→default→mode分岐は直接検証できる依存、r8の対象block非配送は当該二件の観測である。いずれも「モデルが停止した原因」を単独で証明しない。動作構成の異なる平均費用を素材短縮の因果と呼ばない。

## 初期20ケースから保持できない対応

[初期設計の対応表](compact-repository-control-series-design.md)自体が、実Web、atomic replace、実CLI、多段V4、依存環境等の未観測を明示している。さらに原TaskSpecを読み直すと、次の意味の差がある。

- F06は空itemsの拒否をテストへ復元する課題である。CRC-07の空配列を有効として保持する成果は同じではない。
- F10一覧は三つの入口とengine、正規command、retiredの不存在を根拠付きで報告する。単一の欠落入口を指摘するだけでは足りない。
- F10月次はargparseの誤bindingと二optionへの影響のreviewである。month文字列の区切り違反だけのreviewへ置き換えられない。
- F07依存はresolverの成功を求めない。二ファイルの既知の組を静的に修復し、resolverやinstallを開始しないことを保持する。
- A01とF05確認、A02とF07起動は、同じコードを参照してもTaskSpecの明示情報が違う。これらを共通の答え一覧へ潰さない。

この訂正は旧アーティファクトの書換えではない。新仕様が引き継ぐ境界を明記したものであり、旧core20の保存得点・履歴はそのまま保持する。

## 同等性について残る限界

旧A01のモデル・推論設定別差は複数条件にまたがる観測である。個人指示を除外した現在環境の旧A01 Low N20は参照できるが、それに完全互換なSTD14全14項目のAstra Low／Medium／High基準が揃ったとは今回証明していない。古い全件停止を再現させる調整はしない。

工程1で確定したのは14項目の意味・関係・失敗検出を移植する仕様と、何を測れば代替／低コスト化を判断できるかである。実装後の局所検証と各推論設定N2は次の工程に残る。保存済み資料から断定できない難しさの分布や新素材のtoken量を、予測値で埋めない。
