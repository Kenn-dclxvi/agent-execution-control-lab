# Candidate開発の経緯（系譜と知見）

Baselineから各Candidateまでの系譜と、固定した変更単位・保存evidence・評価状態をまとめる。効率改善メカニズムのテーマ別整理は[control-mechanisms.md](control-mechanisms.md)、全体像は[README](../README.md)を参照。

## BaselineからCandidate5までの成果

固定したBaselineの役割別surfaceと一律の実装後確認を起点に、1つのcandidateで1つの制御境界を扱い、保存した観測を次の変更理由へ接続した。Candidate5の直接の系譜は`Baseline → Candidate2 → Candidate3 → Candidate4 → Candidate5`である。Candidate1はBaselineから直接派生したcompact構造の比較枝であり、Candidate5の親ではない。

| prompt set | 由来 | 固定した変更単位 |
| --- | --- | --- |
| Baseline | `the-caption-3ce91a4-current-r2` | 19 pathの比較元。専用実装SAへの委任と、実装後のAudit / Reviewを既定とする |
| Candidate1 | Baselineの直接child（比較枝） | rootを単一execution authorityへ統合し、JIT Context、ordered gate、変更class別completion、conditional Audit / Review、bounded rework、single terminalを同じ契約へまとめる |
| Candidate2 | Baselineの直接child（Candidate5本流） | 実装SA、permission、required validation、rework境界を維持したまま、riskとmachine coverageから`none` / `audit` / `review` / `audit+review`を選ぶ |
| Candidate3 | Candidate2の直接child | validationにtestを使うだけのtaskをtest変更とみなさないよう、test contract riskとchange classの導出境界を限定する |
| Candidate4 | Candidate3の直接child | 専用実装SAへの必須委任を外し、親直接、SA委任、分担の選択をモデル判断へ戻す |
| Candidate5 | Candidate4の直接child | 実行開始後は、完了条件または明示済み停止条件が観測事実として成立するまで継続する一般的な完了志向を加える |

この積み上げにより、Baselineの固定的な多段実行から、安全境界を維持しながら、実装主体、独立確認、停止をtaskと観測事実に応じて選択するprompt setまでを、immutableなfull bundleとして分離して構築できた。identity、変更target、構築時provenanceは[`prompts/candidates/README.md`](../prompts/candidates/README.md)と各manifestに記録している。

expanded 12 case、`N=5`、global queue `M=24`の互換条件で保存した現行all-agent再集計値は次のとおりである。`total_tokens`は12 caseのiteration合計の中央値、`elapsed_seconds`も各iterationで12 caseを合計した値の中央値である。

| prompt set | `quality_score` | all-agent `total_tokens` | `elapsed_seconds` |
| --- | ---: | ---: | ---: |
| Baseline | 100.000 | 8,925,798 | 2,828.032 |
| Candidate1 | 97.917 | 5,732,480 | 1,932.971 |
| Candidate2 | 100.000 | 7,381,355 | 2,477.185 |
| Candidate3 | 100.000 | 6,240,246 | 2,465.865 |
| Candidate4 | 100.000 | 5,909,205 | 1,676.820 |
| Candidate5 | 100.000 | 5,740,441 | 1,714.914 |

Candidate5とBaselineの数値差は、`quality_score`が`0.000`、`total_tokens`が`-3,185,357`、`elapsed_seconds`が`-1,113.118`だった。qualityの内訳では、Baselineがscore 4を58 run、score 3を2 run、Candidate4がscore 4を57 run、score 3を1 run、score 1を2 run記録したのに対し、Candidate5は60 runすべてscore 4だった。Candidate5の40 implementation runはすべて親直接を選び、選択した独立Audit / Review workerはすべて実際に起動された。

数値の正本は[`v3 all-agent token再集計`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)、Candidate5の一次evidenceとrouting観測は[`Candidate5 N=5 result`](../evaluations/results/candidate5-expanded12-global-m24-n5_2026-07-16.md)に置く。この結果は12 case、`N=5`の観測であり、採点は独立blind raterによるものではない。Candidate5は`observed_n5`だが、採用、release化、THE-CAPTION本体への反映、runtime有効化は未判断、未実施である。

## Candidate6からCandidate22までの成果

Candidate5以降は、C5の完了志向を維持してcontext効率化を調べる系列と、C1のcompact構造を維持してTaskSpec、worker、role、validationの接続境界を収束させる系列に分けた。現存する直接の系譜は`C5 → C6`、`C5 → C7 → C8`、`C1 → C9`、`C1 → C10 → C11 → C12 → C13 → C14 → C15 → C16 → C17 → C20 → C21 → C22`であり、candidate番号の順番をそのまま単一の親子関係として扱わない。

| prompt set | 由来 | 固定した変更単位 |
| --- | --- | --- |
| Candidate6 | Candidate5の直接child | 正本のJIT節参照、SA packet最小化、最終結果の再掲抑制を追加する |
| Candidate7 | Candidate5の直接child | required commandの完全evidence保存と、次工程へ渡すmodel-visible outputを分離する |
| Candidate8 | Candidate7の直接child | command単位のprojectionを工程間result全体へ一般化する |
| Candidate9 | Candidate1の直接child（診断枝） | invariant、TaskSpec明示値、change-class defaultの優先順位を解決し、解決済み契約をworkerへbindする |
| Candidate10 | Candidate1の直接child（C15本流） | machine reworkとenvironment recoveryのcounter domainを、責務が適用対象の場合だけ評価する |
| Candidate11 | Candidate10の直接child | workerのcontext継承を、担当criterionに必要十分な最小範囲へ収束させる |
| Candidate12 | Candidate11の直接child | TaskSpecのcriterion / ownerとrequired non-machine workerを必要十分な一対一対応へ収束させる |
| Candidate13 | Candidate12の直接child | review-onlyとaudit+reviewで異なる起動前提をreview role promptへ接続する |
| Candidate14 | Candidate13の直接child | TaskSpecが明示したrequired machine commandを変更class別defaultより優先する |
| Candidate15 | Candidate14の直接child | manifest-boundなselected roleのcontrol inputと、TaskSpecが制限するrepository evidence readを分離する |
| Candidate16 | Candidate15の直接child | bind済みevidenceだけがgate statusを変更できる原則へ既存記述を再編する |
| Candidate17 | Candidate16の直接child | constraint / terminalもoperation identityごとに限定する |
| Candidate20 | Candidate17の直接child | criterion ownerとproducer execution identityが一致するresultだけをevidenceとする |
| Candidate21 | Candidate20の直接child | owner固定criterionを全routeのrequired worker起動とcompleted resultへ接続する |
| Candidate22 | Candidate21の直接child | worker成立をruntimeが返すchild execution identity、そのidentityへのwait、child final resultへ限定する |

C6〜8では、prompt上のcontext参照や投影formatを狭めるだけでは、C5の品質特性を維持しながらall-agent tokenを減らす根拠にならないことを確認した。C9ではTaskSpecとdefaultの優先順位を導入した一方、適用外counterの解釈が分岐したため、その境界だけをC1へ加えたC10を別の直接childとして構築した。C10〜15は各観測で残ったcontext継承、worker cardinality、role起動条件、validation authority、control inputの境界を原則1 targetずつ接続した。C16 / C17はC15連続試験のF04 / F10低scoreを入口に、operation identityとevidenceの既存記述を再編したtargeted diagnostic系列である。C18 / C19は明示的に合意された候補ではなく、実施指示を広く解釈して診断中に追加された効果のない派生案だったため、経緯と観測値だけを履歴recordへ残してcandidate artifactを破棄した。C20は番号を再利用せずC17から直接派生し、criterion ownerをevidenceのproducer identity条件へ接続する。C21 / C22はC20連続試験のscore `3`原因に対し、required owner resultと実child lifecycleを順に接続する。

expanded 12 case、`N=5`、global queue `M=24`で保存したall-agent値は次のとおりである。C6、C10〜12、C14、C15、C17はBaseline、C1、C5と同じ互換条件のresultである。C9は同じ実行条件で12 caseを完了したが、先行2 caseと残り10 caseを異なるEvaluation set capsuleへ固定したstaged campaignであり、strict compatibilityの同一comparisonへ混ぜない。C7、C8はF02 `N=1`の診断、C13はF03 / F04各`N=3`のtargeted checkまでである。

| prompt set | 評価状態 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | score 4 / 3 / 1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate6 | `observed_n5` | 100.000 | 5,951,457 | 1,715.486 | 58 / 1 / 1 |
| Candidate7 | `observed_f02_n1` | — | — | — | — |
| Candidate8 | `observed_f02_n1` | — | — | — | — |
| Candidate9 | `observed_n5`（staged campaign） | 93.750 | 8,331,893 | 2,353.169 | 53 / 2 / 5 |
| Candidate10 | `construction_complete / observed_n5` | 100.000 | 6,798,932 | 2,359.190 | 60 / 0 / 0 |
| Candidate11 | `observed_n5` | 100.000 | 5,726,760 | 2,301.432 | 60 / 0 / 0 |
| Candidate12 | `observed_n5` | 97.917 | 4,757,900 | 1,777.127 | 57 / 3 / 0 |
| Candidate13 | `construction_complete / observed_targeted` | — | — | — | — |
| Candidate14 | `observed_n5` | 100.000 | 4,648,809 | 1,753.159 | 59 / 1 / 0 |
| Candidate15 | `observed_n5` | 100.000 | 4,590,751 | 1,723.986 | 60 / 0 / 0 |
| Candidate17 | `observed_n5` | 100.000 | 4,422,933 | 1,388.239 | 60 / 0 / 0 |

Candidate15とBaselineの中央値差は、`quality_score`が`0.000`、`total_tokens`が`-4,335,047`、`elapsed_seconds`が`-1,104.046`だった。Candidate5との差は順に`0.000`、`-1,149,690`、`+9.072`秒、Candidate14との差は`0.000`、`-58,058`、`-29.172`秒だった。Candidate15ではCandidate14のF10 inventory未完了停止は再現せず、60 runすべてscore 4を記録した。

Candidate17とCandidate15は同じcompatibility keyを持つ。Candidate17 - Candidate15の中央値差は、`quality_score`が`0.000`、`total_tokens`が`-167,818`、`elapsed_seconds`が`-335.747`秒だった。Candidate17も60 runすべてscore 4を記録した。

owner-producer証跡をscore `4`の必要条件にする新rating revisionは、旧resultを変更せずC17とC20を新規実行した。この2 resultだけが相互に互換であり、上表の旧rating revisionとは混ぜない。

