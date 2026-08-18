# Profiles

現行Profileは[`portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r4.json`](portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r4.json)である。Codex CLI 0.146.0、GPT-5.6 Sol、reasoning `medium`、read-only permission、N=1、全14 Case、Structured Outputs subsetへの意味保存投影、canonical事後検証、all-agent token accounting v2および共通TaskSpec wrapperを固定する。

Profile記録上のlifecycle値は`registered_not_qualified`を履歴互換のため維持するが、r4の資格確認resultは14/14有効で測定成立gateを通過した。品質はscore 4が5/14で、採用gateではない。

r1からr3はそれぞれ`uniqueItems`、型なし`const`、exec JSONL一次token欠落を観測した失敗Profileとして保持する。現行登録は[`profile-registration-r4.json`](profile-registration-r4.json)、発行許可は[`preflight-r4`](../plans/portable-semantic-control-free-heldout-r1-n1-preflight-r4.json)、結果は[`qualification-r4`](../results/portable-semantic-control-free-heldout-r1-n1-qualification-r4.json)を正とする。

portable full-agent Candidateは[`Profile r1`](portable-semantic-c147-portable-full-agent-codex-cli0146-sol-medium-heldout-r1-n1-r1.json)と[`registration`](profile-registration-portable-full-agent-r1.json)へ別系列で登録した。control-free r4からprompt identityと系列identityだけを変更し、runtime、Case、rating、schema transport、token accountingおよびN=1条件を維持する。C147 reference ProfileはCandidateのquality gate通過前なので未作成である。

Candidate r1は14 / 14 valid、7 / 14 score 4だった。後続監査で、semantic set自体をC147 referenceで先に資格確認する必要があると判定したため、[`C147 reference Profile r1`](portable-semantic-c147-full-agent-reference-codex-cli0146-sol-medium-heldout-r1-n1-r1.json)と[`registration`](profile-registration-c147-reference-r1.json)を別系列で固定した。referenceは14 / 14 valid、6 / 14 score 4となり、held-out r1をC147同等性テストとして使用しない。旧Candidate-first停止条件は履歴として保持する。

response fieldを今回の遷移だけへ限定するTaskSpec r2は、[`C147 transition calibration Profile`](portable-semantic-c147-reference-transition-calibration-codex-cli0146-sol-medium-r2-n1-r1.json)と[`registration`](profile-registration-c147-reference-transition-calibration-r2.json)へ登録した。既存14 Caseはreference calibrationだけへ再利用し、portable Candidateのheld-outには使わない。

契約矛盾を修正した校正revisionは、[`r3 Profile`](portable-semantic-c147-reference-transition-calibration-codex-cli0146-sol-medium-r3-n1-r1.json)／[`registration`](profile-registration-c147-reference-transition-calibration-r3.json)と[`r4 Profile`](portable-semantic-c147-reference-transition-calibration-codex-cli0146-sol-medium-r4-n1-r1.json)／[`registration`](profile-registration-c147-reference-transition-calibration-r4.json)へ分離した。r4がC147 14 / 14 gateを通過したが、portable評価は独立heldoutの凍結まで開始しない。

独立heldoutのC147先行Profileは、設計不適格となった[`heldout r2`](portable-semantic-c147-reference-heldout-r2-codex-cli0146-sol-medium-n1-r1.json)と、14 / 14を通過した[`heldout r3`](portable-semantic-c147-reference-heldout-r3-codex-cli0146-sol-medium-n1-r1.json)を別登録で保持する。r3通過後にだけ[`portable heldout r3 Profile`](portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n1-r1.json)を作成し、prompt identity以外の条件を一致させた。

N=5拡張は[`C147 Profile`](portable-semantic-c147-reference-heldout-r3-codex-cli0146-sol-medium-n5-r1.json)／[`registration`](profile-registration-c147-reference-heldout-r3-n5-r1.json)と[`portable Profile`](portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n5-r1.json)／[`registration`](profile-registration-portable-full-agent-heldout-r3-n5-r1.json)へ分離した。既存i001を再利用し、新規発行はi002〜i005だけとする。

N=20拡張は[`C147 Profile`](portable-semantic-c147-reference-heldout-r3-codex-cli0146-sol-medium-n20-r1.json)／[`registration`](profile-registration-c147-reference-heldout-r3-n20-r1.json)と[`portable Profile`](portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n20-r1.json)／[`registration`](profile-registration-portable-full-agent-heldout-r3-n20-r1.json)へ分離した。N=5の70 runを再利用し、新規発行はi006〜i020の210 runだけとする。
