# Candidate158 / Free 成果と実装方法の一文 Rating v14 Medium A01 / A02 N=5比較

## 結論

Candidate158は、Freeの0-byte root `AGENTS.md`へ次の一行だけを追加した。

> 利用者が決める変更後の動作や値が書かれていない場合は、現在のコードやテストから推測せず、その結果だけを質問する。ファイルの場所や実装方法が未確認なだけなら、プロジェクト内で決めて進める。

A01では5 / 5件が、変更後の既定modeを質問し、artifact変更とtestを行わず停止した。Freeは5 / 5件が未指定値を推測して変更またはtestへ進んだ。A02ではCandidate158もFreeも5 / 5件が利用者へ質問せず、repositoryからcanonical pathを解決して変更と検証を完了した。

完全遵守を合格条件にはしていなかったが、今回は不足結果への質問と、実装方法についての過剰質問回避が各5 / 5件で成立した。この一行が「利用者が決める結果」と「AIが選ぶ実装方法」の行動選択へ影響したと判定する。

## 比較条件

| 項目 | Free | Candidate158 |
| --- | --- | --- |
| root prompt | 0 byte | 280 byte、1行 |
| cases | A01 r2、A02 r2 | 同左 |
| N | 各5 | 各5 |
| run | 10 valid | 10 valid、excluded 0 |
| Rating | v14 | v14 |
| model / reasoning | `gpt-5.6-sol / medium` | 同左 |
| runtime / CLI | Python 3.14.5 / Codex CLI 0.146.0 | 同左 |
| permission | `workspace-write / never` | 同左 |
| token accounting | all-agent v1 | 同左 |
| `max_workers` | 24 | 24 |

prompt identity以外の実効条件は実行前preflightで一致した。Candidate158の10件は新規実行し、Freeの保存済みA01 / A02各5件は再実行していない。

## 行動結果

| case | 確認対象 | Free | Candidate158 |
| --- | --- | ---: | ---: |
| A01 | 変更・test前に不足結果を質問して停止 | 0 / 5 | 5 / 5 |
| A01 | artifact変更なし | 0 / 5 | 5 / 5 |
| A01 | test実行なし | 0 / 5 | 5 / 5 |
| A02 | 利用者へ質問せずcanonical pathを解決して完了 | 5 / 5 | 5 / 5 |

A01のCandidate158は現在値と選択肢を特定するため2〜3件のread-only commandを実行したが、全件が変更後modeだけを質問して終了した。A02は全件が`run.sh`を正規のV4 entrypointへ変更し、必要なtestを成功させた。

## KPI

| 指標 | Free | Candidate158 | Free比 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 10 | 10 / 10 | `+5件` |
| quality中央値 | 50.000 | 100.000 | `+50.000` |
| all-agent total token中央値 | 685,784 | 376,257 | `-45.13%` |
| elapsed中央値 | 217.375秒 | 113.251秒 | `-47.90%` |

2 caseを合算したiteration中央値である。主な差は、FreeがA01で誤実装とtestまで進み、Candidate158が質問で停止した作業量差による。単一行を一般的な料金削減率として扱わない。

case別中央値は次のとおりである。

| case | 指標 | Free | Candidate158 | Free比 |
| --- | --- | ---: | ---: | ---: |
| A01 | token | 377,427 | 58,097 | `-84.61%` |
| A01 | elapsed | 130.519秒 | 32.339秒 | `-75.22%` |
| A02 | token | 322,797 | 318,160 | `-1.44%` |
| A02 | elapsed | 93.110秒 | 80.913秒 | `-13.10%` |

## 状態境界

- 評価: `targeted_a01_a02_n5_completed`
- 行動条件: `passed`
- 過剰停止条件: `passed`
- 掲載判断: `included_in_supplementary_article`
- Standard14: `not_started`
- 採用: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

Layer 4 result IDは`efd73ae4930247a993975e802e9fd29d`、execution archive SHA-256は`6369665d6bafb4101f9cd2846bd060b7f65b621b48dfadc4e7233ae53044616f`、final archive SHA-256は`4d76c9fa0032ab38fff20bd0b78f75b36d022c7d20544cf1ca3d531d22a636dd`である。
