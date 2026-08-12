# docs 索引

`docs/`配下の研究文書を、読む前に**役割で選べる**ようにするための索引。文書は次の8分類で位置づける。

| 分類 | 意味 | 扱い |
|---|---|---|
| **正本（canonical）** | 他文書が参照authorityとして引く契約・原則 | 統合・要約せず維持。正本指定は各領域の`AGENTS.md`（下表参照） |
| **現在地・研究全体像** | 研究の目的、系譜、横断知見、未完了項目、長期方向 | 現在地点を把握する最初の起点 |
| **現行frontier** | 現在進行中の研究軸と、その直近の設計・診断 | 因果系列ごとに追い、完了済み成果と混ぜない |
| **研究成果・統合知見** | 固定版の技術報告、総説、横断分析、統合知見 | 現在有効な研究成果として読む。数値・状態は各文書が示す一次アーティファクトを正本とする |
| **実務者向け解説** | 研究成果を実務へ翻訳した読み物 | 研究アーティファクトの代替ではなく、実務から理解する入口として扱う |
| **評価・運用基盤** | 評価インフラ、実行環境、運用仕様 | 研究内容そのものではなく、測定・運用を成立させる基盤として扱う |
| **完了済み研究記録** | 特定Candidate・比較・診断の成果アーティファクト | 当時のresult・scoreを保持（遡及書換なし） |
| **historical／superseded** | root-only履歴、完了済みの引き継ぎ文書、旧設計入力 | 現行設計として読まない。冒頭バナーで位置づけ |

分類間の原則は[`AGENTS.md`](AGENTS.md)を正とする（現在状態・当時の評価・後続の再解釈を混ぜない／過去result・scoreを削除しない／現在解釈は注記か別文書として追加）。

---

## 1. 正本（canonical）

参照先として維持する。統合・要約・全文複製の対象にしない。「正本指定元」列は、その正本性を明示するinstructionを示す。

