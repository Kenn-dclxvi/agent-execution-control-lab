# agent-execution-control-lab PRレビュー測定 instructions

この領域は、`agent-execution-control-lab`を対象とするPRレビュー方式のnamespacedターゲットインスタンスである。ルート、`evaluations/AGENTS.md`、`evaluations/targets/AGENTS.md`を追加適用する。

- ケース、セット、プロファイル、rating contract、result、target固有の採点補助をこのインスタンス配下へ閉じる。target固有case IDや分岐をルート`scripts/`へ追加しない。
- 各case revisionの`input.json`だけをmodel-visibleなcase入力とする。`oracle.json`、expected finding、grader内部値をreviewer jobへ渡さない。
- fixture、contract、schemaはrevision単位で固定し、result確認後にその場で変更しない。
- 新インスタンスゲート未通過の間は、profileへ固定したqualificationスロット以外を発行しない。profile外のGitHub Actions artifactを正式evaluation resultとして登録しない。
- 2026-08-08のprobeは新インスタンス登録前のdiagnostic receiptであり、quality score、3 KPI比較、採用判断へ使わない。
- 生のAction出力、非公開log、credentialをcommitしない。診断receiptへは許可済みfieldとGitHub run identityだけを保持する。
- Core ReviewではGitHubへcommentを書き込まない。GitHub反映はquality gate通過後に別のIntegration測定として設計する。
- エラー、schema不適合、quality失敗、timeout、取消、計測不完全を別statusとして保持する。

## 利用者向けの呼称

- 試験問題は`Case`、一つの比較目的と条件を固定する単位は`Measurement Series`、実行条件JSONは`Profile`、各実行の一次結果は`Run Result`と呼ぶ。
- PRレビュー方法の版を利用者向けに識別するときは、機能名を略した呼称ではなく、リポジトリ全体で一意な連番の`Candidate<number>`を使う。機能名は変更内容の説明にだけ使い、版の略称にはしない。
- Candidate番号は一度割り当てたprompt identityから別identityへ付け替えない。modelやCaseなどの測定条件はCandidate番号へ含めず、ProfileまたはRun Resultで区別する。
- 正式なprompt identityと既存の不変identityは改称しない。Candidate番号との対応は`prompts/README.md`を正本とする。