| prompt set | 評価状態 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | score 4 / 3 / 1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Candidate17 | `observed_n5_owner_producer_v1` | 95.833 | 4,510,093 | 1,635.175 | 49 / 11 / 0 |
| Candidate20 | `observed_n5_owner_producer_v1` | 95.833 | 4,404,154 | 1,613.670 | 49 / 10 / 1 |
| Candidate22 | `observed_n5_owner_producer_v1` | 100.000 | 4,904,017 | 1,746.454 | 58 / 2 / 0 |

C20 - C17の中央値差は`quality_score 0.000`、`total_tokens -105,939`、`elapsed_seconds -21.506`秒だった。F10 monthlyのowner producer resultはC17 / C20とも0 / 5で、C20では1件が開始identity誤認によりreview未実施のscore `1`となった。このN=5ではC20の狙いの挙動は観測できなかった。

C22 - C20の中央値差は`quality_score +4.167`、`total_tokens +499,863`、`elapsed_seconds +132.784`秒だった。C22はscore `4 / 3 = 58 / 2`で、F05 clarification、F05 out-of-scope、F07 dependency provenanceを含む11 caseは各5 / 5でscore `4` eligibleだった。F10 monthlyの2件はreceiver未確定のwait後にrootがchild result受領を自己申告しており、owner producer evidence不足としてscore `3`に残した。

C20の同条件連続試験は登録済み3 batch、180 runで中止した。score `4 / 3 / 1 = 148 / 31 / 1`で、score `3`の31件はすべて所定成果を満たした一方、criterion ownerに対応する別execution identityのproducer resultが成立しなかった。特にF05 clarificationとF10 monthlyが各14 / 15であり、owner evidenceの流用禁止だけでなく、必要なowner workerの起動とresult生成をgate flowへ接続する課題が残った。未登録のbatch 4と未実施batchは集計へ含めない。

C21 / C22の4-case targeted `N=5`では、owner producer eligibleがC21の19 / 20からC22の20 / 20になった。続くC22 expanded 12-case `N=5`は60 valid runをappend-onlyで登録し、C20とのcomparison viewを生成した。targeted resultとexpanded resultを混ぜず、Step 5の連続試験は実施していない。

