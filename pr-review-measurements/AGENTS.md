# PRレビュー測定 instructions

この領域は、GitHub上のAI PRレビュー方式を固定fixtureで比較する測定アーティファクトを扱う。既存の`evaluations/`はプロンプト比較基盤であり、この領域のfixture、oracle、resultを混ぜない。

- `input.json`だけをmodel-visible入力とする。`oracle.json`、expected finding、grader内部値をreviewer jobへ渡さない。
- fixture、contract、schemaはrevision単位で固定し、result確認後にその場で変更しない。
- run resultはappend-onlyとし、同じ`case / variant / repetition / attempt`を上書きしない。
- 生のAction出力、非公開log、token、credentialをcommitしない。一次resultへは許可済みfieldだけを抽出する。
- BaselineとCandidate Aで、review contract、model、Action revision、fixture revision、permission profile、timeoutを一致させる。
- Core ReviewではGitHubへcommentを書き込まない。GitHub反映はquality gate通過後のIntegration測定へ限定する。
- エラー、schema不適合、quality失敗、timeout、取消、計測不完全を別statusとして保持する。
