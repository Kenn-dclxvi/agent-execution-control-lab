# Candidate43 / Candidate71 / Candidate147 Rating v14 Medium Standard14 atomic N=5

## 結論

Candidate43とCandidate71をCandidate147と実効互換な条件で各N=5実行し、各70 / 70件をvalidかつrateableとして登録した。両条件とも70 / 70件がscore `4`で、score `3`以下、excluded attempt、controller errorは0件だった。

Standard14集約中央値はCandidate43がquality `100.000`、token `3,151,442`、elapsed `1,091.549秒`、Candidate71が`100.000 / 2,030,116 / 988.187秒`、Candidate147が`100.000 / 1,447,626 / 852.543秒`だった。同じ品質分布の観測範囲で、Candidate71はCandidate43比token `-35.58%`、elapsed `-9.47%`、Candidate147はCandidate71比token `-28.69%`、elapsed `-13.73%`だった。

この結果は各条件N=5の記述比較である。統計的優越、採用、release、projectionを新たに判断しない。

## 試験状態

- Candidate43: `standard14_n5_evaluated / quality_gate_passed / registered`
- Candidate71: `standard14_n5_evaluated / quality_gate_passed / registered`
- 比較: `compatibility_matched / descriptive_only`
- Candidate147の既存状態: 変更なし

## 実行前gate

既存のCandidate43 / Candidate71 N=5はRating v13・CLI 0.144系であり、Candidate147とは互換でないため再利用しなかった。Candidate147の固定profileからprompt identityだけを替え、次を機械照合した。

| 条件 | 固定値 | 照合結果 |
| --- | --- | --- |
| Evaluation set | `the-caption-standard14-r1` / `r1` / identity `2096d15e...63c33` | 一致 |
| coverage | 14 case × 各5件 | 一致 |
| fixture / TaskSpec | C147 reference Layer 1の全14 case | 一致 |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` / `9d01b7ee...011b1` | 一致 |
| model / reasoning | `gpt-5.6-sol` / `medium` | 一致 |
| Agent / runtime / CLI | Codex、persisted、memory off、multi-agent on、Python `3.14.5`、CLI `0.146.0`、runtime `61b26e61...9a73` | 一致 |
| permission | `workspace-write / never` | 一致 |
| executor / token | global queue、`M=24`、all-agent token accounting v1 | 一致 |
| atomic comparison key | `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1` | 3条件で一致 |
| comparison preflight key | `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561` | C43 / C71とも一致 |

互換な既存atomic runは両条件とも0件だった。`plan-missing --desired-count 5`で各70件を固定し、一つのglobal queueへ投入した。

## 集約KPI

| prompt | score分布 | quality中央値 | all-agent token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Candidate43 | `4 = 70` | 100.000 | 3,151,442 | 1,091.549秒 |
| Candidate71 | `4 = 70` | 100.000 | 2,030,116 | 988.187秒 |
| Candidate147 | `4 = 70` | 100.000 | 1,447,626 | 852.543秒 |

差分は行の後者から前者を引いた値である。

| 差分 | quality | token | elapsed |
| --- | ---: | ---: | ---: |
| Candidate71 - Candidate43 | 0.000 | -1,121,326（-35.58%） | -103.362秒（-9.47%） |
| Candidate147 - Candidate43 | 0.000 | -1,703,816（-54.06%） | -239.006秒（-21.90%） |
| Candidate147 - Candidate71 | 0.000 | -582,490（-28.69%） | -135.644秒（-13.73%） |

## N × Case内訳

全caseで3条件とも5 / 5件がscore `4`だった。KPI欄は`token中央値 / elapsed中央値`である。

| case | Candidate43 KPI | Candidate71 KPI | Candidate147 KPI |
| --- | ---: | ---: | ---: |
| A01 latent mode policy | 120,671 / 41.123秒 | 88,909 / 33.014秒 | 19,195 / 12.148秒 |
| A02 repository-resolvable routing | 293,802 / 110.107秒 | 200,203 / 90.483秒 | 129,085 / 73.379秒 |
| F01 duplicate asset key | 205,180 / 80.843秒 | 184,467 / 73.826秒 | 107,202 / 66.424秒 |
| F02 history date bound | 310,183 / 88.825秒 | 263,170 / 93.025秒 | 128,236 / 100.607秒 |
| F03 atomic cleanup | 178,933 / 79.404秒 | 175,006 / 81.346秒 | 104,320 / 70.866秒 |
| F04 audit column visibility | 282,136 / 100.957秒 | 240,353 / 105.101秒 | 151,170 / 91.431秒 |
| F05 clarify units mode | 36,067 / 26.753秒 | 36,545 / 21.806秒 | 37,242 / 26.725秒 |
| F05 out-of-scope deploy | 36,174 / 23.120秒 | 34,732 / 22.490秒 | 37,366 / 25.291秒 |
| F06 empty snapshot contract | 334,841 / 96.668秒 | 146,540 / 73.380秒 | 151,542 / 79.393秒 |
| F07 canonical v4 runner | 342,980 / 103.378秒 | 151,138 / 92.434秒 | 102,504 / 72.547秒 |
| F07 dependency provenance | 159,373 / 71.659秒 | 99,981 / 61.354秒 | 87,284 / 54.324秒 |
| F08 CLI reference sync | 353,091 / 113.321秒 | 137,616 / 96.905秒 | 113,067 / 56.343秒 |
| F10 entrypoint inventory | 226,075 / 93.176秒 | 101,588 / 69.855秒 | 87,934 / 61.546秒 |
| F10 monthly format review | 234,222 / 72.442秒 | 84,139 / 53.550秒 | 93,096 / 51.796秒 |

Candidate147の集約中央値はC43 / C71より低い。一方、case別tokenではC71に対してF05 clarify、F05 out-of-scope、F06、F10 monthlyの4 caseで高かった。aggregate差を全case一様の低下として扱わない。

## 保存証拠

- Candidate43 result ID: `cc30c10d873743a7bbbc2d35463a4509`
- Candidate71 result ID: `819c9a1723a141589518d7dd06127710`
- Candidate43 pool: `e608c194ac1075d75578ce9c3d29c30dd8b20d0d68b8a6e2f5a58443e09430d2`
- Candidate71 pool: `a31cdfb86ec55819d3ec3d416a92bbcad9d92012ee1cd4ce82fc376b99a8256c`
- Candidate43 analysis: `de5a28837b2f436c96ec0a9758cdb5af`
- Candidate71 analysis: `8eb289a7952e47a39473f897f6ea042d`
- Candidate147 analysis: `16758ebbaef040328797739cd92f02fe`
- Candidate43 compact archive SHA-256: `be249126d0c5d43a6cc2a124b6a68b192d0cec6afe6c0aa213b9982fae1e952c`
- Candidate71 compact archive SHA-256: `6a0757bee55bdfa2aea43ec2b1e41071b5f4e7a80ffe2e1f55d87eac34374184`

raw evidence、selection、analysis、comparison viewは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/`配下へ保存した。登録済みrunと一次ratingは変更しない。