系譜と評価状態の正本は[`prompts/candidates/README.md`](../prompts/candidates/README.md)、C6〜8の調査境界は[`Candidate6からCandidate8までの効率化調査`](candidate6-candidate8-efficiency-investigation.md)、C13 / C14の部分確認は[`targeted checks`](../evaluations/results/candidate13-candidate14-targeted-checks_2026-07-16.md)、C15までの互換比較は[`Baseline / Candidate5 / Candidate14 / Candidate15 comparison view`](../evaluations/results/baseline-candidate5-candidate14-candidate15-expanded12-global-m24-n5_2026-07-16.md)、C16 / C17の原則化とC18 / C19破棄の経緯は[`evidence boundary targeted checks`](../evaluations/results/candidate16-candidate19-evidence-boundary-targeted_2026-07-17.md)に置く。C17の旧rating同条件expanded `N=5`は[`C17 expanded result`](../evaluations/results/candidate17-operation-qualified-evidence-expanded12-global-m24-n5_2026-07-17.md)、新ratingのC17 / C20比較は[`owner-producer v1 result`](../evaluations/results/candidate17-candidate20-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)、C20の登録済み3 batchは[`continuous B=3 result`](../evaluations/results/candidate20-owner-producer-v1-continuous-n5-b3_2026-07-17.md)、C21 / C22の部分確認は[`owner worker targeted check`](../evaluations/results/candidate21-candidate22-owner-worker-targeted_2026-07-17.md)、C20 / C22比較は[`owner worker lifecycle expanded result`](../evaluations/results/candidate20-candidate22-owner-worker-lifecycle-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ保存した。adapter-levelの別条件診断は[`typed boundary evidence`](typed-boundary-evidence.md)と[`F10 N=90 result`](../evaluations/results/candidate17-typed-boundary-evidence-f10-n90_2026-07-17.md)へ明示的に分離する。これらは記載したcaseと反復条件の観測であり、採点は独立blind raterによるものではない。現存candidateはいずれも採用、release化、THE-CAPTION本体への反映、runtime有効化を行っていない。

ControlFreeRepository直接派生のCandidate23は[`expanded 12-case N=5 result`](../evaluations/results/control-free-repository-candidate23-operation-boundary-expanded12-global-m24-n5_2026-07-17.md)へ登録し、60 / 60がscore `4`だった。F04のcleanup停止は5回中0件だが、ControlFreeRepositoryで観測した低頻度停止の解消までは一般化していない。

Candidate23へprompt-onlyのowner result AND predicateを追加したCandidate24は[`owner-producer expanded 12-case N=5 result`](../evaluations/results/candidate22-candidate24-control-free-owner-result-gate-owner-producer-v1-expanded12-global-m24-n5_2026-07-17.md)へ登録し、60 / 60がscore `4`、owner-producer eligible 60 / 60だった。F10 monthlyは5 / 5で実child resultが成立したが、prompt-only制御の完全保証や範囲外への一般化はしていない。

同条件の[`Candidate24 continuous N=5 B=5`](../evaluations/results/candidate24-owner-result-gate-owner-producer-v1-continuous-n5-b5_2026-07-17.md)は300 valid runを5つのappend-only resultへ登録した。score `4 / 3 / 1 = 294 / 2 / 4`で、F10 monthlyは実child resultが25 / 25で成立した一方、4件はchildがrootの開始状態を逆に解釈してreview未実施となった。prompt-onlyの次の境界はchild lifecycleではなく、rootとchildがcriterion判定に使うmachine state値の一致である。

F10の一つの失敗形だけを避けるroute固有案C25〜C27は公開候補にせず破棄した。Candidate28はCandidate24を直接sourceとし、各operation identityのproducerをpredicate実行前に一つへbindする。独立確認が必要な場合は同じpredicateの再実行ではなく、先行result / artifactを入力とする別predicateの別operationへ分ける。この変更はroute、role、artifact種別に依存しない。rootだけを見ていた旧ratingの採点不能は、同じrunのrecursive descendant commandをbindする[`owner-producer quality v2 N=5`](../evaluations/results/candidate28-single-producer-operation-binding-owner-producer-v2-expanded12-global-m24-n5_2026-07-17.md)へ更新した。60 / 60がrateable、score `4 / 3 = 58 / 2`で、残る2件はF03 / F07のindependent owner producer resultが成立しなかった。旧v1 runは履歴として変更していない。

Candidate29はCandidate28を直接sourceとし、criterion ownerの語列をoperationとproducer role identityへ保持する。owner型5 caseのtargeted `N=5`は25 / 25がscore `4`だった。expanded 12-case `N=5`ではF03とF07 dependencyのowner証跡が各5 / 5で成立し、C28のowner名不一致は再現しなかった。一方、全体ではowner-producer eligible 59 / 60、rateable 55 / 60だったため、expanded resultは未登録である。[staged result](../evaluations/results/candidate29-owner-role-identity-binding-staged_2026-07-17.md)の停止条件に従い、continuous試験、採用、release判断へ進めていない。

Candidate30はCandidate29を直接sourceとし、Owner結果受領を実runtimeのspawn `task_name`、`FINAL_ANSWER.Sender`、criterion bindingへ限定する。targeted 25 / 25、expanded 60 / 60、continuous 300 / 300でOwner証跡の不成立は0件だった。continuousのscore `4 / 3 = 293 / 7`であり、score `3`はすべてrequired command成功証跡不足だった。F10 monthlyの開始条件修正はcase `r3`、valid runを未採点にしない変更はrating v3としてprompt変更と分離した。[result](../evaluations/results/candidate30-runtime-owner-result-binding-owner-producer-v3-continuous-n5-b5_2026-07-17.md)は試験完了だけを示し、採用、release、THE-CAPTION本体反映は未判断である。

## Candidate17からCandidate34までの要約

Candidate17以降は、operation単位のevidence境界を起点に、owner resultの実行identity、child lifecycle、単一producer、terminal closureを順に接続した。その後、制御意味を維持したprompt縮約、worker context継承の最小化、owner result状態の分離を行った。

Candidate17からCandidate34までは単一の親子系譜ではない。owner evidenceを既存compact promptへ接続した系列は`C17 → C20 → C21 → C22`である。root制御なしの対照から必要な制御だけを積み上げた系列は`ControlFreeRepository → C23 → C24 → C28 → C29 → C30 → C31 → C32 → C33 → C34`である。C22とC24は同じ試験で比較したが親子ではない。C18 / C19とC25〜C27は診断中の不採用案であり、現行candidate chainへ含めない。

| prompt set | 直接source | 追加または変更した制御境界 | 主な保存evidence |
| --- | --- | --- | --- |
| Candidate17 | Candidate16 | `constraint / terminal`をoperation identity内へ限定 | 旧rating expanded 60 / 60 score `4`。owner-producer rating v5ではscore `4 / 3 / 1 = 49 / 10 / 1` |
| Candidate20 | Candidate17 | criterion ownerとproducer execution identityが一致するresultだけをevidence化 | continuous B=3のscore `3` 31件から、owner worker起動とresult生成の未接続を特定 |
| Candidate21 | Candidate20 | owner固定criterionをrequired worker起動とcompleted resultへ接続 | 4-case targetedでowner-producer eligible 19 / 20 |
| Candidate22 | Candidate21 | producer成立をruntime child identity、wait、child final resultへ限定 | targeted 20 / 20 eligible。expanded score `4 / 3 = 58 / 2` |
| Candidate23 | ControlFreeRepository | operation-scoped constraint / terminal、手段選択、recovery counterだけを復元 | expanded 60 / 60 score `4` |
| Candidate24 | Candidate23 | owner resultをchild identity、completed wait、final result、criterion bindingのAND predicateへ固定 | expanded 60 / 60 score `4`。continuous B=5はscore `4 / 3 / 1 = 294 / 2 / 4` |
| Candidate28 | Candidate24 | operationごとにproducerを一つだけbindし、独立確認を別operation化 | rating v2 expanded score `4 / 3 = 58 / 2` |
| Candidate29 | Candidate28 | criterion owner語列を短縮・言換えずproducer role identityへ保持 | owner型targeted 25 / 25 score `4`。expandedは停止条件により未登録 |
| Candidate30 | Candidate29 | Owner result受領をspawn `task_name`、`FINAL_ANSWER.Sender`、criterion bindingへ接続 | targeted 25 / 25、expanded 60 / 60、continuous 300 / 300でOwner証跡成立 |
| Candidate31 | Candidate30 | 全predicateのbind済みproducer terminal resultが揃うまでoperationをnonterminalに保持 | rating v5 expanded 60 / 60 score `4` |
| Candidate32 | Candidate31 | rootの見出し、説明、重複表現を8つの制御規則へ縮約 | root promptは32.6%縮約したが、C31比token中央値は`+6.45%`。score `4 / 2 / 1 = 58 / 1 / 1` |
| Candidate33 | Candidate32 | worker packetが十分なら`fork_turns=none`、不足時も必要最小turnだけ継承 | C32比token中央値`-24.63%`、quality中央値`-6.250`。score `4 / 3 / 1 = 56 / 1 / 3` |
| Candidate34 | Candidate33 | owner result未取得とbind済みcriterionの`false / failed`を分離し、別operationへの失効伝播を禁止 | targeted 10 / 10 score `4`。現行rating v7 expanded 60 / 60 score `4` |

Candidate32ではprompt表面の縮約だけではtoken削減を確認できなかった。Candidate33ではworker継承contextを削減し、C32比でall-agent token中央値が`-959,484`となったが、quality中央値も`-6.250`となった。Candidate34はC33で欠けたF05 out-of-scopeとF10 inventoryの必須responseをtargetedとexpandedの合計20 / 20で成立させ、owner result未取得とcriterionの`false / failed`を別状態へ戻した。

Candidate34のv5 expandedで残ったF05 clarifyのscore `1` 2件は、日本語の「フォールバック」を英字`fallback`と同義に扱わないrating偽陰性だった。rating v6でsemantic markerを修正した。v6で残ったCandidate34 F07 dependencyのscore `3` 1件は、markdown-heading形式の成功commandをcollectorがbindできない別の偽陰性だった。command evidence v4とrating v7でこの形式を修正し、保存済みv5 / v6 resultは再採点せず履歴として保持した。

現行のC31 / C34比較は、同じrating v7、expanded 12 case、`N=5`、global queue `M=24`で新規実行したresultである。

| KPI中央値 | Candidate31 | Candidate34 | Candidate34 - Candidate31 |
| --- | ---: | ---: | ---: |
| `quality_score` | 100.000 | 100.000 | 0.000 |
| all-agent `total_tokens` | 3,916,601 | 3,290,615 | -625,986（-15.98%） |
| `elapsed_seconds` | 1,485.419 | 1,467.115 | -18.304（-1.23%） |

両setとも60 / 60がscore `4`で、retryとexcluded attemptは0件だった。Candidate34のtoken合計は5 / 5反復、12 case中10 caseでCandidate31より小さかった。elapsedは反復別でCandidate34が小さい回が1 / 5のため、安定した短縮とは判断しない。

C31とC34の19 target中18 targetは同一で、prompt差分はroot `AGENTS.md`だけである。C34はC31の主要制御境界をlabel化し、root promptを`3,785 bytes`から`3,235 bytes`へ`550 bytes`（`14.53%`）縮約したうえで、worker context最小化とowner result状態分離を追加した。静的なprompt縮約だけで実行時token差の因果を証明しない。

Candidate34のrelease bundleは作成時に`prepared_for_decision`、approval `pending`だったが、2026-07-19にCandidate41を唯一のrelease候補としたため、現在は`cancelled`である。C34 continuous B18は未実施である。詳細は[`Candidate31 / Candidate34 rating v7 N=5 comparison`](../evaluations/results/candidate31-candidate34-owner-producer-v7-expanded12-global-m24-n5_2026-07-18.md)と[`Candidate34 release preparation`](../prompts/releases/the-caption-3ce91a4-owner-result-state-separation-release-r1/README.md)を正本とする。

## Candidate35からCandidate41までの要約

Candidate35以降は、C34のroot execution controlを残してlegacy role / process surfaceだけをstub化したC35を共通の起点とした。F05のrequired output省略とF10のfinding location誤差に対する診断枝を作った後、C35 / C38 / C40の制御graphを棚卸しし、criterion owner語列をworker起動条件へ変換しないC41をC35から直接派生させた。

この範囲もcandidate番号順の一本道ではない。直接の系譜は`C34 → C35 → C36 → C37`、`C35 → C38 → C39`、`C38 → C40`、`C35 → C41`である。C36はartifactだけを保持した未評価candidateである。C39は停止条件に従ってexpanded試験へ進めていない。

| prompt set | 直接source | 追加または変更した制御境界 | 主な保存evidence |
| --- | --- | --- | --- |
| Candidate35 | Candidate34 | root execution controlとpath-scoped repository authorityを残し、legacy role / process 7 targetを0-byte stubへ置換 | B18保存evidence 1,080 runのv8診断replayはprojected score `4 / 3 = 1075 / 5`。v9 expandedは60 / 60 score `4` |
| Candidate36 | Candidate35 | 同じproducer final内でbind可能なrequired outputを、別criterion / constraintの`false / failed`から分離してproject | `not_evaluated` |
| Candidate37 | Candidate36 | findingの`path:line`をtarget revisionのline番号付きsourceによる直接確認へbind | v8 expanded 60 / 60 score `4` |
| Candidate38 | Candidate35 | evidenceまたはinvalidation条件が異なるrequired outputを最小result unitへ分割 | v8 targetedはscore `4 / 3 = 9 / 1`。v9 targetedは10 / 10 score `4` |
| Candidate39 | Candidate38 | operation producerをcriterion ownerと同一role identityへ固定 | v8 targetedは成果内容10 / 10、score `4 / 3 = 9 / 1`。expanded未実施 |
| Candidate40 | Candidate38 | result unitをoperation terminal resultのprojectionへ限定し、non-root evidenceをproducer terminal resultへbind | v9 targetedはscore `4 / 1 = 9 / 1` |
| Candidate41 | Candidate35 | owner語列だけではworkerを起動せず、TaskSpecが独立producer executionを明示した場合だけ委譲 | v9 targeted 10 / 10、expanded 60 / 60がscore `4` |

C35 B18の保存済みv7 evidenceに対するv8 replayでは、command evidence収集、許可path判定、F10 finding評価に由来する試験側の誤判定をcandidate側観測から分離した。projected score分布は`4 / 3 / 2 / 1 = 1075 / 5 / 0 / 0`だが、新しい公式resultではなく、元のv7 resultも変更していない。詳細は[`Candidate35 B18 saved-evidence replay`](../evaluations/results/candidate35-owner-producer-v8-saved-evidence-replay_2026-07-18.md)を正本とする。

C38はv9 targetedでC35と同じ10 / 10 score `4`だったが、10 run token合計はC35比`+255,767`だった。差の90.50%はF10に集中し、F10では`exec +8`、`wait +3`、model step `+10`を観測した。C40もF10のtool call、model step、token合計をC38から減らさず、正しいchild findingをowner identity不一致として省略した1 runがscore `1`になった。result unit、evidence、invalidation、projectionを追加したC38 / C40の境界は、狙った実行経路削減をこの試験では示さなかった。

この観測を受け、[`prompt control graph review`](prompt-control-graph-review.md)では、TaskSpecとrepository authorityが既に持つ条件の再定義と、owner語列・runtime identity・result unitを多段照合する判断点を分離した。C41は棚卸しで合意した一つのpredicateだけを実装し、TaskSpecが独立producer executionを明示しないF05 / F10をroot-onlyの最短経路へ戻した。v9 targetedでは10 / 10がscore `4`で、C35比の中央値差は`quality_score 0.000`、`total_tokens -238,617`、`elapsed_seconds -131.504`だった。worker spawnとwaitは0である。

C41 expanded 12-case `N=5`は60 / 60がvalid、rateable、score `4`で、全runがroot-onlyだった。同じv9、evaluation set、target、model、Agent、permission、executor parameter、反復条件へ固定した4-result比較は次のとおりである。

| prompt set | score 4 / 3 | `quality_score`中央値 | all-agent `total_tokens`中央値 | token合計 | `elapsed_seconds`中央値 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 58 / 2 | 100.000 | 10,826,033 | 60,750,594 | 3,705.409 |
| ControlFreeRepository | 59 / 1 | 100.000 | 2,808,523 | 14,877,979 | 1,135.178 |
| Candidate35 | 60 / 0 | 100.000 | 4,565,773 | 22,035,738 | 1,841.107 |
| Candidate41 | 60 / 0 | 100.000 | 2,861,019 | 14,688,469 | 1,172.182 |

C35とC41は12 caseすべてで5 / 5がscore `4`だった。C35のtoken合計はC41より`7,347,269`、`50.02%`多く、case別では11 / 12 caseで多かった。C35の`elapsed_seconds`中央値はC41より`668.926`秒、`57.07%`長かった。ControlFreeRepositoryはC41と近いtoken量だったが、F10 monthly reviewでlocation mismatchが1件あった。N=5の1件対0件から低頻度誤経路の解消を一般化しない。

数値と互換条件の正本は[`Candidate41 targeted N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-targeted2-n5_2026-07-19.md)、[`Candidate41 expanded 12-case N=5`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-expanded12-n5_2026-07-19.md)、[`Candidate41 continuous B18`](../evaluations/results/candidate41-owner-metadata-delegation-boundary-v9-continuous-n5-b18_2026-07-19.md)、[`Baseline / ControlFreeRepository / Candidate35 / Candidate41 comparison`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md)に置く。C41 releaseはTHE-CAPTION PR [#334](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/334)で投影され、merge commit `8409eb9899b92a76870b066d88406754f4365b52`を候補43の巻き戻し先として保持する。C34のrelease候補状態は一旦`cancelled`のまま保持する。これはC34の不採用を意味しない。

## Candidate42からCandidate43までの要約

C41のTaskSpec前段を補う第1段階として、リポジトリから補える不足と、ユーザー確認なしには確定できない変更後の成果値を分離した。直接の系譜は`C41 → C42 → C43`である。両candidateともC41の19 targetを維持し、変更したのはroot `AGENTS.md`の既存`SPEC`だけである。

| prompt set | 直接source | 追加または変更した制御境界 | 主な保存evidence |
| --- | --- | --- | --- |
| Candidate42 | Candidate41 | required outcome、permission、constraintが未固定の間はwrite、test、dependency変更を開始しない`spec_ready`境界を追加 | A01は5 / 5が未固定値を推測してscore `0`。A02は成果を満たしたが旧v9の非公開command要件により5 / 5 score `3`。試験後に停止 |
| Candidate43 | Candidate42 | 変更後の値を直接要求する適用repository規則だけを成果値確定の根拠として認め、それ以外の未固定値は編集・試験前に確認 | v10 A01 / A02は10 / 10 score `4`。標準14項目は70 / 70 score `4`。B18完了後にrelease status `projected`・approval `approved`・runtime projection `projected` |

C42は`spec_ready`を追加したが、A01の5 runすべてで「現在値が`daily`なら変更後は別選択肢の`strict`」と推測して編集と試験へ進んだ。開始可否だけを定めても、値を確定するevidenceの適格性を限定しなければ誤った開始を防げないことを確認し、追加試験へ進めず停止した。A02のscore `3`は、実行役へ提示していない`bash scripts/dev/main_verify.sh`を旧v9 ratingだけが必須にした評価境界の問題である。保存済みresultは変更せず、v10の診断replayではA02を5 / 5 score `4`、A01を5 / 5 score `0`として分離した。

C43は新しいlabelを増やさず、C42の`SPEC`を一つのoutcome authority条件へ置換した。リポジトリから一意に解決できるA02の起動先は質問せず確定する一方、リポジトリが変更後値を直接要求しないA01は推測せず確認して停止する。実行役へ提示する入力を変えないv10 targetedでは、C41がA01の5 / 5でscore `0`、A02の5 / 5でscore `4`だったのに対し、C43は10 / 10がscore `4`だった。

同じv10、標準14項目、各`N=5`の互換条件では、C41のscore分布が`4 / 3 / 0 = 64 / 1 / 5`、C43が`4 = 70`だった。C43は14項目すべてを5 / 5で満たした。C41 / C43の70 run使用量合計は`17,824,901 / 17,732,662`で、差はC41からC43を引いて`+92,239`だった。中央値ではC41が`3,486,800`、C43が`3,647,298`であり、合計と中央値の方向が異なるため、token値だけを採用理由にしていない。

C43の同条件18回継続試験は、標準14項目 × 5反復 × 18 resultの1,260 / 1,260 runをvalid、rateableとして登録・圧縮した。公式score分布は`4 / 3 / 1 = 1,255 / 4 / 1`である。score `3`の4件はF10 monthly reviewの正しい主要findingに対するlocationずれだった。score `1`のA01 1件は、変更と試験を開始せず確認して停止した実responseをratingが質問表現として認識しなかった偽陰性である。1,259 / 1,260 runはroot-onlyで、F04の1件だけが担当情報を独立実行指定と解釈してchildを1件起動した。

C43 releaseは`approved`、release statusとruntime projectionは`projected`である。19 / 19 targetをTHE-CAPTIONへ投影し、C41との差分はroot `AGENTS.md`だけだった。THE-CAPTION PR [#335](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/335)をmerge commit `f729810ba8693acff963ef8e1cc2f2a175197072`として統合し、`bash ./scripts/dev/verify_change_set.sh`は364 testを通過した。投影前のC41 commit `8409eb9899b92a76870b066d88406754f4365b52`は巻き戻し先として保持する。

正本は[`Candidate42 A01 / A02 N=5`](../evaluations/results/candidate42-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)、[`Candidate41 / Candidate43 v10 targeted`](../evaluations/results/candidate41-candidate43-outcome-boundary-v10-targeted2-n5_2026-07-20.md)、[`Candidate41 / Candidate43 standard 14 N=5`](../evaluations/results/candidate41-candidate43-outcome-boundary-v10-standard14-n5_2026-07-20.md)、[`Candidate43 continuous B18`](../evaluations/results/candidate43-outcome-authority-boundary-v10-standard14-continuous-n5-b18_2026-07-20.md)、[`Candidate43 release / projection`](../prompts/releases/the-caption-3ce91a4-outcome-authority-boundary-release-r1/README.md)に置く。F10 locationずれ、A01 rating偽陰性、F04の1 child route、F08追加探索の関与可能性、N=5 / B18範囲外への一般化不能は未解決事項として保持する。計画と実施記録は[`TaskSpec確認 第1段階`](task-spec-planner-phase1-plan.md)に置く。

## Candidate44からCandidate71までの要約

C44以降は、C43の成果値境界を維持したまま、TaskSpec readiness、広域監査のworker topology、root-only経路、prompt圧縮、model再入、validation closureを別々の変更軸で調べた。この範囲も番号順の一本道ではない。主な系譜は`C43 → C44`、`C43 → C45 → C46 → C47 → C48`、`C43 → C49 → C51 → C52`、`C43 → C50 / C53 / C54`、`C54 → C55`からの複数枝、`C43 → C63〜C69`、`C69 → C70 / C71`である。

C44はC43の`SPEC`へ「成果を変える全未固定値を一度の確認へ含める」条件を追加した。[A01 / A02各`N=5`](../evaluations/results/candidate44-complete-spec-readiness-boundary-ambiguity-targeted2-n5_2026-07-20.md)は10 / 10がvalid・rateableだったが、A01で必要な確認事項が揃ったのは2 / 5、A02ではリポジトリから解決できる対象を質問して停止したrunが1 / 5あった。確認範囲を広げてもA01を安定させず、A02の最短正常経路を阻害したためC44は停止した。

C45〜C48は、THE-CAPTION-DEVの広域適合性監査A06をAgent-visible concurrency 31、Memoryなし、`N=1`で診断した枝である。これはblind quality ratingを持たない`diagnostic_only`であり、標準14項目やB18と互換な品質比較ではない。

| prompt set | 直接source | 追加した境界 | 保存traceでの主な観測 | 状態 |
| --- | --- | --- | --- | --- |
| Candidate45 | Candidate43 | 一つのjudgment resultの成立責任を一つのproducer execution identityへ固定 | C43の再検証waveは消えたが、all-agent tokenは`+2.33%`。入れ子探索と個別context再取得が残った | `diagnostic_only / draft` |
| Candidate46 | Candidate45 | 解決済みauthorityをproducer inputへbind | C45比token`-29.13%`。sessionとworkerが増え、durationは`+46.51%`。主要findingの維持を確定できず停止 | `diagnostic_only / draft` |
| Candidate47 | Candidate46 | 新規対象を同じrequired outcomeの適用域へ分類 | C46比token`-12.71%`。Web Editorを主結論へ戻したが、入れ子分割、root再読、nonterminal resultが残った | `diagnostic_only / draft` |
| Candidate48 | Candidate47 | 先行premiseのterminal後だけ下流judgmentを開始 | known finding 6 / 6を報告したが、C47比token`+42.22%`、tool call`+20.57%`。root再読とnonterminal補完が残り停止 | `diagnostic_only / draft` |

C49〜C54は、C43のroot-only正常経路を短くするため、worker制御の圧縮、read batch、root completion、independence、目的別graph、evidence-backed coreを個別に試した。全candidateが対象試験では成果を概ね保持したが、短いpromptや少ないlabelだけでは実行時token、model step、tool callの削減へ一貫して結び付かなかった。

| prompt set | 変更 | 主な保存evidence | 判定 |
| --- | --- | --- | --- |
| Candidate49 | worker制御6 labelを明示委譲時だけの3 labelへ圧縮 | 20 / 20 score `4`。root bytes`-39.12%`だが20 run token合計`+13.21%` | 停止 |
| Candidate50 | 順序依存のないroot readを同一model stepへbatch | F05 / F10 token合計`-40.08%`だが、A01 / A02は`+15.70%`。全20 run合計は`-2.49%` | 探索型A02の拡大により停止 |
| Candidate51 | C49へroot producer bindingと全predicate completionを復元 | 10 / 10 score `4`。F10 model step / tool callは`60 / 55`、token合計`+22.70%` | 停止 |
| Candidate52 | C51へC43の`INDEPENDENCE`一文を復元 | 10 / 10 score `4`。F05`-13.36%`、F10`+6.76%`、全体`+2.01%` | 停止 |
| Candidate53 | A系readiness、F系operation graph、明示委譲を別領域へ再配置 | 10 / 10 score `4`。同じ11-call経路の平均tokenはほぼ同値だが、全体token`+13.02%` | 停止 |
| Candidate54 | 保存traceで必要性を確認できたcontrol coreだけを残す | 10 / 10 score `4`、root bytes`-36.56%`。F10 model step / tool call`+5 / +5`、token合計`+9.44%` | 停止 |

C54以降の圧縮再検討では、[`Candidate43制御要素の目的別分別`](candidate43-control-element-classification.md)を入力とした。C54で欠けた固定済みpredicate・permission・constraintの実行前bindingを復元したCandidate55は、初回F10でmodel step `48 → 38`、tool call `43 → 33`、token合計`-19.31%`を観測したが、route gate r2では短経路が安定しなかった。C56〜C62は固定read methodを常時可視prompt内の条件で隔離できず、A02への流入を止められなかった。そこでCandidate63はC43を唯一の共通全文sourceとし、固定証拠reviewでだけ一行deltaを実行前合成した。[新しいF10-only各`N=5`](../evaluations/results/candidate43-candidate63-fixed-evidence-route-projection-f10-n5_2026-07-22.md)では両promptが5 / 5 score `4`、shell command 55件を維持し、Candidate63は5 / 5で3 tool call、token合計`-52.90%`へ収束した。route gateは通過したが、採用、release、本体反映は未判断である。

C43の32 clauseを4 blockへ再配置し、root / delegatedへF coreを全文重複したCandidate64は、[`catalog固定A01 / A02、F05 / F10、明示producer D01各N=5`](../evaluations/results/candidate43-candidate64-self-contained-execution-paths-catalog-fixed-n5_2026-07-22.md)で25 / 25 score `4`だった。一方、root-only F10はtool call `43 → 54`、model step `48 → 59`、token合計`+28.90%`となった。意味分別は成果を保持したが、全文重複は実行costを抑えなかったためCandidate64は停止した。

Candidate65はCandidate43の32 clauseを重複なしの11 labelへ短文化し、root bytesを`3,980 → 3,701`、`-7.01%`とした。[catalog固定F05 / F10各`N=5`](../evaluations/results/candidate43-candidate65-shared-operation-core-catalog-fixed-f-n5_2026-07-22.md)は10 / 10 score `4`、root-onlyだったが、F10はtool call `43 → 49`、model step `48 → 54`、token合計`+14.25%`となった。事前gateに従いCandidate65は停止し、A / Dへ進めていない。

Candidate66はCandidate43の一層9 label、label順、32 clause所属を維持し、root bytesを`3,980 → 3,923`、`-1.43%`とした。[F10-onlyとcatalog固定A01 / A02、F05 / F10、明示producer D01各`N=5`](../evaluations/results/candidate43-candidate66-topology-preserving-compression-catalog-fixed-n5_2026-07-22.md)はCandidate66の30 / 30がscore `4`だった。最初のF10-only gateはtoken合計`-2.04%`で通過したが、追加F set内のF10はtool call `43 → 57`、model step `48 → 62`、token合計`+31.36%`となった。表面圧縮のruntime効果を再現できなかったためCandidate66は停止した。

Candidate67はCandidate43の9 labelと本文を維持し、明示委譲gateとproducer再割当て禁止の短い重複文2件だけを正本labelへ統合した。root bytesは`3,980 → 3,792`、`-4.72%`である。[標準14項目各`N=5`](../evaluations/results/candidate43-candidate67-cross-label-predicate-deduplication-v10-standard14-n5_2026-07-22.md)はCandidate43とCandidate67の両方が70 / 70 score `4`だった。Candidate67からCandidate43を引いた3 KPI中央値差はquality `0.000`、all-agent token `-2.33%`、elapsed `-0.69%`である。一方、70件token合計は`+0.28%`で、反復ごとの方向も揃わない。状態は`standard14_evaluated`とし、採用、release、本体反映は未判断である。

Candidate68はCandidate43の9 labelと残りの本文を維持し、`INDEPENDENCE`からF9一文だけを削除した。root bytesは`3,980 → 3,860`、`-3.02%`である。[F10-only `N=5`](../evaluations/results/candidate43-candidate68-independent-review-operation-removal-f10-n5_2026-07-22.md)は5 / 5 score `4`、root-only、zero driftだった。3 KPI中央値はquality同値、all-agent token `+1.16%`、elapsed `+26.04%`で、token合計も`+426`となった。事前gateに従いCandidate68は停止した。

Candidate69はprompt自体のtoken数ではなくC43実runのall-agent `total_tokens`を対象とし、未発行invocationの選択を変えないresult間でmodelへ戻らない`DECISION_BOUNDARY`一文を追加した。[標準14項目各`N=5`](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-n5_2026-07-22.md)では、3 KPI中央値差がquality `0.000`、all-agent token `-26.21%`、elapsed `-18.37%`、70件token合計が`-22.59%`、top-level tool callが`-26.60%`だった。一方、F10 monthlyのfinding location mismatchが1件あり、点数分布は`4 / 3 = 69 / 1`だった。[同条件B18](../evaluations/results/candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)は1,260 / 1,260件を登録・圧縮し、C43比で18結果token中央値`-11.08%`、token合計`-13.00%`、top-level tool call `-15.29%`を観測したが、elapsed中央値は`+4.12%`だった。事前gateに従いCandidate69は`standard14_evaluated / stopped`とした。

Candidate70はCandidate69へ`MACHINE_BOUNDARY`を追加し、bind済みmachine resultだけで後続commandまたはstopが一意な区間をさらに明示した。[標準14項目B18](../evaluations/results/candidate69-candidate70-machine-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)は1,260 / 1,260件がvalid・rateableで、Candidate69比のtoken合計`-16.52%`、18結果token中央値`-18.64%`、elapsed合計`-9.16%`、tool call`-19.41%`だった。一方、shell commandは`+3.04%`で、意味確認後もA02 required validation欠落2件とF10 locationずれ2件が残った。品質、不要command、worker routingのgateを通過せず、Candidate70は`standard14_evaluated / stopped`とした。

Candidate71はCandidate70を継承せず、Candidate69へ`VALIDATION_CLOSURE`一labelだけを追加した。artifact変更後の完全なrequired-validation集合を同一waveで発行し、全result受領後に一度だけ判断し、成功後の根拠なき追加readを止める境界である。[第12版標準14項目B18](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)はCandidate69 / Candidate71とも1,260 / 1,260件がvalid・rateableだった。Candidate71は18 / 18 Batchでtoken中央値とelapsed中央値が小さく、Candidate69比のtoken合計は`-27.93%`、elapsed合計は`-11.71%`、top-level tool callは`-30.16%`だった。

一方、Candidate71の公式score分布は`4 / 3 / 0 = 1,255 / 4 / 1`だった。意味確認後もA02の`git diff --check`欠落3件と、A01で未固定modeを確認せず実装・試験へ進んだ1件が残り、Candidate69より実質的な低得点が3件多かった。このため評価上は`standard14_b18_evaluated / stopped`であり、事前の品質gateは不通過のままである。

評価停止とは別に、2026-07-23の明示判断でCandidate71 releaseを`approved`とし、THE-CAPTIONへ`projected`にした。変更対象はroot `AGENTS.md`だけである。THE-CAPTION PR [#340](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/340)を統合commit `326fdd343a50522629592d67b0f028fb66e94eb3`としてmergeし、`bash ./scripts/dev/verify_change_set.sh`は`362 passed / 3 skipped`だった。品質gate不通過と未解決riskは取り消していない。評価・承認・本体反映の現在状態は[`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)を正本とする。

## Candidate72からCandidate103までの要約

C71の`VALIDATION_CLOSURE`以降は、closureの短縮表現、flat 11 labelの型付き状態機械への再編、独立validationのfast-path、potential mutator後のfinal-state wave、例外trigger限定適用、project indexへの条件付き導線、複数required commandの発行単位安定化、明示producer gateの重複削除、Worker価値による委譲判断、planning-first producer選択、producer内部のinvocation batching、Worker admission、tool output ingress、operation criterion totality、required judgment owner boundaryを別々の軸で調べた。この範囲も番号順の一本道ではない。主な系譜は`C71 → C72`、`C71 → C73`、`C71 → C74 → C75 → C76`、`C71 → C77`、`C71 → C78`、`C71 → C79`、`C71 → C80`、`C71 → C81 → C82 → C83 → C84`、`C81 → C85`、`C81 → C86 → C87 → C88`、`C87 → C89`、`C81 → C90`、`C81 → C91`、`C81 → C92`、`C81 → C93`、`C81 → C94 → C95`である。Candidate72〜Candidate95の系譜と現在状態の一覧は[`prompts/candidates/README.md`](../prompts/candidates/README.md)にある（Candidate72とCandidate73は当初index表へ未掲載だったが、後にbundle実在分を全件掲載する追補で追加した）。identityの正本は各bundleの`manifest.json`、評価状態の正本は独立したevaluation result、release・approval・projectionの正本は[`prompts/releases/README.md`](../prompts/releases/README.md)とする。

Candidate72とCandidate73は、いずれもCandidate71を直接sourceとし`VALIDATION_CLOSURE`一行だけを短い表現へ置換したcandidateである。両者はcandidate bundle（`artifact_role: candidate`、`evaluation_status: targeted_evaluated`、`state: stopped`、bundle SHA-256固定）と独立したtargeted評価resultを持ち、candidate index表にも掲載している。Candidate72（`closed-validation-state-r1`、[manifest](../prompts/candidates/the-caption-3ce91a4-closed-validation-state-r1/manifest.json)、[設計記録](candidate72-closed-validation-state-design.md)、[targeted result](../evaluations/results/candidate71-candidate72-closed-validation-state-v12-targeted4-n5_2026-07-23.md)）はF06の編集後model再入中央値がCandidate71の`2`から`3`、token中央値`157,863 → 198,552`へ増え、抽象名だけの保持では不十分だった。Candidate73（`terminal-closure-preserving-compression-r1`、Candidate72非継承、[manifest](../prompts/candidates/the-caption-3ce91a4-terminal-closure-preserving-compression-r1/manifest.json)、[設計記録](candidate73-terminal-closure-preserving-compression-design.md)、[targeted result](../evaluations/results/candidate71-candidate73-terminal-closure-preserving-compression-v12-targeted4-n5_2026-07-23.md)）も同方向で不足を示し、[`Candidate71 control abstraction分析`](candidate71-control-abstraction-analysis.md)は、保持が必要なのは入口の完全性・同時発行・result有効性・成功後のtool closure・成功後のresponse closureであり、抽象名の保持やtool実行の閉包だけでは不十分だと総括した。

Candidate74以降はbundleを構築し評価した。番号「Candidate74」は上記分析中の`P3`削除提案の作業呼称とは別で、下表の型付き状態機械identityへ実際に割り当てられている（[`candidate71-control-abstraction-analysis.md`冒頭注記](candidate71-control-abstraction-analysis.md)）。

| prompt set | 直接source | 変更軸 | 評価状態（正本: リンク先の評価result） |
| --- | --- | --- | --- |
| Candidate74（`typed-execution-state-machine-r1`） | Candidate71 | flatな11 labelをauthority、identity、execution state、producer、validation DAG、method / recoveryの型付き状態機械へ再編 | [`v12 standard14 N=5 / evaluated`](../evaluations/results/candidate71-candidate74-typed-execution-state-machine-v12-standard14-n5_2026-07-23.md) |
| Candidate75（`authority-bound-validation-fast-path-r1`） | Candidate74 | 型付き状態構造を維持し、authorityでdependencyが固定されない独立required validationを同一waveへ閉じる | [`F06 targeted N=5 / stopped`](../evaluations/results/candidate74-candidate75-candidate76-validation-wave-v12_2026-07-23.md) |
| Candidate76（`final-state-validation-wave-r1`） | Candidate75 | potential mutator後の最終target versionを観測するvalidationだけを後続waveへ固定 | [`F06 targeted pass、standard14 69 / 70 score 4 / stopped`](../evaluations/results/candidate74-candidate75-candidate76-validation-wave-v12_2026-07-23.md) |
| Candidate77（`triggered-exception-transition-r1`） | Candidate71 | C71の11 labelを維持し、型付き状態仕様を例外triggerが成立したoperationだけへ適用 | [`v12 standard14 70 / 70 score 4 / stopped`](../evaluations/results/candidate71-candidate77-triggered-exception-transition-v12-standard14-n5_2026-07-23.md) |
| Candidate78（`project-index-navigation-r1`） | Candidate71 | TaskSpecで未解決の静的project事実が必要な場合だけ、repository-wide探索前に既存project indexを参照 | [`v13 standard14 70 / 70 score 4 / stopped`](../evaluations/results/candidate71-candidate78-project-index-navigation-v13-standard14-n5_2026-07-26.md) |
| Candidate79（`ordered-validation-wave-r1`） | Candidate71 | 順序依存required validationをfail-stopの順序付き個別invocation群として同一model stepへ閉じる | [`v13 Medium F04 5 / 5 score 4 / stopped`](../evaluations/results/candidate71-candidate79-ordered-validation-wave-v13-medium-f04-n5_2026-07-26.md) |
| Candidate80（`root-validation-wrapper-r1`） | Candidate71 | root producerのrequired validationを一つのcustom wrapper内の順序付き個別commandへ固定 | [`v13 Medium F04 10 / 10 score 4、1-step closure 9 / 10 / stopped`](../evaluations/results/candidate71-candidate80-root-validation-wrapper-v13-medium-f04-n10_2026-07-26.md) |
| Candidate81（`validation-wrapper-precedence-r1`） | Candidate71 | 後段の「順に」「1 commandずつ個別」をroot wrapper内の発行順・invocation単位として固定 | [`v13 Medium standard14 70 / 70 score 4 / quality and prompt stability gates passed`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md) / [`release approved / projected`](../prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1/README.md) |
| Candidate82（`producer-gate-deduplication-r1`） | Candidate81 | `OWNER_ROLE`に完全な正本がある明示producer gateの短い再記述P3だけを`PRODUCER`から削除 | [`v13 Medium standard14 B20 / stopped`](../evaluations/results/candidate82-producer-gate-deduplication-v13-medium-standard14-continuous-n5-b20_2026-07-28.md) |
| Candidate83（`delegation-value-boundary-r1`） | Candidate82 | `OWNER_ROLE`の明示producer限定predicateを、未完了判断への固有価値とroot非重複を要求する`delegation_value_ready`へ置換 | [`v14 Medium F02 N=5 / stopped`](../evaluations/results/candidate83-delegation-value-boundary-v14-medium-f02-n5_2026-07-28.md) |
| Candidate84（`delegation-marginal-value-boundary-r1`） | Candidate83 | 語義上の独立性ではなく、Worker専有scopeと5種の実質的価値stateを要求する`delegation_value_ready`へ置換 | [`v14 Medium F02 N=5 / stopped`](../evaluations/results/candidate84-delegation-marginal-value-boundary-v14-medium-f02-n5_2026-07-28.md) |
| Candidate85（`planning-first-producer-selection-r1`） | Candidate81 | operation分解、AIによるproducer選択、dependency、execution wave、待機条件を実行前の`execution_plan_ready`へ接続 | [`v14 Medium F02 cost_tradeoff、F04 cost_control_failed / stopped`](../evaluations/results/candidate81-candidate85-planning-first-v14-medium-f04-n5_2026-07-28.md) |
| Candidate86（`producer-plan-fast-path-r1`） | Candidate81 | 単一operationのroot直行と、必要時だけのproducer topology展開を既存`PRODUCER`へ統合 | [`v14 Medium F02 / F04 cost_tradeoff、D01 cost_control_failed / stopped`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-d01-n5_2026-07-29.md) |
| Candidate87（`producer-local-invocation-wave-r1`） | Candidate86 | producer内部の非依存invocationを同一model stepの一つのcustom exec wrapperへ閉じる | [`v14 Medium標準14 quality passed / aggregate cost both higher`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md) / [`not adopted / stopped`](candidate87-adoption-decision.md) |
| Candidate88（`parallel-worker-admission-r1`） | Candidate87 | AI裁量Workerを非重複・非依存のroot operationと同じready waveで開始できる場合だけ許可し、明示必須producerを別境界として保持 | [`v14 Medium F02 quality passed / route and cost gates failed / stopped`](../evaluations/results/candidate81-candidate88-parallel-worker-admission-v14-medium-f02-n5_2026-07-29.md) |
| Candidate89（`dispatch-time-worker-admission-r1`） | Candidate87 | AI裁量Workerを、独立root operationのdispatch済み・実行中状態をschedulerが起動時に観測した場合だけ許可し、明示必須producerを対象外として保持 | [`v14 Medium F02 quality passed / dispatch and cost gates failed / stopped`](../evaluations/results/candidate81-candidate89-dispatch-time-worker-admission-v14-medium-f02-n5_2026-07-29.md) |
| Candidate90（`tool-output-ingress-boundary-r1`） | Candidate81 | raw tool outputをmodel contextへ入れる前に、次predicateに必要な観測値とmachine-bound exitへ限定 | [`v14 Medium F02 quality passed / ingress and cost gates failed / stopped`](../evaluations/results/candidate81-candidate90-tool-output-ingress-boundary-v14-medium-f02-n5_2026-07-29.md) |
| Candidate91（`concise-output-ingress-r1`） | Candidate81 | Candidate90の複数分岐を除き、一時file wrapperの単一動作へ短文化 | [`v14 Medium F02 quality passed / compliance and cost gates failed / stopped`](../evaluations/results/candidate81-candidate91-concise-output-ingress-v14-medium-f02-n5_2026-07-29.md) |
| Candidate92（`bound-output-route-r1`） | Candidate81 | 最初のcommand前にoutput routeを固定し、対象success resultへ4096 bytes上限を設定 | [`v14 Medium F02 route passed / cap and cost gates failed / stopped`](../evaluations/results/candidate81-candidate92-bound-output-route-v14-medium-f02-n5_2026-07-29.md) |
| Candidate93（`result-classification-r1`） | Candidate81 | 一律byte capを`EXACT / STRUCTURED / NOISE`の粗いresult classへ置換 | [`v14 Medium F02 classification not observed / stopped`](../evaluations/results/candidate81-candidate93-result-classification-v14-medium-f02-n5_2026-07-29.md) |
| Candidate94（`operation-criterion-totality-r1`） | Candidate81 | operation-localなcriterion stateを、`spec_ready(operation)`、machine-onlyの`owner=none`、producer terminal後の`unavailable` terminal failureへ全域化 | [`v14 Medium標準14 69 / 70 score 4 / stopped`](../evaluations/results/candidate81-candidate94-operation-criterion-totality-v14-medium-standard14-n5-cli0146_2026-07-30.md) |
| Candidate95（`required-judgment-owner-boundary-r1`） | Candidate94 | criterion ownerをriskラベルではなく、operation完了にrequiredなnon-machine judgment resultへ限定 | [`v14 Medium標準14 B20 1,398 / 1,400 score 4 / route・quality failed / stopped`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md) |
| Candidate96（`successful-validation-result-projection-r1`） | Candidate81 | 全required validation成功時の返却をvalidation identity / exact command / exit codeへ限定し、成功stdout / stderrをmodelへ返さない | [`v14 Medium F02 quality passed / success projection 0 / 5 / stopped`](../evaluations/results/candidate81-candidate96-successful-validation-result-projection-v14-medium-f02-n5-cli0146_2026-07-30.md) |
| Candidate97（`decision-round-closure-r1 / r2`） | Candidate81 | `DECISION_BOUNDARY`へ追加invocationのevidence bindingとterminal result済みinvocationの再発行禁止を追加。631文字のr1は結果生成前に中止し、238文字のr2だけを評価 | [`v14 Medium F02 quality passed / completion closure 0 / 5 / stopped`](../evaluations/results/candidate81-candidate97-decision-round-closure-r2-v14-medium-f02-n5-cli0146_2026-07-30.md) |
| Candidate98（`validation-completion-sheet-r1`） | Candidate81 | required validationと完了証拠を検証前の一つの実行票へ固定する`VALIDATION_PLAN`追加 | [`v14 Medium標準14 70 / 70 score 4 / result registered`](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md) |
| Candidate99（`decision-evidence-boundary-r1`） | Candidate98 | predicateの判断入力をbind済み証拠へ限定し、不足時だけ未取得証拠と消費先predicateを固定して入力範囲を広げる`EVIDENCE_SCOPE`追加 | [`v14 Medium F07 quality passed / mechanism failed / result not registered / stopped`](../evaluations/results/candidate99-decision-evidence-boundary-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) |
| Candidate100（`outcome-source-closure-r1`） | Candidate98 | 成果値、repository authority、対象artifactの現在状態の役割を分離し、変更predicate一意化後の変更前調査終了を要求する`OUTCOME_SOURCE`追加 | [`v14 Medium F07 quality passed / mechanism failed / result registered / stopped`](../evaluations/results/candidate100-outcome-source-closure-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) |
| Candidate101（`additional-investigation-trigger-r1`） | Candidate98 | 追加調査を具体的な曖昧さ、波及、矛盾、変更起因の検証失敗を観測した場合だけにする`METHOD`置換 | [`v14 Medium F07 quality passed / mechanism failed / result registered / stopped`](../evaluations/results/candidate101-additional-investigation-trigger-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) |
| Candidate102（`prechange-evidence-freeze-r1`） | Candidate98 | `spec_ready=true`時に変更前の未解決predicateとrequired evidence identityを固定する`SPEC`置換 | [`v14 Medium F07 quality passed / mechanism 2 / 5 / result registered / stopped`](../evaluations/results/candidate102-prechange-evidence-freeze-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) |
| Candidate103（`prechange-evidence-receipt-r1`） | Candidate98 | 変更前invocation、固定済みconsumer、結果で変わる判断を最初のinvocation前に可視化する`SPEC`置換 | [`v14 Medium F07 quality passed / mechanism 0 / 5 / result registered / stopped`](../evaluations/results/candidate103-prechange-evidence-receipt-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) |
| Candidate104（`staged-evidence-admission-r1`） | Candidate98 | 初期evidence集合をTaskSpecから固定し、許可済みresultが具体的不足または矛盾を示した場合だけ次の一件を開く`EVIDENCE_GATE`追加 | [`v14 Medium targeted 10 / 10・標準14 70 / 70 score 4 / adoption not decided`](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md) |
| Candidate105（`validation-terminal-return-r1`） | Candidate104 | 検証実行票がterminalになる前の意図的な短時間yieldを閉じ、nonterminal result後は同じsessionのterminal待機だけを継続する`VALIDATION_PLAN`置換 | [`v14 Medium標準14 70 / 70 score 4 / terminal return improved not complete / adoption not decided`](../evaluations/results/candidate104-candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146_2026-07-30.md) |
| Candidate106（`compact-validation-terminal-wait-r1`） | Candidate104 | C105で増えた既存規則の再説明を除き、短時間yield禁止とnonterminal後の同一session待機だけを残す`VALIDATION_PLAN`置換 | [`v14 Medium F03・F08 B20各200 / 200 score 4 / F03対象経路1件再発 / stopped`](../evaluations/results/candidate104-candidate106-validation-terminal-wait-v14-medium-f03-f08-continuous-n5-b20-cli0146_2026-07-30.md) |
| Candidate107（`validation-wrapper-reentry-closure-r1`） | Candidate106 | outer deadlineを内部wait以上へ制約し、cell ID付きnonterminal result後を同じcell IDへのwait-only遷移にする`VALIDATION_PLAN`置換 | [`v14 Medium F03 B20 100 / 100 score 4 / wait-only passed / outer deadline failed / stopped`](../evaluations/results/candidate107-validation-wrapper-reentry-closure-v14-medium-f03-continuous-n5-b20-cli0146_2026-07-30.md) |

Candidate94は2026-07-30のread-only semantic auditで再現した三つの未定義分岐を、一つのoperation criterion totality軸として扱う。ユーザーの明示依頼によりtargeted gateより先にRating v14 Medium標準14 N=5を実行した。C81は70 / 70、Candidate94は69 / 70がscore `4`で、A02 iteration 5がrepository authorityから解決できる正規routeを質問して停止した。事前停止条件に従い現在状態を`standard14_evaluated / quality_gate_failed / stopped`とする。targeted評価、採用、release、本体反映は未実施であり、Candidate81を採用・投影済み基準として維持する。

Candidate95はCandidate94のA02失敗traceを直接の作成根拠とする。A02ではrequested outcome valueをrepository authorityから一意に解決できていたが、risk記載だけでcriterion ownerを別のreadiness値として要求した。Candidate95は`SPEC`一行だけを置換し、別のnon-machine judgment resultがrequiredでないrepository-resolvable criterionへ`owner=none`をbindする。Rating v14 Medium A02 N=5は5 / 5 score `4`、標準14 N=5も70 / 70 score `4`、後続A02 B20も100 / 100 score `4`だった。matched C81 / C95 A02 B20ではelapsedだけC95が有意に短かったため、両promptの標準14 B20へ進んだ。標準14 B20はC81 1,400 / 1,400 score `4`に対し、C95はscore `4 / 2 / 1 = 1,398 / 1 / 1`だった。A02でrisk記載からownerを再要求した1件と、F06で明示owner語列を具体的主体ではないと再解釈した1件が、いずれも変更・test前に停止した。C81比の中央値もtoken`+4.49%`、elapsed`+5.53%`で、両方有意に悪化した。現在状態は`standard14_b20_evaluated / quality_gate_failed / route_stability_gate_failed / cost_both_significantly_higher / stopped`であり、採用、release、本体反映へ進めない。

Candidate96は、Candidate81の最新Rating v14 Medium標準14 B20で観測した成功validation後の再実行を直接の作成根拠とする。F01 / F02の8 / 200 runでfull validationが再発行され、raw traceでは長い成功出力後にmachine-bound exit codeを確認できない経路が記録された。TaskSpecとexecutor adapterは変更せず、C81の`VALIDATION_CLOSURE`一規則だけを置換した。F02 r1 Rating v14 Medium N=5では両promptとも5 / 5 score `4`で、Candidate96のtoken中央値はC81比`-11.03%`、elapsed中央値は`-15.78%`だった。しかしrequired commandは直接発行され、全5 runで成功stdoutがmodel-visible resultへ返ったため、success projectionは`0 / 5`だった。KPI差は狙った機構へ帰属できない。現在状態は`targeted_f02_evaluated / mechanism_gate_failed / stopped`であり、F04以降、採用、release、本体反映へ進めない。

Candidate97は、C81 F02 B20の上振れ側で増えたdecision roundを、`DECISION_BOUNDARY`だけで閉じられるかを確認した。具体的なinspection / completion列挙を含む631文字のr1は、長すぎるとの判断でterminal result生成前に中止し、result registryへ登録していない。238文字へ縮めたr2はF02 N=5の5 / 5がscore `4`で、full validationの重複も0 / 5だった。しかし5 / 5すべてでfull validation成功後に別の`git status` commandを発行し、completion decision-round closureは0 / 5だった。token中央値は保存済みC81比`+4.72%`、elapsed中央値は`+0.31%`で、低elapsed側への移動も示さなかった。現在状態は`targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped`であり、r2の追記、Standard14、B20、採用、release、本体反映へ進めない。

Candidate98は、検証成功後に別の判断として追加される完了証拠と再検証を、検証前に固定する一つの実行票へ閉じる。Candidate99はその直接childであり、F07の長いtraceで観測した履歴・対象外探索・未bind出力の流入を、methodや読取回数ではなくpredicateが消費できる証拠の所属で制御する。F07 N=5は5 / 5 score `4`、root-only、required command evidence充足だったが、履歴参照を1 / 5、対象外を含む広い検索を4 / 5で観測した。tokenは`110,083〜135,549`、elapsedは`64.806〜77.347秒`へ狭まったが、N=5の診断値であり狙った境界も成立していないため効果と判断しない。全14 caseのLayer 1にF07 5 slotだけを実行したためLayer 4登録条件を満たさず、結果は非登録である。現在状態は`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_not_registered / stopped`とし、Standard14以降へ進めない。

Candidate100もCandidate98の直接childである。Candidate99は失敗経路の観測証拠としてだけ使い、系譜には含めていない。成果値、repository authority、対象artifactの現在状態の役割を分離したが、F07 N=5で広い検索なしは1 / 5のままだった。履歴参照なしは5 / 5、品質は5 / 5 score `4`だったが、4件はrunner gate、fixture、検証script、局所authorityを追加確認した。tokenは`109,688〜172,884`、elapsedは`58.392〜86.432秒`で、Candidate99より振れ幅も大きい。F07 5 slotを実行前coverageへbindしたためLayer 4 resultは登録済みだが、mechanism gate不通過により`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とする。Standard14、B20、採用以降へ進めない。

Candidate101もCandidate98の直接childである。別実行者への事後聞き取りで得た追加調査の発火条件を`METHOD`へ移したが、F07 N=5の5 / 5すべてが対象外検索を行い、1件はGit履歴も参照した。正式評価executorは、追加規則に含めたstart gate、適用repository authority、曖昧さの有無を確認するため、かえって検索を先行させた。品質は5 / 5 score `4`、tokenは`121,223〜143,700`、elapsedは`64.663〜77.354秒`だった。Layer 4 resultは登録済みだが、現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とし、Standard14、B20、採用以降へ進めない。

Candidate102もCandidate98の直接childである。`spec_ready=true`時の変更前証拠集合を内部的に固定したところ、履歴参照は0 / 5、広い検索なしは2 / 5だった。失敗3件は「TaskSpecを固定した」と宣言した後にauthority、fixture、start identityを検索しており、内部bindingを後から書き換えても検出できなかった。品質は5 / 5 score `4`だが、token中央値`154,014`、elapsed中央値`85.546秒`でCandidate101より両方増えた。現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とし、Standard14、B20、採用以降へ進めない。

Candidate103もCandidate98の直接childである。変更前invocationとconsumerをmodel-visibleな実行票へ固定したが、4件はTaskSpec固定済みの判断へauthority・fixture・開始gate実装等の証拠探索を追加し、1件は広い探索後に実行票を作った。品質は5 / 5 score `4`だが、実行票先行4 / 5、履歴参照なし4 / 5、広い検索なし0 / 5で、狙ったmechanismは0 / 5だった。保存済みCandidate100 iteration 4は同じTaskSpecをidentity、status、`run.sh`だけで完了しており、問題は判断項目不足ではなく証拠範囲の過剰拡張である。token中央値は`137,344`、elapsed中央値は`98.189秒`である。現在状態を`targeted_f07_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped`とし、Standard14、B20、採用以降へ進めない。

Candidate104もCandidate98の直接childである。初期evidence集合をTaskSpec本文、明示開始状態、対象artifact、明示read-only path、適用中のrepository instructionへ限定し、追加evidenceをdefault denyにした。A02 / F07 N=5は10 / 10 score `4`でmechanism gateを通過した。正規`comparison-preflight.json`でC98の保存済みLayer 1へ固定した標準14 N=5も70 / 70 score `4`、excluded 0だった。C104 minus C98の中央値はtoken`-6.48%`、elapsed`-9.77%`である。現在状態は`targeted_a02_f07_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / result_registered / adoption_not_decided`とし、B20、release、本体反映は未実施である。

Candidate105はCandidate104 F03 N=5の保存traceを直接の作成根拠とする。5件のmodel stepは`5 / 5 / 6 / 7 / 7`、tokenは`112,196〜192,530`で、上振れ側はcustom exec wrapperへ一秒のyieldを指定し、nonterminal result後に進捗報告とwaitへ分岐した。full validationは進捗報告前に開始済みであり、required command順序ではなくterminal前のmodel再入を対象とする。Candidate104の`VALIDATION_PLAN`一規則だけを置換し、TaskSpec、required validation、rating、executorは変更していない。F03 r2 N=5は5 / 5 score `4`、意図的なnonterminal yield 0 / 5、validation中進捗message 0 / 5だった。一方、一回wrapperと実行票後toolなしは4 / 5で、設計時の停止条件によりいったん停止した。

その後、ユーザーがStandard14評価だけを明示的に再開した。正規preflightでCandidate104 resultへ固定した標準14 N=5は70 / 70 score `4`、excluded 0だった。C105 minus C104の集約中央値はtoken`+0.70%`、elapsed`+2.65%`であり、両KPI改善は成立しない。F03では検証後のdiff / status再取得なしがC104の2 / 5からC105の4 / 5へ増え、required validation再実行は0 / 5だった。残る1件はfull gate出力のtruncation後にdiff / statusだけを再取得しており、prompt制御は改善したがtool result配送軸を完全には閉じない。現在状態は`targeted_f03_stopped_gate_user_reopened_for_standard14 / standard14_evaluated / quality_gate_passed / terminal_return_improved_not_complete / result_registered / adoption_not_decided`とし、B20、採用、release、本体反映は未実施・未判断である。

Candidate106はCandidate104の直接childである。Candidate105のC104比`+314`文字からwrapper構造、stop condition、result返却、例外処理の再説明を除き、短時間yield禁止とnonterminal result後の同一session terminal待機だけを残した。C104比は`+104`文字で、C105より210文字短い。F03 N=5は5 / 5 score `4`で、focused / full validation各一回、validation中messageなし、required validation再実行なし、検証後再取得なしを5 / 5で満たしmechanism gateを通過した。正規preflight後のStandard14 N=5も70 / 70 score `4`、excluded 0だった。C106 minus C104の集約中央値はtoken`-2.52%`、elapsed`-6.38%`、C106 minus C105はtoken`-3.20%`、elapsed`-8.80%`だった。その後のF03・F08 N=5 B20は両promptとも200 / 200件がscore `4`だった。F03のrequired validation間messageなしはC104の89 / 100からC106の99 / 100へ改善したが、C106で対象経路が1件再発した。F03・F08のtokenとelapsedには有意差がなかった。事前のzero-regression gateに従い、現在状態を`targeted_f03_f08_b20_evaluated / quality_gate_passed / route_stability_gate_failed / cost_no_significant_difference / result_registered / stopped`とする。Standard14 B20、採用、release、runtime projection、本体反映へ進めない。

Candidate107はCandidate106の直接childである。C106 F03 B20で再発した一件の保存traceを根拠とし、`VALIDATION_PLAN`の定性的な短時間yield禁止を、outer deadlineを内部required commandのwait deadline以上にする条件へ置換した。cell ID付きnonterminal resultが返った場合の次actionも、同じcell IDへの`wait`だけに限定した。変更対象はroot `AGENTS.md`一つ、変更predicateは`VALIDATION_PLAN`一つである。F03 B20は100 / 100件がscore `4`で、途中messageとrequired validation再実行は0 / 100だった。nonterminal返却6件の直後は6 / 6件とも同じcell IDへの`wait`だった。一方、内部waitより短いouter deadlineが4 / 100件再発したため、現在状態を`targeted_f03_b20_evaluated / quality_gate_passed / wait_only_gate_passed / outer_deadline_gate_failed / result_registered / stopped`とする。Standard14、採用、release、本体反映へ進めない。

Candidate74は`standard14_evaluated`である。Candidate75・Candidate76・Candidate77・Candidate78・Candidate79・Candidate80は事前gateまたは品質・効率・安定性gateにより`stopped`である。Candidate81はRating v13 Medium標準14項目70 / 70でscore `4`を維持し、複数required command caseの1-step closureをCandidate71の30 / 35から35 / 35へ改善したため、`standard14_evaluated / quality_gate_passed / prompt_stability_gate_passed`となった。token中央値はCandidate71比`-0.30%`、elapsed中央値は`+5.78%`であり、速度改善は主張しない。Candidate82はF10 / D01 targeted 10 / 10と単発標準14 70 / 70を通過したが、採用前B20の1,400件中2件でcriterion ownerを独立producer指定へ変換してchildを起動した。Candidate82設計の停止条件に従い、現在状態を`standard14_b20_evaluated / stopped`とする。公式score `1`の1件は意味上正しく確認停止したRating v13偽陰性である。Candidate83はF02の5 / 5でscore `4`を満たし、全runが独立contract check Workerを起動し、1 runは同じ確認を別Workerへ再割当てした。Candidate84もF02の5 / 5でscore `4`を満たし、3 runはroot-only、2 runはWorkerありだった。当時の停止条件によるC83 / C84の`stopped`履歴は保持する。後続の[`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)ではWorker起動を独立停止条件にせず、現在解釈をC83 `quality_passed / cost_control_not_demonstrated`、C84 `quality_passed / cost_control_mixed`へ分離した。互換baselineと事前toleranceがないため、両者の採用、追加評価、release、本体反映へは進めない。Candidate85はこの再設計をC81直系のplanning-first変更として構築し、試験内容を変更せず評価した。F02は`quality_passed / cost_tradeoff`、F04は`quality_passed / cost_control_failed`だったため、現在状態は`targeted_f02_f04_evaluated / stopped`である。Candidate86はC85で観測した単一operationのplan維持を除くC81直系candidateである。F02 / F04は`cost_tradeoff`だったが、D01で指定worker routeを5 / 5件成立させた一方、token中央値`+83.28%`、elapsed中央値`+45.81%`となったため、現在状態は`targeted_f02_f04_d01_evaluated / stopped`である。Candidate87はC86のproducer選択を維持し、producer内部のinvocation batchingだけを置換した。指定worker routeを5 / 5件維持し、C86比でtoken中央値`-51.06%`、elapsed中央値`-26.54%`となった。個別監査のcontract bindingを訂正したD01は5 / 5 score `4`で、保存済みC81比も両KPI悪化ではない。後続F02も5 / 5 score `4`で、C81比の中央値はtoken`-5.26%`、elapsed`-10.63%`だった。F04も5 / 5 score `4`で、token中央値`+15.48%`、elapsed中央値`-12.62%`のtradeoffだった。targeted gate通過後の標準14はC81 / C87とも70 / 70 score `4`だったが、C87の集約中央値はtoken`+6.09%`、elapsed`+1.35%`だった。一次評価状態は`standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`のまま保持する。後続の別stateの採用判断で`not_adopted / stopped`とし、releaseは作成せずruntime projectionも承認しない。Candidate88はC87のAI裁量Workerを同一ready waveへ限定したが、F02で4 / 5件がWorkerを起動し、そのうち2件は逐次実行だった。C81比の中央値はtoken`+26.28%`、elapsed`+8.03%`で、`targeted_f02_evaluated / stopped`とした。Candidate89は起動時のdispatch状態を制御へ加えたが、Workerを起動した4 / 5件すべてでroot validationより`9.276〜16.549`秒先に起動し、`root_parallel_inflight=false`だった。C81比の中央値もtoken`+6.45%`、elapsed`+4.14%`で、`targeted_f02_evaluated / stopped`とした。Candidate90はC81へ`OUTPUT_INGRESS`だけを追加し、TaskSpec等を変えずF02を各`N=5`で比較した。品質は5 / 5 score `4`だったが、取得時projectionは0 / 5で、C81比の中央値はtoken`+5.35%`、elapsed`+23.31%`だった。Candidate91は同じ変更軸を147文字・2文へ短文化した。wrapperを一度以上使うrunは4 / 5へ増えたが、strict complianceは2 / 5で、C81比token中央値`+5.90%`、elapsed中央値`+12.94%`だった。両candidateとも事前停止条件により`targeted_f02_evaluated / stopped`とし、F04以降へ進めない。

