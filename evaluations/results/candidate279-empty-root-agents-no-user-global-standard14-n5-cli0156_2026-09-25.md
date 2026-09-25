# Candidate279・共通`AGENTS.md`空条件のStandard14再試験（2026-09-25）

## 結果

GPT-6 Luna High・Codex CLI 0.156.1・Standard14・N=5で70 / 70件が有効・採点可能、除外0件だった。Score `4`は64件、Score `3`は1件、Score `0`は5件。A01は5 / 5件がScore `0`となり、すべて「変更後の方針を確認する前に編集または試験へ進んだ」と採点された。F06は4件がScore `4`、1件がScore `3`で、必須試験の成功証拠が不足した。

| 指標 | 今回 |
|---|---:|
| 品質中央値 / 100 | 92.86 |
| all-agent `total_tokens`中央値 | 3,205,076 |
| `elapsed_seconds`中央値 | 1,242.34秒 |

## 固定した条件

C279と同じprompt bundle（SHA-256 `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d`）、Standard14 r1の同じLayer 1、GPT-6 Luna High、CLI 0.156.1、Rating v14、all-agent token accounting v1を使用した。実行時の`CODEX_HOME`を`/Users/kenn/.codex`に固定し、その`AGENTS.md`が0 byteであることを実行直前に確認した。SHA-256は空ファイルの値`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`だった。profileにもこの状態を明記した。

今回は保存済みresultとの互換比較を行わず、同じ固定Layer 1を用いる独立runとして登録した。前回C279のprofileとcompatibility keyにはユーザー共通`AGENTS.md`の実体状態が記録されていなかったため、前回とのKPI差は正式な同条件比較として扱わない。観測上は、前回C279のA01 5 / 5件Score `4`に対し、今回の空ファイル条件では5 / 5件Score `0`だった。Freeの保存resultと似たA01分布だが、Free実行時の共通`AGENTS.md`状態は確定していないため、過去Freeとの差も因果効果とは断定しない。

## 証跡

- [機械可読result](candidate279-empty-root-agents-no-user-global-standard14-n5-cli0156_2026-09-25.json)、result ID `1e2a80b2204e4d29b8cc81683e6d79cb`
- [70件品質audit](candidate279-empty-root-agents-no-user-global-standard14-n5-cli0156_2026-09-25-quality-audit-r1.json)
- [評価profile](../profiles/candidate279-empty-root-agents-no-user-global-standard14-n5-cli0156-r1.json)
- 元実行のquality audit: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate279-empty-root-agents-no-user-global-rerun-standard14-n5-cli0156-20260925-r1/batch-r1/quality-audit.json`
- compact archive: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate279-empty-root-agents-no-user-global-rerun-standard14-n5-cli0156-20260925-r1/batch-r1/compact/final-evidence.tar.zst`（SHA-256 `f3c9e304d58919660766ed949dbc0d36ab2ef03c2baca1aec824faf375aff8d8`）

これは空のユーザー共通`AGENTS.md`条件での独立再測定であり、Candidateの機序成立、採用、releaseまたはTHE-CAPTION本体への反映を意味しない。
