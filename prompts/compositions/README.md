# Prompt composition sources

このdirectoryは、エージェントへ直接読ませるprompt bundleではなく、自己完結した一枚のinstruction fileを事前生成するための管理用sourceを置く。

- `components/`は管理用の逐語sourceであり、評価workspaceや対象platformへ配置しない。
- `composition.json`は`artifact_role=composition_source`、`model_visible=false`、`evaluation_eligible=false`を固定する。componentの順序、機能分類、各content SHA-256、生成後のtarget、出力prompt identity、最終content SHA-256およびcomposition全体SHA-256も保持する。
- bundle用の`manifest.json`とはschema、ファイル名、identityおよび探索対象を分離する。`composition_identity`または`composition_sha256`を`prompt_set_identity`や互換条件へ使用しない。
- エージェントへ渡す成果物は、`scripts/compose_prompt.py`が生成する一枚の`AGENTS.md`だけとする。
- 生成後の`AGENTS.md`からcomponent、manifestまたは別prompt fileをreadさせない。
- prompt bundleのidentityは管理用sourceではなく、生成された最終ファイルのbytesを含むbundle manifestで固定する。
- 評価へ接続する前に`verify-bundle`で、構成結果のtarget、content SHA-256、出力prompt identityが検証済みfull bundleと一致することを確認する。
- 同じbytesを再構成した場合は既存prompt identityを維持する。bytesが変わる構成は、新しいCandidateの作成前gateを通過した後に、新しいfull bundleとprompt identityへ固定する。
- 既存baseline、candidate、releaseのfull bundleは変更せず、composition sourceを履歴bundleの代替正本として扱わない。

`the-caption-c147-full-agent-r1`は、Candidate147のroot `AGENTS.md`を逐語の条項componentへ分離した最初のcompositionである。全componentをmanifest順に構成した出力は、保存済みCandidate147の`AGENTS.md.txt`とbyte一致する。

確認command：

```bash
.venv/bin/python scripts/compose_prompt.py check \
  --manifest prompts/compositions/the-caption-c147-full-agent-r1/composition.json \
  --against prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/files/AGENTS.md.txt

.venv/bin/python scripts/compose_prompt.py verify-bundle \
  --manifest prompts/compositions/the-caption-c147-full-agent-r1/composition.json \
  --bundle prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1
```
