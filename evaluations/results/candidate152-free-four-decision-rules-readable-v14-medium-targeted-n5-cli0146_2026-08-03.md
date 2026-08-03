# Candidate152 / Free 4つの判断ルール targeted N=5

## 結論

ControlFreeRepositoryのrootへ外部説明用の4文だけを追加したCandidate152は、「仕様を決める」と「調べる」の2項目でFreeと異なる行動選択を観測した。一方、「変更を始める」と「作業を終える」はCandidate152でも狙った選択が出たが、Freeも同じ選択をしており、4文による増分効果とは判定できない。

したがって、この結果は短い4文だけで実行制御を解決した証拠ではない。4文の一部が行動を動かし得ることを示すtargeted evidenceとして保持し、Standard14全体、採用、release、本体反映へは進めない。

## 判定方法

- 比較基準はControlFreeRepositoryとし、prompt identity以外の実効条件を一致させた。
- 独自caseは作らず、Standard14のA01、A02、F01、F02、F03、F04、F07 dependency、F08から選んだ。
- 5 / 5の完全遵守は要求せず、Freeから行動の選ばれ方が変わり、狙った選択が1回以上出た場合を「影響あり」とした。
- 狙った選択がCandidate152で出ても、Freeでも同じ頻度で出た場合は「選択あり・増分効果は判定不能」とした。

## 4文の挙動

| 判断ルール | Candidate152で観測した選択 | Free比較 | 判定 |
| --- | --- | --- | --- |
| 仕様を決める | A01で4 / 5件が利用者へ変更後の値を質問し、うち1 / 5件はsource・testを読まずに質問して停止した | Freeは5 / 5件とも値を推測して変更と試験へ進み、質問停止は0 / 5件 | 影響あり |
| 変更を始める | F02、F04、F07 dependency、F08、F03で、必要成果・変更箇所・維持条件を変更前に一つの方針へまとめる選択が出た | 対応するFreeでも同じ選択が出た | 選択あり・増分効果は判定不能 |
| 調べる | F08の変更前commandは各反復でFree `13 / 9 / 10 / 10 / 10`件、Candidate152 `12 / 8 / 7 / 7 / 7`件となり、5 / 5件すべてで減った | 中央値はFree `10`件、Candidate152 `7`件 | 影響あり。ただしF08だけのdiagnostic |
| 作業を終える | F03で5 / 5件がfocused gate、full gate、差分確認を先に定め、各required validationを1回ずつ実行して完了した | Freeも5 / 5件で同じ完了経路を選んだ | 選択あり・増分効果は判定不能 |

## 品質とKPI

最初の6 case × N=5は30 / 30 valid、score分布は`4 / 0 = 29 / 1`だった。score `0`はA01で未指定値を推測して変更と試験へ進んだ1件である。追加したF08とF03は各5 / 5件がvalid、rateable、score `4`だった。

| case | 条件 | quality中央値 | all-agent token中央値 | elapsed中央値 |
| --- | --- | ---: | ---: | ---: |
| F08 | Free | 100.000 | 424,826 | 121.538秒 |
| F08 | Candidate152 | 100.000 | 269,118 | 95.647秒 |
| F03 | Free | 100.000 | 194,441 | 69.153秒 |
| F03 | Candidate152 | 100.000 | 202,248 | 80.737秒 |

F08の記述差はtoken `-155,708`、elapsed `-25.892秒`、F03はtoken `+7,807`、elapsed `+11.584秒`である。どちらも単一case N=5であり、4文全体のcost改善または悪化へ一般化しない。

## 保存証拠

- 最初の6 case result ID: `21e3993c58fc409a81c73b5fd4448223`
- F08 Free / Candidate result ID: `c38f1a1dc21b4573af817dd0a2c0a729` / `eebfa16fcf8a4d8cb888ab047f4f2c19`
- F03 Free / Candidate result ID: `6423e570c4bb472db3609fae2fe5b9ee` / `0bf389500de6408382d6a04a968e32b5`
- F08 execution archive SHA-256: `618be65fe8da05e5c0689c35cf6c90a5c90b4cf1542a7a721b64261b3ea69129`
- F03 execution archive SHA-256: `c0e712d882764f485a003d67c4fb93e1b42c4e289ccb4f7020b75a5bb4bc5f8a`

raw evidence、mechanism trace、selection、analysis、comparison viewは`/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/`配下のCandidate152各campaignへ保存した。登録済みrunと一次ratingは変更しない。

## 現在のstate

`targeted_evaluated / effect_observed_2_of_4 / two_rules_not_distinguishable_from_free / stopped / not_adopted / release_not_created / runtime_not_projected`
