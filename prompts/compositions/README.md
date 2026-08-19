# Prompt composition sources

このdirectoryは、エージェントへ直接読ませるprompt bundleではなく、自己完結した一枚のinstruction fileを事前生成するための管理用sourceを置く。

- `components/`は管理用の逐語sourceであり、評価workspaceや対象platformへ配置しない。
- `composition.json`は`artifact_role=composition_source`、`model_visible=false`、`evaluation_eligible=false`を固定する。componentの順序、機能分類、各content SHA-256、生成後のtarget、出力prompt identity、最終content SHA-256およびcomposition全体SHA-256も保持する。`v2`は各componentの`provides / requires`も固定し、未解決の依存と複数providerを構成時に拒否する。
- bundle用の`manifest.json`とはschema、ファイル名、identityおよび探索対象を分離する。`composition_identity`または`composition_sha256`を`prompt_set_identity`や互換条件へ使用しない。
- エージェントへ渡す成果物は、`scripts/compose_prompt.py`が生成する一枚の`AGENTS.md`だけとする。
- 生成後の`AGENTS.md`からcomponent、manifestまたは別prompt fileをreadさせない。
- prompt bundleのidentityは管理用sourceではなく、生成された最終ファイルのbytesを含むbundle manifestで固定する。
- 評価へ接続する前に`verify-bundle`で、構成結果のtarget、content SHA-256、出力prompt identityが検証済みfull bundleと一致することを確認する。
- 同じbytesを再構成した場合は既存prompt identityを維持する。bytesが変わる構成は、新しいCandidateの作成前gateを通過した後に、新しいfull bundleとprompt identityへ固定する。
- 既存baseline、candidate、releaseのfull bundleは変更せず、composition sourceを履歴bundleの代替正本として扱わない。

`the-caption-c147-full-agent-r1`は、Candidate147のroot `AGENTS.md`を逐語の条項componentへ分離した最初のcompositionである。全componentをmanifest順に構成した出力は、保存済みCandidate147の`AGENTS.md.txt`とbyte一致する。

`provides / requires`は管理上の参照閉包であり、Agentに表示する処理順序ではない。現行C147の`PRODUCER`は、単一actorにも必要な一意bindingとworker選択を同一条項に持つ。そのため、依存参照を追加しただけでworker機能を安全に取り外せるとは判断しない。現行台帳とroot-only構成の境界は[`C147 component依存閉包台帳`](../../docs/c147-component-dependency-ledger.md)を参照する。

`c147-portable-kernel-draft-r1`はその後続草案である。`actor-core / actor-input`を共通にし、`single-actor / multi-actor`を択一してroot-onlyとfull-agentを別の一枚へ構成する。schema `v3`の`draft / bundle_binding_eligible=false / output_prompt_identity=null`であり、renderはできるがfull bundleにはbindできない。

P001 Standard14 N=5の後続診断により、`validation-execution`は共通semantic closureとplatform固有carrier能力を同じcomponentに持つことが分かった。Codex CLI 0.146.0の独立probeで7能力を確認した後、[`P001 validation carrier platform分離設計`](../../docs/p001-validation-carrier-platform-separation-design.md)に従う管理用r2 draftを追加した。`validation-plan-semantics-r2 / validation-result-closure-r2`と`validation-carrier-codex-r2`を分けるが、最終成果は自己完結した一枚である。既存r1は変更せず、r2もCandidateまたは評価入力へ昇格していない。

P002 VCC6 N=5のcost退行監査後、固定済みplanをcarrier admission用fieldへ再bindできるdependencyだけを閉じる管理用r3 draftを追加した。r2のplan semanticsとresult closureを保持し、Codex blockだけを`validation-plan-identity-carrier-codex-r3`へ置換する。r3自体はschema `v3`の管理用sourceであり、静的gate通過後に同一bytesをP003専用Candidate manifestとfull bundleへ別途bindした。

P003 VCC6 N=1のtrace診断後、taskごとのcarrier capability・projection admission再判定を削除する管理用r4 draftを追加した。terminal投影要求をimmutable planへ移し、Codex blockのcontractをcomposition時に成立済みとする。r4自体はschema `v3`の管理用sourceであり、静的gate通過後に同一bytesをP004専用Candidate manifestとfull bundleへ別途bindした。

P004 VCC6 N=1のH06 trace診断後、raw nested resultをcarrier-localへ閉じ、plan terminal後のterminal projection objectだけをouter output producerにする管理用r5 draftを追加した。r5自体はschema `v3`の管理用sourceであり、静的gate通過後に同一bytesをP005専用Candidate manifestとfull bundleへ別途bindした。

P005 Standard14 N=5のC147移植損失監査後、共通`FRONTIER`の意味を変更せず、全member commit前の個別result ingressだけを閉じるCodex frontier carrierを管理用r6 draftへ追加した。r6自体はschema `v3`の管理用sourceであり、14 classの静的gate通過後に同一bytesをP006専用Candidate manifestとfull bundleへ別途bindした。

確認command：

```bash
.venv/bin/python scripts/compose_prompt.py check \
  --manifest prompts/compositions/the-caption-c147-full-agent-r1/composition.json \
  --against prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt

.venv/bin/python scripts/compose_prompt.py verify-bundle \
  --manifest prompts/compositions/the-caption-c147-full-agent-r1/composition.json \
  --bundle prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1
```
