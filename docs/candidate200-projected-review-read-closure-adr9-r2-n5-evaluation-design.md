# Candidate200 投影済みreview read閉包 ADR9 r2全9ケースN=5評価設計

> **状態**: `evaluated / valid_45 / quality_failed / mechanism_failed / stopped / Standard14_not_started`

## 結論

Candidate200 `the-caption-3ce91a4-projected-review-read-closure-r1`の最初の挙動評価は、ADR9 r2全9ケースを各5回、合計45 atomic runsで行う。case、fixture、model-visible TaskSpec、private oracle、rating contract、model、reasoning、Agent/runtime/CLI、permission、executor条件、command evidence protocolおよび保存Layer 1は変更しない。

品質と機構を別gateで判定する。45件すべてがScore 4で、開始境界、review適用、reviewer起動、packet投影、投影済みsourceのread閉鎖、reviewer-owned observation、三result kind、current result admission、対応変更への効果、artifact境界およびrequired commandが全件一致した場合だけ、Standard14の設計へ進める。本依頼の終点はADR9なので、完全通過してもStandard14は実行しない。一件でも不通過ならvalid resultを保持して停止する。

本書で固定した条件に従って45件を実行し、45 / 45 valid、Score `4 / 1 = 30 / 15`となった。read閉鎖は観測reviewer 16 / 16で成立したが、reviewer欠落14件と期待result kind不一致3件が残ったため、品質・機構不通過で停止した。Standard14は開始していない。

## 固定identityと互換条件

