# Quality rating contracts

quality ratingの必要条件をrevision別に固定する。結果確認後の変更は新revisionとし、既存resultのscoreをin-placeで読み替えない。

[`owner-producer-quality-v1`](owner-producer-quality-v1.json)は、TaskSpecがcriterion ownerを固定したrunで、ownerに対応するproducer execution identityのresultをquality raterが確認できることをscore `4`の必要条件にする。独立ownerのproducerはactive executorと別execution identityでなければならない。

[`owner-producer-quality-v2`](owner-producer-quality-v2.json)はv1のowner-producer条件を維持し、required validation commandの成功証跡をroot sessionだけでなく、そのrunのall-agent usageにbindされたrecursive descendant sessionまで含める。対象sessionは同一workspaceの全sessionではなく、正確なroot threadから到達できるthread graphだけとする。descendantのfinal responseだけではcommand成功証跡にならない。

[`owner-producer-quality-v3`](owner-producer-quality-v3.json)はv2のevidence scopeを維持し、valid runにcommandまたはowner evidence不足がある場合も0〜3の全体scoreを必ず返す。score `4`の必要条件はv2から変更しない。nullまたはunrateableでLayer 4全体を止めず、不足証跡と成果全体を区別して短い理由へ記録する。

[`owner-producer-quality-v4`](owner-producer-quality-v4.json)はv3の採点条件を維持し、all-agent command evidenceをv2へ更新する。command evidence v2はrootのCodex command eventsに加え、all-agent usageへbindされたdescendant rollout内のstructured command arrayと、`write_stdin`でterminalになったcommand continuationを収集する。既存v3 resultは変更しない。

[`owner-producer-quality-v5`](owner-producer-quality-v5.json)はv4の採点条件を維持し、all-agent command evidenceをv3へ更新する。command evidence v3は、command nameと成功結果を一意に対応付けられるcustom `exec` wrapperの`<name>: exit=0`集約行を収集する。sourceに`${r.name}`または`${r.label}`と`${r.exit_code}`がなく、固定command表へnameをbindできないtextは証跡にしない。既存v4 resultは変更しない。

[`owner-producer-quality-v6`](owner-producer-quality-v6.json)はv5の採点条件とcommand / producer evidence revisionを維持し、F05 clarificationのresponse evidenceだけをsemantic marker groupへ更新する。`daily`、`strict`に加え、live CSV fallback policyは英字`fallback`または日本語`フォールバック`のどちらでも同じ概念証拠として扱う。Unicode NFKCとcasefold後に各概念groupの少なくとも1表現を要求する。既存v5 resultは変更せず、v6 resultと互換比較へ混ぜない。

[`owner-producer-quality-v7`](owner-producer-quality-v7.json)はv6の採点条件とresponse / producer evidenceを維持し、all-agent command evidenceをv4へ更新する。command evidence v4は、custom `exec` wrapperが出力する`### <name>`直後の`exit_code=0`を、source側の`${r.name}`と`${r.exit_code}`および固定name-command表へ一意にbindできる場合だけ成功証跡へ含める。process開始失敗、`exit_code`欠落、固定nameへbindできないtextは成功証跡にしない。既存v6 resultは変更しない。

[`owner-producer-quality-v8`](owner-producer-quality-v8.json)は採点anchorとresponse / producer evidenceを維持し、all-agent command evidenceをv5へ更新する。v5はattempted、successful、failed、protocol violationを別配列へ保存する。required command callがない場合とmachine-boundな非zero exitはtask outcomeとして採点する。callはあるがzero / nonzero exitのどちらもbindできない場合は`command_evidence_incomplete`のexternal failureとして除外し、同じslotを再試行する。format違反とadapter-owned cleanup試行は診断へ保存するがquality KPIへ入れない。既存v7 resultは変更しない。

[`outcome-quality-owner-diagnostic-v9`](outcome-quality-owner-diagnostic-v9.json)はv8のresponse evidence、command evidence、0〜4 anchorを維持し、成果・boundary・required validationを`quality_score`の対象にする。owner-producer evidenceは同じcollectorで必ず保存するが、独立worker経路の成立可否をdiagnostic observationへ分離し、quality scoreを変更しない。既存v8 resultは変更せず、新profile revisionとして実行する。

[`outcome-boundary-owner-diagnostic-v10`](outcome-boundary-owner-diagnostic-v10.json)は、実行役へ提示したTaskSpecと適用されるリポジトリ規則から導ける成果条件、禁止境界、必須試験だけを採点する。実行役へ提示していない特定の質問項目、特定の試験コマンド、非公開の正解情報を点数4の必要条件にしない。A01では未固定値の推測と確認前の編集・試験を禁止する。A02ではリポジトリから一意に決まる対象を質問せず実行する。第9版の結果は変更せず、第2版評価項目を使う新しい採点条件として分離する。

