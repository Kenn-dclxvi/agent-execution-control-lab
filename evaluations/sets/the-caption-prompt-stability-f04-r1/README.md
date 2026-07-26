# THE-CAPTION prompt stability F04対象試験 第1版

## 結論

Candidate71とCandidate80について、同一F04課題の1-step validation closureをprompt変更だけで各10回確認する。

主判定は動作再現率である。tokenとelapsedは診断として記録するが、prompt安定性の合否条件にしない。

## 構成

| 評価項目 | 版 | 観測対象 |
| --- | --- | --- |
| `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | `r2` | 3 required commandの1-step closureと成果品質 |

## 固定条件

- prompt以外のmodel、Medium、Agent環境、TaskSpec、permission、fixture、Rating v13、command evidence protocol v1、反復条件、実効`M=10`を一致させる。
- C71 / C80のprofile差は`profile_id`と`prompt_set_identity`だけにする。
- 各prompt setはF04を10回実行する。
- required commandは個別commandとstructured exitを維持し、shell compound commandへまとめない。

## 成功条件

- Candidate80の1-step closureが10 / 10である。
- Candidate80の10 / 10がvalid・rateable・score `4`である。
- required validation欠落、protocol違反、順序違反、workspace driftが0件である。

token、elapsed、tool call、message数は診断として保存するが成功条件にしない。

この対象試験は標準14項目完了、採用、release、runtime projectionを判断しない。
