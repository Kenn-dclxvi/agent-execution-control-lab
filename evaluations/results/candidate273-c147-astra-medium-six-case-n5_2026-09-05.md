# Candidate273とC147: Astra medium・6ケース各N=5

Candidate273は30 / 30件がvalid、採点可能かつScore 4だった。除外attempt・controller errorは0件。品質の初回確認は通過したが、同じAstra条件のC147比で全エージェントトークンは+110.84%、経過時間は+6.04%となった。事前に固定したコスト条件を満たさず、残り8ケースと追加Nへの拡張を停止する。Standard14全14ケースの完了や、モデル差縮小の再現を意味しない。

## 集約結果

値は同一6ケース・各N=5のselection sampleごとの合計を集約した中央値。経過時間は各runの計測値の合計であり、並列実行全体の壁時計時間ではない。

| KPI | C147 | Candidate273 | 差 |
| --- | ---: | ---: | ---: |
| 品質中央値 | 100 | 100 | 0 |
| Score分布 | 4が30件 | 4が30件 | 低Scoreなし |
| 全エージェントトークン | 693,205 | 1,461,546 | +110.84% |
| 経過時間（秒） | 589.081 | 624.660 | +6.04% |

並列実行の壁時計時間は149.451秒、configured max_workersは24。これは上表のKPIの代替値にはしない。

## ケース別の中央値

| ケース | C147 token | C273 token | token差 | C147秒 | C273秒 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `TC-A01-LATENT-MODE-POLICY` | 18,827 | 17,766 | -5.64% | 16.991 | 24.195 |
| `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | 140,866 | 196,754 | +39.67% | 117.934 | 102.625 |
| `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | 117,762 | 301,281 | +155.84% | 93.016 | 137.239 |
| `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | 165,408 | 428,116 | +158.82% | 172.092 | 141.231 |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | 158,751 | 410,998 | +158.89% | 92.122 | 140.990 |
| `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | 91,936 | 87,741 | -4.56% | 105.367 | 89.221 |

トークン増加は特にF01・F02・F04で大きい。条項削除のどれが増加を引き起こしたか、必要な正常処理のための増加かは未判定であり、ケース別の差だけから原因を断定しない。本文の文字数削減は実行トークン削減を示さなかった。

## 条件と証拠

- 対象: `the-caption-standard14-r1`のA01 r2、A02 r2、F01 r3、F02 r1、F04 r2、F07 dependency r1
- model / reasoning: `gpt-6-astra / medium`
- CLI / Python: `0.153.3 / 3.14.5`
- permission: `approval_policy=never / sandbox=workspace-write`
- 採点: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- token accounting: `all_agents / v1`
- Candidate273 bundle: `748b9eb7137ebfb63866ad18155f10b5dbd2ab6c644fd95c4c5873e80e823910`
- C147 bundle: `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`
- [Candidate273登録result](4c15af38e95849db803ed0e6b2abbede.json)
- [C147の同じ6ケースの選択result](2c5c5b8c1576471b81f2c05947a92a08.json)。元のAstra N=5 resultは`654d171e89a547d9af421ec9ee05ad96`。基準runは再実行していない
- [atomic analysis比較](candidate273-c147-astra-medium-six-case-n5-comparison_2026-09-05.json)。execution stratumは一致
- [実行準備とcoverage修正](../../docs/candidate273-astra-medium-n5-execution-record.md)
- [事前設計と停止条件](../../docs/candidate273-c147-outcome-evidence-core-design.md)

初回準備r1はcoverageが6対14で不一致となり、発行0件で停止した。r2では元setと全fixtureを保持した複製から選択coverageを新規固定し、実行前の正式照合を通過した。環境・fixture・TaskSpec・ratingを試験に合わせて変更したものではない。

実行後は既存`standard14_quality_audit.py`のcollect・applyで30件を採点し、各runをatomic registryへ登録した。owner-producer診断の不一致を品質失敗へ読み替えていない。実行・採点の生証跡はローカルに保持し、公開アーティファクトへ含めない。

## 状態

`targeted_n5_completed / quality_gate_passed / cost_regression / expansion_stopped / standard14_not_completed / not_adopted / release_not_created / not_projected`