### C81以降の現在整理

現在の採用・投影済み基準はCandidate81である。Candidate82〜Candidate89のbundle、設計、profile、resultは、Candidate81を置き換えた成果ではなく、将来の制御設計に使う評価証拠である。Candidate87の別stateの[`採用判断`](candidate87-adoption-decision.md)も`not_adopted / stopped`であり、Candidate82〜Candidate89のサブエージェント制御系列は完了・停止した。

Candidate81の後続[`Rating v14 A01限定B20`](../evaluations/results/candidate81-validation-wrapper-precedence-v14-medium-a01-continuous-n5-b20_2026-07-29.md)は、20 result、100 / 100件をvalid・rateable・score `4`として登録した。全件が`awaiting_required_value`、artifact unchanged、read-only、試験・変更operation未開始、root-onlyだった。このresultはA01のrating長期診断であり、標準14全体のB20、v13 B20の再採点、Candidate81の新しい採用・release・projection stateではない。

後続の[`observation delivery executor A/B`](../evaluations/results/candidate81-observation-delivery-executor-ab-v14-medium-f02-n5_2026-07-29.md)は、promptとTaskSpecを固定したまま直接tool result配送だけを閉じた。treatmentは5 / 5件で直接resultを0件にしたが、model再入はcontrol / treatmentとも中央値`7`回、合計`36`回で変わらず、token中央値も`+1.92%`だった。これはCandidate81のprompt評価や新しい採用状態ではない。executor機構は成立したが再入削減を示さなかったため、`executor_f02_evaluated / mechanism_enforced / no_reentry_reduction / stopped`である。

