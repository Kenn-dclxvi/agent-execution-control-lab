# Profiles

qualification、candidate-onlyおよびpaired comparison Profileの索引を置く。control-free N=1 qualification Profileは[`codex-validation-carrier-control-free-heldout-r1-codex-cli0146-sol-medium-n1-r1.json`](codex-validation-carrier-control-free-heldout-r1-codex-cli0146-sol-medium-n1-r1.json)で6件のvalid resultを取得し、測定経路をqualificationした。P002 candidate-only N=1 Profileは[`codex-validation-carrier-p002-heldout-r1-codex-cli0146-sol-medium-n1-r1.json`](codex-validation-carrier-p002-heldout-r1-codex-cli0146-sol-medium-n1-r1.json)で6件のvalid、Score 4、mechanism passを取得した。VCC6 P001/P002 N=5は[`vcc6-p001-p002-codex-cli0146-sol-medium-n5-r1.json`](vcc6-p001-p002-codex-cli0146-sol-medium-n5-r1.json)でP002 iteration 1の6件を再利用し、新規54 slotを共通キューへ発行した。結果はcost gate不通過である。

Candidate固有runnerを比較変数から除外する新しいN=1系列は、初回発行がfixture mode driftでmodel開始前に外部失敗となったため、初回[`P001`](vcc6-p001-shared-runner-sol-medium-n1-r1.json)、[`P002`](vcc6-p002-shared-runner-sol-medium-n1-r1.json)、[`P003`](vcc6-p003-shared-runner-sol-medium-n1-r1.json)を履歴として保持する。modeを固定Layer 1へ復元した後続は[`P001 r2`](vcc6-p001-shared-runner-sol-medium-n1-r2.json)、[`P002 r2`](vcc6-p002-shared-runner-sol-medium-n1-r2.json)および[`P003 r2`](vcc6-p003-shared-runner-sol-medium-n1-r2.json)を使う。3件はidentityとprompt bundle以外を同一にし、保存済みresultを再利用しない。

P004 candidate-only N=1は[`vcc6-p004-shared-runner-sol-medium-n1-r1.json`](vcc6-p004-shared-runner-sol-medium-n1-r1.json)を使う。P003 r2とprompt identity、Profile identityおよびexecution gate identity以外を一致させ、同じ共有runnerでfresh 6 slotだけを発行した。

P005 candidate-only N=1は[`vcc6-p005-shared-runner-sol-medium-n1-r1.json`](vcc6-p005-shared-runner-sol-medium-n1-r1.json)を使う。P004とprompt identity、Profile identityおよびexecution gate identity以外を一致させ、同じ共有runnerでfresh 6 slotを発行した。全件Score 4かつ機序成立となり、次のprofile class `vcc6_prompt_only_shared_runner_n5`を許可した。

P001・P003・P005のformal N=5は[`P001`](vcc6-p001-shared-runner-sol-medium-n5-r1.json)、[`P003`](vcc6-p003-shared-runner-sol-medium-n5-r1.json)、[`P005`](vcc6-p005-shared-runner-sol-medium-n5-r1.json)を使う。3件はprompt identityとProfile identity以外の条件を一致させ、各30 fresh slot、合計90 slotを発行した。