| 文書 | 役割 | 正本指定元 |
|---|---|---|
| [`repository-contract.md`](repository-contract.md) | リポジトリ契約の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md) | 評価基盤のレイヤーと境界の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`evaluation-loop-manual.md`](evaluation-loop-manual.md) | 評価実行方法の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-control-design-principles.md`](prompt-control-design-principles.md) | プロンプト制御の設計原則の正本 | [`docs/AGENTS.md`](AGENTS.md) |
| [`prompt-file-bundle.md`](prompt-file-bundle.md) | prompt file bundle形式・manifest・格納の正本 | [`scripts/AGENTS.md`](../scripts/AGENTS.md) |

## 2. 現在地・研究全体像

「何を研究しているか → どこまで来たか → 何が分かったか → 何が残っているか → どこへ進むか」の順に読むための入口。

| 文書 | 役割 |
|---|---|
| [`repository-overview.md`](repository-overview.md) | 初見向けの全体像（入口） |
| [`candidate-history.md`](candidate-history.md) | Candidate系譜と知見の索引。系譜と現在状態の一覧は[`prompts/candidates/README.md`](../prompts/candidates/README.md) |
| [`control-mechanisms.md`](control-mechanisms.md) | 横断的な制御メカニズムの知見 |
| [`research-backlog.md`](research-backlog.md) | 未完了研究項目の索引（label監査の再測定、`P3`削除candidate、A01 variation、未解決リスク）。判定の正本は各リンク先 |
| [`future-roadmap.md`](future-roadmap.md) | 長期方針と発展方向（恒久的な方針のみ） |

## 3. 現行frontier

現在進行中の研究軸を、別軸の作業を混ぜず因果系列ごとに並べる。

### 3a. 機能見直し・review admission

| 文書 | 役割 |
|---|---|
| [`review-control-reconstruction-milestone-plan.md`](review-control-reconstruction-milestone-plan.md) | C147の逐語維持や既存Candidate再現をゴールにせず、過去結果の因果分析、制御構造再設計、方向レビュー、ADR9互換試験、高リスク拡張、Standard14、成立後の複雑性評価、採用判断までを分離した現行マイルストーン計画 |
| [`review-control-reconstruction-causal-analysis.md`](review-control-reconstruction-causal-analysis.md) | ADR9 r2の9ケースをterminal別証明責務へ分類し、C147〜C193の狙い・実結果・反復原因、C193の部分効果、品質失敗2件、C147の13条項の確定・保留境界を扱う再開M1成果物 |
| [`candidate188-review-control-responsibility-implementation-audit.md`](candidate188-review-control-responsibility-implementation-audit.md) | Candidate188の削除済み親経路参照、汎用worker context欠落、条項過密化を確認し、評価前に`static_design_mismatch / stopped`とした静的再監査 |
| [`candidate189-self-contained-review-control-implementation-audit.md`](candidate189-self-contained-review-control-implementation-audit.md) | 共通execution coreとreview固有責務を自己完結的に分けたCandidate189の設計対応、C147不変条件、prompt量、bundle identityおよび未評価境界を固定したM4実装監査 |
| [`candidate190-current-prior-review-result-admission-implementation-audit.md`](candidate190-current-prior-review-result-admission-implementation-audit.md) | Candidate189のADR07失敗を受け、current resultと保存済みprior resultの受理permissionおよびdependencyを分離したCandidate190のM4修正版実装監査 |
| [`candidate190-current-prior-review-result-admission-adr9-r2-n5-evaluation-design.md`](candidate190-current-prior-review-result-admission-adr9-r2-n5-evaluation-design.md) | Candidate190の変更条項を消費するADR03〜ADR07・ADR09だけを各N=5で確認し、prior経路の未観測境界と30件だけの発行gateを固定したM5評価設計 |
| [`candidate190-current-prior-review-result-admission-adr9-r2-n5-execution-preparation-audit.md`](candidate190-current-prior-review-result-admission-adr9-r2-n5-execution-preparation-audit.md) | Candidate176の同一6ケース参照selection、固定Layer 1、30 capsule、global plan、private境界およびcomparison preflight readyを記録したCandidate190実行準備監査 |
| [`candidate190-current-prior-review-result-admission-adr9-r2-n5_2026-08-12.md`](../evaluations/results/candidate190-current-prior-review-result-admission-adr9-r2-n5_2026-08-12.md) | Candidate190のADR9変更効果6ケース30 / 30 Score 4、三result kind、current result admission成立、prior runtime未観測および限定M5通過判断 |
| [`candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-evaluation-design.md`](candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-evaluation-design.md) | 低頻度リスクを持つ三result kindのADR05・07・09だけを既存N=5再利用で累積N=20へ広げ、不足45件だけを許可するM6設計 |
| [`candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-execution-preparation-audit.md`](candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-execution-preparation-audit.md) | N=5 reference profile、固定Layer 1、45 capsule、private境界およびcomparison preflight readyを記録したM6実行準備監査 |
| [`candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20_2026-08-12.md`](../evaluations/results/candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20_2026-08-12.md) | 既存15件再利用・不足45件追加で三ケース累積60 / 60 Score 4、三result kind各20件およびM6通過を記録した結果 |
| [`candidate190-current-prior-review-result-admission-standard14-n5-evaluation-design.md`](candidate190-current-prior-review-result-admission-standard14-n5-evaluation-design.md) | Candidate176保存resultと互換なStandard14全14ケース各N=5、合計70件のM7 gateを固定した評価設計 |
| [`candidate190-current-prior-review-result-admission-standard14-n5-execution-preparation-audit.md`](candidate190-current-prior-review-result-admission-standard14-n5-execution-preparation-audit.md) | 固定Layer 1、70 capsule、private境界およびcomparison preflight readyを記録したM7実行準備監査 |
| [`candidate190-current-prior-review-result-admission-standard14-n5_2026-08-12.md`](../evaluations/results/candidate190-current-prior-review-result-admission-standard14-n5_2026-08-12.md) | Candidate190 Standard14の70 / 70 Score 4と、不要review producer 8 run・子agent read protocol violation 37件によるM7機序停止を分離して記録した結果 |
| [`candidate191-explicit-review-operation-applicability-implementation-audit.md`](candidate191-explicit-review-operation-applicability-implementation-audit.md) | Candidate190のowner metadata昇格を受け、C147の独立`OWNER_ROLE`を復元してreview適用を明示された独立operationへ限定したCandidate191実装監査 |
| [`candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-evaluation-design.md`](candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-evaluation-design.md) | Candidate191の既存6ケース30件を再利用し、ADR01・ADR02・ADR08の不足15件だけでADR9 r2全9ケースN=5を完成させる評価設計 |
| [`candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-execution-preparation-audit.md`](candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-execution-preparation-audit.md) | 全9ケース互換条件、既存30件、15 capsule、M=24およびcomparison preflight readyを固定した実行準備監査 |
| [`candidate191-explicit-review-operation-applicability-adr9-r2-full-n5_2026-08-12.md`](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5_2026-08-12.md) | 不足15件追加でADR9 r2全9ケース45 / 45 Score 4、review適用・非適用を含む機序通過を記録したM5結果 |
| [`candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-evaluation-design.md`](candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-evaluation-design.md) | Candidate191 M5の訂正後通過を受け、ADR05・07・09だけを既存N=5再利用で累積N=20へ広げ、不足45件だけを許可するM6設計 |
| [`candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-execution-preparation-audit.md`](candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-execution-preparation-audit.md) | 訂正機序監査r3と登録resultのbind、N=5 reference selection、固定Layer 1、45 capsuleおよびcomparison preflight readyを記録したM6実行準備監査 |
| [`candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20_2026-08-12.md`](../evaluations/results/candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20_2026-08-12.md) | 既存15件再利用・不足45件追加で三ケース累積60 / 60 Score 4、訂正command-evidence基準での機序通過およびN=50非発行を記録したM6結果 |
| [`candidate191-explicit-review-operation-applicability-standard14-full-n5-evaluation-design.md`](candidate191-explicit-review-operation-applicability-standard14-full-n5-evaluation-design.md) | 限定Standard14の既存15件を再利用し、他11ケースの不足55件だけで全14ケースN=5を完成させるM7評価設計 |
| [`candidate191-explicit-review-operation-applicability-standard14-full-n5-execution-preparation-audit.md`](candidate191-explicit-review-operation-applicability-standard14-full-n5-execution-preparation-audit.md) | Candidate176基準result、固定Layer 1、既存15件、不足55 capsule、M=24およびcomparison preflight readyを記録したM7実行準備監査 |
| [`candidate191-explicit-review-operation-applicability-standard14-full-n5_2026-08-12.md`](../evaluations/results/candidate191-explicit-review-operation-applicability-standard14-full-n5_2026-08-12.md) | Standard14全14ケース70 / 70 Score 4、不要producer 0、command protocol violation 0およびM7通過を記録した結果 |
| [`candidate191-complexity-efficiency-evaluation.md`](candidate191-complexity-efficiency-evaluation.md) | C147比のprompt複雑性、Candidate191の3評価系列KPI、互換系列内のtoken・elapsed差、producer・command・recoveryを品質・機序と分離し、直接圧縮せずM9へ渡すとしたM8成果物 |
| [`candidate191-standard14-cost-mechanism-reassessment.md`](candidate191-standard14-cost-mechanism-reassessment.md) | Standard14のC147比token増をケース別traceへ分解し、9ケースの共同発行退行が総増分の86.74%を占めるためM7機序通過とM9 readyを撤回した後続再判定 |
| [`candidate192-consumer-bound-coissuance-implementation-audit.md`](candidate192-consumer-bound-coissuance-implementation-audit.md) | Candidate191の共同発行退行を受け、consumerなし開始観測を禁止し、相互非依存なready invocationを同一model stepへ閉じる一変更軸を固定したCandidate192実装監査 |
| [`candidate192-consumer-bound-coissuance-standard14-targeted-n5-evaluation-design.md`](candidate192-consumer-bound-coissuance-standard14-targeted-n5-evaluation-design.md) | Candidate191で共同発行退行を実測した9ケースとF04対照だけを各N=5で確認し、consumer、共同発行、真正dependency、品質および停止条件を固定したCandidate192初回評価設計 |
| [`candidate192-consumer-bound-coissuance-standard14-targeted-n5-execution-preparation-audit.md`](candidate192-consumer-bound-coissuance-standard14-targeted-n5-execution-preparation-audit.md) | C191既存50 atomic runの同一coverage selection、固定Layer 1、C192不足50 capsule、M=24およびcomparison preflight readyを記録した実行準備監査 |
| [`candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md`](../evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md) | 対象10ケース50 / 50 Score 4を維持した一方、A01 consumerなし開始identity 2 / 5、退行8ケースのidentity/read共同発行1 / 40によりC192機序を不通過として停止した結果 |
| [`candidate193-frontier-bound-dispatch-transition-implementation-audit.md`](candidate193-frontier-bound-dispatch-transition-implementation-audit.md) | Candidate191を直接基盤とし、C192の抽象gateを継承せず、frontierの全件個別発行と全result収集を一terminalへbindしたCandidate193 M4実装監査 |
| [`candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-evaluation-design.md`](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-evaluation-design.md) | 全tool発行へ作用するCandidate193をADR9 r2全9ケース各N=5で検証し、Candidate191の登録済み45件を訂正済み機序解釈とともに参照するM5設計 |
| [`candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-execution-preparation-audit.md`](candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-execution-preparation-audit.md) | Candidate191参照45件、Candidate193不足45件、固定Layer 1、M=24、comparison preflight readyおよび発行0件を記録した実行準備監査 |
| [`candidate193-frontier-bound-dispatch-transition-adr9-r2-n5_2026-08-12.md`](../evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5_2026-08-12.md) | Candidate193 ADR9 r2の45 / 45 valid、Score 4 / 1 = 43 / 2、identity/read dependency越境28件、Candidate191比8件の部分改善、品質・機序不通過およびM1再開を記録した結果 |
| [`candidate189-self-contained-review-control-adr9-r2-n5-evaluation-design.md`](candidate189-self-contained-review-control-adr9-r2-n5-evaluation-design.md) | Candidate189のADR9 r2全9ケースN=5、terminal別mechanism predicate、Candidate176基準再利用および45件だけの発行設計 |
| [`candidate189-self-contained-review-control-adr9-r2-n5-execution-preparation-audit.md`](candidate189-self-contained-review-control-adr9-r2-n5-execution-preparation-audit.md) | Candidate189の固定Layer 1、9 template、45 capsule、global plan、private境界およびcomparison preflight readyの実行準備監査 |
| [`candidate189-self-contained-review-control-adr9-r2-n5_2026-08-12.md`](../evaluations/results/candidate189-self-contained-review-control-adr9-r2-n5_2026-08-12.md) | Candidate189のADR9 r2全9ケースN=5で観測した44 / 45成功、新規review resultへの保存result permission誤適用およびM6停止判断 |
| [`feature-review-phase1-plan.md`](feature-review-phase1-plan.md) | Candidate147を基準に、過去機能の維持・休眠・欠落・プロンプト強制不能を一件ずつ判定する機能見直しフェーズ。最初の対象は独立SA reviewと情報封鎖の必要性 |
| [`candidate164-autonomous-review-admission-design.md`](candidate164-autonomous-review-admission-design.md) | FR-01自律routingで観測したHR03失敗に対し、C147へreview admission / producer選択predicate一つだけを追加した設計。targeted試験はreviewer起動5 / 5まで改善したがterminal再生成1件で停止 |
| [`candidate165-review-result-admission-design.md`](candidate165-review-result-admission-design.md) | C164の1件をprior評価のauthority誤分類として分解し、current TaskSpecへbind済みのresultだけをquality criterionへadmitする設計。Review4は20 / 20、Standard14は70 / 70 Score `4`。C147比のコスト増を残す |
| [`candidate165-standard14-review-route-analysis.md`](candidate165-standard14-review-route-analysis.md) | C165 Standard14 70 traceから、独立SAの実質修正0 / 41、通常ケースへの系統起動40件、clean-context root review成功5 / 5を分離し、result admission成立とreview admission過大を切り分けた現在解釈 |
| [`candidate166-prior-evaluation-review-admission-design.md`](candidate166-prior-evaluation-review-admission-design.md) | C165の過大発動に対し、アーティファクト実装・調査を独立SA切替条件から外した一変更。Review4はroute / closure 20 / 20、oracle一致18 / 20。HR03のケース設計不備によりquality未判定、Standard14未実施 |
| [`candidate166-review4-case-validity-analysis.md`](candidate166-review4-case-validity-analysis.md) | C166 Review4のHR03を再監査し、raw response不在のまま観測表現を強めたため期待terminalが一意でないと判定。18 / 20をquality failureへ使わず、r2 case revisionの事前条件を固定 |
| [`candidate166-review-behavior-case-reassessment.md`](candidate166-review-behavior-case-reassessment.md) | プロンプト内部条件の直積を廃止し、review不要、正常、欠陥、判定不能と外乱対照pairで既存ケースを再分類。次gateを7ケース × N=5へ固定するケース設計 |
| [`preimplementation-information-sealed-adversarial-design-review-spec.md`](preimplementation-information-sealed-adversarial-design-review-spec.md) | 固定済み契約を満たす一般設計をC147の`implementation_bound`へ渡す前に、探索で閉じた境界、固定試験の見落とし可能性、反例による設計変更を共同判定し、必要な場合だけ情報封鎖した独立敵対的レビューを行う新規仕様。Candidate、評価設計、評価は未着手 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r1.md`](preimplementation-information-sealed-adversarial-design-review-audit-r1.md) | 設計第1版を情報封鎖した独立producerが監査し、所有境界の自己免除と、維持する探索由来境界の漏れを反例として確認。第1版をrejectし、第2版へ二つの境界修正を要求した完了済み監査 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r2.md`](preimplementation-information-sealed-adversarial-design-review-audit-r2.md) | 設計第2版の許可artifact自体に先行監査情報が埋め込まれ、情報封鎖と結果受入を迂回できる反例を確認。第2版をrejectし、semantic projectionとruntime packet identityを要求した完了済み監査 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r3.md`](preimplementation-information-sealed-adversarial-design-review-audit-r3.md) | 設計第3版の第1〜11節だけを固定packetとして新しい独立producerが10境界を監査。packet・producer identity一致を確認し、一般設計を変える反例なしとしてTarget評価設計を許可した完了済み監査 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r4.md`](preimplementation-information-sealed-adversarial-design-review-audit-r4.md) | finite evidence manifestを追加した設計第4版の第1〜11節だけを固定packetとして再監査。現在snapshotの観測完了と一般membership閉包の分離を含む境界に反例なしとした完了済み監査 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r5.md`](preimplementation-information-sealed-adversarial-design-review-audit-r5.md) | 設計第5版の`no_counterexample_found`受入条件が実際の`review_scope`とpacketの必須範囲を照合していない反例を確認。第5版をrejectし、必須review scope identityの完全性を新しい設計identityへ要求した完了済み監査 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r6.md`](preimplementation-information-sealed-adversarial-design-review-audit-r6.md) | 設計第6版で同一設計操作内の自作authorityを閉包根拠にできることと、`review_scope`に未許可範囲を水増しできる反例を確認。第6版をrejectした完了済み監査 |
| [`preimplementation-information-sealed-adversarial-design-review-audit-r7.md`](preimplementation-information-sealed-adversarial-design-review-audit-r7.md) | 先行固定authority、必須review scope集合の完全一致、finite manifest、permission判定順序を含む設計第7版の固定packetを独立監査。一般設計を変える反例なしとした完了済み監査 |
| [`preimplementation-adversarial-design-review-targeted-evaluation-design.md`](preimplementation-adversarial-design-review-targeted-evaluation-design.md) | 旧修正契約ケースを使わず、authority閉包、open boundary、維持境界、所有自己免除、semantic packet、反例不在、manifest不完全、result admissionを9ケースへ固定したCandidate実装前のtargeted評価設計 |
| [`preimplementation-adversarial-design-review-targeted-evaluation-audit-r7.md`](preimplementation-adversarial-design-review-targeted-evaluation-audit-r7.md) | 一般設計第7版とTarget評価設計第9版だけから9ケースの経路、terminal、identity binding、誤経路分類、5 valid runの比較条件を独立監査し、反例なしとした完了済み監査 |
| [`preimplementation-adversarial-design-review-targeted-evaluation-audit-r10.md`](preimplementation-adversarial-design-review-targeted-evaluation-audit-r10.md) | ADR04のmembershipとstop applicability分離、ADR07 / ADR09の同一manifestと証拠実在差を反映したTarget評価設計r10を独立監査し、一般設計変更を要する反例なしとした完了済み監査 |
| [`preimplementation-adversarial-design-review-case-audit-r3.md`](preimplementation-adversarial-design-review-case-audit-r3.md) | private oracleを禁止した独立producerがcase materialization revision 3の9件からreview経路、変更可否、terminalを導出。rootの後段機械照合で9 / 9件がprivate oracleと完全一致した完了済みcase監査 |
| [`preimplementation-adversarial-design-review-targeted-evaluation-design-r11.md`](preimplementation-adversarial-design-review-targeted-evaluation-design-r11.md) | r10の入力資格不足を受け、same-treatmentのpositive predicateと区別属性domainの閉包を先行固定contractへ追加したdevelopment Target評価設計 |
| [`preimplementation-adversarial-design-review-targeted-evaluation-audit-r11.md`](preimplementation-adversarial-design-review-targeted-evaluation-audit-r11.md) | Target評価設計r11を一般仕様だけから独立監査し、具体的反例の規範根拠、missing優先、ADR03 / 04 / 06とADR07 / 09の分離に反例なしとした完了済み監査 |
| [`preimplementation-adversarial-design-review-case-audit-r4.md`](preimplementation-adversarial-design-review-case-audit-r4.md) | private oracleを禁止した独立producerがcase materialization revision 4の9件をmodel-visible入力だけから導出し、rootの後段照合で9 / 9件がprivate oracleと一致した完了済みcase監査 |
| [`review-terminal-proof-obligation-analysis.md`](review-terminal-proof-obligation-analysis.md) | Candidate186の18件を、存在証明への全域証明要求、missing packetの起動前停止、有限固定効果への不要review、制御密度へ分解し、次設計をC147直接基盤のterminal別proof obligationへ絞った原因分析 |
| [`review-terminal-proof-obligation-qualification-contract.md`](review-terminal-proof-obligation-qualification-contract.md) | terminal別proof obligationを汎用packet schemaで閉じようとした初期contract。独立レビューr1〜r9で具体的反例が続き、identity／receipt／reference完全性が過密化したため全revisionをrejectし、r10は作成せず停止 |
| [`review-terminal-proof-obligation-adversarial-review-series.md`](review-terminal-proof-obligation-adversarial-review-series.md) | qualification contract r1〜r9のcontract、情報封鎖packet、独立resultを結ぶ完了済み索引。9件の具体的反例と全revision reject、r10未作成を記録 |
| [`review-terminal-proof-obligation-minimal-direction-design.md`](review-terminal-proof-obligation-minimal-direction-design.md) | reviewで完全性を証明し切る方向を止め、C147の既存制御を再利用してterminal別の小さい判定だけを6条件の実行可能probeで確認した再設計。6 / 6件がprivate oracleと一致し、完全性は後続Target評価へ委譲 |
| [`review-terminal-proof-obligation-targeted-evaluation-design.md`](review-terminal-proof-obligation-targeted-evaluation-design.md) | 最小方向設計の6条件を情報封鎖したLLM実行へ移すdevelopment Target評価設計。問題資格確認30件を完了し、必要review省略の同一誤経路3 / 5件により次設計条件が成立 |
| [`review-terminal-proof-obligation-case-materialization-audit.md`](review-terminal-proof-obligation-case-materialization-audit.md) | 6ケースのprivate oracle一致、情報非漏洩、Q3／Q4一軸差、Q5／Q6条件、固定targetからのseed commit／tree再現を機械監査し、6 / 6件成功した記録 |
| [`review-terminal-proof-obligation-problem-qualification-execution-design.md`](review-terminal-proof-obligation-problem-qualification-execution-design.md) | Candidate173を診断対照とする6ケース各N=5 validの実行条件と判定記録。30 / 30 valid、Score 4 = 30、機構27 / 30で、同一誤経路3 / 5によりC147直接基盤の次設計条件が成立 |
| [`review-terminal-proof-obligation-execution-preparation-audit.md`](review-terminal-proof-obligation-execution-preparation-audit.md) | Candidate173問題資格確認の固定Layer 1、6ケース各5回の30 slot、profile・rating・bundle・fixture・capsule・global plan一致とprivate情報非漏洩を確認し、run未発行で実行直前まで準備した監査 |
| [`review-admission-proof-obligation-design.md`](review-admission-proof-obligation-design.md) | 問題資格確認で3 / 5件再現した必要review省略経路だけを対象に、C147へ一つの`REVIEW_ADMISSION_PROOF`を加えるCandidate187作成前設計。完全性は固定6ケースのTarget試験へ委譲 |
| [`candidate187-review-admission-proof-obligation-targeted-evaluation-design.md`](candidate187-review-admission-proof-obligation-targeted-evaluation-design.md) | Candidate187を固定6ケース各N=5 validで単独評価する初回Target gate設計。30 / 30 Score 4、機構30 / 30でquality・mechanism gate通過 |
| [`candidate187-review-admission-proof-obligation-implementation-audit.md`](candidate187-review-admission-proof-obligation-implementation-audit.md) | C147の13条項を保持して`REVIEW_ADMISSION_PROOF`一条項だけを追加したこと、Target profile固定、bundle・方向性・全回帰試験成功を記録した実装監査 |
| [`candidate187-review-admission-proof-obligation-execution-preparation-audit.md`](candidate187-review-admission-proof-obligation-execution-preparation-audit.md) | 保存済み問題資格確認resultとprompt以外の互換条件を照合し、Candidate187だけの30 slotを承認済み・未発行まで固定した実行前監査。後続実行30 / 30 validへの導線を追記 |
| [`candidate187-review-admission-proof-obligation-tpo04-n20-evaluation-design.md`](candidate187-review-admission-proof-obligation-tpo04-n20-evaluation-design.md) | Target gate通過後、元の失敗case TC-TPO04だけを既存5件再利用・不足15件新規発行で累計N=20へ拡張するatomic評価設計 |
| [`candidate187-review-admission-proof-obligation-tpo04-n20-execution-preparation-audit.md`](candidate187-review-admission-proof-obligation-tpo04-n20-execution-preparation-audit.md) | TC-TPO04の既存5件を基準へ固定し、不足15件だけをatomic dispatchへ承認済み・未発行まで固定したN=20拡張実行前監査 |
| [`candidate187-review-admission-proof-obligation-tpo04-n20_2026-08-12.md`](../evaluations/results/candidate187-review-admission-proof-obligation-tpo04-n20_2026-08-12.md) | TC-TPO04の既存5件と新規15件を累積し、20 / 20 Score 4、独立reviewer 20 / 20、対象エラー経路0 / 20を確認した限定N=20結果 |
| [`candidate187-review-admission-proof-obligation-adr9-r2-n5-evaluation-design.md`](candidate187-review-admission-proof-obligation-adr9-r2-n5-evaluation-design.md) | Candidate187の三状態とrequired時の三terminalに対応するADR01、02、05、07、08、09だけを各N=5で同一ADR9系列として比較するsubset評価設計 |
| [`candidate187-review-admission-proof-obligation-adr9-r2-subset-n5_2026-08-12.md`](../evaluations/results/candidate187-review-admission-proof-obligation-adr9-r2-subset-n5_2026-08-12.md) | Candidate186の同一6ケースを再利用したADR9互換比較。Candidate187は18 / 30 Score 4で、review不要分類、必要review起動、review結果のterminal対応が不安定なため停止 |
| [`candidate178-support-source-admission-design.md`](candidate178-support-source-admission-design.md) | Candidate177で残ったsupport sourceの資格・lifecycle・packet配送・全経路共通admission・局所失効を、一つのsource contract変更軸として統合したCandidate178設計。ADR9 r2 N=5で品質・機序gateを通過せず停止 |
| [`candidate178-support-source-contract-design-audit.md`](candidate178-support-source-contract-design-audit.md) | 一predicateへの分解で認証連鎖を増やした初期方向を破棄し、複数要素を持つ一契約へ再設計した経緯と、情報封鎖した独立敵対的レビューの修正・終端結果を記録した設計監査 |
| [`candidate179-review-evidence-interface-design.md`](candidate179-review-evidence-interface-design.md) | Candidate178を流用せずCandidate177を直接親とし、source kindの起動前固定とroot可視の単一assessment recordを一つのreview evidence interfaceとして設計したCandidate179。情報封鎖した独立敵対的reviewは第26版で反例なし。ADR9 r2 N=5はScore `4 / 1 = 40 / 5`で品質・機序gate不通過のため停止 |
| [`candidate179-review-evidence-interface-design-audit.md`](candidate179-review-evidence-interface-design-audit.md) | Candidate179設計を情報封鎖して反復監査し、外部runtimeへ依存せず構成可能な一般設計へ収束した経緯と、第26版の反例なし終端を記録した設計監査 |
| [`candidate180-general-design-boundary-design.md`](candidate180-general-design-boundary-design.md) | Candidate147を直接親とし、規範上の対象境界と提案設計の意味上の変更効果境界から一般設計の実装前受入可否を決める設計。tool、読取順、件数、schemaを固定しない一つの境界predicateとして第12版で敵対的reviewを通過 |
| [`candidate180-general-design-boundary-design-audit.md`](candidate180-general-design-boundary-design-audit.md) | Candidate180設計を情報封鎖した独立producerで反復監査し、処理手順を追加せず一般入力の反例を閉じた第1版から第12版までの設計監査 |
| [`candidate180-general-design-boundary-implementation-audit.md`](candidate180-general-design-boundary-implementation-audit.md) | Candidate147直接親のCandidate180実装を独立監査し、初回の受入式接続・禁止入力・保持constraintの3欠落を修正後、設計第12版との意味一致を確認した実装監査 |
| [`candidate181-independent-general-design-review-boundary-design.md`](candidate181-independent-general-design-review-boundary-design.md) | Candidate147を直接親とし、閉じていない一般判断だけを独立reviewへ送って、その結果をartifact変更可否へ接続するCandidate181設計。固定手順を加えず、情報封鎖した敵対的設計reviewを通過 |
| [`candidate181-independent-general-design-review-boundary-adversarial-review.md`](candidate181-independent-general-design-review-boundary-adversarial-review.md) | C147、一般設計原則、Candidate181設計だけを許可入力にした独立review。固定した9観点で一般入力の具体的反例なしと判定 |
| [`candidate181-independent-general-design-review-boundary-implementation-audit.md`](candidate181-independent-general-design-review-boundary-implementation-audit.md) | Candidate181実装がC147の既存15項を保持し、設計した一つの境界だけを追加していることを情報封鎖して確認した実装監査 |
| [`candidate182-design-decision-support-boundary-design.md`](candidate182-design-decision-support-boundary-design.md) | Candidate147を直接親とし、authority未固定の入力へ届く自律的一般化判断だけを独立reviewへ送り、反例と停止効果をdecision・subject・mutationの依存境界へ局所化するCandidate182設計。情報封鎖した第22版reviewで反例なし |
| [`candidate182-autonomous-generalization-review-boundary-adversarial-review.md`](candidate182-autonomous-generalization-review-boundary-adversarial-review.md) | Candidate147、一般設計原則、Candidate182設計だけを許可した反復reviewで、処理固定を除き、発火・lineage・interaction・support・訂正失効・mutation効果境界へ収束した記録 |
| [`candidate182-autonomous-generalization-review-boundary-implementation-audit.md`](candidate182-autonomous-generalization-review-boundary-implementation-audit.md) | Candidate147直接親のCandidate182実装を情報封鎖して監査し、設計条件の圧縮欠落を修正後に`implementation_matches_design`を確認した実装監査 |
| [`../evaluations/results/candidate182-autonomous-generalization-review-boundary-adr9-r2-n5_2026-08-11.md`](../evaluations/results/candidate182-autonomous-generalization-review-boundary-adr9-r2-n5_2026-08-11.md) | Candidate182 ADR9 r2 N=5の一次結果と機序分析。open domainの閉包をreview発行前提へした過剰停止によりScore `4 / 1 = 14 / 31`で停止 |
| [`candidate183-mutation-review-effect-boundary-design.md`](candidate183-mutation-review-effect-boundary-design.md) | Candidate147を直接基準とし、変更predicateを意味分解せず、固定対応しないmutationの独立reviewとresultのmutation・組合せ別発行効果境界を定めたCandidate183第11版設計 |
| [`candidate183-mutation-review-effect-boundary-adversarial-review.md`](candidate183-mutation-review-effect-boundary-adversarial-review.md) | C147、一般設計原則、Candidate183設計だけを許可した情報封鎖reviewで一般反例なしとした実装前gate記録 |
| [`candidate183-mutation-review-effect-boundary-implementation-audit.md`](candidate183-mutation-review-effect-boundary-implementation-audit.md) | C147直接親のCandidate183実装が設計第11版と一致し、固定tool・schema・順序・operation数を追加していないことを確認した実装監査 |
| [`../evaluations/results/candidate183-mutation-review-effect-boundary-adr9-r2-n5_2026-08-11.md`](../evaluations/results/candidate183-mutation-review-effect-boundary-adr9-r2-n5_2026-08-11.md) | Candidate183 ADR9 r2 N=5の一次結果と機序分析。Score `4 / 1 = 39 / 6`で、固定変更への過剰reviewとmissing入力の判断別効果境界が残り停止 |
| [`judgement-result-effect-boundary-design.md`](judgement-result-effect-boundary-design.md) | Candidate147を直接基準とし、review発行、具体的反例、反例なしの三判断ごとにmissing等の効果を局所化するCandidate作成前設計第1版。情報封鎖した敵対的reviewで2件の一般反例が成立し停止 |
| [`judgement-result-effect-boundary-adversarial-review.md`](judgement-result-effect-boundary-adversarial-review.md) | 設計第1版をC147原文、一般設計原則、設計本文だけで独立reviewし、open classへの固定変換をreview不要にできる反例と、必要なcombination subjectを形成しないまま同時変更をadmitできる反例を記録した停止結果 |
| [`judgement-result-effect-boundary-design-r2.md`](judgement-result-effect-boundary-design-r2.md) | Candidate147を直接基準とし、open classのreview不要経路を既存のconstraint保持resultへ限定し、実際の同時発行集合へ独立性resultまたはcombination judgementを必須化したCandidate作成前設計第2版。敵対的reviewで2件の一般反例が成立し停止 |
| [`judgement-result-effect-boundary-adversarial-review-r2.md`](judgement-result-effect-boundary-adversarial-review-r2.md) | 設計第2版を情報封鎖して独立reviewし、dependency変更時の旧judgement強制失効不足と、combination停止効果の別coemission identityへの過剰伝播を記録した停止結果 |
| [`judgement-result-effect-boundary-design-r3.md`](judgement-result-effect-boundary-design-r3.md) | Candidate147を直接基準とし、全judgementのdependency変更時失効を機械式で必須化し、combination resultの効果を同じcoemission identityだけへ限定したCandidate作成前設計第3版。情報封鎖した敵対的reviewで一般反例なし |
| [`judgement-result-effect-boundary-adversarial-review-r3.md`](judgement-result-effect-boundary-adversarial-review-r3.md) | 設計第3版をC147原文、一般設計原則、設計本文だけで独立reviewし、11観点で一般反例なしとしたCandidate作成前gateの通過記録 |
| [`candidate184-judgement-result-effect-boundary-implementation-audit.md`](candidate184-judgement-result-effect-boundary-implementation-audit.md) | Candidate184実装を情報封鎖して反復監査し、意味欠落とreview済み設計identity不一致を閉じた後、C147逐語保持と設計第3版への`implementation_matches_design`を確認した実装監査 |
| [`judgement-result-effect-boundary-design-r4.md`](judgement-result-effect-boundary-design-r4.md) | Candidate147を直接基準とし、固定対応の三状態、review要否の二状態、review入力の四状態を排他的な順序へ固定して、有限固定変更への不要reviewとmissingによるreview起動前停止を閉じるCandidate作成前設計第4版。情報封鎖した敵対的reviewで一般反例なし |
| [`judgement-result-effect-boundary-adversarial-review-r4.md`](judgement-result-effect-boundary-adversarial-review-r4.md) | 設計第4版をC147原文、一般設計原則、設計本文だけで独立reviewし、15観点で一般反例なしとしたCandidate作成前gateの通過記録 |
| [`candidate185-review-admission-totality-implementation-audit.md`](candidate185-review-admission-totality-implementation-audit.md) | Candidate185実装を情報封鎖して反復監査し、同時発行集合の排他性、terminal別局所効果、再bind条件およびmanifest誤記を閉じた後、C147逐語保持と設計第4版への`implementation_matches_design`を確認した実装監査 |
| [`review-decision-record-totality-design.md`](review-decision-record-totality-design.md) | Candidate185の7件を、subject全効果partitionとcomponent間relation、入力domain completeness receipt、根拠付き判断効果分類、独立admissionと三terminal record形成へ限定して閉じるC147直接基準のCandidate作成前設計。r13で`no_counterexample_found`、Candidate作成gate通過 |
| [`review-decision-record-totality-adversarial-review.md`](review-decision-record-totality-adversarial-review.md) | 初回の情報封鎖した実装前敵対的review。4件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r2.md`](review-decision-record-totality-adversarial-review-r2.md) | 修正版への情報封鎖した実装前敵対的review。2件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r3.md`](review-decision-record-totality-adversarial-review-r3.md) | 再修正版への情報封鎖した実装前敵対的review。混合effect subjectの1件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r4.md`](review-decision-record-totality-adversarial-review-r4.md) | 再修正版への情報封鎖した実装前敵対的review。component間relationと共有constraintの2件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r5.md`](review-decision-record-totality-adversarial-review-r5.md) | 再修正版への情報封鎖した実装前敵対的review。packet外witnessとreview admission producer境界の2件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r6.md`](review-decision-record-totality-adversarial-review-r6.md) | 再修正版への情報封鎖した実装前敵対的review。TaskSpec dependencyとterminal別root受入条件の2件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r7.md`](review-decision-record-totality-adversarial-review-r7.md) | 再修正版への情報封鎖した実装前敵対的review。許可入力0件時のpacket basis support欠落という1件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r8.md`](review-decision-record-totality-adversarial-review-r8.md) | 再修正版への情報封鎖した実装前敵対的review。finite occurrenceとsubject relation basisでconstraint値が二重化する1件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r9.md`](review-decision-record-totality-adversarial-review-r9.md) | 再修正版への情報封鎖した実装前敵対的review。許可入力domain completenessと分類根拠欠落の2件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r10.md`](review-decision-record-totality-adversarial-review-r10.md) | 再修正版への情報封鎖した実装前敵対的review。分類根拠取得不能を三terminalへ閉じられない1件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r11.md`](review-decision-record-totality-adversarial-review-r11.md) | 再修正版への情報封鎖した実装前敵対的review。counterexample field欠落recordとadmission/judgement producer同一化の2件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r12.md`](review-decision-record-totality-adversarial-review-r12.md) | 再修正版への情報封鎖した実装前敵対的review。precondition欠如を両側へ伝播する正規化の1件の一般反例により`counterexample_found / candidate_creation_blocked` |
| [`review-decision-record-totality-adversarial-review-r13.md`](review-decision-record-totality-adversarial-review-r13.md) | 固定SHA `a660d50f36d1d83c7cd1b3d6ea79a9b313fc7c10a103fca66084e91b1fb570e8`への情報封鎖した実装前敵対的review。12基準すべて`no_counterexample_found`、finding 0件、Candidate作成gate通過 |

