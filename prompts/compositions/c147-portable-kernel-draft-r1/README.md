# C147 portable kernel draft composition

このdirectoryは、C147の81 primitiveをruntime固有語なしで再構成した管理用草案を置く。生成物は自己完結した一枚の`AGENTS.md`になるが、まだCandidate、prompt identity、full bundleまたは評価入力ではない。

## variant

| manifest | actor capability | 構成結果 |
| --- | --- | --- |
| `root-only.composition.json` | 一つのactorだけを利用可能とし、独立execution要求は`unavailable`へ閉じる | 10,418 bytes / SHA-256 `0e625b4c527e8b520c676cee15424ba222576ebc0e29d6f37eeea1ec08166a36` |
| `full-agent.composition.json` | request contractが明示した場合だけ独立actorを開始し、result provenanceとcoordinator非代行を適用する | 10,781 bytes / SHA-256 `3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3` |
| `full-agent-codex-validation-carrier-draft-r2.composition.json` | full-agentのvalidation意味を共通二componentへ分け、観測済み7能力を持つCodex carrierを組み合わせる | 12,922 bytes / SHA-256 `999d409cd90b83408739d0140ddb5dc4e052f5af40bc603834553df5a6a0ad0b` |
| `full-agent-codex-validation-carrier-candidate-r1.composition.json` | r2の同一component集合とbytesをP002 prompt identityへbindするCandidate用manifest | 12,922 bytes / SHA-256 `999d409cd90b83408739d0140ddb5dc4e052f5af40bc603834553df5a6a0ad0b` |
| `full-agent-codex-validation-plan-identity-carrier-draft-r3.composition.json` | r2の共通validation意味を保持し、固定済みplan identityとterminal projection contractだけをcarrier inputにする管理用draft | 12,864 bytes / SHA-256 `caf7da152e1b7e2686a65dcc8b3ce4f5b40671ca75b9f8adde7d7b4432cce901` |
| `full-agent-codex-validation-plan-identity-carrier-candidate-r1.composition.json` | r3の同一component集合とbytesをP003 prompt identityへbindするCandidate用manifest | 12,864 bytes / SHA-256 `caf7da152e1b7e2686a65dcc8b3ce4f5b40671ca75b9f8adde7d7b4432cce901` |
| `full-agent-codex-validation-prebound-carrier-draft-r4.composition.json` | terminal投影要求をplanへ移し、Codex carrier contractをblock適用時に成立済みとする管理用draft | 12,781 bytes / SHA-256 `82792275a9e120e1e9e794244ca72ef804c1b7f8c9ac39a4ae0c56493aad468a` |
| `full-agent-codex-validation-prebound-carrier-candidate-r1.composition.json` | r4の同一component集合とbytesをP004 prompt identityへbindするCandidate用manifest | 12,781 bytes / SHA-256 `82792275a9e120e1e9e794244ca72ef804c1b7f8c9ac39a4ae0c56493aad468a` |
| `full-agent-codex-validation-terminal-projection-draft-r5.composition.json` | raw nested resultをcarrier-localへ閉じ、terminal projection objectだけをouter output producerにする管理用draft | 12,830 bytes / SHA-256 `2cb70ccd11fcfe605accf9b212050ed08b6db0eb0a522d502d35c33d58301681` |
| `full-agent-codex-validation-terminal-projection-candidate-r1.composition.json` | r5の同一component集合とbytesをP005 prompt identityへbindするCandidate用manifest | 12,830 bytes / SHA-256 `2cb70ccd11fcfe605accf9b212050ed08b6db0eb0a522d502d35c33d58301681` |
| `full-agent-codex-frontier-carrier-draft-r6.composition.json` | P005の全componentを保持し、構成済みfrontierの途中result ingressだけを閉じるCodex platform blockを追加する管理用draft | 14,593 bytes / SHA-256 `669a66d8350e250260922eb25706a11f0e75b5aeb1064ca323a62a9be26c5c91` |
| `full-agent-codex-frontier-carrier-candidate-r1.composition.json` | r6の同一component集合とbytesをP006 prompt identityへbindするCandidate用manifest | 14,593 bytes / SHA-256 `669a66d8350e250260922eb25706a11f0e75b5aeb1064ca323a62a9be26c5c91` |

root-onlyとfull-agentの二つのactor variantは`actor-core`と`actor-input`を共有し、`single-actor`または`multi-actor`のどちらか一方だけを選ぶ。各variantの`provides / requires`は閉じており、81 primitiveの逆引きは`primitive-coverage.json`に固定する。

r2は新しいactor variantではなく、既存full-agentのvalidation部分だけを`validation-plan-semantics-r2 / validation-result-closure-r2 / validation-carrier-codex-r2`へ分離した管理用draftである。既存validation primitive 15件の対応は`validation-carrier-r2-coverage.json`に固定し、残る66件のcomponent bytesはr1と共有する。

r2の静的反例監査では、空plan開始、部分capabilityでの開始、観測不能evidenceでの開始という初回blocking edge 3件をcarrier admissionで修正した。修正後9 Caseの残存blocking counterexampleは0件だが、これは効率改善または評価通過ではない。

r3はP002のcost退行を受け、r2のplan fieldをcarrier admission用に再bindできるdependencyだけを閉じた管理用draftである。11 classの静的反例0件と15 / 15 primitive coverageを確認し、同一bytesをP003 Candidateへbindした。これは評価結果または効率改善ではない。

