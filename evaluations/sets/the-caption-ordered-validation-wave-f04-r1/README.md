# THE-CAPTION ordered validation wave F04対象試験 第1版

## 結論

Candidate71とCandidate79について、順序依存required validationのmodel再入をF04 r2で各5回確認する。

これは項目固有の原因確認であり、標準14項目の全体試験へ読み替えない。

## 構成

| 評価項目 | 版 | 観測する境界 |
| --- | --- | --- |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | `r2` | `npm ci`成功後のlint、lint成功後のbuildを一つのmodel stepへ閉じる |

## 固定条件

- target commit / tree、model、Agent環境、permission、token accountingはrating v13標準14項目試験と同じにする。
- reasoning effortは`medium`へ固定する。
- case revisionとmodel-visible TaskSpecは標準14項目から変更しない。
- quality ratingは`outcome-abstract-condition-preserving-owner-diagnostic-v13`を使用する。
- 3 required commandは個別commandとstructured exitを維持する。shell commandを結合しない。
- C71 / C79のprofile差は`profile_id`と`prompt_set_identity`だけにする。
- 各prompt setはF04を5回実行する。

## 判定範囲

両条件とも5 / 5 valid・rateable・score `4`、zero drift、required command欠落0、protocol違反0を必要条件とする。

Candidate79ではvalidation中間のmodel再入がCandidate71より減ることを要求する。3 KPIを記録し、tokenまたはelapsedが減らない場合はその削減を主張しない。

この対象試験は標準14項目完了、採用、release、runtime projectionを判断しない。

## 実行結果

[Candidate71 / Candidate79各N=5結果](../../results/candidate71-candidate79-ordered-validation-wave-v13-medium-f04-n5_2026-07-26.md)をappend-only registryへ登録した。Candidate79は1-step closureが`3 / 5 -> 0 / 5`、token中央値が`+16.88%`となり、事前gate不通過のため`targeted_evaluated / stopped`である。
