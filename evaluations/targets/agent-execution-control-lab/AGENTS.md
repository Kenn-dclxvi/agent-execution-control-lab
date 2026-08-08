# agent-execution-control-lab PRレビュー測定 instructions

この領域は、`agent-execution-control-lab`を対象とするPRレビュー方式のnamespacedターゲットインスタンスである。ルート、`evaluations/AGENTS.md`、`evaluations/targets/AGENTS.md`を追加適用する。

- ケース、セット、プロファイル、rating contract、result、target固有の採点補助をこのインスタンス配下へ閉じる。target固有case IDや分岐をルート`scripts/`へ追加しない。
- `cases/*/r1/input.json`だけをmodel-visible入力とする。`oracle.json`、expected finding、grader内部値をreviewer jobへ渡さない。
- fixture、contract、schemaはrevision単位で固定し、result確認後にその場で変更しない。
- `current_rating_contract=null`かつ新インスタンスゲート未通過の間は、GitHub Actions artifactを正式evaluation resultとして登録しない。
- 2026-08-08のprobeは新インスタンス登録前のdiagnostic receiptであり、quality score、3 KPI比較、採用判断へ使わない。
- 生のAction出力、非公開log、credentialをcommitしない。診断receiptへは許可済みfieldとGitHub run identityだけを保持する。
- Core ReviewではGitHubへcommentを書き込まない。GitHub反映はquality gate通過後に別のIntegration測定として設計する。
- エラー、schema不適合、quality失敗、timeout、取消、計測不完全を別statusとして保持する。