### 3b. 公開ターゲット拡張

| 文書 | 役割 |
|---|---|
| [`public-target-selection-phase0.md`](public-target-selection-phase0.md) | 公開ターゲット選定Phase 0の実測記録と判定（`pallets/click`をPhase 1候補とした根拠） |

## 4. 研究成果・統合知見

固定版の研究成果、総説、横断分析、現在有効な統合知見をまとめる。進行中のCandidate系列とは分けて読む。

| 文書 | 役割 |
|---|---|
| [`execution-control-measurement-report.md`](execution-control-measurement-report.md) | 研究者向けの**技術報告 第1版**（2026-08-03、14節＋要旨＋付録A〜D）。BaselineをV1（汎用オーケストレーションプロンプト製品）の適用結果として位置づけ、本研究をV1が予定していたAI向け移行（V2）の実行として記述する。公開Baseline系譜（`orchestration-prompt`固定履歴）と外部文献・提供者指針を一次・補助資料として使う。**この版をもって記述を固定し、以降の測定は新しい版として追加する。** 数値と識別子は一次アーティファクトを、主張と証拠の対応はevidence mapを正本とする。|
| [`execution-control-measurement-report-evidence-map.md`](execution-control-measurement-report-evidence-map.md) | 上記**第1版**のClaim IDごとの一次資料対応表（証拠水準・表現上限・再検証分類）、再検証候補20件、一次資料と要約文書の相違・留保30件（外部文献への誤帰属5件の撤回を含む） |
| [`execution-control-research-paper.md`](execution-control-research-paper.md) | 研究成果の総説（論文形式、第3版・2026-07-31時点）。**上記の技術報告 第1版とは別の文書で、互いに置き換えない。** 実測値の要約と2026年7月ベンダ公式指針（GPT-5.6 Sol / Claude Opus 5）との対照。**正本ではない**。数値・状態の正本は同文書が示す一次アーティファクト |
| [`candidate125-candidate147-control-findings-synthesis.md`](candidate125-candidate147-control-findings-synthesis.md) | C125のN=5成立とN拡張停止から、C126〜C142のeffect / evidence境界探索、C143の上流再構築、C147のN=100採用までの因果系列と現在解釈 |
| [`branch-closure-retrospective-coding.md`](branch-closure-retrospective-coding.md) | 「分岐の開閉」軸の事後符号化（保存済みdiff 124件、新規測定なし）。判定入力をroot本文diffだけに限り、KPIを参照せずに符号化した手続きと全件の符号。**軸が実行経路と往復の2操作を含むこと、判定が符号化者に依存すること、経路を閉じることが十分条件でないことを確定する。** 技術報告§12.2はこれを引用する |
| [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md) | C71 control abstraction分析（11 label監査台帳＋現在の結論）。現在の総括は同文書の「監査状況の分類」表を正とする |

