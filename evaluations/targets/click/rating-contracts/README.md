# click rating contract index

`click` target instanceのquality rating contract revisionを引くための索引である。instance固有contractの更新、kernel登録、再採点禁止の規則は[`../AGENTS.md`](../AGENTS.md)を正本とする。現行contract identityは[`target.json`](../target.json)の`current_rating_contract`、各revisionの条件とSHA-256はcontract JSONを正とする。

## Contract revisions

| contract_id | schema | contract SHA-256 | 対象case |
| --- | --- | --- | --- |
| [`click-outcome-abstract-condition-preserving-v1`](click-outcome-abstract-condition-preserving-v1.json) | `the-caption-prompt.quality-rating-contract/v13` | `7057dd0790a62a636f7de4b389d2f3e8526c4b578819842472d92ff49a93747d` | `CLICK-F01-ANSI-SEQUENCE-STRIP`（履歴） |
| [`click-outcome-abstract-condition-preserving-v2`](click-outcome-abstract-condition-preserving-v2.json) | `the-caption-prompt.quality-rating-contract/v13` | `9f09b4230e19497bb752f77ef8a22b006fc505aa216a4575b2bff3eeaf143f80` | F01〜F02（履歴） |
| [`click-outcome-abstract-condition-preserving-v3`](click-outcome-abstract-condition-preserving-v3.json) | `the-caption-prompt.quality-rating-contract/v13` | `0d165083c8629223f71aa7a53953a1d05ab90e36b99533ee7c0c1a60a53fd0a2` | F01〜F04（履歴） |
| [`click-outcome-abstract-condition-preserving-v4`](click-outcome-abstract-condition-preserving-v4.json) | `the-caption-prompt.quality-rating-contract/v13` | `e2316a51ab0e51d08191165155781d860b0219350be8f51c2e4583f630f49746` | F01〜F05-OS（履歴） |
| [`click-outcome-abstract-condition-preserving-v5`](click-outcome-abstract-condition-preserving-v5.json) | `the-caption-prompt.quality-rating-contract/v13` | `054335e43d386251b81040bae080430cbca2a85e60c96f6a7100e536242ed5ab` | F01〜F06（履歴） |
| [`click-outcome-abstract-condition-preserving-v6`](click-outcome-abstract-condition-preserving-v6.json) | `the-caption-prompt.quality-rating-contract/v13` | `d8fe38996cf270120977bb22f0434edb85de9040e4e5593b18481dddb69a78c4` | F01〜F07（履歴） |
| [`click-outcome-abstract-condition-preserving-v7`](click-outcome-abstract-condition-preserving-v7.json) | `the-caption-prompt.quality-rating-contract/v13` | `23458c2abc303f657265c8769268883bb659e34c1c499fc5a8e8d9b45e3137bb` | F01〜F07-P（履歴） |
| [`click-outcome-abstract-condition-preserving-v8`](click-outcome-abstract-condition-preserving-v8.json) | `the-caption-prompt.quality-rating-contract/v13` | `6be7e5816c764cd5651f6f9a89f3632da228fef659d3f34a98d7e54cd2ec7c8a` | F01〜F08（履歴） |
| [`click-outcome-abstract-condition-preserving-v9`](click-outcome-abstract-condition-preserving-v9.json) | `the-caption-prompt.quality-rating-contract/v13` | `acefd9f032146d6b685203bd38f19263b5189e69f5cd08119d7b62d2d1c42557` | F01〜A01（履歴） |
| [`click-outcome-abstract-condition-preserving-v10`](click-outcome-abstract-condition-preserving-v10.json) | `the-caption-prompt.quality-rating-contract/v13` | `ad5ca3b4ba526fe0fb9c9ec079231d5b7476335b00d540ff8cf67b9e95cd5929` | Click標準14項目（現行） |

Click contractは`the-caption`側と同じschemaを利用するrevisionを含むが、case rule、working-directory contract、forbidden rater input、diagnostic observationはClick instanceへbindした別artifactである。schema一致をcontract identityの共有と読み替えない。

scoreと評価状態はcontract READMEではなく[`results/`](../results/README.md)の一次resultを正とする。
