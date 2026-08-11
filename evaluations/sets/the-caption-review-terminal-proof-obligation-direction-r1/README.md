# review terminal proof obligation direction

最小方向設計を情報封鎖したLLM実行で確認するdevelopment Evaluation set。held-out evidenceではない。

- set identity: `the-caption-review-terminal-proof-obligation-direction-r1`
- general design identity: `review-terminal-proof-obligation-minimal-direction-r1`
- Target評価設計identity: `review-terminal-proof-obligation-targeted-evaluation-design-r1`
- case suite revision: `review-terminal-proof-obligation-r1`

| case | identity |
|---|---|
| `TC-TPO01` | `TC-TPO01/review-terminal-proof-obligation-r1` |
| `TC-TPO02` | `TC-TPO02/review-terminal-proof-obligation-r1` |
| `TC-TPO03` | `TC-TPO03/review-terminal-proof-obligation-r1` |
| `TC-TPO04` | `TC-TPO04/review-terminal-proof-obligation-r1` |
| `TC-TPO05` | `TC-TPO05/review-terminal-proof-obligation-r1` |
| `TC-TPO06` | `TC-TPO06/review-terminal-proof-obligation-r1` |

Candidate173を診断対照として各ケース`N=5 valid`を実行し、30 / 30 valid、Score `4 = 30 / 30`、機構成立27 / 30だった。`TC-TPO04`で必要reviewを省略してartifact変更と完了へ進む同一誤経路が3 / 5件再現し、controlの`TC-TPO05`はreview 0件で5 / 5件を完了した。事前条件により新Candidate作成条件は成立したが、新Candidateはまだ作成していない。結果は[`問題資格確認 r1`](../../results/candidate173-review-terminal-proof-obligation-problem-qualification-r1_2026-08-12.md)を正本とする。

後続のCandidate187[`Targeted r1`](../../results/candidate187-review-admission-proof-obligation-targeted-r1_2026-08-12.md)は30 / 30 Score `4`、機構30 / 30だった。`TC-TPO04`の必要reviewerは5 / 5件、対象誤経路は0 / 5件となり、`TC-TPO05`と`TC-TPO06`のreview 0件controlも維持した。これはdevelopment Target gate通過であり、expanded評価、採用、releaseまたはprojectionではない。