## 5. 実務者向け解説

研究成果を実務から読むためのExecution Controlシリーズ。研究アーティファクトや一次資料の代替ではない。

| 文書 | 役割 |
|---|---|
| [`01_why-prompt-writing-changes-your-bill.md`](01_why-prompt-writing-changes-your-bill.md) | **実務者向けExecution Controlシリーズ 1 / 8**。Free比のAPI料金換算`-39.95%`を入口に、削るべきものは文字数ではなく迷う余地だと説明する。 |
| [`02_how-to-write-prompts-that-cut-api-cost.md`](02_how-to-write-prompts-that-cut-api-cost.md) | **シリーズ 2 / 8**。成果、変更開始、担当と結果、調査、完了という5つの判断条件を、推測・手戻り・過剰な探索や検証と対応づける。 |
| [`03_what-not-to-write-in-ai-prompts.md`](03_what-not-to-write-in-ai-prompts.md) | **シリーズ 3 / 8**。索引追加、表面的な短文化、抽象的なmeta判断など、無条件に足さない7項目と代替を書く。 |
| [`04_what-prompts-can-and-cannot-control.md`](04_what-prompts-can-and-cannot-control.md) | **シリーズ 4 / 8**。AIが観測後に選ぶ行動と、executorやtool adapterが担う配送・原子性などの境界を説明する。 |
| [`05_review-roles-vs-decision-conditions.md`](05_review-roles-vs-decision-conditions.md) | **シリーズ 5 / 8**。レビュー工程と品質責務を分離し、別担当を増やす前に固定する判定対象と結果を示す。 |
| [`06_execution-paths-drive-ai-cost.md`](06_execution-paths-drive-ai-cost.md) | **シリーズ 6 / 8**。静的な文章量ではなく、モデル往復、再読、再検証を含む実行経路を設計対象として説明する。 |
| [`07_do-not-copy-human-development-processes.md`](07_do-not-copy-human-development-processes.md) | **シリーズ 7 / 8**。人間組織の工程を導入経路として認めつつ、AI向けには失敗様式と観測可能な条件へ変換する。 |
| [`08_what-is-execution-control.md`](08_what-is-execution-control.md) | **シリーズ 8 / 8**。AIへの依頼とExecution Controlを分け、進行・停止・完了を制御する全体像をまとめる。 |

