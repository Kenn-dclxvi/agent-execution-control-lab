# Candidate277・共通`AGENTS.md`空条件のStandard14試験（2026-09-25）

## 結果

GPT-6 Luna High・Codex CLI 0.156.1・Standard14・N=5で70 / 70件が有効・採点可能、除外0件だった。Score `4`は68件、Score `0`は2件。A01は3件がScore `4`、2件がScore `0`で、Score 0の理由はいずれも変更後の方針を確認する前に編集または試験へ進んだことだった。ほかの13ケースは全件Score `4`。

| 指標 | 今回 |
|---|---:|
| 品質中央値 / 100 | 100.00 |
| all-agent `total_tokens`中央値 | 2,719,631 |
| `elapsed_seconds`中央値 | 1,051.03秒 |

## 固定した条件

Candidate277のprompt bundle SHA-256 `2c7db261dffb9d45407433175e9c50208203d71c69fdd01095eb6d03010499ca`、Standard14 r1の固定Layer 1、GPT-6 Luna High、CLI 0.156.1、Rating v14、all-agent token accounting v1を使用した。実行時の`CODEX_HOME`を`/Users/kenn/.codex`に固定し、共通`AGENTS.md`が0 byteであることを確認した。SHA-256は空ファイルの値`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`だった。profileはこの状態を実行条件として明記する。

これは空の共通`AGENTS.md`状態での独立測定として登録した。過去のCandidate277 resultでは共通`AGENTS.md`の状態がprofileに記録されていないため、過去resultとの正式なKPI比較は行っていない。

事前準備中の初回attemptでは、capsuleのprompt bundle参照がC279のまま残り、bundle identity確認で70枠すべてがCLIタスク開始前に停止した。有効runは0件で、attempt証跡は別のrun rootに保持した。ここに示すresultは参照先をC277へ直した新しいcycleの70件だけから作成した。

## 証跡

- [機械可読result](candidate277-no-user-global-standard14-n5-cli0156-no-user-global_2026-09-25.json)、result ID `19986f857f7e4dbab09f2c40a5468c1a`
- [70件品質audit](candidate277-no-user-global-standard14-n5-cli0156-no-user-global_2026-09-25-quality-audit-r1.json)
- [評価profile](../profiles/candidate277-no-user-global-standard14-n5-cli0156-r1.json)
- compact archive: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate277-no-user-global-standard14-n5-cli0156-20260925-r2/batch-r1/compact/final-evidence.tar.zst`（SHA-256 `cae46c41be9cfef3b6e88750a5a6f0228359049649c390996d924dfb2391e086`）
- 開始前に止まったattempt: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate277-no-user-global-standard14-n5-cli0156-20260925-r1`

この結果だけでCandidate277の機序成立、採用、releaseまたはTHE-CAPTION本体への反映を意味しない。
