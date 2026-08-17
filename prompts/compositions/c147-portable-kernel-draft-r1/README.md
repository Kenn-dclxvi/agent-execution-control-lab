# C147 portable kernel draft composition

このdirectoryは、C147の81 primitiveをruntime固有語なしで再構成した管理用草案を置く。生成物は自己完結した一枚の`AGENTS.md`になるが、まだCandidate、prompt identity、full bundleまたは評価入力ではない。

## variant

| manifest | actor capability | 構成結果 |
| --- | --- | --- |
| `root-only.composition.json` | 一つのactorだけを利用可能とし、独立execution要求は`unavailable`へ閉じる | 10,418 bytes / SHA-256 `0e625b4c527e8b520c676cee15424ba222576ebc0e29d6f37eeea1ec08166a36` |
| `full-agent.composition.json` | request contractが明示した場合だけ独立actorを開始し、result provenanceとcoordinator非代行を適用する | 10,781 bytes / SHA-256 `3d3733a4ec0bb531a5be8eb53922e92fafe37b479b6190d24a8176ae452805e3` |

両variantは`actor-core`と`actor-input`を共有し、`single-actor`または`multi-actor`のどちらか一方だけを選ぶ。各variantの`provides / requires`は閉じており、81 primitiveの逆引きは`primitive-coverage.json`に固定する。

静的なbytes差は効率改善の証拠ではない。品質維持後のall-agent `total_tokens`と`elapsed_seconds`を互換条件で測定するまでcost改善を主張しない。

Q01〜Q08の静的反例監査で初回草案の4境界を修正した。修正後の初回静的反例は0件だが、Q01〜Q08は本文作成に使ったtuning Caseなので評価通過とは扱わない。

## lifecycle境界

両manifestはcomposition schema `v3`のdraftであり、次を固定する。

- `model_visible=false`
- `evaluation_eligible=false`
- `bundle_binding_eligible=false`
- `output_prompt_identity=null`

`render`と既知bytesへの`check`は許可するが、`verify-bundle`は必ず拒否する。Candidate作成前gateを通過して新しいfull bundleとprompt identityを作るまでは、評価profileまたは対象platformへ渡さない。

full-agentはCandidate作成前gate通過後もdraft manifestを変更せず、同じcomponent集合とoutput bytesを新prompt identityへbindする[`full-agent.candidate.composition.json`](full-agent.candidate.composition.json)を別identityとして追加した。target固有bundleはこのCandidate用manifestでだけ`verify-bundle`を通し、root-only draftへ昇格を一般化しない。

## render

```bash
.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/root-only.composition.json \
  --output /tmp/c147-portable-root-only-AGENTS.md

.venv/bin/python scripts/compose_prompt.py render \
  --manifest prompts/compositions/c147-portable-kernel-draft-r1/full-agent.composition.json \
  --output /tmp/c147-portable-full-agent-AGENTS.md
```

Agentへcomponent fileを読ませる運用は行わない。将来platformへ配送する場合も、gate通過後のfull bundleから構成済みの一枚だけを配置する。
