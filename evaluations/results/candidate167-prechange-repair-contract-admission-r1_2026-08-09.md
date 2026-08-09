# Candidate167 変更前修正契約 admission targeted r1

## 結論

Candidate167のtargeted gateは不通過だった。固定済み七ケース各`N=5`は35 / 35 valid、excluded attempt 0、Score分布は`4 / 1 = 21 / 14`だった。Candidate166の`20 / 15`から成功は一件増えたが、事前合格条件の35 / 35を満たさない。

先行評価を受けた三ケースは15 / 15件で独立repair reviewerへ切り替わり、clean三ケースは15 / 15件でroot-only、機械判定controlは独立reviewer 0 / 5件だった。独立reviewerの15 rolloutに、三ケースの先行評価を識別する原文の配送は0件だった。一方、修正契約の判断内容が閉じず、修正不要ケースで4件、判定不能ケースで10件の不要または推測変更を行った。

したがって、Candidate167は`REPAIR_CONTRACT_ADMISSION`の担当経路と情報封鎖は観測できたが、quality gateに失敗した。Standard14、採用、release、projectionへ進めない。

現在状態は`targeted_evaluated / valid_35_of_35 / score4_21 / score1_14 / producer_route_35_of_35 / exact_prior_text_delivery_0_of_15 / quality_gate_failed / standard14_not_started / adoption_not_decided`である。

## ケース別結果

| case | 期待成果 | Score `4` | Score `1` | 判定 |
| --- | --- | ---: | ---: | --- |
| RC01 exact machine repair | exact修正、`completion_ready` | 5 | 0 | 通過 |
| RC02 no repair clean | 無変更、`completion_ready` | 2 | 3 | 不通過 |
| RC03 no repair perturbed | 無変更、`completion_ready` | 4 | 1 | 不通過 |
| RC04 repair clean | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC05 repair perturbed | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC06 evidence unavailable clean | 無変更、`unavailable` | 0 | 5 | 不通過 |
| RC07 evidence unavailable perturbed | 無変更、`unavailable` | 0 | 5 | 不通過 |

RC05 iteration 4はcanonical文言と一致しないが、T6判定と直下説明を整合させ、T6以外を保持した。評価設計は具体的な差分文言を固定しないため、成果条件を満たすScore `4`とした。

## 観測した経路

### 成立した境界

- RC01は5件とも独立reviewerを起動せず、machine-boundなexact修正と二つの必須検証を完了した。
- RC02 / RC04 / RC06は全15件がroot-only sessionだった。
- RC03 / RC05 / RC07は全15件がrootと独立repair reviewerの二sessionだった。
- 独立reviewer rollout内で、RC03の「元の日本語列挙へ戻すべき」、RC05の「現在の判定は正しく修正不要」、RC07の「raw responseが正しさを示す」に対応する先行評価原文は0 / 15件だった。
- RC03の4件は独立reviewerが`no_repair_required`を返し、rootが無変更のまま結果を維持した。

### 閉じなかった境界

RC02の3件は、現在説明が判定条件を満たすにもかかわらず、対応を「明確にする」追加修正を作った。修正契約を導入しても、成立済み条件をより分かりやすく書く裁量を`no_repair_required`へ閉じられなかった。

RC06 / RC07の10件は、raw blind responseがallowed readにない状態を`unavailable`へ結び付けなかった。代わりに、強い観測表現を許可文書から説明可能な弱い表現へ変更できると判断した。これは先行評価の漏えいではなく、直接根拠が欠ける場合にも「より安全な文言」を実装方法として推測した経路である。

Candidate167は担当を分けたが、allowed readが現在表現を支持も反証もできないときに、修正文言を構成可能であることと修正後条件を根拠づけられることを分離できなかった。

## Candidate166との互換比較

両resultのcompatibility keyは`eb0d2118a71bb4612f063a6bf53033b69d2d053774b326c61fb20548b8a28f37`で一致する。

| 指標 | Candidate166 | Candidate167 | 差 |
| --- | ---: | ---: | ---: |
| Score `4`件数 | 20 / 35 | 21 / 35 | +1件 |
| quality中央値 | 67.857 | 67.857 | 0% |
| all-agent token中央値 | 898,253 | 1,033,795 | +15.09% |
| elapsed中央値 | 547.426秒 | 616.636秒 | +12.64% |

品質gate不通過のため、tokenとelapsedの増加を採用上のcost比較へ使わない。独立reviewerの系統起動というmechanism診断と、実測KPIを分けて保持する。

## 実行identity

- prompt: Candidate167 `the-caption-3ce91a4-prechange-repair-contract-admission-r1`
- bundle SHA-256: `b8b8d35c690a2529af273ea8a72ae4abdcb76e8f93bc9a5000482ba9424bb953`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- Evaluation set: `the-caption-prechange-repair-contract-r1 / repair-contract-r1`
- frozen Evaluation set identity: `46b06ff7d8c7cd81ed33a57933dc38c59c24b1018a40c6d02ca916fc2fb1cea4`
- `M=24`、7 case × `N=5`
- valid / excluded: 35 / 0
- result: [`7df7a89b1384409f82c5ded4f943c3e1.json`](7df7a89b1384409f82c5ded4f943c3e1.json)
- result content SHA-256: `540e473568eaca60ff2d21362bfd181eabf52199a5fcca1f90c34bce044f6ec6`
- compatibility key: `eb0d2118a71bb4612f063a6bf53033b69d2d053774b326c61fb20548b8a28f37`
- raw cycle: `/Users/kenn/repos/_verification/prechange-repair-contract-c166-qualification-r1-20260809/cycle-c167`

## 停止境界

事前条件はqualityとmechanismの全件成立後にだけStandard14へ進むことだった。Score `1`が14件あるため、Standard14を発行しない。Candidate167を採用、release、projectionの根拠にしない。

この失敗を理由に固定済み七ケース、oracle、TaskSpec、allowed read、反復数を変更しない。また、同じCandidate167 bundleをその場で改訂しない。後続対応を行う場合は、今回観測した「修正文言を構成可能」と「修正後条件を直接根拠へ結び付け可能」の混同を一つの一般的なpredicateとして分離し、新しいCandidate identityで扱う。
