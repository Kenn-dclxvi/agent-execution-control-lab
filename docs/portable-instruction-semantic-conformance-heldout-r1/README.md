# Portable instruction semantic conformance held-out r1

> [!IMPORTANT]
> **状態**: `pre_registration_contract_fixed / held_out_cases_14_fixed / model_visible_private_split_fixed / formal_target_not_created / execution_not_started`
>
> このdirectoryは正式なtarget instanceではない。portable kernel草案の設計後に固定した、登録前のheld-out Case契約である。`input-cases.json`だけを将来のmodel-visible入力候補とし、`oracle.json`、`rating-contract.json`およびschemaをmodelへ渡さない。

## 固定内容

- `input-cases.json`: 14件のheld-out Case。期待応答、score、禁止集合を含まない。
- `oracle.json`: Case別のexact応答、重大違反selector、mechanism predicate。
- `response.schema.json`: 複数の制御効果を同じ応答で表す共通応答schema。
- `rating-contract.json`: exact一致を4とし、欠落、誤状態、重大なpermission / dependency違反を分ける採点契約。
- `freeze.json`: input、private oracle、schema、ratingおよび汎用graderのSHA-256を固定するreceipt。

Q01〜Q08の文字列置換ではなく、operation数、decoy位置、依存関係およびpaired stateを変えた。frontierは2件、4件、真正dependency混在およびcommit capability欠落を分け、validationはsuccess-only、first failure、middle failure、nonterminalを別Caseにした。

## 使用境界

1. この固定後は、held-out結果を見て`prompts/compositions/c147-portable-kernel-draft-r1/`を修正しない。
2. 修正が必要なら現草案をfailed lineageとして保持し、新しいdraft identityと新しいheld-out revisionを作る。
3. 正式target登録時は、各Caseをtarget固有の`cases/<case_id>/<revision>/input.json`と`oracle.json`へ移すのではなく、新revisionとして複製し、target descriptor、rating contract、setおよびbaseline qualificationを別gateで固定する。
4. このdirectoryの存在は、evaluation readiness、評価済み、採用、releaseまたはsurface間の一般化を意味しない。

汎用graderは[`scripts/portable_semantic_conformance.py`](../../scripts/portable_semantic_conformance.py)を使う。Case固有の分岐をcodeへ持たず、oracleのexact集合、重大違反selectorおよびpartial-set ruleだけを解釈する。
