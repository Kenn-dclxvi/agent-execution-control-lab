# Candidate194 C147直接基盤review制御再構成 実装監査

## 結論

Candidate194 `the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1`は、C147を直接親とするfull bundleとして作成した。変更targetはroot `AGENTS.md`だけであり、設計で固定した24責任が24の独立labelへ対応している。bundleの構造、file identity、source identityは静的検証に通過した。

現在状態は`candidate_created / static_verification_passed / not_evaluated`である。prompt本文の存在と静的対応は、品質、機構、採用、releaseまたはprojectionの成立を意味しない。評価profileと評価runは未作成である。

## identity

| 項目 | 値 |
|---|---|
| Candidate番号 | Candidate194 |
| prompt identity | `the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1` |
| 直接親 | `the-caption-3ce91a4-result-effect-scope-r1` |
| bundle SHA-256 | `226fd8599620ed5e71b9963a39faab51ed3dbb42b0f45078838680fa13818243` |
| root prompt SHA-256 | `6c560013893d4df0751d548c8eb257f9260270bef76537cd8a30a384335088c6` |
| root prompt Git blob SHA-1 | `03fd9996e11455ad404613046c5a9f42f0c524a3` |
| target commit | `3ce91a403f9e0c83f29d56bbe9e7b449b713445d` |
| target tree | `88eecfa29f7016b4d77061d3aabe3e7d176fea9b` |
| storage format | `instruction-suffixed/v1` |
| changed target | `AGENTS.md`のみ |

manifestは`prompts/candidates/the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1/manifest.json`、実行原文は`prompts/candidates/the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1/files/AGENTS.md.txt`を正本とする。

## 直接親と証拠の境界

Candidate194はC147のbit列へ単純追記したものではないが、系譜上の直接親はC147だけである。

- C147からrequired outcome、producer、owner、root非代行、worker context、evidence admission、局所result effect、method、recovery、validation、安全停止の不変条件を責任対応付きで保持した。
- C191はreview、terminal、current resultの成立経路を示す診断証拠として使った。
- C192はconsumerとdependencyを分ける判断軸、および論理gateだけでは発行挙動を拘束できなかった反例として使った。
- C193は発行順序への部分効果、開始identity/read越境、ADR05とADR06のcertificate dependency失敗を示す診断証拠として使った。
- C191、C192、C193のprompt本文、`DISPATCH_ADMISSION`、`DISPATCH_TRANSITION`、`dispatch_candidate`、`dispatch_predecessor`、`dispatch_frontier`は継承していない。

## 設計責任と実装labelの対応

| 番号 | 設計責任 | 実装上の所有範囲 |
|---:|---|---|
| 1 | `OPERATION_SPEC` | required outcome、consumer、dependency、terminal、clarification operation |
| 2 | `PRODUCER_BINDING` | 一operation一producer、変更時の新identity |
| 3 | `PRODUCER_RESULT` | spawn・Sender・criterion・targetのresult真正性 |
| 4 | `OWNER_ROLE` | owner metadataとproducer指定の分離 |
| 5 | `ROOT` | root非producer時の再判定禁止 |
| 6 | `WORKER_CONTEXT` | 共通packetと最小context継承 |
| 7 | `RESULT_DEPENDENCY` | atom単位dependency、局所失効、terminal再開禁止 |
| 8 | `METHOD` | 未固定手段の選択、failureとpermissionの分離 |
| 9 | `RECOVERY` | environment-only repairと同一command再実行 |
| 10 | `EVIDENCE_ADMISSION` | consumer付きrepository evidenceのdefault deny |
| 11 | `DECISION_BOUNDARY` | 限定・無限定停止、共同発行集合、部分発行禁止、wait-only継続 |
| 12 | `IMPLEMENTATION_BINDING` | target、instruction、effect、relation、constraintの変更predicate化 |
| 13 | `REVIEW_REQUIREMENT` | primary reviewとの分離、適用可否、finite direct match |
| 14 | `PRIOR_REVIEW_RESULT_ADMISSION` | 保存result固有の利用permissionとcurrent dependency |
| 15 | `REVIEW_EXECUTION_PERMISSION` | 新規独立reviewのpermission stateだけを所有 |
| 16 | `REVIEW_PACKET` | 起動前packet、情報封鎖、missing targetの配送 |
| 17 | `OBSERVATION_RESULT` | value、missing、unreadable、terminal failureとresult contract |
| 18 | `REVIEW_JUDGEMENT` | counterexample、no-counterexample、unavailableのcertificate |
| 19 | `CURRENT_REVIEW_RESULT_ADMISSION` | current producer resultの機械照合 |
| 20 | `CHANGE_ADMISSION` | review resultとsubject・coupled relationの変更許可 |
| 21 | `VALIDATION_PLAN` | 変更後の実行票とcommand method binding |
| 22 | `VALIDATION_CLOSURE` | 個別command、順序、停止、cell ID、完了closure |
| 23 | `OPERATION_TERMINAL` | operation局所のterminal |
| 24 | `OUTER_TERMINAL` | clarification、completion、blocked、unavailableの外側集約 |