別executor条件の[`success-silent delivery F02 N=5`](../evaluations/results/candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md)は、成功したrequired validationのraw出力をmodelへ配送せず、失敗resultは変更しない境界を追加した。5 / 5 score `4`とmechanism 5 / 5を維持し、sealed control比token中央値`-17.86%`、合計`-21.60%`、elapsed中央値`-16.32%`だった。これはCandidate81の新しい採用・release・projection stateではなく、現在は`executor_f02_evaluated / cost_reduced / f04_not_started`である。

後続の[`pytest exact allowlist success delivery F02 N=5`](../evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f02-n5_2026-07-29.md)は、保存済みStd14 traceでrequired validation成功出力の`99.92%`を占めたpytest系だけをexact argvへ限定し、成功raw保存とreceipt生成をexecutor wrapperへ移した。5 / 5 score `4`、mechanism 5 / 5、local raw evidence failure 0件だった。instruction-based v1比tokenは中央値`-8.65%`、合計`+1.87%`であり、総量削減は未確認である。現在は`executor_f02_evaluated / exact_allowlist_mechanism_passed / aggregate_token_reduction_not_demonstrated / f06_not_started`である。

同executorの[`F06 N=5`](../evaluations/results/candidate81-pytest-allowlist-success-delivery-v14-medium-f06-n5_2026-07-29.md)はfocused pytestとfull pytestを5 / 5 runでexact allowlistへ通し、5 / 5 score `4`を維持した。raw `896,030 bytes`をlocalへ保存し、validation model-visible bytesは合計`4,802`、raw markerは0件だった。同条件のmatched controlは未取得であるためcost効果は判断しない。現在は`executor_f02_f06_evaluated / exact_allowlist_mechanism_passed / cost_effect_unmatched / std14_not_started`である。

