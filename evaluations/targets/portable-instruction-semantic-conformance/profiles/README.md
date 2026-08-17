# Profiles

現行Profileは[`portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r4.json`](portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r4.json)である。Codex CLI 0.146.0、GPT-5.6 Sol、reasoning `medium`、read-only permission、N=1、全14 Case、Structured Outputs subsetへの意味保存投影、canonical事後検証、all-agent token accounting v2および共通TaskSpec wrapperを固定する。

Profile記録上のlifecycle値は`registered_not_qualified`を履歴互換のため維持するが、r4の資格確認resultは14/14有効で測定成立gateを通過した。品質はscore 4が5/14で、採用gateではない。

r1からr3はそれぞれ`uniqueItems`、型なし`const`、exec JSONL一次token欠落を観測した失敗Profileとして保持する。現行登録は[`profile-registration-r4.json`](profile-registration-r4.json)、発行許可は[`preflight-r4`](../plans/portable-semantic-control-free-heldout-r1-n1-preflight-r4.json)、結果は[`qualification-r4`](../results/portable-semantic-control-free-heldout-r1-n1-qualification-r4.json)を正とする。
