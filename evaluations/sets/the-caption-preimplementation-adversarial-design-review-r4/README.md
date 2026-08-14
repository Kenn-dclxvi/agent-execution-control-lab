# 実装前の情報封鎖敵対的設計レビュー r4

一般設計第7版の`DESIGN_ADMISSION`境界を、source外のrequired scope別exact carrierとともに評価するdevelopment Evaluation set。

## identity

- general design: `design_revision_7:semantic-sha256:e84906bf8e1c48446e305fbebbc3004e61da3865ff719ba90b1f6ddafe212f56`
- Target評価設計: `preimplementation-adversarial-design-review-targeted-evaluation-design-r13`
- case suite revision: `adversarial-design-review-r4`

## r2からの差分

fixtureの意味、oracleおよび期待terminalはr2から変更しない。各trial TaskSpecへ`review-scope-carrier-contract/v2`を追加し、source読取前にroot packet observationとreviewer direct observationをrequired review scope別に固定する。

| case | expected terminal | reviewer direct carrier |
| --- | --- | --- |
| `TC-ADR01` | `completion_ready` | なし |
| `TC-ADR02` | `completion_ready` | なし |
| `TC-ADR03` | `blocked` | inventory、contracts |
| `TC-ADR04` | `blocked` | inventory、contracts |
| `TC-ADR05` | `blocked` | inventory、contracts |
| `TC-ADR06` | `blocked` | inventory、contracts |
| `TC-ADR07` | `completion_ready` | paired scope |
| `TC-ADR08` | `unavailable` | なし |
| `TC-ADR09` | `unavailable` | paired scope |

missing paired evidenceは追加しない。対応表にないsource内manifest targetは配送不能とする。

## 進行境界

Candidate223の新規45件だけを発行し、品質、必要review完遂、root delivery、reviewer deliveryおよびresult effectを独立判定する。通過しても採用、releaseまたはprojectionを意味しない。