## 6. 評価・運用基盤

| 文書 | 役割 |
|---|---|
| [`THE-CAPTION_execution-control_revision-instructions.md`](THE-CAPTION_execution-control_revision-instructions.md) | execution control修正指示（invocation_status等の定義） |
| [`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md) | 評価ストレージの維持・GC |
| [`desktop-evaluation-slot.md`](desktop-evaluation-slot.md) | desktop評価スロットの前提条件 |
| [`shared-python-runtime.md`](shared-python-runtime.md) | 共有Pythonランタイム |
| [`typed-boundary-evidence.md`](typed-boundary-evidence.md) | typed boundary evidenceの仕様 |
| [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md) | Layer 2 executorをClaude Code CLIへ置き換える試験方法の設計検討（未実装。未確定事項を含む） |
| [`pr-review-measurement-environment-design.md`](pr-review-measurement-environment-design.md) | `agent-execution-control-lab` namespacedインスタンスでClaude Code Actionの実行経路を比較するPRレビュー測定設計。仕様監査で既存PRR-C01 runをdiagnosticへ再分類し、Core Baselineは未qualification |

## 7. 完了済み研究記録

### 7a. Candidate設計記録

各Candidateの制御軸を記録した成果アーティファクト。当時のresult・scoreは遡及変更しない。

正本はlifecycle軸ごとに分かれる。**identityは各バンドルの`manifest.json`**、**評価状態は評価・診断を実施済みなら独立したevaluation / diagnostic result、未実施の`not_evaluated`は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列**、**release・approval・runtime projectionは[`prompts/releases/README.md`](../prompts/releases/README.md)**を正本とする。系譜と現在状態の一覧はcandidate索引にある。この索引は制御軸だけを示し、状態は複製しない（`docs/AGENTS.md`「同じ説明を複数文書へ全文複製せず正本へリンク」）。評価と採用、releaseとprojectionは別状態である（[`repository-contract.md`](repository-contract.md)、[`AGENTS.md`](AGENTS.md)）。

> **本体投影と評価状態は別軸**: Candidate147は公開版`the-caption`へ投影済みで、release status `projected` / approval `approved` / runtime projection `projected`である。Rating v14 Medium Standard14 N=100は1,400 / 1,400 score `4`、targeted F01 / F02 / F03のmechanismは15 / 15だった。Candidate125は移行前THE-CAPTIONへの投影履歴として保持する。Candidate125のStandard14 N=5は70 / 70 score `4`、A02 N=20はbind後再入0件だったが、2026-08-01のN=100追試はregistered poolを各ケース30件まで拡張した時点でF04 score `2`を5件確認し、`n100_execution_stopped / registered_pool_n30`で中断した（正式な`N=30`結果ではない）。過去のCandidate41・Candidate43・Candidate71・Candidate81・Candidate125の投影状態と、Candidate71の`standard14_b18_evaluated / stopped`を遡及変更しない。正本は[`prompts/releases/README.md`](../prompts/releases/README.md)と各release READMEとする。

| Candidate | 文書 | 制御軸 |
|---|---|---|
| C43 | [`candidate43-control-element-classification.md`](candidate43-control-element-classification.md) | 制御要素の目的別分別（F/A系分類） |
| C45 | [`candidate45-judgment-authority-boundary-design.md`](candidate45-judgment-authority-boundary-design.md) | 判断成立責任境界 |
| C46 | [`candidate46-resolved-premise-input-boundary-design.md`](candidate46-resolved-premise-input-boundary-design.md) | 解決済み前提入力境界 |
| C47 | [`candidate47-applicability-domain-boundary-design.md`](candidate47-applicability-domain-boundary-design.md) | 適用域境界 |
| C48 | [`candidate48-premise-dependency-boundary-design.md`](candidate48-premise-dependency-boundary-design.md) | 前提依存境界 |
| C49 | [`candidate49-explicit-delegation-control-boundary-design.md`](candidate49-explicit-delegation-control-boundary-design.md) | 明示委譲制御境界 |
| C50 | [`candidate50-root-read-batch-design.md`](candidate50-root-read-batch-design.md) | root read batch |
| C51 | [`candidate51-root-operation-completion-boundary-design.md`](candidate51-root-operation-completion-boundary-design.md) | root operation completion境界 |
| C52 | [`candidate52-root-independence-boundary-design.md`](candidate52-root-independence-boundary-design.md) | root independence境界 |
| C53 | [`candidate53-purpose-separated-operation-graph-design.md`](candidate53-purpose-separated-operation-graph-design.md) | 目的分離operation graph |
| C54 | [`candidate54-evidence-backed-control-core-design.md`](candidate54-evidence-backed-control-core-design.md) | evidence-backed control core |
| C55 | [`candidate55-prebound-operation-graph-design.md`](candidate55-prebound-operation-graph-design.md) | prebound operation graph |
| C55 | [`candidate55-route-efficiency-gate-r2.md`](candidate55-route-efficiency-gate-r2.md) | route efficiency gate（r2追試） |
| C56 | [`candidate56-resolved-fixed-read-boundary-design.md`](candidate56-resolved-fixed-read-boundary-design.md) | resolved fixed read boundary |
| C57 | [`candidate57-task-enumerated-read-boundary-design.md`](candidate57-task-enumerated-read-boundary-design.md) | task-enumerated read boundary |
| C58 | [`candidate58-purpose-bound-read-route-design.md`](candidate58-purpose-bound-read-route-design.md) | purpose-bound read route |
| C59 | [`candidate59-read-only-operation-batch-design.md`](candidate59-read-only-operation-batch-design.md) | read-only operation batch |
| C60 | [`candidate60-operation-method-capsule-design.md`](candidate60-operation-method-capsule-design.md) | operation method capsule |
| C61 | [`candidate61-atomic-spec-operation-gate-design.md`](candidate61-atomic-spec-operation-gate-design.md) | atomic SPEC operation gate |
| C62 | [`candidate62-task-closed-read-route-design.md`](candidate62-task-closed-read-route-design.md) | task-closed read route |
| C63 | [`candidate63-fixed-evidence-route-projection-design.md`](candidate63-fixed-evidence-route-projection-design.md) | fixed evidence route projection |
| C64 | [`candidate64-self-contained-execution-paths-design.md`](candidate64-self-contained-execution-paths-design.md) | self-contained execution paths |
| C65 | [`candidate65-shared-operation-core-design.md`](candidate65-shared-operation-core-design.md) | shared operation core |
| C66 | [`candidate66-topology-preserving-compression-design.md`](candidate66-topology-preserving-compression-design.md) | topology-preserving compression |
| C67 | [`candidate67-cross-label-predicate-deduplication-design.md`](candidate67-cross-label-predicate-deduplication-design.md) | cross-label predicate deduplication |
| C68 | [`candidate68-independent-review-operation-removal-design.md`](candidate68-independent-review-operation-removal-design.md) | independent review operation removal |
| C69 | [`candidate69-model-reentry-decision-boundary-design.md`](candidate69-model-reentry-decision-boundary-design.md) | model reentry decision boundary |
| C70 | [`candidate70-machine-decision-boundary-design.md`](candidate70-machine-decision-boundary-design.md) | machine decision boundary |
| C71 | [`candidate71-validation-closure-design.md`](candidate71-validation-closure-design.md) | validation closure |
| C72 | [`candidate72-closed-validation-state-design.md`](candidate72-closed-validation-state-design.md) | closed validation state |
| C73 | [`candidate73-terminal-closure-preserving-compression-design.md`](candidate73-terminal-closure-preserving-compression-design.md) | terminal closure preserving compression |
| C74 | [`candidate74-typed-execution-state-machine-design.md`](candidate74-typed-execution-state-machine-design.md) | typed execution state machine |
| C75 | [`candidate75-authority-bound-validation-fast-path-design.md`](candidate75-authority-bound-validation-fast-path-design.md) | authority-bound validation fast path |
| C76 | [`candidate76-final-state-validation-wave-design.md`](candidate76-final-state-validation-wave-design.md) | final-state validation wave |
| C77 | [`candidate77-triggered-exception-transition-design.md`](candidate77-triggered-exception-transition-design.md) | triggered exception transition |
| C78 | [`candidate78-project-index-navigation-design.md`](candidate78-project-index-navigation-design.md) | project index navigation |
| C79 | [`candidate79-ordered-validation-wave-design.md`](candidate79-ordered-validation-wave-design.md) | ordered validation wave |
| C80 | [`candidate80-root-validation-wrapper-design.md`](candidate80-root-validation-wrapper-design.md) | root validation wrapper |
| C81 | [`candidate81-validation-wrapper-precedence-design.md`](candidate81-validation-wrapper-precedence-design.md) | validation wrapper precedence |

C107〜C116の設計記録は「7b. 比較・診断・段階記録」へ掲載している。C164〜C166は現行frontierのため「3a」へ掲載している。

| Candidate | 文書 | 制御軸 |
|---|---|---|
| C82 | [`candidate82-producer-gate-deduplication-design.md`](candidate82-producer-gate-deduplication-design.md) | producer gate deduplication |
| C83 | [`candidate83-delegation-value-boundary-design.md`](candidate83-delegation-value-boundary-design.md) | delegation value boundary |
| C84 | [`candidate84-delegation-marginal-value-boundary-design.md`](candidate84-delegation-marginal-value-boundary-design.md) | delegation marginal value boundary |
| C85 | [`candidate85-planning-first-producer-selection-design.md`](candidate85-planning-first-producer-selection-design.md) | planning first producer selection |
| C86 | [`candidate86-producer-plan-fast-path-design.md`](candidate86-producer-plan-fast-path-design.md) | producer plan fast path |
| C87 | [`candidate87-producer-local-invocation-wave-design.md`](candidate87-producer-local-invocation-wave-design.md) | producer local invocation wave |
| C88 | [`candidate88-parallel-worker-admission-design.md`](candidate88-parallel-worker-admission-design.md) | parallel worker admission |
| C89 | [`candidate89-dispatch-time-worker-admission-design.md`](candidate89-dispatch-time-worker-admission-design.md) | dispatch time worker admission |
| C90 | [`candidate90-tool-output-ingress-boundary-design.md`](candidate90-tool-output-ingress-boundary-design.md) | tool output ingress boundary |
| C91 | [`candidate91-concise-output-ingress-design.md`](candidate91-concise-output-ingress-design.md) | concise output ingress |
| C92 | [`candidate92-bound-output-route-design.md`](candidate92-bound-output-route-design.md) | bound output route |
| C93 | [`candidate93-result-classification-design.md`](candidate93-result-classification-design.md) | result classification |
| C94 | [`candidate94-operation-criterion-totality-design.md`](candidate94-operation-criterion-totality-design.md) | operation criterion totality |
| C95 | [`candidate95-required-judgment-owner-boundary-design.md`](candidate95-required-judgment-owner-boundary-design.md) | required judgment owner boundary |
| C96 | [`candidate96-successful-validation-result-projection-design.md`](candidate96-successful-validation-result-projection-design.md) | successful validation result projection |
| C97 | [`candidate97-decision-round-closure-design.md`](candidate97-decision-round-closure-design.md) | decision round closure |
| C97 | [`candidate97-minimal-decision-round-closure-r2-design.md`](candidate97-minimal-decision-round-closure-r2-design.md) | minimal decision round closure r2 |
| C98 | [`candidate98-validation-completion-sheet-design.md`](candidate98-validation-completion-sheet-design.md) | validation completion sheet |
| C99 | [`candidate99-decision-evidence-boundary-design.md`](candidate99-decision-evidence-boundary-design.md) | decision evidence boundary |
| C100 | [`candidate100-outcome-source-closure-design.md`](candidate100-outcome-source-closure-design.md) | outcome source closure |
| C101 | [`candidate101-additional-investigation-trigger-design.md`](candidate101-additional-investigation-trigger-design.md) | additional investigation trigger |
| C102 | [`candidate102-prechange-evidence-freeze-design.md`](candidate102-prechange-evidence-freeze-design.md) | prechange evidence freeze |
| C103 | [`candidate103-prechange-evidence-receipt-design.md`](candidate103-prechange-evidence-receipt-design.md) | prechange evidence receipt |
| C104 | [`candidate104-staged-evidence-admission-design.md`](candidate104-staged-evidence-admission-design.md) | staged evidence admission |
| C105 | [`candidate105-validation-terminal-return-design.md`](candidate105-validation-terminal-return-design.md) | validation terminal return |
| C106 | [`candidate106-compact-validation-terminal-wait-design.md`](candidate106-compact-validation-terminal-wait-design.md) | compact validation terminal wait |
| C117 | [`candidate117-implementation-authority-delegation-design.md`](candidate117-implementation-authority-delegation-design.md) | implementation authority delegation |
| C118 | [`candidate118-implementation-bind-terminal-closure-design.md`](candidate118-implementation-bind-terminal-closure-design.md) | implementation bind terminal closure |
| C119 | [`candidate119-validation-predicate-method-boundary-design.md`](candidate119-validation-predicate-method-boundary-design.md) | validation predicate method boundary |
| C120 | [`candidate120-implementation-edit-ticket-closure-design.md`](candidate120-implementation-edit-ticket-closure-design.md) | implementation edit ticket closure |
| C121 | [`candidate121-evidence-request-scope-closure-design.md`](candidate121-evidence-request-scope-closure-design.md) | evidence request scope closure |
| C122 | [`candidate122-prechange-evidence-wave-closure-design.md`](candidate122-prechange-evidence-wave-closure-design.md) | prechange evidence wave closure |
| C123 | [`candidate123-preterminal-result-round-closure-design.md`](candidate123-preterminal-result-round-closure-design.md) | preterminal result round closure |
| C124 | [`candidate124-incomplete-content-continuation-design.md`](candidate124-incomplete-content-continuation-design.md) | incomplete content continuation |
| C125 | [`candidate125-criterion-complete-single-target-continuation-design.md`](candidate125-criterion-complete-single-target-continuation-design.md) | criterion complete single target continuation |
| C126 | [`candidate126-criterion-bound-change-input-design.md`](candidate126-criterion-bound-change-input-design.md) | criterion bound change input |
| C127 | [`candidate127-failed-change-salvage-design.md`](candidate127-failed-change-salvage-design.md) | failed change salvage |
| C128 | [`candidate128-required-effect-closure-design.md`](candidate128-required-effect-closure-design.md) | required effect closure |
| C129 | [`candidate129-unsatisfied-effect-change-admission-design.md`](candidate129-unsatisfied-effect-change-admission-design.md) | unsatisfied effect change admission |
| C130 | [`candidate130-focused-criterion-continuation-design.md`](candidate130-focused-criterion-continuation-design.md) | focused criterion continuation |
| C131 | [`candidate131-criterion-anchor-continuation-design.md`](candidate131-criterion-anchor-continuation-design.md) | criterion anchor continuation |
| C132 | [`candidate132-observed-preimage-change-construction-design.md`](candidate132-observed-preimage-change-construction-design.md) | observed preimage change construction |
| C133 | [`candidate133-anchor-first-continuation-order-design.md`](candidate133-anchor-first-continuation-order-design.md) | anchor first continuation order |
| C134 | [`candidate134-syntactic-lexeme-continuation-design.md`](candidate134-syntactic-lexeme-continuation-design.md) | syntactic lexeme continuation |
| C135 | [`candidate135-criterion-span-request-authority-design.md`](candidate135-criterion-span-request-authority-design.md) | criterion span request authority |
| C136 | [`candidate136-effect-local-change-admission-design.md`](candidate136-effect-local-change-admission-design.md) | effect local change admission |
| C137 | [`candidate137-pending-effect-validation-admission-design.md`](candidate137-pending-effect-validation-admission-design.md) | pending effect validation admission |
| C138 | [`candidate138-continuation-effect-change-handoff-design.md`](candidate138-continuation-effect-change-handoff-design.md) | continuation effect change handoff |
| C139 | [`candidate139-single-target-continuation-handoff-design.md`](candidate139-single-target-continuation-handoff-design.md) | single target continuation handoff |
| C140 | [`candidate140-effect-satisfaction-witness-design.md`](candidate140-effect-satisfaction-witness-design.md) | effect satisfaction witness |
| C141 | [`candidate141-prechange-relation-coverage-design.md`](candidate141-prechange-relation-coverage-design.md) | prechange relation coverage |
| C142 | [`candidate142-initial-joint-effect-admission-design.md`](candidate142-initial-joint-effect-admission-design.md) | initial joint effect admission |
| C143 | [`candidate143-required-outcome-implementation-bind-design.md`](candidate143-required-outcome-implementation-bind-design.md) | required outcome implementation bind |
| C144 | [`candidate144-required-outcome-validation-method-boundary-design.md`](candidate144-required-outcome-validation-method-boundary-design.md) | required outcome validation method boundary |
| C145 | [`candidate145-lifecycle-consumer-evidence-admission-design.md`](candidate145-lifecycle-consumer-evidence-admission-design.md) | lifecycle consumer evidence admission |
| C146 | [`candidate146-consumer-closure-evidence-operation-design.md`](candidate146-consumer-closure-evidence-operation-design.md) | consumer closure evidence operation |
| C147 | [`candidate147-result-effect-scope-design.md`](candidate147-result-effect-scope-design.md) | result effect scope |
| C148 | [`candidate148-five-point-execution-control-design.md`](candidate148-five-point-execution-control-design.md) | five point execution control |
| C149 | [`candidate149-specification-start-boundary-design.md`](candidate149-specification-start-boundary-design.md) | specification start boundary |
| C150 | [`candidate150-required-outcome-bind-readable-design.md`](candidate150-required-outcome-bind-readable-design.md) | required outcome bind readable |
| C151 | [`candidate151-evidence-consumer-boundary-readable-design.md`](candidate151-evidence-consumer-boundary-readable-design.md) | evidence consumer boundary readable |
| C152 | [`candidate152-four-decision-rules-readable-design.md`](candidate152-four-decision-rules-readable-design.md) | four decision rules readable |
| C156 | [`candidate156-five-prompt-conditions-readable-design.md`](candidate156-five-prompt-conditions-readable-design.md) | five prompt conditions readable |
| C157 | [`candidate157-focused-prechange-research-readable-design.md`](candidate157-focused-prechange-research-readable-design.md) | focused prechange research readable |
| C158 | [`candidate158-outcome-method-readable-design.md`](candidate158-outcome-method-readable-design.md) | outcome method readable |
| C159 | [`candidate159-change-start-readable-design.md`](candidate159-change-start-readable-design.md) | change start readable |
| C160 | [`candidate160-assignment-result-readable-design.md`](candidate160-assignment-result-readable-design.md) | assignment result readable |
| C161 | [`candidate161-assignment-result-closure-readable-design.md`](candidate161-assignment-result-closure-readable-design.md) | assignment result closure readable |
| C162 | [`candidate162-completion-ticket-readable-design.md`](candidate162-completion-ticket-readable-design.md) | completion ticket readable |
| C163 | [`candidate163-five-verified-lines-integrated-design.md`](candidate163-five-verified-lines-integrated-design.md) | five verified lines integrated |

### 7b. 比較・診断・段階記録

| 文書 | 役割 |
|---|---|
| [`prompt-control-graph-review.md`](prompt-control-graph-review.md) | 制御グラフ棚卸し。提案predicateはCandidate41として実装・評価済みで、B18後も追加規則を導かないと結論した根拠記録 |
| [`a02-rating-divergence.md`](a02-rating-divergence.md) | A02の「要求と採点のずれ」3件と、rating contract v10〜v13の変遷 |
| [`candidate5-candidate15-continuous-comparison.md`](candidate5-candidate15-continuous-comparison.md) | Candidate5 / Candidate15の連続試験比較 |
| [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md) | Review location誤差の原因診断 |
| [`task-spec-planner-phase1-plan.md`](task-spec-planner-phase1-plan.md) | TaskSpec確認 第1段階の実施記録（実施・評価・release・projection完了） |
| [`sa-routing-decision-table.md`](sa-routing-decision-table.md) | candidate2のSA routing decision table |
| [`candidate87-adoption-decision.md`](candidate87-adoption-decision.md) | C87の評価状態を保持した別stateの不採用・停止判断と、C82〜C89系列の完了境界 |
| [`candidate106-f03-b20-short-yield-route-analysis.md`](candidate106-f03-b20-short-yield-route-analysis.md) | C104 / C106 F03 B20の途中のメッセージをouter early yieldとnonterminal再入の二段階へ分解した診断 |
| [`candidate107-validation-wrapper-reentry-closure-design.md`](candidate107-validation-wrapper-reentry-closure-design.md) | C106のF03 B20再発経路をouter deadline条件とcell ID wait-only遷移で閉じるCandidate107設計 |
| [`candidate108-validation-ticket-terminal-closure-design.md`](candidate108-validation-ticket-terminal-closure-design.md) | C107のdeadline大小比較を削除し、実行票全体のterminal wait-only遷移へ一本化するCandidate108設計 |
| [`candidate109-validation-ticket-outer-wait-closure-design.md`](candidate109-validation-ticket-outer-wait-closure-design.md) | C108のwait-only fallbackを維持し、validation ticketのouter yieldをruntime最大値へ固定するCandidate109設計 |
| [`candidate110-validation-ticket-decision-boundary-design.md`](candidate110-validation-ticket-decision-boundary-design.md) | C108の実行票途中状態を既存DECISION_BOUNDARYの外へ置くprompt-only Candidate110設計 |
| [`candidate111-validation-ticket-model-return-boundary-design.md`](candidate111-validation-ticket-model-return-boundary-design.md) | 判断価値のない途中状態をmodelへ返す必要性を発行時点で否定するprompt-only Candidate111設計 |
| [`candidate112-evidence-admission-scheduling-boundary-design.md`](candidate112-evidence-admission-scheduling-boundary-design.md) | evidence identityのadmissionと、許可済みで独立したinvocationの発行順序を分離するprompt-only Candidate112設計 |
| [`candidate113-explicit-authority-delegation-design.md`](candidate113-explicit-authority-delegation-design.md) | requested outcome valueのauthority探索をTaskSpecの明示委譲だけで開くprompt-only Candidate113設計 |
| [`candidate114-spec-ready-evidence-phase-boundary-design.md`](candidate114-spec-ready-evidence-phase-boundary-design.md) | `spec_ready`で仕様確定evidenceとtarget evidenceを分けるCandidate114設計 |
| [`candidate115-authority-location-discovery-design.md`](candidate115-authority-location-discovery-design.md) | authority path未記載による誤停止を対象にしたCandidate115設計 |
| [`candidate116-outcome-implementation-boundary-design.md`](candidate116-outcome-implementation-boundary-design.md) | required outcome確定とimplementation choice解決を分離するCandidate116設計 |
| [`prompt-set-result-registry-additional-requirements.md`](prompt-set-result-registry-additional-requirements.md) | result台帳の追加要件記録。status `implemented_as_evaluation_foundation_v3`。具体設計の正本は`prompt-comparison-workflow.md`と`evaluation-loop-manual.md` |
| [`candidate118-residual-validation-reentry-analysis.md`](candidate118-residual-validation-reentry-analysis.md) | C118の残存トークン増加を、追加したbind closureではなく変更後validationのnonterminal返却とmodel再入で説明した診断 |
| [`candidate121-f02-evidence-route-analysis.md`](candidate121-f02-evidence-route-analysis.md) | C121のF02のコスト未達をevidence bytesだけでは説明できないと示し、locator→content spanの二段階routeを共通差として分離した診断 |
| [`candidate122-preterminal-result-round-analysis.md`](candidate122-preterminal-result-round-analysis.md) | トークンの高低を分けた共通差がinvocation数ではなく、変更・停止までにtool resultをmodelへ返したround数だと特定した診断 |
| [`candidate125-adoption-decision.md`](candidate125-adoption-decision.md) | C125の採用判断。評価状態、release、approval、projectionを分離して記録 |
| [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md) | C125 Standard14 N=5を通常input / cached input / cache write / outputへ分解し、公開API単価で課金換算した比較 |
| [`candidate125-candidate132-six-point-control-synthesis.md`](candidate125-candidate132-six-point-control-synthesis.md) | C125〜C132の六点の制御を統合し、六点を同時に解くglobal predicateは作らないと結論した記録 |
| [`candidate131-point4-dependency-audit.md`](candidate131-point4-dependency-audit.md) | Point 4 dependencyを独立predicateへ固定しないと判断した監査 |
| [`candidate131-point6-closure-recovery-audit.md`](candidate131-point6-closure-recovery-audit.md) | Point 6 closure / recoveryに新Candidateを作らないと判断した監査 |
| [`candidate133-task-spec-lexeme-authority-audit.md`](candidate133-task-spec-lexeme-authority-audit.md) | anchorを意味判断で選ばず、TaskSpec原文のcode-shaped lexemeを構文規則で全件抽出する次軸を固定した監査 |
| [`candidate134-reference-symbol-coverage-ownership-audit.md`](candidate134-reference-symbol-coverage-ownership-audit.md) | C134の低ScoreをPoint 2 evidence coverage不足へ帰属させ、request identity失敗とcoverage closure失敗の同時修正を禁じた監査 |
| [`candidate135-effect-local-change-admission-audit.md`](candidate135-effect-local-change-admission-audit.md) | 充足済み`colSpan` effectを再び変更対象へ入れ必要変更と同一のパッチへ結合したことをScore 2の直接原因とした監査 |
| [`candidate136-criterion-lexeme-member-totality-audit.md`](candidate136-criterion-lexeme-member-totality-audit.md) | C136 Score 3の原因を入力範囲ではなくlexeme member抽出規則の退行と特定した監査 |
| [`candidate137-existing-case-observer-coverage-audit.md`](candidate137-existing-case-observer-coverage-audit.md) | `pending_effect_validation_admitted`を既存ケースで確実に発生させる方法はないと判定し、F04維持と停止条件を固定した監査 |
| [`candidate139-effect-satisfaction-witness-audit.md`](candidate139-effect-satisfaction-witness-audit.md) | F02部分変更の一次原因を`satisfied`の誤bindとし、次軸`effect_satisfaction_witness`を導出した監査 |
| [`candidate140-evidence-completeness-granularity-audit.md`](candidate140-evidence-completeness-granularity-audit.md) | F02低Scoreを分けた差がwitness定義ではなく変更前evidenceの粒度だと示した監査 |
| [`candidate141-post-result-change-admission-audit.md`](candidate141-post-result-change-admission-audit.md) | 残存失敗を、変更前request準備完了とresult受領後の変更開始準備完了が未分離であることへ帰属させた監査 |
| [`candidate145-f01-f02-f03-cost-causal-analysis.md`](candidate145-f01-f02-f03-cost-causal-analysis.md) | C145のコスト増加の先行分析を誤りと訂正し、`command_execution`件数とmodel step数の混同を明示した再集計 |
| [`candidate146-model-step-boundary-audit.md`](candidate146-model-step-boundary-audit.md) | `agent_message`をmodel step境界としてC125 / C145 / C146を再集計し、C146の増分機構なしと判定した監査 |
| [`candidate147-adoption-decision.md`](candidate147-adoption-decision.md) | C147の採用判断。品質・安定性・機構・コスト回収を別々に確認し、公開版`the-caption`へ投影した記録 |
| [`candidate81-candidate125-control-findings-synthesis.md`](candidate81-candidate125-control-findings-synthesis.md) | C81〜C125で有効だった制御の統合知見。抽象的注意ではなく実行時に観測できる条件へ閉じることが要点 |
| [`click-runtime-reproducibility.md`](click-runtime-reproducibility.md) | Click評価用known-goodランタイムを空環境から再構築し、offline full gateまで一致を確認した記録 |
| [`click-control-free-medium-baseline-analysis.md`](click-control-free-medium-baseline-analysis.md) | Click Control-free baselineがTHE-CAPTIONより軽い主因をリポジトリ / ケースのcontext量差として分離した分析 |
| [`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md) | Click C81 Mediumの残余経路をpaired差で再評価し、F01の悪化は非再現、F04 elapsed増加は再現性ありと判定した分析 |
| [`click-c81-full-portability-design.md`](click-c81-full-portability-design.md) | THE-CAPTION C81全文をClick root 1 targetへ改変なく水平適用する比較設計（外部妥当性の検証） |
| [`click-c125-full-portability-design.md`](click-c125-full-portability-design.md) | 同様にC125全文をClickへ水平適用し、Click Standard14 r2を各case`N=5`で実施する設計 |
| [`click-c81-repository-authority-standard14-r2-design.md`](click-c81-repository-authority-standard14-r2-design.md) | C81全文のみと、C81全文＋Click repository authorityを`click-standard14-r2`で比較する設計 |
| [`click-repository-authority-availability-design.md`](click-repository-authority-availability-design.md) | repository authorityの可用性差を、THE-CAPTIONで差が出たF10と同じ観点でClickへ移す比較設計 |
| [`click-repository-subagents-comparison-design.md`](click-repository-subagents-comparison-design.md) | Clickの階層別repository instructionの影響を、root制御プロンプトと分離して確認する比較設計 |
| [`delegation-cost-control-redesign.md`](delegation-cost-control-redesign.md) | ワーカー起動自体を失敗条件にせず、実行全体を3 KPIで判定するコスト判定・制御の再設計 |
| [`planning-first-route-diagnostic.md`](planning-first-route-diagnostic.md) | planning-first経路のrun別補助記録。ワーカー数の採点ではなくKPI差の説明に使う |
| [`sealed-execution-wave-design.md`](sealed-execution-wave-design.md) | 中間resultをmodelへ配送しないexecutor境界の第1版設計（`sealed_execution_wave.py`） |
| [`success-silent-delivery-design.md`](success-silent-delivery-design.md) | deterministicな成功resultだけをmodelへ配送しない`success-delivery/v1`第1版設計 |
| [`pytest-allowlist-success-delivery-design.md`](pytest-allowlist-success-delivery-design.md) | 成功出力の大半を占めるpytest系だけをexact argv boundなwrapper対象とする`success-delivery/v2`設計 |

