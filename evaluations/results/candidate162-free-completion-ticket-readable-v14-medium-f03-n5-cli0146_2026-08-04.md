# Candidate162 / Free 完了実行票一文 Rating v14 Medium F03 N=5比較

## 結論

Candidate162は、Freeの0-byte root `AGENTS.md`へ次の一文だけを追加した。

> 変更後は、必要なテストと差分確認を一つの実行票として先に固定し、実行中は同じ結果だけを待ち、失敗なら後続を止め、全結果がそろったら追加確認せず一度だけ完了を判断する。

F03 N=5では5 / 5件がscore `4`だった。最初のcommand前にfocused test、full validation、差分確認を具体的な実行票として示した実行はFreeの`0 / 5件`からCandidate162の`5 / 5件`へ増えた。Candidate162ではrequired validationの根拠のない再実行と、最終差分確認後の追加調査も0 / 5件だった。

したがって、この一文が完了条件を作業開始時に具体化する選択へ影響したと判定する。token中央値は下がったがelapsed中央値は増えたため、料金または所要時間の一律改善には一般化しない。

## 比較条件

| 項目 | Free | Candidate162 |
| --- | --- | --- |
| root prompt | 0 byte | 1文 |
| case | F03 r2 | 同左 |
| N | 5 | 5 |
| Rating | v14 | 同左 |
| model / reasoning | `gpt-5.6-sol / medium` | 同左 |
| runtime / CLI | Python 3.14.5 / Codex CLI 0.146.0 | 同左 |
| permission | `workspace-write / never` | 同左 |
| token accounting | all-agent v1 | 同左 |
| `max_workers` | 24 | 24 |

prompt identity以外の実効条件は実行前preflightで一致した。Candidate162の不足5 runだけを新規発行し、Freeの保存済みF03 5件は再実行していない。

## 結果

| 指標 | Free | Candidate162 | Free比 |
| --- | ---: | ---: | ---: |
| score `4` | 5 / 5 | 5 / 5 | 差0 |
| 最初のcommand前の具体的実行票 | 0 / 5 | 5 / 5 | +5件 |
| required validation再実行 | 0 / 5 | 0 / 5 | 差0 |
| 最終差分確認後の追加調査 | 0 / 5 | 0 / 5 | 差0 |
| all-agent total token中央値 | 194,441 | 175,411 | `-9.79%` |
| elapsed中央値 | 69.153秒 | 76.564秒 | `+10.72%` |

## 状態境界

- 評価: `targeted_f03_n5_completed`
- 品質gate: `passed`
- 行動条件: `passed`。最初のcommand前の具体的実行票`0 / 5 → 5 / 5`
- 閉鎖条件: `passed`。再検証・追加調査`0 / 5`
- cost結果: `mixed`
- 掲載判断: `included_in_supplementary_article`
- Standard14: `not_started`
- 採用: `not_decided`
- release: `not_created`
- runtime projection: `not_authorized`

Layer 4 result IDは`5e7a309c793246f3909fab458d5332b2`、execution archive SHA-256は`a8c4f16d24f98148793a129d21de59bb5c2da4b237e478ef6da6c0ce8347bd9a`、final archive SHA-256は`10630995416af2e698745681cf23b10d26e924ab9c67c76fbae7082bf61ac355`である。
