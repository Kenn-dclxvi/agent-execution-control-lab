# Candidate81 / Candidate93 result classification Rating v14 Medium F02 N=5

## 結論

Candidate93はF02で5 / 5件がvalid・rateable・score `4`だった。保存済みCandidate81比の中央値はall-agent token `-4,449`（`-1.45%`）、elapsed `-10.866`秒（`-10.10%`）だった。

一方、`EXACT / STRUCTURED / NOISE`をcommand経路へ一貫してbindできたrunは0 / 5だった。searchとtestは全runでraw outputを返し、STRUCTUREDへの機械field投影とNOISE除去は成立しなかった。したがってKPI差を3分類の効果へ帰属させない。Candidate93を`targeted_f02_evaluated / classification_not_observed / cost_improved_unattributed / stopped`とする。

## Identity

- evaluation set identity: `d81b4b66d0b4c51c44a1751c107638630d68bb66bfabaf5a5f5bb0baba72e801`
- model / reasoning / N: `gpt-5.6-sol` / `medium` / `5`
- compatibility key: `96d27a484091ba1f250994226743e5977a84def62ab72182e82bdfc179819973`
- C81 result: `886348bb48f44605965c2112c8f1ee91`
- C93 result: `76edc84190a543c0b20f5b850892edf9`
- C93 result content SHA-256: `63e3a559d5e058fe6a5d78bc089db1938a9750df7c7007a2992d5836a332375e`
- execution archive SHA-256: `7ceb9a08b50b222484da68dbf79f19bed362221c0771b526f6abf12769b0c0e4`

TaskSpec、fixture、oracle、allowed path、required validation、rating、executorは変更していない。

## 3 KPI

| prompt | score 4 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: |
| C81 | 5 / 5 | `307,886` | `107.629`秒 |
| C93 | 5 / 5 | `303,437` | `96.763`秒 |
| C93 - C81 | `0` | `-4,449`（`-1.45%`） | `-10.866`秒（`-10.10%`） |

| iteration | token | elapsed | command数 | 一時file使用 | 最大result |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `207,132` | `90.668`秒 | `15` | `0` | `159,445` bytes |
| 2 | `244,118` | `93.117`秒 | `18` | `0` | `159,445` bytes |
| 3 | `303,437` | `126.397`秒 | `16` | `2` | `159,445` bytes |
| 4 | `348,667` | `96.763`秒 | `16` | `0` | `159,445` bytes |
| 5 | `337,197` | `109.637`秒 | `15` | `13` | `159,445` bytes |

iteration 5はrawを`tee`で一時fileへ保存したが、同じrawをstdoutへ返したため圧縮ではない。iteration 3は開始statusだけをJSON fieldへ投影したが、後続search / testは直接出力へ戻った。残る3 runは通常の直接command経路だった。

## 解釈とGate

粗い3分類でも、分類名から具体的なshell projectionへ変換する動作は安定しなかった。今回のtoken / elapsed改善は、分類を実施しなかった通常経路のrun差であり、採用根拠にしない。

- quality gate: `passed`
- classification mechanism gate: `failed`（0 / 5）
- cost state: `improved_but_unattributed`
- state: `targeted_f02_evaluated / stopped`
- F04、標準14、採用、release、本体反映: 未実施・未判断