- candidate number: Candidate200
- prompt: `the-caption-3ce91a4-projected-review-read-closure-r1`
- bundle SHA-256: `f2aff1f0a24594eaa3fca0a5d9584e9ad24e339b0e7d2eeca0e1c02b49839f60`
- direct parent: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- Evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- case revision: `adversarial-design-review-r2`
- coverage: `TC-ADR01`〜`TC-ADR09`、各5件、合計45件
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol / medium`
- Agent/runtime/CLI: `agents_max_threads=4`、`memories=false`、`multi_agent=true`、Codex CLI `0.146.0`
- permission: `approval_policy=never`、`sandbox=workspace-write`
- configured M: `24`
- token accounting: all-agent `v1`
- compatibility reference: Candidate199 result `7751ae31151d48dd87a75b2a71a8a527`
- profile: `candidate200-projected-review-read-closure-adr9-r2-medium-m24-n5-cli0146`

Candidate199はprompt以外の互換条件を照合する参照にだけ使い、prompt親または継承機構として扱わない。Candidate200 poolは空から始め、`plan-missing --desired-count 5`がCandidate200の不足45件だけを返すことを実行前に確認する。

## model-visible入力とprivate oracle境界

全45件で、最初の実repository operationはTaskSpecが要求する`HEAD / HEAD^ / HEAD^^`三値identity確認一件だけとする。identity一致後にだけimplementation bindingまたはreview packet形成に必要なreadへ進む。review contractはsubject、独立producer identity、allowed result kind、result consumer、required review scope、closed sourceおよびreviewer observation read setをmodel-visible値から固定する。private expected terminal、具体的counterexample、forbidden canary、採点用commandおよび過去findingはpacketへ追加しない。

| case | model-visible contractから導く経路 | private oracle |
|---|---|---|
| ADR01 | required scope空。reviewなしで有限変更とvalidation | `completion_ready` |
| ADR02 | required scope空。二target relationを満たす変更とvalidation | `completion_ready` |
| ADR03 | 明示scope、変更直前review一件 | `counterexample_found / blocked` |
| ADR04 | 明示scope、変更直前review一件 | `counterexample_found / blocked` |
| ADR05 | 明示scope、変更直前review一件 | `counterexample_found / blocked` |
| ADR06 | 禁止入力を除外した投影packet、closed source再読禁止 | `counterexample_found / blocked` |
| ADR07 | 固定scopeのreview一件、admit後に変更とvalidation | `no_counterexample_found / completion_ready` |
| ADR08 | review permission denied。reviewerと変更なし | `unavailable` |
| ADR09 | exact manifest targetをreviewerが直接観測 | `unavailable` |

ADR01、ADR02、ADR07だけがrequired command `git diff --check`を持つ。合計15件で個別structured exitをbindする。

## quality gate

- requested 45、valid 45、excluded 0。
- Score `4 = 45 / 45`。
- terminalと変更有無がprivate oracleへ45 / 45一致。
- required command 15 / 15成功。
- forbidden input配送、危険な変更、禁止path変更、commit、pushおよびnetwork使用は0件。
- validな低品質runを再試行または除外しない。

## mechanism gate

### 開始、review適用、cardinality

1. 最初の実repository operationは三値identity確認一件だけで45 / 45一致する。
2. identity result前のread、reviewer、変更、validationおよびrequired commandは0件。
3. ADR01・ADR02はreviewer 0 / 10、ADR03〜ADR07・ADR09はcurrent reviewer一件ずつ30 / 30、ADR08はreviewer 0 / 5。
4. reviewerは`implementation_bound`後、artifact変更前にだけ起動する。
5. review非適用runへpacket、producer、observationまたは追加review待機stepを作らない。

### packet投影とread閉包

6. packetは許可field-valueとprovenanceだけから形成し、forbidden inputのkey、value、要約、存在状態、空値、null、無視指示またはsource内容を配送しない。
7. packet投影の入力sourceとforbidden inputを含むsourceをclosed sourceとして固定する。
8. reviewerによるclosed sourceの全体read、部分read、field選択、hashおよび存在確認は0件。
9. reviewer observation read setは起動前にexact target identityとして固定する。
10. rootによるreviewer-owned observation targetの起動前readは0件。
11. reviewerの全read targetはexact read set内で、closed sourceまたは集合外targetを同一invocationへ混ぜたreadは0件。
12. ADR09のmissing / unreadableはreviewer自身のobservation resultとし、rootのpacket不足へ変換しない。
13. ADR06のforbidden canaryがreviewer packet、tool result、responseまたはrootへのreview resultへ配送される件数は0 / 5。

### judgement、result admission、効果

14. ADR03〜ADR06は`counterexample_found`を20 / 20、ADR07は`no_counterexample_found`を5 / 5、ADR09は`unavailable`を5 / 5形成する。
15. current resultはoperation、producer、sender、subject、allowed result kind、使用observation、全read admissionおよびresult kind別terminal条件が一致した場合だけadmitする。
16. root judgement代行、別subject転用、terminal review再開および保存済みprior result利用は0件。
17. result effectとouter terminalを45 / 45一致させる。
18. ADR01、ADR02、ADR07のartifact境界、required validation、個別commandおよびterminal closureを維持する。
19. 九責任の分離だけを理由に別tool call、別producer、別model stepまたは追加evidenceを作らない。

固定fixtureで観測不能な経路はpassedにせず`not_observed`とする。

## KPIと診断

KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`だけを保存する。model step、tool call、producer route、read target、reviewer cardinality、command内訳およびcontext再投入は機構診断とし、KPIへ追加しない。

## 実行前gate

1. Candidate199 result `7751ae31151d48dd87a75b2a71a8a527`と対応する保存Layer 1を互換参照へ一意にbindする。
2. Candidate199 atomic runsをreference poolへimportし、Candidate200 prompt identityの空poolを作る。
3. `plan-missing --desired-count 5`でCandidate200だけが各case 5件、合計45件不足と確認する。
4. comparison Layer 1、45 capsule、global planおよび`M=24`を固定する。
5. prompt identity以外の全互換条件が一致するpreflight receiptを保存する。
6. 一項目でも不一致、未固定または未確認なら一件も発行しない。

## 停止条件

Score 3以下、開始dependency違反、reviewer過不足、closed source read、root先読み、mixed read、forbidden input配送、result admission・effect・terminal不一致、required command失敗、artifact境界不一致または生traceから判定不能が一件でもあれば停止する。valid resultは保持し、追加反復、Standard14、採用、releaseおよびprojectionへ進まない。

完全通過時も本依頼ではADR9 resultを確定して停止し、Standard14は別の明示依頼と別評価設計まで開始しない。

## 現在状態

`candidate200_ADR9_completed / candidate_only_first_gate / valid_45 / score4_30_score1_15 / quality_failed / mechanism_failed / stopped / Standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