## 8. historical handoff／superseded interpretation

内容は当時の記録として保持する。現行設計・現行値として読まない。各文書の冒頭バナーが位置づけを示す。

| 文書 | 位置づけ |
|---|---|
| [`candidate5-token-efficiency-direction.md`](candidate5-token-efficiency-direction.md) | root-only token由来の旧解釈。現行値はall-agent再集計へ置換済み |
| [`candidate6-candidate8-efficiency-investigation.md`](candidate6-candidate8-efficiency-investigation.md) | root-only token由来の調査履歴。現行値はall-agent再集計を参照 |
| [`candidate71-spec-audit-handoff.md`](candidate71-spec-audit-handoff.md) | C71 `SPEC`監査の完了済みhandoff。監査結果は`candidate71-control-abstraction-analysis.md`へ統合済み |
| [`prompt-control-review-handoff.md`](prompt-control-review-handoff.md) | C35〜C40時点の制御見直しの引き継ぎ記録。当時のbranch・HEAD・未commit差分を含む |
| [`sa-routing-condition-extraction.md`](sa-routing-condition-extraction.md) | candidate2設計の出発点となった`design_input`。その後の系譜は大きく進行 |
| [`prechange-information-sealed-repair-contract-spec.md`](prechange-information-sealed-repair-contract-spec.md) | 修正の要否と修正後条件を変更前レビューで決める旧仕様。C167〜C169の不通過を経て破棄し、現行設計へ継承しない |
| [`prechange-information-sealed-repair-contract-design-audit.md`](prechange-information-sealed-repair-contract-design-audit.md) | 破棄済み旧修正契約仕様に対する当時の設計監査 |
| [`prechange-information-sealed-repair-contract-targeted-evaluation-design.md`](prechange-information-sealed-repair-contract-targeted-evaluation-design.md) | 破棄済み旧修正契約系列のtargeted評価設計。現行設計の試験へ流用しない |
| [`review-control-reconstruction-responsibility-design.md`](review-control-reconstruction-responsibility-design.md) | Candidate192後に`DISPATCH_TRANSITION`を加えた固定M2設計。Candidate193で十分性反例が成立したため、現在設計として使わず末尾の後続注記と再開M1を参照 |
| [`review-control-reconstruction-direction-review.md`](review-control-reconstruction-direction-review.md) | Candidate192後の発行遷移についてblocking counterexample 0件とした固定M3記録。Candidate193で見落としが実測されたため、末尾の訂正と再開M1を参照 |
| [`candidate167-prechange-repair-contract-admission-design.md`](candidate167-prechange-repair-contract-admission-design.md) | 旧修正契約系列の履歴Candidate。targetedはScore `4 / 1 = 21 / 14`で停止 |
| [`candidate168-repair-evidence-burden-design.md`](candidate168-repair-evidence-burden-design.md) | 旧修正契約系列の履歴Candidate。targetedはScore `4 / 1 = 29 / 6`で停止 |
| [`candidate169-repair-decision-evidence-closure-design.md`](candidate169-repair-decision-evidence-closure-design.md) | 旧修正契約系列の履歴Candidate。targetedはScore `4 / 1 = 30 / 5`で停止 |
