# C147 portable kernel Q01〜Q08静的反例監査

> [!IMPORTANT]
> **状態**: `tuning_cases_8_audited / initial_blocking_edges_4 / repaired_in_draft / remaining_blocking_counterexample_0 / candidate_not_created / evaluation_not_started`
>
> 本書はroot-onlyとfull-agentの管理用草案をQ01〜Q08の正常経路と禁止経路へ静的に当てた設計監査である。実行evidence、Candidate、評価result、採用、releaseまたはprojectionではない。

## 結論

初回草案には、問題operationの禁止はあるが正常resultへ正に進まない境界が4件あった。

1. Q02で必要observationは許可されるが、開始しない経路。
2. Q04のroot-onlyで、一致actor resultをadmitする共通境界がなく、正しいresultまで`unavailable`へ過剰遮断する経路。
3. Q05でfrontier全件を開始できないとき、subset開始またはnonterminal停止が残る経路。
4. Q08でrecovery allowanceまたはcapabilityがないとき、recoveryは開始しないが`unavailable`へterminal化しない経路。

これらを、成功runのtool順または判断順を追加せず、資格成立時の正の開始、result admission、不可分frontierとcapability欠落時のterminalとして修正した。修正後のQ01〜Q08静的反例は0件である。

## 監査方法

各Caseについて次を別々に確認した。

- required stateへ進む正のstatementがある。
- forbidden operationは、判断順を変えてもprompt準拠で構成できない。
- capability欠落時に、結果の推測、別actorの代行、subset実行または無限nonterminalで補完しない。
- full-agentだけの機能をroot-onlyで成立済みにせず、必要な場合は`unavailable`にする。

この監査はmodelが実際に文を守ることや、トークン・経過時間の改善を証明しない。

## Case別結果

| Case | root-only | full-agent | 正の経路を開くstatement | 閉じる問題経路 | 修正 |
| --- | --- | --- | --- | --- | --- |
| Q01 outcome-method | `supported` | `supported` | `outcome:2-4`, `method-recovery:1-2`, `observation:11-12` | 未固定成果の推測、不要observation、成果確認への戻り | なし |
| Q02 observation | `supported_after_repair` | `supported_after_repair` | `observation:3` | decoy observation、全observation停止、method探索 | 資格成立した一件の開始を追加 |
| Q03 local effect | `supported` | `supported` | `outcome:5`, `observation:6`, `frontier:1-7` | task全体停止、独立operation失効、failed result無視 | なし |
| Q04 provenance | `supported_after_repair` | `supported` | `actor-core:1,5`, `single-actor:4`または`multi-actor:3-5`, `completion:1-3` | 異actor result、同期のみ、coordinator補完 | actor共通のresult admissionと観測不能時`unavailable`を追加 |
| Q05 frontier | `supported_after_repair` | `supported_after_repair` | `frontier:4-7,12` | identityだけ、readの一部だけ、action先行 | frontierを分割できない場合のsubset開始禁止と`unavailable`を追加 |
| Q06 validation | `supported` | `supported` | `actor-core:4-5`, `validation-plan:1,4-5`, `validation-execution:3-9` | v3開始、全件success補完、v2再実行、追加observation | なし |
| Q07 nonterminal | `supported` | `supported` | `validation-plan:6`, `completion:2-3` | 別operation開始、terminal補完、別identity再実行 | なし |
| Q08 recovery | `supported_after_repair` | `supported_after_repair` | `method-recovery:7-9` | allowance推測、別methodで代替、別executionへ置換、nonterminal停止 | allowanceまたはcapability欠落時の`unavailable`を追加 |

## 修正後の不変条件

- Q02の修正は、consumer eligibilityを変更せず、成立済みの一件だけを開始する。
- Q04の修正は、独立actor選択と切り離し、単一actorでも必要なoperation、actor、inputおよびresult kindの対応だけを`actor-core`へ置く。
- Q05の修正はfrontier形成をモデルの分割判断へ戻さず、全件開始能力がなければsubset permissionを閉じる。
- Q08の修正はallowanceの値を追加せず、明示authorityへbind済みかどうかだけを使う。
- Q01、Q03、Q06およびQ07の対応statementは変更しない。

## 草案の境界

修正後も両variantは`draft / bundle_binding_eligible=false / output_prompt_identity=null`である。Q01〜Q08は本文作成に使ったtuning Caseであり、同じCaseの静的無反例を一般化、stability、採用またはreleaseの証拠にしない。

## 後続gate

後続の[`held-out r1`](portable-instruction-semantic-conformance-heldout-r1/)で、Q01〜Q08と異なるliteral、cardinalityおよびdecoy配置を持つ14件、model-visible operation ledger、model-invisible oracle、rating contractおよびhashを固定した。今後は次を守る。

1. held-out inputをportable kernel本文または修正理由へ流入させない。
2. held-out実行前にcontrol-free baselineの測定成立を確認する。
3. formal target identityとCandidate作成前gateを固定するまで、Candidate bundle、profileまたは評価slotを作成しない。

## 参照

- [`Prompt制御の検討原則`](prompt-control-design-principles.md)
- [`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`C147 portable kernel一枚化草案`](c147-portable-kernel-one-sheet-draft.md)
- [`C147 portable kernel draft composition`](../prompts/compositions/c147-portable-kernel-draft-r1/README.md)