一つの状態遷移を複数labelが発行しないよう、次の所有境界を固定した。

- 変更前の実tool発行は`DECISION_BOUNDARY`だけが所有する。
- repository evidenceの資格は`EVIDENCE_ADMISSION`だけが所有する。
- 新規review permissionは`REVIEW_EXECUTION_PERMISSION`がstateだけを返し、review起動は`DECISION_BOUNDARY`が行う。
- missingの観測分類は`OBSERVATION_RESULT`、terminalへの意味づけは`REVIEW_JUDGEMENT`が行う。
- 変更後validationは`VALIDATION_PLAN`と`VALIDATION_CLOSURE`だけが発行する。
- 個別operationと依頼全体のterminalは別labelが所有する。

## C147不変条件の保持

C147の13条項に含まれた不変条件を無条件には削除していない。

- `SPEC`は`OPERATION_SPEC`、`IMPLEMENTATION_BINDING`、clarification operationへ分けた。
- `PRODUCER`、`OWNER_ROLE`、`ROOT`、`CONTEXT`は責任を保ったまま独立labelへ置いた。
- `TERMINAL`は`OPERATION_TERMINAL`と`OUTER_TERMINAL`へ分けた。
- `EVIDENCE_GATE`はevidence資格、implementation binding、validation所有へ分けた。
- `INDEPENDENCE`はproducer bindingとresult dependencyへ移した。
- `DECISION_BOUNDARY`は局所result effectを保持し、consumer、停止文言、実発行集合、nonterminal継続を追加した。
- `VALIDATION_PLAN`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`は独立責任として保持した。

## prompt量

| prompt | 行数 | UTF-8 byte数 |
|---|---:|---:|
| C147 root `AGENTS.md` | 15 | 10,772 |
| Candidate194 root `AGENTS.md` | 26 | 20,640 |
| 差 | +11 | +9,868 |

Candidate194は責任分離のためC147より長い。prompt量の増加は評価前の失敗条件ではないが、品質・機構成立後の複雑性および効率評価対象として保持する。短縮、label数またはbyte数だけから改善を主張しない。

## 静的検証

次を確認した。

- exporterのbundle verificationが成功した。
- manifestの`files`、個別SHA、symlink、bundle SHAが一致した。
- C147とCandidate194のmanifest file entryは`AGENTS.md`以外で完全一致した。
- root promptの責任labelは24件で、設計上の24責任と同名・同順だった。
- Candidate194 focused testは`1 passed`だった。
- 全test discoveryは`1189 passed, 1837 subtests passed`だった。
- `git diff --check`で書式違反がなかった。
- Candidate以外のprompt bundle、評価profile、case、set、rating contract、resultを変更していない。

## 評価境界

Candidate194は`not_evaluated`である。次に評価設計へ進む場合も、作成前設計で固定した二段階gateを維持する。

1. ADR9全9ケース各N=5で、45件すべてScore 4かつ全機構predicateを要求する。
2. 第1段階通過後だけ、Standard14のA01、A02、F02、F04、F06、F10 entrypoint inventory、F10 monthlyを各N=5で実行する。
3. 第2段階通過後だけ、Standard14全14ケース各N=5を別profile・別preflightで判断する。

評価profileを作る前に、case revision、model-visible input hash、rating contract、Layer 1、atomic run identity、traceから機構predicateを算出する方法を固定する。一件でも品質または機構が不合格なら後続stageを発行せず、同じCandidate identityを修理しない。

この監査は評価profileの作成、slot発行、採用、releaseまたはprojectionを許可するreceiptではない。