後続の[`F06 matched control`](../evaluations/results/candidate81-success-delivery-executor-ab-v14-medium-f06-n5_2026-07-29.md)も5 / 5 score `4`だった。treatmentはmodel-visible result bytesを中央値`-67.33%`、合計`-64.47%`へ減らしたが、token中央値`+41.76%`、合計`+22.29%`、elapsed中央値`+25.94%`、合計`+7.63%`だった。model再入は中央値`4 → 7`、合計`22 → 31`へ増えた。現在状態を`executor_f02_f06_evaluated / output_reduced / cost_control_failed / stopped`とし、Std14へ進めない。

同日の透過runtime shim probeは、元のpytest commandを変えずに成功rawをlocalへ退避できたが、allowlist外Pythonの`sys.executable`を`.venv/bin/python.codex-delegate`へ変更した。runtime identity gateを満たさないため、profile、evaluation set、N5を作成せず`stopped_before_profile / runtime_identity_failed`とした。これは新Candidateの評価結果ではなく、executor実装可能性の停止証跡である。

得られた成果は三つある。第一に、producer指定の重複を一文削除するだけでは低頻度のowner語列変換を防げない。第二に、Workerの期待価値、同一wave、dispatch済み状態を個別predicateとして追加しても、実際のoperation分解と発行順を安定して制御できない。第三に、Worker起動そのものではなく、rootとWorkerを含むproducer内部のinvocation分割が大きなコスト差を作り得る。