[`outcome-semantic-location-owner-diagnostic-v11`](outcome-semantic-location-owner-diagnostic-v11.json)は第10版の条件を維持し、F10 Monthlyだけ数値lineをqualityの必須条件から外す。TaskSpecは引き続き`path:line`を依頼する。採点ではmajor、`src/app/entrypoints/monthly_main.py`、`format_test=args.force`の誤binding、`-t`と`-F`の両方への影響、zero driftを必須とする。数値lineは`exact`、`mismatch`、`absent`としてdiagnosticへ保存するが、scoreを変更しない。既存v10 resultとprofileは変更しない。

[`outcome-semantic-evidence-normalized-owner-diagnostic-v12`](outcome-semantic-evidence-normalized-owner-diagnostic-v12.json)は第11版の条件を維持し、保存済みC69/C70で再現した三つの採点偽陰性を修正する。A01は疑問符がなくても「変更後の既定値を明示してください」を確認要求として扱う。A02は`exit_code=0`にbindされたcommand tokenのsingle quote / double quote直列化をbare token列と同じ成功commandとして照合する。F10 Monthlyは`format_test=args.force`という字面だけでなく、`--force`がformat-test分岐へ誤接続し`--format-test`値が渡らない同じ意味の説明を認める。未実行・失敗command、誤binding関係を示さないCLI言及、数値line診断の扱いは変更しない。既存v10 / v11 resultは変更しない。

[`outcome-abstract-condition-preserving-owner-diagnostic-v13`](outcome-abstract-condition-preserving-owner-diagnostic-v13.json)は第12版の条件を維持し、提示した抽象成果条件を特定コマンドへ具体化して必須化することを禁止する。実行役へ提示した成果条件が抽象的なときは、成立を判定できる任意の証拠で満たされたとみなし、コマンド名がmodel-visibleに明示された場合だけそのコマンドを必須試験として扱う。A02では「最終diffからrouting成立を確認する」という提示条件を、diff内容確認・変更path限定確認・name-only確認などの任意の証拠で満たされたとみなし、`git diff --check`はmodel-visibleに明示された場合だけ必須試験とする。owner-producer evidenceは第9版以降と同じく診断専用で、成果品質の点数を変更しない。既存v12以前のresultは変更せず、再採点しない。

[`outcome-terminal-state-evidence-owner-diagnostic-v14`](outcome-terminal-state-evidence-owner-diagnostic-v14.json)は第13版の条件を維持し、A01だけを応答文面の分類からversioned terminal-state evidenceへ切り替える。`required_value_state=unresolved`、terminal responseあり、final changed path 0件、試験・変更operation未開始を合わせて`outcome_state=awaiting_required_value`とする。疑問符、質問語、文末表現、応答本文はこの状態の導出とquality scoreに使用しない。本文は表示証拠として保持する。既存v13以前のresultは変更せず、v14で再採点したものとして扱わない。

今後新規に作る[`標準14項目`](../sets/the-caption-standard14-r1/README.md) profileはv14を使用する。v10 / v11 / v12 / v13 profileは既存resultの再現用として保持する。2026-07-26に[`Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71の標準14項目各N=5`](../results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録した。v14は新しいcompatibility conditionであり、v13以前のresultと同一comparisonへ混ぜない。

`scripts/owner_producer_evidence.py`はmodel-visible TaskSpecと実行済みsession metadataからblind evidence viewを作る。このscriptはscoreを決めず、evidenceの利用可否だけを検査する。成果全体の0〜4採点は引き続きquality raterが行う。

現行`evaluation_loop.py rate`はowner付きTaskSpecの採点時にowner-producer evidence viewを必須とする。rating v2 / v3は`all-agent-command-evidence/v1`、rating v4は`v2`、rating v5 / v6は`v3`、rating v7は`v4`、rating v8 / v9 / v10 / v11 / v12 / v13 / v14は`v5`を要求する。v14はA01に`terminal-state-evidence/v1`も要求する。v8以降のmeasurement-incomplete runはLayer 2で除外されるためLayer 3へ渡さない。v1〜v8は該当runの`score_4_owner_evidence_eligible` fieldがtrueでなければscore `4`の保存を拒否する。v9以降は同fieldを診断へ保持し、成果品質の点数4を拒否する条件には使わない。既存resultとprofileは履歴として保持し、新revisionへ読み替えない。
