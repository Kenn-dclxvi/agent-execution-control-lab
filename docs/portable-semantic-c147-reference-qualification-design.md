# Portable semantic C147 reference先行資格確認設計

> [!IMPORTANT]
> **状態**: `reference_first_order_fixed / heldout_r1_immutable / c147_reference_issued_14 / c147_reference_valid_14 / c147_reference_score4_6 / semantic_set_reference_not_qualified / Standard14_remains_end_to_end_authority`

## 結論

portable instructionの完成を判定する前に、新しいsemantic evaluation setが直接の親C147自身を正しく表現できることを確認する。従来の「portable Candidateを先にquality判定し、通過時だけC147 referenceを実行する」順序は廃止する。control-free resultが証明したのは計測成立だけであり、C147同等性を判定するoracleの資格ではない。

既存held-out r1、TaskSpec wrapper、response schema、oracle、rating、runtimeおよび保存済みportable r1 resultは変更しない。同じ14 Case N=1をC147 reference一枚へ発行し、全件validかつScore 4の場合だけ、held-out r1をportable同等性の局所診断へ使用できる。C147が一件でもScore 4を外れた場合は、held-out r1を`reference_not_qualified`として停止し、portable r1の7 / 14をC147機能再現率へ読み替えない。

## Standard14との役割分担

| 評価 | 役割 | authority |
| --- | --- | --- |
| semantic held-out | runtime固有toolを使わず、permission、dependency、result admissionおよびterminalの局所意味を診断する安価な事前資格確認 | C147が同じrevisionを全件通過した場合だけ局所診断として有効 |
| Standard14 | THE-CAPTIONの実repository、実変更、実validationおよび3 KPIをend-to-endで評価する | portable採用判断の正式評価。semantic held-outで置き換えない |

semantic held-outがC147を通過してもportable完成、採用または効率改善を意味しない。portable Candidateが同じsemantic revisionを通過した後、Standard14の互換条件でC147との正式比較へ進む。

## 固定identity

- direct parent prompt: `portable-semantic-c147-full-agent-reference-r1`
- source identity: `the-caption-3ce91a4-result-effect-scope-r1`
- source content SHA-256: `46ed3811aa798fec6356cf53feb7403ff15bf75c71a9c76af6d6893b05fb8fc7`
- bundle SHA-256: `d330421521b231d6029e69e8cd6d4e175fb46b06254e80b3d2f4d8f8f3a55d9f`
- evaluation set: `portable-instruction-semantic-heldout-r1` / `r1`
- rating: `portable-instruction-semantic-exact-v1`
- Profile: `portable-semantic-c147-full-agent-reference-codex-cli0146-sol-medium-heldout-r1-n1-r1`
- dispatch series: `portable-semantic-c147-full-agent-reference-heldout-r1-n1`
- runtime: Codex CLI `0.146.0`
- model / reasoning: `gpt-5.6-sol` / `medium`
- token accounting: all-agent `v2`
- permission: read-only / approval `never`
- N / M: `N=1` / `M=24`

prompt identityと系列identity以外はportable r1 Profileおよびcontrol-free r4の有効計測条件から変更しない。既存resultをreferenceの代用にせず、不足14 slotだけを発行する。

## 発行前gate

1. reference bundleがsource C147の`AGENTS.md`一枚とbyte一致する。
2. Profileのprompt identity以外のCase、TaskSpec、rating、runtime、model、reasoning、permission、schema transport、token accounting、NおよびMがportable r1と一致する。
3. planがPIC-H01からPIC-H14まで各一回だけを許可する。
4. preflightがProfile、target、bundle、runner、adapter、Codex executableおよび14 slotをhash固定する。
5. preflight receiptが`dispatch_allowed=true / issued_slot_count=0`でなければ一件も発行しない。

## 判定

- 14 / 14 valid、schema valid、token／elapsed取得、Score 4の場合だけ`semantic_set_reference_qualified`とする。
- validだがScore 4未満が一件でもあれば`semantic_set_reference_not_qualified`とする。低Scoreを再試行せず、portable品質へ帰属しない。
- schema不適合、一次token欠落、elapsed欠落または採点不能があれば`reference_execution_invalid`として評価セットの資格を判定しない。
- reference不通過時はCase別に、C147にない新機能要求、model-visible contract不足、oracle不整合またはC147本文の実際の境界へ分類する。結果確認後にheld-out r1を変更せず、必要なら別revisionを別作業で設計する。
- reference通過時だけ、保存済みportable r1 resultとの同条件比較を許可する。semantic setは局所診断に限定し、Standard14を省略しない。

## 非目標

- C147のsemantic target上の結果を、保存済みStandard14 N=100結果の置換にすること。
- C147が通るようoracleを事後調整すること。
- portable r1を再実行すること。
- compact化、byte削減、N=5、N=20、採用、releaseまたはruntime projection。

## 参照

- [`C147 reference bundle`](../evaluations/targets/portable-instruction-semantic-conformance/prompts/baselines/portable-semantic-c147-full-agent-reference-r1/)
- [`portable r1正式result`](../evaluations/targets/portable-instruction-semantic-conformance/results/portable-semantic-c147-portable-full-agent-heldout-r1-n1-qualification-r1.json)
- [`portable conformance r1境界監査`](portable-full-agent-conformance-r1-boundary-audit.md)
- [`portable semantic評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`Candidate147 Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)

## 実施結果

C147 referenceは14 / 14 validだったがScore 4は6 / 14であり、14 / 14のreference gateを通過しなかった。詳細は[`C147 reference先行資格確認r1結果`](portable-semantic-c147-reference-qualification-r1-result.md)を正とする。held-out r1をportable同等性評価へ使用せず、Standard14を正式end-to-end authorityとして維持する。