再開時の未解決問題は「Workerをいつ許可するか」だけではない。C81のprompt全体を基準に、TaskSpecからoperation identityをどう導出し、どのoperationをrootまたはWorkerへbindし、非依存invocationをどのwaveへまとめ、resultをどの後続operationが消費するかというcontrol graph全体を再検討する必要がある。fresh C81互換traceで同じoperation誤分解を再観測するか、TaskSpecへ別resultまたは別producer identityの明示要件が追加されるまでは、次candidateを作成しない。再開してもC82・C83・C87・C88・C89の文面を継ぎ足さず、変更軸と事前gateを固定してからC81の直接childとして設計する。

評価完了後の2026-07-27、明示判断でCandidate81 releaseを`approved`とし、THE-CAPTIONへ`projected`にした。THE-CAPTION PR [#343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343)を統合commit `592e73aae4f5cf71964efea0d49836e8c894cbbc`としてmergeし、実効変更はroot `AGENTS.md`一つ、`bash ./scripts/dev/verify_change_set.sh`は`401 passed`だった。THE-CAPTION本体へ投影済みのreleaseはCandidate41 → Candidate43 → Candidate71 → Candidate81の順で、Candidate41・Candidate43・Candidate71は投影履歴と巻き戻し先として保持する。過去のprojection履歴と現在の投影構成の正本は[`prompts/releases/README.md`](../prompts/releases/README.md)とする。
