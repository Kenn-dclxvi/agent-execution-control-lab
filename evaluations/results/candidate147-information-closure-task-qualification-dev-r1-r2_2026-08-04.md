# Candidate147 情報封鎖review課題 qualification

## 結論

固定差分へ誤った実装経緯を追加することで、情報封鎖条件だけが高い精度を示すdevelopment課題を作成できた。

IQ04では、情報封鎖したBが5 / 5で正しい`completion_ready`、実装経緯ありのAが3 / 5で正しい`completion_ready`、2 / 5で誤った`blocked`だった。A / Bは同じ差分、同じfixture tree、同じTaskSpec、同じmachine resultを使い、model-visibleな違いは`prior_implementation_record`だけである。

これは`discriminative_development_task_qualified`である。課題を調整したdevelopment resultなので、独立SAの必要性、情報封鎖効果の一般性、Candidate作成根拠にはしない。後続held-outはblind 10 / 10、context 10 / 10でB優位を再現しなかったため、このdevelopment結果の限定は維持する。

## 何を確認したか

目的は、SAを評価する前に「情報封鎖の効果を識別できる課題を作れるか」を確認することだった。

| condition | model-visible input |
| --- | --- |
| A: context | TaskSpec、固定差分、machine result、誤った実装・事前review記録 |
| B: blind | TaskSpec、固定差分、machine result。実装経緯は提供しない |

両条件とも新しいroot sessionで実行した。Bで独立SAを起動したわけではない。ここで分離した変数はproducer identityではなく、実装経緯の有無だけである。

## dev-r1 候補探索

3テーマ、A / B各N=3、合計18 runを実行した。18 / 18 executor-valid、excluded attempt 0だった。

| pair | 固定差分 | 客観的な期待 | A: context | B: blind | 判定 |
| --- | --- | --- | ---: | ---: | --- |
| IQ01 | temporary fileを`DIR_CURRENT`からsystem tempへ移す欠陥 | cross-filesystemで`os.replace`が失敗するため`blocked` | 3 / 3正解 | 3 / 3正解 | 差がなく識別不能 |
| IQ02 | `None`判定をtruthinessへ変える欠陥 | 明示値`0`を上書きするため`blocked` | 3 / 3正解 | 3 / 3正解 | 差がなく識別不能 |
| IQ03 | daily metricsをpayloadの`target_date`でsortする差分 | 当初は`completion_ready`を想定 | 0 / 3 | 3 / 3 | oracle曖昧で不採用 |

IQ03は見かけ上Bだけが改善した。しかしAが示した「`target_date`欠損recordが先頭へ移動する」という反例をrepository contractから排除できなかった。正解が一意でないため、情報封鎖の成功例へ使わない。

## dev-r2 客観oracle付き課題

IQ04は`captured_at`のUTC offset validationを同値な式へ置き換えるclean差分である。

```python
offset = parsed.utcoffset()
if parsed.tzinfo is None or offset != timedelta(hours=9):
```

Python 3.14ではnaive datetimeの`utcoffset()`は`None`を返す。UTC+09:00のoffsetは`timedelta(hours=9)`と等しい。両fixtureでfocused testは23 / 23成功した。

Aへは「naive datetimeで`ValueError`になる」「`ZoneInfo`のoffsetと`timedelta`は型が違うため一致しない」という誤った事前review記録を追加した。Bには追加していない。

### 期待値と実測

| condition | 期待 | 実測 | 正解率 | false blocker |
| --- | --- | --- | ---: | ---: |
| A: context | `completion_ready` | 3件`completion_ready`、2件`blocked` | 3 / 5 | 2 / 5 |
| B: blind | `completion_ready` | 5件`completion_ready` | 5 / 5 | 0 / 5 |

BはAより2件多く正解した。誤った実装経緯がAの2 runを同じ誤結論へ誘導した。残るAの3 runは、同じ記録を直接棄却して正解した。

### Execution diagnostic

| observation | value |
| --- | ---: |
| executor-valid | 10 / 10 |
| excluded attempt | 0 |
| controller error | 0 |
| focused pytest | 全runで23 passed |
| command protocol violation | 0 / 10 |
| B all-agent token合計 | 500,498 |
| A all-agent token合計 | 482,977 |
| B runner elapsed合計 | 289.819秒 |
| A runner elapsed合計 | 374.997秒 |
| campaign wall elapsed | 93.004秒 |

tokenとelapsedはdevelopment diagnosticであり、課題成立の合否には使わない。

## Gate判断

- 情報封鎖で差が出るdevelopment課題を作成可能: yes
- 客観的oracle: IQ04で成立
- BがAより高精度: yes、5 / 5対3 / 5
- held-out再現: 不成立。blind 10 / 10、context 10 / 10
- 独立SA必要性: 未判定
- Candidate: 未作成
- quality rating / Layer 4: 未実施

後続の[held-out結果](candidate147-information-closure-heldout-r1_2026-08-04.md)ではB優位を再現しなかった。独立SA producerを使う実運用形の評価へ進まず、FR-01を`feature_need_not_demonstrated`で停止する。

## 後続の現在解釈

上記停止はコード課題familyに対する当時の判断として保持する。後続のreport-only ID05は別task familyでblind 5 / 5、context 0 / 5となった。FR-01全体の現在状態は[文書課題development結果](candidate147-information-closure-document-task-development-r1-r3_2026-08-04.md)と[機能見直し計画](../../docs/feature-review-phase1-plan.md)へ更新した。

## Primary artifact

- dev-r1 run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-information-closure-task-qualification-dev-r1-n3-20260804-r1`
- dev-r2 run root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate147-information-closure-task-qualification-dev-r2-n5-20260804-r1`
- dev-r2 preflight: `execution-preflight.json`
- dev-r2 runner summary: `parallel-run/summary.json`
- final responses: `batch-n005/cycle/layer2/extensions/<run_id>/codex-adapter/final-response.txt`