r4はP003 N=1のtrace診断を受け、taskごとのcapability・projection admission再判定とpre-invocation `unavailable`生成routeを閉じた管理用draftである。13 classの静的反例0件と15 / 15 primitive coverageを確認し、同一bytesをP004 Candidateへbindした。これは評価結果または効率改善ではない。

r5はP004 H06のtrace診断を受け、raw nested resultと外部へ渡せるterminal projectionのproducer permissionを分離した管理用draftである。14 classの静的反例0件と15 / 15 primitive coverageを確認し、同一bytesをP005 Candidateへbindした。後続N=5は30件でScore 4と機序成立を確認し、P003比でtokensとelapsedを減らしたが、P001比elapsed増によりcost gate不通過となった。

r6はP005 Standard14 N=5のC147移植損失監査を受け、P005の13 componentをbyte保持したまま`frontier-carrier-codex-r1`だけを追加した管理用draftである。14 classの静的反例0件と8 / 8 carrier primitive coverageを確認し、同一bytesをP006 Candidateへbindした。評価は未実施である。

full-agentの機能block別bytes、primitive、tuning Caseおよび削除不可境界は[`functional-block-cost-ledger.json`](functional-block-cost-ledger.json)へ固定する。byte比率は効率KPIや削除優先度ではない。

静的なbytes差は効率改善の証拠ではない。品質維持後のall-agent `total_tokens`と`elapsed_seconds`を互換条件で測定するまでcost改善を主張しない。

Q01〜Q08の静的反例監査で初回草案の4境界を修正した。修正後の初回静的反例は0件だが、Q01〜Q08は本文作成に使ったtuning Caseなので評価通過とは扱わない。

## lifecycle境界

五つのdraft manifestはcomposition schema `v3`であり、次を固定する。

- `model_visible=false`
- `evaluation_eligible=false`
- `bundle_binding_eligible=false`
- `output_prompt_identity=null`

`render`と既知bytesへの`check`は許可するが、`verify-bundle`は必ず拒否する。Candidate作成前gateを通過して新しいfull bundleとprompt identityを作るまでは、評価profileまたは対象platformへ渡さない。

full-agentはCandidate作成前gate通過後もdraft manifestを変更せず、同じcomponent集合とoutput bytesを新prompt identityへbindする[`full-agent.candidate.composition.json`](full-agent.candidate.composition.json)を別identityとして追加した。target固有bundleはこのCandidate用manifestでだけ`verify-bundle`を通し、root-only draftへ昇格を一般化しない。

Codex validation carrier r2も同じ境界を適用し、管理用draftを変更せず[`full-agent-codex-validation-carrier-candidate-r1.composition.json`](full-agent-codex-validation-carrier-candidate-r1.composition.json)をP002専用identityとして追加した。この昇格はr2の固定済みcomponent集合とoutput bytesに限り、別platformまたはCompact系列へ一般化しない。

validation plan identity carrier r3も同じ境界を適用し、管理用draftを変更せず[`full-agent-codex-validation-plan-identity-carrier-candidate-r1.composition.json`](full-agent-codex-validation-plan-identity-carrier-candidate-r1.composition.json)をP003専用identityとして追加した。P001だけを直接親とし、P002は非継承の失敗反例として扱う。

validation prebound carrier r4も同じ境界を適用し、管理用draftを変更せず[`full-agent-codex-validation-prebound-carrier-candidate-r1.composition.json`](full-agent-codex-validation-prebound-carrier-candidate-r1.composition.json)をP004専用identityとして追加した。P001だけを直接親とし、P002とP003は非継承の反例として扱う。

validation terminal projection r5も同じ境界を適用し、管理用draftを変更せず[`full-agent-codex-validation-terminal-projection-candidate-r1.composition.json`](full-agent-codex-validation-terminal-projection-candidate-r1.composition.json)をP005専用identityとして追加した。P001だけを直接親とし、P002、P003およびP004は非継承の反例として扱う。

Codex frontier carrier r6も同じ境界を適用し、管理用draftを変更せず[`full-agent-codex-frontier-carrier-candidate-r1.composition.json`](full-agent-codex-frontier-carrier-candidate-r1.composition.json)をP006専用identityとして追加した。P005だけを直接親とし、C147、Candidate193、Candidate205およびCandidate253からCandidate258まではsourceまたは非継承の反例として扱う。

## render

```bash
.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/root-only.composition.json \
  --output /tmp/c147-portable-root-only-AGENTS.md

.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent.composition.json \
  --output /tmp/c147-portable-full-agent-AGENTS.md

.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-carrier-draft-r2.composition.json \
  --output /tmp/c147-portable-full-agent-codex-validation-carrier-r2-AGENTS.md

.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-plan-identity-carrier-draft-r3.composition.json \
  --output /tmp/c147-portable-full-agent-codex-validation-plan-identity-carrier-r3-AGENTS.md

.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent-codex-validation-prebound-carrier-draft-r4.composition.json \
  --output /tmp/c147-portable-full-agent-codex-validation-prebound-carrier-r4-AGENTS.md
```

Agentへcomponent fileを読ませる運用は行わない。将来platformへ配送する場合も、gate通過後のfull bundleから構成済みの一枚だけを配置する。
