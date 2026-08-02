# 論文仮組みのevidence map

> [!IMPORTANT]
> **位置付け**: この文書は[`execution-control-research-paper-reframed-draft.md`](execution-control-research-paper-reframed-draft.md)の各主張と一次資料の対応表である。契約、評価状態、採用、release、本体反映の正本ではない。数値と識別子はリンク先の一次artifactを正本とする。
>
> **作成方針**: 数値は一次result（`evaluations/results/`および`evaluations/targets/*/results/`）とprompt bundleの実体から取得した。**Baselineの公開系譜については、既存論文が使用していなかった公開リポジトリ[`orchestration-prompt`](https://github.com/Kenn-dclxvi/orchestration-prompt)の固定履歴を補助一次資料として追加した**（R1-7a、第4節の留保10）。要約文書（`candidate-history.md`、`control-mechanisms.md`、`candidate81-candidate125-control-findings-synthesis.md`、既存の`execution-control-research-paper.md`）は所在の索引としてだけ使い、数値の正本としては使っていない。一次resultと要約文書の相違は第4節へ記録した。
>
> **新規測定は行っていない。** 既存証拠で接続できない主張は第3節へ再検証候補として分離した。
>
> **`論文節`列は2026-08-01に本文の現行14節構成へ振り直した。** 本文から削除された節に対応するClaimは`—`と記す。
>
> **作成日**: 2026-08-01（研究状態は2026-07-31時点）

---

## 1. 用語の定義

### 1.1 証拠水準

**実験観測と、artifact確認・規則定義・算術・解釈を別水準として区別する。**

| 水準 | 定義 | 例 |
| --- | --- | --- |
| `same_condition_observation` | 同一compatibility keyの保存済みresult、または宣言した変更軸以外を機械照合した条件での観測 | 層Bの7条件KPI |
| `repeated_observation` | 同一条件の反復（B18 / B20）または複数campaignで方向が一致した観測 | C81 / C95のB20 |
| `derived_arithmetic` | 保存済み値からの算術。一次resultに列として存在しない値 | 全case得点率、all-agent差の割合 |
| `artifact_verified` | bundle実体、manifestのhash、rating contract本文、prompt本文から直接確認できる事実 | root `AGENTS.md`のbyte数、target別SHA-256の差分 |
| `protocol_defined` | 基盤規則・契約・workflowとして定義されている事項。実験観測ではない | 4 Layerの境界、採点契約の`score_4_requires` |
| `historical_design_record` | 当時のmanifest、設計文書、prompt本文に記録された意図または判断の記録。効果の測定ではない | C35の`change_reason`、`prompt-guide.md`の設計理由 |
| `interpretive_synthesis` | 本論文が複数の観測やartifactから構成した解釈・分類・対応づけ | 9責務の抽出、工程と判定条件の対応表 |
| `descriptive_cross_layer` | compatibility keyが異なる条件の並置。効果量として読めない記述的比較 | 料金換算表、model軸の3条件 |
| `author-provided_historical_premise` | 研究者から与えられた歴史的前提。本リポジトリでも公開artifactでも検証できない | Baselineの実務利用の規模と成果（R1-7b） |
| `unverified` | 該当するcase、result、測定条件が存在しない | 長期・部分曖昧タスク、Claude系model |

### 1.2 再検証分類

**不足している証拠の種類ごとに分ける。「同条件再試験」と「holdout target」へ寄せない。**

| 値 | 意味 |
| --- | --- |
| 不要 | 現在の表現が保存済み証拠の範囲に収まっている |
| 文言限定 | 追加測定なしで、限定語または留保の明示によって成立させる |
| 既存データ再解析 | 新規実行なしで、保存済みrunまたはresultの再集計・再算出で答えられる |
| 同条件追加反復 | 同一compatibility keyでの追加実行が必要（反復数を増やす） |
| ablation | 境界の除去条件、順序入れ替え条件、同時追加条件の新規実行が必要 |
| 新case family | 新しいcase設計とrating contract revisionが必要 |
| 別model / CLI | 別のmodel系列または別の実行環境での測定が必要 |
| holdout target | 未使用のcaseまたは未使用のtarget repositoryが必要 |
| 独立再採点 | 固定契約による監査ではなく、独立した第三者採点者による再採点が必要 |
| field study | 実務利用における利用者価値の測定設計が必要 |
| 計装追加 | 現在保存していない量（入力要素別token、項別cost）の計装が必要 |
| 対象外 | 本研究の境界の外にある（executor実装、runtime強制など） |

### 1.3 主要なcompatibility key

| ラベル | key | 固定条件 |
| --- | --- | --- |
| 層B | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` | set `the-caption-standard14-r1` r1（identity `430d1d4b…`）/ target `THE-CAPTION@3ce91a4` / `gpt-5.6-sol` `medium` / Codex CLI `0.144.0` / rating v13（`d2dd4096…`）/ `workspace-write`・approval `never` / 14 case × `N=5` / global queue `M=24` / all-agent v1 |
| 層A（expanded12 v9） | `abc7d7a9a4db052f417a200e5c7b873e39edb27bc5d564163fbb150f560100a4` | set `the-caption-expanded12-f04r2-f10r3-r2`（`de4d1dea…`）/ `gpt-5.6-sol` `high` / Codex CLI `0.144.0` / rating v9 / 12 case × `N=5` / `M=24` |
| 層A（expanded12 旧rating） | `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e` | set `the-caption-revision-2-expanded12-r1` / `gpt-5.6-sol` `high` / `N=5` / `M=24` |
| 層C（B20） | `c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c` | set `the-caption-standard14-r1` r1 / `gpt-5.6-sol` `medium` / rating v14 / Codex CLI `0.146.0` / 各1,400件 / `M=24` / 実行順を batchごとに交互化 |
| 層C（atomic reuse N=5） | 各resultの`固定条件とidentity`節を正本とする（rating v14 `9d01b7ee…` / CLI `0.146.0` / fixture `bb9eb7f5…` / runtime `61b26e61…`） | Evaluation set identity `2096d15e…`（atomic run経路） |
| 層D（model軸） | 3 resultで互いに異なる（modelがkeyに含まれる） | 上記層C条件のうち`model`だけをSol / Terra / Lunaへ変更。preflightで差分が`$.comparison_conditions.model`と`$.profile_id`だけであることを機械照合 |
| Click C125 | `39dcb70f20256935b2e257e57cda1cba0c1f15d41ca77bb4e5b4c13734484472` | set `click-standard14-r2` r2（`bbba58d8…`）/ rating `click-outcome-abstract-condition-preserving-v10` / `gpt-5.6-sol` `medium` / Codex CLI `0.146.0` / 14 case × `N=5` / `M=24` |

---

## 2. Claim対応表

### 2.1 第1節 背景：Baselineの到達点

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1-1 | 3.1 | Baselineは人間の開発工程（指示書化・実装・監査・レビュー・差し戻し・完了判定・PR）を役割と関所として写している | prompt本文の工程と役割の限定列挙 | `prompts/baselines/the-caption-3ce91a4-current-r2/files/AGENTS.md.txt`（§役割・§指示書草案・§SA起動と分離・§停止と自動再修正・§完了判定・§PR作成）、`files/docs/orchestration-process.md`（§基本方針・§SA利用ケース・§自動修正ループ）、`files/prompts/{plan,implement,audit,review}.md` | Baseline bundle `63225d2d…`（19 path） | `artifact_verified` | 「工程・成果物・関所の構造を写している」まで。工程が人間の職能配分の写しであるという意図は主張できない（R1-3） | 不要 |
| R1-2 | 3.1 | 親エージェントは実装・修正・テスト実行・監査・レビュー相当の品質確認・指示書作成を直接行わない | prompt本文の禁止列挙 | Baseline root `AGENTS.md` §役割、`orchestration-process.md` §基本方針 | 同上 | `artifact_verified` | prompt上の規定であり、tool levelの強制ではない（`orchestration-process.md` §制約が明記） | 不要 |
| R1-3 | 3.2 | Baselineの設計記録は、この分業を「人間の組織図の写し取りではない」と明示し、AI固有の失敗様式（確証バイアス・迎合・reward hacking）へ向けた設計として7点の理由を挙げていた | 設計理由の原文 | `files/docs/prompt-guide.md` §AI最適化の設計理由 | 同上 | `historical_design_record` | 当時の設計意図の記録である。設計理由の妥当性が測定されたわけではない | 不要 |
| R1-4 | 1.1, 3.6, 5.1, 14#1 | **研究開始前と研究開始後を分けて記述する。** 研究開始前、著者は利用経験からBaselineを初期解として扱っていた（R1-7b）。その汎用コアが公開され、運用上の観測に基づいて改訂されていたことはR1-7aで確認できる。研究開始後の初期測定では拡張12課題で`58 / 60`件が4点・2件が3点・品質中央値`100.000`だった。この測定は研究前の認識を部分的に支持したが、品質制約は満たしていない。その工程構造がAI実行として最適かは未計測だった | R1-1〜R1-3、R1-6、および当時のtoken集計がroot-onlyだった事実 | 上記＋[`v3-all-agent-token-reaccounting_2026-07-16.md`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md) | 混在（設計記録＋層A） | `interpretive_synthesis` | **「品質確保に成功」と断定しない。「当時の評価範囲では品質制約を満たしていた」とも書かない**（2件の減点があり、2.1節の「全課題で減点なし」という定義を完全には満たさない）。**さらに、研究の中で得た拡張12課題の結果を「研究開始時点で初期解と考えていた根拠」として使わない。** 研究開始前の認識（R1-7b。公開artifactと改訂履歴はR1-7a）、研究開始後の初期測定、後続評価の事実（R5-1）を分けて記述する | 文言限定（本文1.4節・要旨・5.1節・14#1で対応済み） |
| R1-5 | 3.5 | Baselineが守ろうとした品質責務を9項目として抽出できる | prompt本文の該当節 | Baseline root `AGENTS.md` §入力境界・§作業単位化・§停止と自動再修正・§完了判定・§出力、`orchestration-process.md` §停止条件・§各工程の確認範囲・§指摘分類、`prompts/audit.md` §指摘、`prompts/implement.md` §ルール、`prompts/review.md` §レビュー観点、`docs/prompt-guide.md` §原則 | 同上 | `interpretive_synthesis` | **本論文が本文から抽出した整理である。** Baseline作者が「9項目」と宣言した記述はなく、この9項目からStandard14を導出した履歴もない（R3-1） | 文言限定（本文1.3節で明示済み） |
| R1-6 | 3.6 | Baselineは拡張12課題60回で score `4 / 3 = 58 / 2`、`quality_score`中央値`100.000`だった | 一次resultのscore分布 | [`baseline-control-free-repository-c35-c41-…-v9-expanded12-n5_2026-07-19.md`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md) | 層A（`abc7d7a9…`）、rating v9、`high` | `same_condition_observation` | この12課題・rating v9・推論`high`の範囲。標準14項目では`92.857`（R5-1） | 不要 |
| R1-7a | 3.1, 3.4 | Baselineの汎用コアは公開リポジトリ`Kenn-dclxvi/orchestration-prompt`で管理されていた。研究Baselineのroot `AGENTS.md`は公開履歴PR #18 headの`AGENTS.md`とGit blob単位で一致する。公開リポジトリにはTHE-CAPTION向けoverlayがあり、実運用上の観測に基づく改訂履歴も保存されている | 公開repoの可視性、固定refのtree、blob SHA、PR本文、overlay READMEの照合 | [`Kenn-dclxvi/orchestration-prompt`](https://github.com/Kenn-dclxvi/orchestration-prompt)（PUBLIC、2026-06-14作成）。固定ref `28fddf7d2734daeca9b9e9756159460c2ec6b09c`（PR [#18](https://github.com/Kenn-dclxvi/orchestration-prompt/pull/18) head、2026-06-28 merged）。`AGENTS.md` blob `9d70bc48adc5699f4e986f2ae9bc79dbf623f8db`（5,980 bytes）は本リポジトリのBaseline manifestの記録値と一致。`overlays/the-caption/{README.md, repo-context.md, files/AGENTS.md, files/prompts/*.md}`。PR #18本文が「プランSA…実運用ではほぼ自律起動しなかった」を変更理由として記録 | 公開repoの固定ref（`main`は参照しない） | `artifact_verified` ＋ `historical_design_record` | **公開された実在のprompt設計だった／THE-CAPTIONへの適用構造が存在した／運用上の観測を理由に改訂されていた、までが上限。** **blob一致は6 targetに限る**（`AGENTS.md`、overlay側の`prompts/{plan,implement,audit,review}.md`、`docs/prompt-guide.md`）。`docs/orchestration-process.md`は公開`22,203`bytes対Baseline`24,209`bytesで**不一致**、`docs/glossary.md`（4,086 bytes）は公開リポジトリに**存在しない**。適用は作業用クローンへ配置してから`THE-CAPTION`へマージする経路をとる。Baselineはマージ後の`THE-CAPTION@3ce91a4`から取得している。**「研究Baseline bundle全体が公開されていた」とは書かない。** 研究Baselineの正本は引き続き本リポジトリの19 path bundle（`63225d2d…`） | 不要 |
| R1-7b | 3.6, 12.6 | Baselineが研究開始前にTHE-CAPTIONの実務開発で継続利用され、品質確保の到達点として認識されていた | 利用件数、運用期間、対象タスク範囲、実務成果の成功率、手戻り・レビュー品質、研究用評価と独立した品質記録 | **該当する一次資料をこのリポジトリでも公開リポジトリでも確認できない。** PR #18本文は運用上の観測を1件記録しているが、利用の規模・期間・成果品質の記録ではない | — | `author-provided_historical_premise` | **利用の規模と成果は本論文が検証した事実ではない。** 「実務利用」を根拠として使う箇所では著者提供の前提である旨を明示するか、初期評価の事実（R1-6）だけを根拠にする。公開artifactの存在と改訂履歴はR1-7aで検証済みであり、この行の対象ではない | 文言限定（前提である旨の明示）／または運用記録・成果記録の追加 |

### 2.2 第2節 研究疑問

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R2-1 | 1.2, 3.3 | 中心問いは「**Baselineが守ろうとしていた品質責務を損なわず、評価で見つかった残余欠陥を閉じながら、AI固有の不要な実行経路を除去できるか**」である | 問いの定義 | 本論文の定義。関連: [`prompt-control-design-principles.md`](prompt-control-design-principles.md)、[`prompts/CLAUDE.md`](../prompts/CLAUDE.md)のcandidate作成前gate | — | — | 問いの定義であり測定主張を持たない。**「Baselineによって得た品質を維持する」とは定義しない。** Baselineは初期測定時点（拡張12課題`58 / 60`）でも本論文の品質制約（全課題で減点なし）を満たしておらず、「Baselineの点数の維持」と操作的定義が一致しないため。**「品質を維持しながら」という表現は、すでに品質制約を満たした候補どうしの比較（C43以降）に限って使う** | 文言限定（本文2.1節・要旨で対応済み） |
| R2-2 | 1.2 | 静的量と動的量が一致するかは実測可能な副問いである | 静的量（bytes）と動的量（token）の両方が保存されている | prompt bundleの`AGENTS.md.txt`実体、各resultのtoken | 層A・層B | — | 問いの定義 | 不要 |
| R2-3 | 1.2, 6 | 「何を削除すると品質が壊れるか」は0バイト条件で測れる | R6-1 | 6.2 | 層B | — | 問いの定義 | 不要 |
| R2-4 | 1.2, 7 | 副問いは「**どの実行境界を残せば品質制約を維持できるか**」である | R7-* | 下記 | 層B・層C | — | **最小性は成立しない。** ablationを実施していないため、境界集合の最小性も各境界の単独の必要性も判定できない。副問いから「最小」を外し、2.2節・7節冒頭・13節へ明示した | 文言限定（実施済み）＋ ablation（最小性を主張する場合） |
| R2-5 | 1.2, 8.3 | promptとexecutorの責務境界は実測可能である | R8-3 | 8.3 | 層C | — | 問いの定義 | 不要 |

### 2.3 第3節 評価設計

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R3-1 | 3.5, 4.6 | Standard14の各caseは品質責務を観測可能な条件（成果条件・許可path・禁止変更・必須検証）として表しており、Baselineの9責務との対応を**事後的に**与えられる | 各caseの`trial-prompt-input.json`と`README.md`、Standard14の正本 | `evaluations/cases/TC-{F01 r3, F02 r1, F03 r2, F04 r2, F05-CLARIFY r1, F05-OUT-OF-SCOPE r1, F06 r2, F07-CANONICAL r2, F07-DEPENDENCY r1, F08 r1, F10-ENTRYPOINT r1, F10-MONTHLY r3, A01 r2, A02 r2}`、[`the-caption-standard14-r1`](../evaluations/sets/the-caption-standard14-r1/README.md) | set identity `430d1d4b…`（層B）／`2096d15e…`（atomic経路） | `artifact_verified`（case定義の形式）＋`interpretive_synthesis`（責務との対応） | **「Baselineの責務をcaseへ変換した」という歴史的因果は書けない。** Standard14の正本から確認できるのは、旧12項目へA01とA02を加えて14項目とし版と評価境界を固定したことだけである。対応表は研究過程を再解釈する分析枠組みである | 文言限定（本文3節冒頭・3.1・3.2で明示済み） |
| R3-2 | 4.6 | Standard14全体はunder-executionとover-executionの両方向を含む。**A01とA02はこの双方向性を明示的な対照課題として設計した唯一の組**であり、他caseは成果条件と禁止境界によって一つ以上の失敗方向を検出する | case READMEの設計意図とrevision delta | `TC-A02-…/r2/README.md`（「A01の対照項目であり、曖昧に見える入力へ常に質問を返す挙動を高く評価しない」）、`TC-F01/r3`・`TC-F03/r2`・`TC-F07-CANONICAL/r2`・`TC-F04/r2`の各revision delta | 各case revision | `artifact_verified`（A01 / A02の明示的対照、および各revision deltaのover-execution側禁止）＋`interpretive_synthesis`（方向の分類） | **「全caseが双方向の失敗を測る」「片側だけを測るcaseは存在しない」とは書けない。** A01はstop-onlyでunder-execution形を持たない。また**「この設計がなければ常に止まるpromptが最良になる」とも書けない**（常時停止はF01〜F10で減点されるためStandard14全体の最良にはならない）。A01 / A02の対照組が担うのは仕様確定境界に限った区別である | 文言限定（本文3.3を修正済み） |
| R3-3 | 4.6 | Standard14の観測範囲を作業種類・実行制御境界・失敗方向の3軸で示せる | 各caseの`task_kind`と成果条件 | 同上、[`evaluations/cases/README.md`](../evaluations/cases/README.md) | 同上 | `interpretive_synthesis` | 「網羅している」ではなく「観測している」。軸の分類は本論文の整理である | 文言限定（見出しを「観測している範囲」へ修正済み） |
| R3-4 | 4.4 | model-visible / private境界が規則として分離されている | 各caseのvisibility boundary記述、基盤規則 | 各case README §提示範囲 / §Visibility boundary、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §Model-visible境界 | — | `protocol_defined` | 規則としての分離である。破れの実例は R8-6 | 不要 |
| R3-5 | 4.6 | 有効な実行はすべて0〜4で採点し、採点不能を認めない | rating contractの`unrateable_or_null_score_is_allowed_for_valid_run: false` | [`v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json)、[`v13`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json) | v13 / v14 | `protocol_defined` | 契約上の規定。計測失敗（コマンド終了状態を取得できない実行）は除外扱いで別 | 不要 |
| R3-6 | 4.6 | 長期・複数段の作業、段階的に変化する仕様、複数人の合意形成、障害対応、正のrecovery scenarioはStandard14に含まれない | 該当caseの不存在 | [`research-backlog.md`](research-backlog.md) 項目11（「未着手・該当caseなし」）、`RECOVERY`項目（「未完了・効果未測定」）、`evaluations/cases/`のcase一覧 | — | `unverified` | 「含まれない」ことは列挙で確定できる。含めた場合の挙動は不明 | 新case family |
| R3-7 | 4.2 | 採点契約は版で固定し、結果を見た後の基準変更は新しい版とする | 契約ファイル群と基盤規則 | `evaluations/rating-contracts/`（v1〜v14）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §Immutable history | — | `protocol_defined` | 規則と実体の一致まで | 不要 |
| R3-8 | 4.6 | v14はA01を「応答本文・疑問符・質問語を使わない」terminal-state evidenceで判定する | 契約本文 | [`v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json) `boundary_rules.TC-A01-LATENT-MODE-POLICY.state_evidence.response_text_policy`、`rater_input.forbidden` | v14 | `artifact_verified` | A01についてのみ確認済み。他caseの判定が同水準で観測可能条件へ落ちているかはcase単位でしか確認していない（R12-7） | 文言限定 |

### 2.4 第4節 測定基盤

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R4-1 | 4.1 | 評価は4 Layerに限定され、各Layerは前段artifactを変更しない | 基盤規則 | [`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §4 Layer、[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md) | — | `protocol_defined` | 規則としての境界。**この境界がR11-1（評価課題集合はruntime mechanismではない）の根拠である** | 不要 |
| R4-2 | 4.2 | 互換条件が全一致しない結果を同一比較へ混ぜない | 基盤規則と各resultの固定条件節 | [`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §Compatibility、各result | — | `protocol_defined` | 規則と実体の一致まで | 不要 |
| R4-3 | 4.2 | 層をまたいだ削減率の連結を行わない | 各層のkeyが異なること | 層Bのkey `79ed04a4…`（rating v13 / CLI `0.144.0`）と層Cのrating v14 / CLI `0.146.0` | — | `protocol_defined` | 記述方針。連結した数値は本論文に存在しない | 不要 |
| R4-4 | 4.5, 5.3 | root-only集計ではBaselineがC5より`615,701`少なく見えていたが、all-agentではBaselineが`3,185,357`多い。**Baselineのall-agent中央値とroot-only中央値の差は、all-agent中央値の56.4%に相当する** | 再集計resultの両集計値 | [`v3-all-agent-token-reaccounting_2026-07-16.md`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)（Baseline root-only `3,888,115` / all-agent `8,925,798`、C5 `4,503,816` / `5,740,441`） | 層A（`5048fe59…`系）、旧rating、`high`、拡張12課題 | `same_condition_observation`（順序の反転）＋`derived_arithmetic`（56.4%） | **56.4%は中央値同士の差をall-agent中央値で割った値である。2つの中央値が同じiterationから来ている保証はないため、run単位の子セッション消費比率としては読めない。** また拡張12課題・`high`・旧ratingの層である | 既存データ再解析（run単位の`descendant_tokens / all_agent_tokens`を算出する場合） |
| R4-5 | 4.3 | 3指標の中央値の実効標本数は`N`であり、70回は同質な70独立標本ではない | 集計方法の定義 | 各resultの中央値表記（「5反復中央値」）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) | — | `protocol_defined` | 集計単位の記述 | 不要 |
| R4-6 | 4.1, 14 | 基盤は`winner`、改善・悪化の断定、採用可否、release判断、projection判断を出力しない。評価は観測、採用は判断である | 基盤規則と実際の状態分離 | [`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §3 KPI末尾、[`candidate125-adoption-decision.md`](candidate125-adoption-decision.md)、[`prompts/releases/README.md`](../prompts/releases/README.md)、C125 resultの`adoption_not_decided` | — | `protocol_defined` | 規則と実体の一致まで | 不要 |

### 2.5 第5節 Baselineの測定

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R5-1 | 5.1, 5.2 | Baselineは層Bで`4 / 3 / 1 / 0 = 63 / 2 / 1 / 4`、品質中央値`92.857`、token中央値`11,977,774`、所要時間中央値`3,568.742`秒、70件合計`64,096,747` / `18,583.648`秒。減点はA01 4件、A02 2件、F07依存関係1件 | 一次resultのKPI表と低得点表 | [`baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)（result ID `107d31cdae9044d08c0768ffc89d3896`） | 層B `79ed04a4…` | `same_condition_observation` | この7条件・`N=5`の観測。所要時間は記述値（R12-15）。F07 canonicalで4 attemptを`command_evidence_incomplete`により除外し再実行している | 不要 |
| R5-2 | 5.1 | 保存された失敗内容の分類に、範囲逸脱・reward hacking・完了偽装・対象外操作は現れていない。落ちたのは推測の禁止・停止の義務・必須検証の非省略である | 低得点表の失敗内容と責務の対応 | 同上 §低得点、R1-5の責務列挙 | 層B | `interpretive_synthesis` | **「0件だった」は保存された失敗内容の分類にこの3類型が現れないことを意味する。** 責務ごとの独立検証ではない | 文言限定（本文で「分類に現れていない」へ修正済み） |
| R5-3 | 5.3 | 拡張12課題・推論`high`の保存結果では、Baselineのall-agent中央値とroot-only中央値の差がall-agent中央値の56.4%に相当した | R4-4 | 4.5, 5.3 | 層A（拡張12課題、`high`、旧rating） | `derived_arithmetic` | **層Aの数値である。層Bの`11,977,774`に対する内訳ではない。この2つを掛け合わせない。** run単位の比率でもない（R4-4） | 既存データ再解析 |
| R5-4 | 5.3 | 実装SAへの必須委任を外して選択可能にすると、40 implementation runすべてが親直接を選び、実装目的の委譲は0件だった。監査SA / レビューSA起動はC2の35 / 17からC5の25 / 16へ | 一次resultのrouting観測 | [`baseline-candidate1-…-candidate5-expanded12-global-m24-n5_2026-07-16.md`](../evaluations/results/baseline-candidate1-candidate2-candidate3-candidate4-candidate5-expanded12-global-m24-n5_2026-07-16.md) §Prompt execution design / §SA routing observation | 層A（`5048fe59…`）、`high`、拡張12課題 | `same_condition_observation` | 拡張12課題・`N=5`・旧rating。「実装の担当者を分ける段はAI実行では選ばれない」は、この60 runの観測に限定した記述 | 同条件追加反復（層Bで再現を主張する場合） |

### 2.6 第6節 削除実験

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R6-1 | 6.2 | ControlFreeRepositoryは層Bでtoken中央値`3,496,976`（Baseline比`-70.80%`）、所要時間`1,250.057`秒（`-64.97%`）、score分布`4 / 0 = 65 / 5`で、A01が5 / 5件0点 | 一次resultのKPI表・差分表・低得点表 | [層B result](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)（result ID `3fb81b94ef1d4770b52bc202bf0a43d8`） | 層B `79ed04a4…` | `same_condition_observation` | この条件の観測。所要時間は記述値 | 不要 |
| R6-2 | 6.1, 11.2, 12.4 | ControlFreeRepositoryはBaseline bundleの19 pathのうちroot `AGENTS.md`の1 targetだけを空ファイルへ置換した条件であり、擬人的な工程仕様（`orchestration-process.md` 24,209 / `prompt-guide.md` 15,421 / `glossary.md` 4,086 bytes）と4つのロールプロンプト（4,183 / 2,128 / 5,161 / 3,910 bytes）はBaselineと同一のまま残っている。**C35はその内容自体を0バイトへ置換した別の操作である（前者は経路の非活性化、後者は静的artifactの除去）** | manifestのtarget別SHA-256の照合、bundle実体のbyte数 | `prompts/candidates/the-caption-3ce91a4-control-free-repository-r1/manifest.json`（`scope`）と`prompts/baselines/the-caption-3ce91a4-current-r2/manifest.json`の照合結果: 差分target = `AGENTS.md`のみ。`the-caption-3ce91a4-root-control-only-r1/manifest.json`の`changed_targets` | bundle `999769800a…` vs `63225d2d74…` vs `f53fbf3649…` | `artifact_verified` | bundle実体から確定できる。**既存論文3.1節・付録A.2はCFR条件を「配下ディレクトリごとの指示書4件はそのまま残した」と記述しており、工程仕様7ファイルの残存に言及していない**（第4節の相違1） | 不要 |
| R6-3 | 6.2, 6.4 | 削除では品質責務1・2（推測の禁止と停止の義務）が閉じない。「lean」の最適点は0ではない | R6-1、R6-6、およびC43で減点が0になったこと（R7-7） | 層B result、層A result | 層B・層A | `repeated_observation` | 2つの層で同方向。ただし層Aは`1 / 60`、層Bは`5 / 5`で欠陥の頻度が違う。「削除では閉じない」までが上限で、「必要制御の集合が一意に定まる」ことは示していない | 不要 |
| R6-4 | 5.2, 6.4 | C81のroot本文は`5,525 bytes`（Baseline `5,980 bytes`の約`0.92`倍）だが、token中央値は`1,917,979`対`11,977,774`で約`6.2`分の1である | bundle実体のbyte数と同一keyのtoken | `prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1/files/AGENTS.md.txt`（5,525 bytes）、Baseline `files/AGENTS.md.txt`（5,980 bytes）、層B result | 層B `79ed04a4…`（同一key内での比較） | `artifact_verified`（byte数）＋`same_condition_observation`（token） | 静的量と動的量の不一致を同一key内で確認した観測 | 不要 |
| R6-5 | 6.2 | 品質中央値の一致を「品質が同じ」と読み替えない。BaselineとCFRは中央値`92.857`が一致するがcase score分布と全case得点率（`92.500%`対`92.857%`）は一致しない | score分布と得点率の算出 | 層B result §3 KPI（分布）。得点率は`259 / 280`と`260 / 280`から算出 | 層B | `same_condition_observation`（分布）＋`derived_arithmetic`（得点率） | 得点率は分布からの算術。一次resultに得点率列は存在しない | 不要 |
| R6-6 | 6.3 | 層Aでも同型の結果。Baseline `58 / 2` token中央値`10,826,033`、CFR `59 / 1` `2,808,523`（`-74.06%`）、C35 `60 / 0` `4,565,773`、C41 `60 / 0` `2,861,019`。C41はCFRより`+1.87%`大きい（一次resultの`-1.83%`はC41を基準にした値で、基準を入れ替えて再計算した） | 一次resultのKPI表 | [層A result](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md) | 層A `abc7d7a9…`、rating v9、`high` | `same_condition_observation` | 層Bと同方向だが別key。`1 / 60`から`0 / 60`を低頻度誤経路一般の解消へ一般化しない | 不要 |

### 2.7 第7節 実行境界の抽出

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R7-1 | 7.5, 1.5, 14 | 研究過程で**識別・検証された**境界ファミリーは**9件**（A1〜A9。成立、部分成立、後続候補による修正のいずれかが観測された制御であり、9件すべてが「成立が確認された制御」ではない）、C125のroot本文のlabelは**13件**、`synthesis`がC81以降の寄与として記録しているのは**7件**であり、**この3つは別の集合である**。いずれも「モデルが実行時に観測できる状態・証拠・結果に対する条件」として書かれている | 各候補のroot本文のpredicate形式と各層のKPI | C43 / C71 / C81 / C104 / C116 / C118 / C122 / C125のroot `AGENTS.md.txt`、[synthesis](candidate81-candidate125-control-findings-synthesis.md) | 層B・層C | `artifact_verified`（本文の形式とlabel集合）＋`interpretive_synthesis`（ファミリーへの分類） | **「観測可能性が効果の原因である」は示していない**（単文効果を測っていない）。反例系列（R8-4）との対照からの解釈にとどまる。**「7つの境界」という単一の数を要旨・結論へ置かない。** また**この軸を「研究開始時点の設計原則」として引用しない**（留保16）。設計原則文書の初版は2026-07-19で、測定開始（2026-07-14）より後、C11〜C40の観測から書かれている。軸は研究前半の産物かつ後半の先行制約である。 また**このファミリー一覧はKPI低下の一覧でも「成立が確認された制御」の一覧でもない**（A3は所要時間`+5.78%`、A6はtoken`+7.44%`、A7は部分成立、A8は品質`69 / 70`）。**9件全体について共通の反復効果が観測されたわけではないため`repeated_observation`は当てない。各候補の効果はR7-7〜R7-13を正本とする。** 表Aの各セルには比較元を併記する（A1の`5 / 5 → 0`はCFR / C5 / C35との比較、token`-77.32%`はBaselineとの比較であり、同一比較ではない） | ablation（原因性を主張する場合） |
| R7-2 | 5.2 | 層Bの7条件は指示書以外の条件（課題、作業指示、fixture、必要な検証、採点契約、実行環境、`M`、`N`）がすべて一致している | resultの固定条件節と「prompt identity以外を一致させた」記述 | 層B result §固定条件、[C71 / C81 result](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)（「両profileの差は`profile_id`と`prompt_set_identity`だけ」） | 層B `79ed04a4…` | `same_condition_observation` | 設定値の一致であり、実行時交絡（実行時刻・同時実行数・キャッシュ・提供側負荷）の排除ではない（R12-15） | 不要 |
| R7-3 | 5.2 | 結果は一つの勝者に収束しない（token最小はC81、所要時間と合計最小はC71、`4 = 70`はC43・C71・C81、1回で出し切れた率最良はC81） | 層Bの2 result | 層B result、C71 / C81 result | 層B | `same_condition_observation` | 記述的な比較。優劣・採用の順位ではない | 不要 |
| R7-4 | 5.2 | Baselineとの差分（CFR `-70.80%`〜C81 `-83.99%`） | resultの差分表 | 層B result §Baselineとの差 | 層B | `same_condition_observation` | 同一key内の記述的差分。個々の一文の効果ではない（R7-14） | 不要 |
| R7-5 | 3.2, 13 | C35以降のbundleでは擬人的な工程仕様7 target（合計59,098 bytes）が0バイトへ置換されている。**C35のmanifestは、保存済み観測で当該7 targetへの参照が成功実行に現れなかったことを置換の設計理由として記録している** | manifestの`change_reason`・`changed_targets`とbundle実体のbyte数 | `prompts/candidates/the-caption-3ce91a4-root-control-only-r1/manifest.json`、C41 / C43 / C71 / C81 / C125 bundleの同7 targetが0バイト | bundle `f53fbf3649…`ほか | `artifact_verified`（byte数と0バイト化）＋`historical_design_record`（非参照の観測） | **「7 targetが一度も参照されなかったことを本論文が一次resultから検証した」とは書けない。** 根拠となったraw command evidenceはリポジトリ外にあり、確認できるのはmanifestの記述である（第4節の留保3） | 文言限定（本文7.2・13節で明示済み） |
| R7-6 | —（本文から削除） | C43のrootは**9つのlabel**（`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`）からなり、各labelが1つのpredicateを持つ | root本文 | `prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1/files/AGENTS.md.txt`（3,980 bytes、11行、bullet 9件）、[`prompt-control-design-principles.md`](prompt-control-design-principles.md) | bundle実体 | `artifact_verified` | 「10行」ではなく「9つのlabel」。file自体は見出し1行を含む11行である | 不要 |
| R7-7 | 7.4a | C43は`spec_ready`のpredicateを置換し、A01の減点を`0`、point分布を`4 = 70`、token中央値をBaseline比`-77.32%`にした。変更理由はC42のA01失敗形である | resultのKPI・低得点表、manifestの`problem` / `change_reason` | 層B result、`the-caption-3ce91a4-outcome-authority-boundary-r1/manifest.json` | 層B `79ed04a4…` | `same_condition_observation`（KPI）＋`historical_design_record`（変更理由） | 版と版の比較。1つのpredicate置換であることはmanifestの`scope`から確定できるが、**そのpredicate単独の効果量は測っていない。またこの比較には同一比較内の経路診断がない**（R11-3） | ablation |
| R7-8 | 7.4b | C71はC43比でtoken中央値`-29.19%`、所要時間`-10.59%`、70件token合計`-31.18%`、品質`4 = 70`維持 | resultのKPI差 | 層B result | 層B | `same_condition_observation` | 同一key内の差分。所要時間は記述値。**同一比較内の経路診断はない**（R11-3） | 不要 |
| R7-9 | 7.4b | C81はC71比でtoken`-0.30%`、所要時間`+5.78%`、品質`4 = 70`維持。1回で出し切れた率はF04の`0 / 5 → 5 / 5`により`30 / 35 → 35 / 35` | C71 / C81 resultのKPI表と1-step closure診断表 | [C71 / C81 result](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md) | 層B `79ed04a4…` | `same_condition_observation` | 「安定化と所要時間の増加を同時に観測した」まで。因果は主張しない。数%の差は検定・信頼区間なし | 不要 |
| R7-10 | 7.4c | C104はC98比でtoken中央値`-6.48%`、所要時間`-9.77%`、品質70 / 70件が4点 | 一次resultのKPI差表 | [C104 result](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md) | 層C（v14 / CLI `0.146.0`） | `same_condition_observation` | 固定Standard14 `N=5`の記述差。一般的効果・採用を意味しない（result本文が明記） | 不要 |
| R7-11 | 7.4d | C116は`required outcome`と`implementation choice`を別状態に分け、A01とA02を安定分離した。Standard14は70 / 70件が4点 | 一次result、C125 root本文の該当predicate | [C118 result](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §6、C125 root `AGENTS.md.txt` §SPEC | 層C | `same_condition_observation`（Standard14 70 / 70）＋`historical_design_record`（分離の設計意図） | 「C112〜C115ではA01とA02を一つの条件で安定分離できなかった」はsynthesisの記述であり、本表では一次resultへ個別に当てていない | 文言限定 |
| R7-12 | 7.4d | C118はA02 `N=20`で20 / 20件が4点、確定後・変更前のコマンド再入`0 / 20`（C116は`5 / 20`・計7コマンド）。Standard14 tokenはC116の`1,599,779`から`1,718,725`へ`+7.44%`、所要時間は`982.872 → 841.648`秒（`-14.37%`） | 一次resultのKPI表と診断 | [C118 result](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | 層C（atomic reuse `N=5`） | `same_condition_observation` | **機構成立とcost改善が別であることを示す観測。tokenは低下していない。** result本文も「token増分はinput側にあり、command総数の増加では説明できない」と記録している | 不要 |
| R7-13 | 7.7 | C125はStandard14 70 / 70件が4点、token中央値`1,401,225`（C107目標`1,523,137`を`8.00%`下回る、C118比`-18.47%`、C122比`-0.19%`）、所要時間中央値`846.377`秒（C107比`-10.48%`、C118比`+0.56%`、C122比`+2.84%`）。F04誤停止`0 / 5`、F02一括取得`5 / 5`（token中央値`124,094`）、A02 `N=20`が20 / 20・再入`0 / 20` | 一次resultのKPI比較表・targeted mechanism節・A02節 | [C125 result](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)（result ID `96fb571308de4c08a7aeed0faefb7d72`） | 層C（atomic reuse `N=5`）。Standard14 70件のうち25件は登録済みatomic runの再利用、45件が新規実行 | `same_condition_observation` | `N=5`の観測。**C95が`N=5`を通過してB20で落ちた事例と同じ証拠水準であり、実際にC125自身が30件/caseで5件落ちた**（R9-4）。したがって「F04の誤停止を解消した」は`N=5`の範囲に限る。 「全指標がC122より改善」とは言えない（所要時間`+2.84%`）。数%の差に検定・信頼区間なし | 同条件追加反復（B20） |
| R7-14 | 1.6, 7.6, 12.2 | 境界の追加順序、同時追加、ablationは測っていない。したがってこの順序が必要条件であるとも、各境界が単独で必要であるとも、集合が最小であるとも主張しない | 該当resultの不存在 | `evaluations/results/`に順序入れ替え・同時追加・ablation条件のresultが存在しない | — | `unverified` | 「測っていない」ことの記述 | ablation |
| R7-15 | 7.4 | `synthesis`が記録しているのは**C81以降の系列がC125へ寄与した7件**である。**C125のroot本文は13 label**で、C43の9 labelにC69 / C71系の`DECISION_BOUNDARY` / `VALIDATION_CLOSURE`とC104以降の`EVIDENCE_GATE` / `VALIDATION_PLAN`が加わった構成である | root本文のlabel集合の照合とsynthesis | C43 root（9 label）、C71 / C81 root（11 label）、C125 root（13 label）の実体照合、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §結論 | bundle `60e95bfe7f…`ほか | `artifact_verified`（label集合）＋`historical_design_record`（系譜） | **7件はC125の全構成ではない。** C43（A1）とC71（A2）はsynthesisの7件に現れないが`SPEC`と`VALIDATION_CLOSURE`として本文に載っている。各制御の寄与分は分離していない | ablation |

### 2.8 第8節 効かなかった仮説

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R8-1 | 8.1, 14#5 | 表面量を操作した8件（**圧縮を主目的とした7件＋全文重複の対照C64 1件**）では、**静的量の減少が動的tokenの減少へ一貫して対応しなかった**（8件中7件で増加または実質不変）。この系列が示すのは、静的なバイト数を動的実行量の代理指標として使用できないことである | 各候補の一次result | C32 / C49 / C54 / C64 / C65 / C66 / C67 / C68の各result、[`candidate-history.md`](candidate-history.md)、[`control-mechanisms.md`](control-mechanisms.md) | 候補ごとに異なるkey・課題範囲・集計軸 | `descriptive_cross_layer` | **効果量の横断比較は行わない。** 中央値・70件合計・単一課題F10が混在し、互換キーと候補系列も異なる。**「判定条件を1つ足した候補は`26`〜`30%`削減した」を同じ比較の中に並べない**（別campaign・別条件）。**またC64は圧縮候補ではないため「表面圧縮を主目的とした8件」とは書かない** | 既存データ再解析（同一集計軸への再集計） |
| R8-2 | 8.2 | 委譲条件の細分化（C82〜C89）は工程分解の誤りを修復しなかった。C87はD01で親候補比token`-51.06%`だがStandard14全体ではC81比token`+6.09%`、所要時間`+1.35%` | 一次resultとsynthesis | [C81 / C87 result](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §2、[`research-backlog.md`](research-backlog.md) §2 | 層C（Standard14）／D01は別case set | `same_condition_observation`（C81 / C87 Standard14）＋`descriptive_cross_layer`（D01との並置） | 局所改善と全体コストの乖離まで。`-51.06%`はC86比であり、Standard14の`+6.09%`と同一比較ではない | 不要 |
| R8-3 | 8.3 | 実行環境側の性質を指示書へ書いても成立しない。C96は成功時stdoutが全5件でモデルへ返り、C97は全5件で成功後に別の`git status`を発行した（completion closure `0 / 5`） | 一次resultと診断 | [synthesis](candidate81-candidate125-control-findings-synthesis.md) §3、C96 / C97の各result、[`candidate97-decision-round-closure-design.md`](candidate97-decision-round-closure-design.md) | 層C | `same_condition_observation`（各`N=5`） | 各`N=5`の観測。「promptで一切制御できない」ではなく「この条件で狙った投影・締めが成立しなかった」まで | 不要 |
| R8-4 | 8.4 | **少数反復の通過は分布の裾にある低頻度欠陥を除外しない。** C95は`N=5`を通過したがB20（1,400回）で`4 / 2 / 1 = 1,398 / 1 / 1`。token`+4.49%`（Holm補正後`p=0.002325`）、所要時間`+5.53%`（`p=0.000019`）でC81より有意に悪化。C81側は`1,400 / 1,400`が4点。command protocol violationはC95のみ19件 / 10 run（McNemar `p=0.001953`） | B20 resultの品質表・検定結果 | [B20 result](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md) | 層C B20 `c5bfcd6d…`。実行順を奇数batch C81→C95、偶数batch C95→C81で交互化 | `repeated_observation` | 本研究で検定を適用した唯一の比較。score `4`件数の差2件はMcNemar `p=0.5`で有意ではないが、事前品質gateは4点未満を1件も許容しない。**「効率改善の代償」の例としてC95を使わない。C95はC81比でtoken`+4.49%`・所要時間`+5.53%`であり効率を改善していない。** **C71を「効率改善の代償が裾に現れた例」として`+3`件の規模で引用しない**（R8-8。補正後に残るのはA01 1件で、一般的トレードオフの確立には足りない）。**一方、品質と実行量のトレードオフ自体はC33で同一条件内に観測されている**（R11-4）。したがって**「本研究は効率改善が品質低下を伴った比較を確立していない」とは書かない** | 不要 |
| R8-5 | 8.5 | 量による証拠の打ち切りは成立しない。C123は正常なdetached HEADを未確定と誤分類し、C124はF04の誤停止を2件出しF02の一括取得も崩した | 一次resultとsynthesis | [synthesis](candidate81-candidate125-control-findings-synthesis.md) §7、[`candidate123-preterminal-result-round-closure-design.md`](candidate123-preterminal-result-round-closure-design.md)、[`candidate124-incomplete-content-continuation-design.md`](candidate124-incomplete-content-continuation-design.md) | 層C | `same_condition_observation`（各targeted `N=5`） | 各targeted `N=5`の観測 | 不要 |
| R8-6 | 9.1, 9.2 | 抽象的な成果条件を採点側で特定コマンドへ具体化すると実体のない減点が出る。C71 B18のA02 score 3の4件のうち3件がこのずれだった。v13で塞ぎ、v14で`not_required_unless_model_visible`として明文化した。同型の事例がClick側でも1件（A01の`resilient_parsing`字句監査で4件） | 個別事例の分析と契約本文 | [`a02-rating-divergence.md`](a02-rating-divergence.md)、[C69 / C71 B18 result](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)、[`v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json)、[Click C125 result](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md) | B18はv12。Clickは別instance・別rating | `artifact_verified`（契約本文）＋`same_condition_observation`（事例）＋`interpretive_synthesis`（偏りの方向） | 「この偏りは効率化された側を不利にする方向を持つ」は2事例からの解釈である。偏りの大きさは定量化していない | 不要 |
| R8-7 | 8（冒頭） | 失敗候補を直系継承せず、最後に成立した親（C122）へ戻して成功predicateだけを別軸で再検証した | manifestの`baseline_identity`と系譜 | `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1/manifest.json`（`baseline_identity` = C122）、[synthesis](candidate81-candidate125-control-findings-synthesis.md) 設計原則8 | bundle実体 | `artifact_verified`（系譜）＋`historical_design_record`（方針） | **「指示書の中身と同じくらい結果に効いた」とは書けない。** 直系継承した場合との比較を測っていない。「系列管理上の採用方針になった」までに限定する | 文言限定（本文8.7で修正済み） |
| R8-8 | 9.1, 14 | B18（v12）の当時の分類「C71はC69比で実質的な低得点が3件多い」は、現在の解釈では維持されない。**C69の実質欠落1件もC71の3件と同じ`git diff --check`未実行であり、v13解釈では両者ともこの分が「要求と採点のずれ」へ再分類される。** 提示条件に照らした実質的な低下として残るのはC71のA01 1件だけである | B18 resultの意味確認表と後続の個別事例分析 | [B18 result](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)（C69 A02 実質欠落1件・C71 A02 実質欠落3件がいずれも`git diff --check`未実行）、[`a02-rating-divergence.md`](a02-rating-divergence.md)（3件は「本物の品質低下とは言えない」） | B18はv12。再分類はv13解釈の適用 | `artifact_verified`（両resultの失敗内容の一致）＋`interpretive_synthesis`（v13解釈の遡及適用） | **当時の判定と保存済みresultはin-placeで書き換えない。** C71の評価状態は`standard14_b18_evaluated / stopped`のまま、release artifactの未解決risk 2件も保持する。**補正後に残る差はC71のA01 1件である。これは効率改善と同時に観測された低頻度の品質未達の一観測ではあるが、1件だけから一般的な品質・効率トレードオフを確立するものではない。** 「C71は1,260回で実質欠落が`+3`件」と書かない。**なお「本研究は効率改善が品質低下を伴った比較を確立していない」とも書かない**（C33が同一条件内の反例。R11-4） | 文言限定（本文8.6・14#9で対応済み） |

### 2.9 第9節 後続設計

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R9-1 | —（本文から削除） | C81以降の系列は**7つ**の軸へ分解された探索として読める | synthesisの系列見取り図と各result | [synthesis](candidate81-candidate125-control-findings-synthesis.md) §系列全体の見取り図、[`candidate-history.md`](candidate-history.md) | 層C | `interpretive_synthesis` | 軸の分類は本論文とsynthesisの整理である。番号順の系譜ではないことはmanifestの`baseline_identity`から確認できる | 不要 |
| R9-2 | 7.7 | C125は現在の設計到達点であり終点ではない。Standard14 B20未実施、**`N=100`追試は実施され`n100_execution_stopped`で停止（pool 30件/caseでF04にscore `2`が5件）**、一次結果は`adoption_not_decided`で、別状態として`adopted / release_projected / runtime_projected`が記録されている | resultのstatus、synthesis、採用判断 | [C125 result](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) §結論のstatus列、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §現在状態と残るrisk、[`candidate125-adoption-decision.md`](candidate125-adoption-decision.md)、[C125 N=100追試停止result](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md) | 層C | `artifact_verified` | 状態の記述。**採用は`N=5`通過を長期安定性の確定として扱ったものではない。またC125を「成立した設計」として記述しない**（R9-4） | 同条件追加反復（B20） |
| R9-3 | 12 | 現在残るriskは、C125 B20未実施、**`N=100`追試の停止とF04の未解決残余欠陥**、Terra / Luna未採用、`CONTEXT`・`RECOVERY`ペンディング、部分曖昧・長期タスク未着手、model / CLI更新時の再測定範囲未着手、Claude Code CLI系列保留である | backlogとsynthesisの状態表 |[C125 N=100追試停止result](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md)、[`research-backlog.md`](research-backlog.md) §状況サマリー、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §現在状態と残るrisk | — | `artifact_verified` | 記録された状態の列挙 | 不要 |
| R9-4 | 7.7, 12.5, 14#10 | C125の`N=100`追試は2026-08-01に実施され完了しなかった。pool各case 30件（計420 run）でF04にscore `2`を5件確認し、N=50 batchを中断した。全体`415 / 420`、F04`25 / 5`、他13 case`390 / 0`。失敗経路は共通で、証拠は足りていたが、正しい変更と開始状態に存在しない値を前提とする不要な変更を同一patchへ入れpreimage不一致で失敗した。後続候補C126はF04 `N=5`で`4 / 2 = 3 / 2`となり停止（誤patchは`0 / 5`へ消えたが誤停止が2件） | 追試resultのpool分布・失敗経路分析、後続候補result | [`C125 N=100追試停止結果`](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md)、[`C125 / C126 F04 targeted結果`](../evaluations/results/candidate125-candidate126-criterion-bound-change-input-v14-medium-f04-atomic-n20-cli0146_2026-08-01.md) | 層C（atomic pool `9437d24c…`。prompt / set / case / fixture / TaskSpec / rating / model / reasoning / runtime / CLI / permission / executor / token accountingをrun単位で固定。`N`・iteration集合・coverage・計画順序はexecution provenanceへ分離） | `same_condition_observation` | **正式な`N=30 result`ではない**（case別30件を固定するselection receiptと集約analysisを作成していないため、pool member数として報告する）。中断したN=50 batchの54 attemptは分布・pool countへ含めない。**C125の既存`adopted / release_projected / runtime_projected` stateをこの結果で履歴上書きしない。** 原因はmodel-visibleな判断の誤りであり、executor変更を解決策にしない | 同条件追加反復（正式な`N=30` / `N=100` selectionの作成） |

### 2.10 第10節 modelおよびtargetへの依存

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10-1 | 12.6 | 全評価結果は`gpt-5.6`系列 / Codex CLIであり、Claude系modelでの測定は0件である | 全resultのmodel欄 | 各result §固定条件、[`research-backlog.md`](research-backlog.md) §8、[`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md) | — | `unverified`（Claude系） | 「0件」の記述 | 別model / CLI |
| R10-2 | 10.1 | C125のmodelだけを変えると、Terraは68 / 70（token`+23.81%`、所要時間`-12.73%`）、Lunaは67 / 70（品質`-7.143`、token`+136.06%`、所要時間`+13.29%`）。Lunaの未達3件はすべてA01でrequired value未解決のまま試験へ進み、1回あたり`650,395`〜`870,391` tokenを使った | 一次resultのKPI表と未達内訳、preflightの機械照合 | [model軸 result](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md)（Sol `96fb5713…` / Terra `b328615b…` / Luna `0736e412…`） | modelはkeyに含まれるため3 resultは互換キーが異なる。preflightで`$.comparison_conditions.model`と`$.profile_id`以外の差分がないことを機械照合 | `descriptive_cross_layer`（KPI差）＋`same_condition_observation`（条件の機械照合） | 「同一系列内の3 model・各`N=5`で維持されなかった」まで。「model一般への依存」ではない。**「C43が閉じた境界がLunaで再び落ちた」は、A01の失敗形が同一（未解決値のまま試験へ進行）であることに基づく解釈である** | 文言限定 |
| R10-3 | 10.2 | Click側でC81はcontrol-free比token中央値`-28.79%`、所要時間`-12.62%`、品質70 / 70件が4点。モデルステップ`-35.06%`、キャッシュ済み入力`-33.92%`。変更前の履歴探索はcontrol-freeの`0 / 10`に対しC81が`4 / 10` | 一次resultと残余経路分析 | [Click C81 result](../evaluations/targets/click/results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md)、[`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md) | Click instance、CLI `0.144.0`、instance固有rating | `same_condition_observation`（Click instance内） | Click内での比較。`quality_score`の絶対値をinstance間で比較しない（`evaluations/CLAUDE.md`の規則） | 不要 |
| R10-4 | 10.2 | C125本文を1バイトも変えずにClickへ移すと`70 / 70`が有効、分布`4 = 65` / `1 = 5`、品質中央値`94.643`、token中央値`1,348,515`、所要時間`786.007`秒。`1`点の5件はすべてF10で`authority_unavailable`停止 | 一次resultの全体結果表 | [Click C125 result](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md)（result ID `7560599fef024dfb8011264352707ab8`）、[`click-c125-full-portability-design.md`](click-c125-full-portability-design.md) | Click C125 `39dcb70f…` | `same_condition_observation` | 「停止境界という機構は別リポジトリでも作動した」まで。**14課題全体の成功は成立していない。** 停止が正しい挙動であるという読みは、事前に採点契約へ組み込んでいない | 同条件追加反復（正本をそろえた条件）＋新case family（停止を成功と判定するrating revision） |
| R10-5 | 10.2 | Click C81（CLI `0.144.0`）とClick C125（`0.146.0`）は互換キーが一致しないため、tokenと所要時間の差は算出できない | 両resultの固定条件 | Click C81 result、Click C125 result（「compatibility keyが異なるため、tokenとelapsedの差は算出しない」） | — | `artifact_verified` | 比較不成立の記述 | 同条件追加反復（現行CLIで両者を再実行） |
| R10-6 | 12.6 | 未知のtarget一般への移植性は示していない。ClickはC125に対する独立な外部検証集合でもない | 測定範囲とClick観測の設計利用 | [`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §7 | — | `unverified` | 「示していない」の記述 | holdout target |

### 2.11 第11節 考察

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R11-1 | 11.1 | Baselineの各工程について、runtimeで残った制御と、評価課題集合で維持確認する品質責務を分けて対応づけられる。**責務は3分類になる。(a) root predicateへ移った、(b) runtimeから削除され評価課題集合で能力・禁止境界を確認している（レビュー、範囲逸脱・reward hacking・完了偽装の防止）、(c) runtimeから削除され現行評価集合でも同等能力を確認していない（監査・レビュー指摘に基づく自動再修正ループ）。評価課題集合はruntime mechanismではなく、実装runごとのレビューまたは独立監査の実施を保証しない** | Baseline本文とC125本文の対応、および4 Layerの境界定義 | Baseline root `AGENTS.md`・`orchestration-process.md`・4ロールプロンプト、C125 root `AGENTS.md.txt`、Standard14のF10×2、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §4 Layer | bundle実体＋基盤規則 | `artifact_verified`（rootに対応制御が存在しないこと、4 Layerの分離）＋`interpretive_synthesis`（対応表） | **対応表は本論文が構成した解釈である。** 各行が「意図的な置換」として記録されているのはC35 / C43 / C118などの個別manifestに限られ、全体を1つの変換として設計した記録はない。**「レビューSAの責務は評価集合へ移った」とは書かない**（Layerが違う）。**同じ限定は監査SAにも適用する。** `VALIDATION_CLOSURE` / `VALIDATION_PLAN` / `TERMINAL`が担うのは必須検証の発行・結果のbind・terminal判定であり、独立した契約準拠監査、reward hackingの敵対的検出、範囲逸脱の第三者判定と同じではない。`CONTEXT`は継承範囲のpredicateであり、独立監査主体が存在しない状態で情報非対称性そのものを再現するものではない。`PRODUCER`はrootが実装と検証双方のproducerになる経路を禁止していない。**さらにBaselineの自動再修正ループ（監査停止指摘・レビュー重大指摘を起点とする最大5回の差し戻し）と`RECOVERY`（`environment-only repair + same required command rerun`）は置換の関係ではない。** 前者は常設ループごと削除され、後者は別種の境界である。`machine_rework_max=1`は評価caseのTaskSpec契約であり実行時ループの代替ではない | 文言限定（本文11.1の限定(1)〜(4)、RECOVERY行の分割、11.2の拡張で対応済み） |
| R11-2 | 11.2 | Baselineは品質責務と工程を同じ文章で表現しており、工程への経路を外すと責務も落ち、責務を守るために不要な工程を払い続ける状態だった | R6-1（経路を外すと責務が落ちる）、R5-3 / R5-4（不要な委譲） | 層B result、`v3-all-agent-token-reaccounting`、`baseline-candidate1…candidate5` result | 層B・層A | `interpretive_synthesis` | 2種類の観測の統合による解釈。単一実験による検証ではない。**CFR（経路の非活性化）とC35（静的artifactの除去）を混同しない**（R6-2） | 不要 |
| R11-3 | 11.4 | **本節が扱うのはall-agent tokenの低下である**（`quality_score`は制約、`elapsed_seconds`は記述的副指標）。条件1〜3（品質制約下でall-agent tokenが低下）を満たすのは表Aの5組。**そのうち条件4〜5（同一比較内の経路診断）まで満たすのはC98→C104、C118→C125、Click control-free→C81の3組だけである。Baseline→C43とC43→C71は同一比較内の経路診断を持たない。C116→C118はtokenが`+7.44%`、所要時間が`-14.37%`でKPIの方向が分かれるため表Bへ分ける。**「KPIが低下していない」とは書かない**（3 KPIのうち所要時間は低下している）** | 各比較のKPI・分布・診断値、および診断値の出所campaign | 該当する各一次result（R7-7、R7-8、R7-10、R7-12、R7-13、R10-3）。C69 / C71のB18は[B18 result](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md) | 各層内。B18はv12・別候補対・別campaign | `same_condition_observation`（各比較個別）＋`interpretive_synthesis`（5条件という枠組み） | **C69 / C71のB18の診断値（tool call `-30.16%`、モデルステップ`-26.54%`）をC43→C71の経路分解として使わない。** 比較元候補・rating revision・campaignがいずれも異なる。表を「表A: 品質制約下でall-agent tokenが低下した比較」と「表B: KPIの方向が分かれた機構成立」へ分け、表A内でも経路診断の有無を列で区別する。**要旨の一般化も「品質制約下でall-agent tokenが低下し、かつ同一比較内の診断値またはtraceが整合する比較では」へ限定する。「KPIが低下した」と一括せず、tokenと所要時間を常に別記する**（表AのC118 → C125は所要時間`+0.56%`） | 文言限定（本文11.3の表A / 表B分離と要旨の限定で対応済み） |
| R11-4 | 11.4 | **品質と実行量のトレードオフが同一条件内で観測された例。** C33はC32比でall-agent token中央値`-24.63%`（`-959,484`）だが`quality_score`中央値も`-6.250`低下した | 一次result | [C33 result](../evaluations/results/candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)、[`control-mechanisms.md`](control-mechanisms.md) メカニズム2 | 層A系（拡張12課題、旧rating） | `same_condition_observation`（当該key内） | この条件の観測。層Bの数値と連結しない。**品質制約を外した削減が品質を損なった例として結論9で引用する。ただし裾の低頻度欠陥の例ではない**（`N=5`の中央値差である） | 不要 |
| R11-5 | 11.4 | 正味token差 = 制御文の読解cost + 追加された判断・確認cost − 回避できた探索・context継承・再読・再試行・手戻りcost | 各系列の符号の一致 | [`prompt-control-design-principles.md`](prompt-control-design-principles.md)、既存論文第10節、R8-1 / R7-8 / R8-4 | 複数層 | `interpretive_synthesis` | **観測されたtoken差を解釈するための概念モデルであり、各項を独立に計装したものではない。「どの項が支配的だったか」は測定結果ではない** | 計装追加 |
| R11-6 | 11.3 | 指示書が制御できるのは、返された結果をどう分類し次に何を選ぶかまでである | R8-3 | 8.3 | 層C | `interpretive_synthesis` | **「指示書が制御できるのは〜までである」と断定しない。** 「本研究で試した条件では、指示書単独で安定して制御できたのは返された結果の分類と後続行動の選択までだった」まで。C90〜C97・C105〜C111の失敗範囲であり、「原理的に不可能」ではない | 対象外（runtime強制の実装はこのリポジトリの範囲外） |
| R11-7 | 11.5 | 制御はmodelと実行環境へ強く結合しており、CLI版更新で比較が失効し、model変更で品質とコストが維持されなかった。B20の概算は1条件約`$311`、2条件約`$622` | R10-2、R10-5、換算単価による外挿 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、[`research-backlog.md`](research-backlog.md) §12 | — | `descriptive_cross_layer`（結合の観測）＋`derived_arithmetic`（費用外挿） | 金額は換算値の線形外挿で、実測でも実請求額でもない。人間の時間を含まない | 不要 |
| R11-8 | —（補助指標の節は本文から削除） | 料金換算では14課題×5回ぶんがBaseline `$91.6701`、0バイト対照`$25.1562`、C125 Sol `$15.5472`、Terra `$6.5447`、Luna `$0.9571`。同一互換キーで成立する比較はBaselineと0バイト対照（`3.64倍`）だけである | 換算の集計と単価、各条件の互換条件 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、各一次resultのtoken内訳 | Baselineと0バイト対照はv13 / CLI `0.144.0`（同一key）。C125系はv14 / `0.146.0` | `same_condition_observation`（`3.64倍`）＋`descriptive_cross_layer`（他の行） | **補助指標であり研究の指標ではない。** C125の`0.62倍`（`-38.20%`）を制御による費用削減として読まない。単価に依存し実請求額でもない | 同条件追加反復（v14 / CLI `0.146.0`での0バイト対照） |
| R11-9 | 11.6 | 移行の設計指針を「書き換える／先に書く／書かない／削らない」の4区分で整理した表。各行はR6-*・R7-*・R8-*・R11-4の既存Claimの再掲であり、新しい主張を追加しない | 参照先Claimの一次result | 各行の根拠列に示した節（6、7.2、7.4a〜7.4e、8.1〜8.5、11.4、4.6、10.1、10.2） | 各行の根拠Claimに従う（同一比較ではない） | `interpretive_synthesis`（4区分への分類と実務向けの言い換え） | **一般的な設計原則としては提示できない。** 単一対象・単一モデル系列・14課題の範囲で、各行の根拠となった比較が保存されているという意味の指針にとどまる。単文ablationがないため個々の記述の寄与は分離していない。**指示書の内容単独の指針ではなく、指示書とモデルの組についての観測である**（R10-1）。表内の率は互換キーが異なるため行間で大小比較できない（R7-1） | ablation（原因性を主張する場合）／別model・CLI（組への依存を外す場合） |
| R12-2b | 12.2 | 保存済みdiff 124件の事後符号化により、(i)軸が実行経路を閉じる述語と往復を閉じる述語の2操作を含み往復側は成立後にのみ現れる（0 / 33 対 33 / 91）、(ii)判定が符号化者に依存する（同一人物で33件中9件、規則との一致29 / 33）、(iii)経路を閉じた48件中37件が停止した | root `AGENTS.md`の親子diffと候補indexの状態 | [`branch-closure-retrospective-coding.md`](branch-closure-retrospective-coding.md)、各候補bundleの`files/AGENTS.md.txt`と`manifest.json`（`prompts/candidates/`配下） | 対象外（promptのみを入力とし、KPIを結果変数にしていない） | `artifact_verified`（diffと区間分割）＋`interpretive_synthesis`（符号化） | **軸の妥当性の検証ではない。** 符号化者は盲検ではなく、約15件のKPIを既知である。**成立前区間を独立検証群として使う設計は完了していない**（候補indexの状態語彙が区間で異なり、成立前33件に`stopped`が0件）。停止率の差を因果として読めない（停止理由が機械可読でなく、区間で問題の難度も異なる） | 対象外（保存済みデータでは独立検証群の検定が成立しない。第4節の留保23） |

### 2.12 第12節 限界

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R12-1 | 12.1 | Standard14は候補の生成・選別に繰り返し使ってきた課題集合であり、C125の`70 / 70`は未使用課題による独立確認ではない。Clickも独立な外部検証集合ではない | 基盤規則と設計利用の記録 | [`evaluations/cases/README.md`](../evaluations/cases/README.md)、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)（「tuningに使ったcaseを同一revisionのheld-out evidenceとして扱わない」）、[`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md) | — | `protocol_defined`＋`artifact_verified` | 反復適応を除外できないことの記述 | holdout target |
| R12-2 | 12.6 | 主targetは非公開1件、公開targetは`pallets/click` 1件で、後者では14課題全体の成功が成立していない | 各resultのtarget欄、R10-4 | 各result §固定条件、[`evaluations/targets/README.md`](../evaluations/targets/README.md) | — | `artifact_verified` | 測定範囲の記述 | holdout target |
| R12-3 | 12.5 | 最大反復は1,400回（B20）。C125はB20未実施。`N=100`追試は実施され30件/caseで停止した。`70 / 70`（`N=5`）はC95がB20で落ちた事例と同じ証拠水準にあり、**実際に同型の現象がC125自身で起きた**（R9-4） | B20 resultとC125 resultのstatus | [B20 result](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md)、[C125 result](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md)、[C125 N=100追試停止result](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md) | 層C | `artifact_verified` | 証拠量の記述。C81のB20で代替しない | 同条件追加反復 |
| R12-4 | 12.6 | 14課題はすべて単発で、部分的に曖昧な長期作業のcaseもevaluation setも存在しない。この未測定領域は実務利用（対話形態）に当たる | 該当caseの不存在とbacklogの記述 | [`research-backlog.md`](research-backlog.md) §11 | — | `unverified` | 未測定であることの記述 | 新case family |
| R12-6 | 12.5 | 信頼区間、課題ブロック考慮の効果量、課題別の反復分布は算出していない。検定を適用したのはB20規模のC81 / C95比較だけである | 各resultの統計記述 | 各result（検定はB20 resultのみ）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) | — | `artifact_verified` | 統計処理の範囲の記述 | 既存データ再解析（保存済みiteration値からの区間推定） |
| R12-7 | 12.3 | 採点は独立した盲検の第三者ではなく、固定契約による監査である | 基盤規則と各resultの採点記述 | [`evaluations/cases/README.md`](../evaluations/cases/README.md) §採点、各result（「採点は独立blind quality raterによるものではない」） | — | `protocol_defined` | 採点方式の記述。契約欠陥の実例はR8-6 | 独立再採点 |
| R12-8 | 8.1 | 表面圧縮系列の動的量は集計軸が不統一で、候補間の横断比較ができない | 各候補resultの集計単位 | 各候補result | — | `artifact_verified` | 集計軸の不統一の記述 | 既存データ再解析 |
| R12-11 | 11.5 | 保守費用の概算は換算値の線形外挿で、実測でも実請求額でもなく、人間の時間を含まない | 換算方法 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md) | — | `derived_arithmetic` | 外挿であることの記述 | 不要 |
| R12-12 | 11.5 | 制御の便益（確認して止まる、誤停止しない、手戻りが減る、待ち時間が短い）を利用者側の価値として測っていない | 測定範囲 | 3 KPIの定義（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)） | — | `unverified` | 未測定であることの記述 | field study |
| R12-13 | —（補助指標の節は本文から削除） | `$25.1562`（v13 / `0.144.0`）と`$15.5472`（v14 / `0.146.0`）の差`-38.20%`は互換キーが違うため制御の効果量ではない | 両条件の互換条件 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、各一次result | — | `descriptive_cross_layer` | 並置にとどまる | 同条件追加反復 |
| R12-15 | 4.3, 12.4 | 所要時間はprompt差から分離されていない。`M=24`の共有待ち行列で実行順のランダム化・交互配置・時刻ブロック化をしておらず、負荷も記録していない。例外はC81 / C95 B20の交互実行だけである | 各resultの実行スケジュール記述 | 層B result（「5つの新規campaignは同時実行せず、Baseline、CFR、C5、C35、C43の順に実行した」）、B20 result（「奇数batchはC81→C95、偶数batchはC95→C81」） | — | `artifact_verified` | 交絡が残ることの記述。`elapsed_seconds`は記述値として扱う | 同条件追加反復（`M=1`および順序統制） |
| R12-17 | —（補助指標の節は本文から削除） | 指示書単体の注入コストは算出できない。キャッシュ済み入力`$2.4741`（総額の`15.91%`）は複数要素が混在した区分の換算額である | 換算の内訳 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、既存論文7.5節 | 層C（C125 Sol） | `derived_arithmetic`（区分総額）＋`unverified`（指示書単体） | 区分総額までが上限。root指示書の寄与は分離できない | 計装追加 |
| R12-20 | 冒頭注記 | この文書は仮組みであり、いずれの状態についても正本ではない | 文書の位置付け | 本文書の冒頭 | — | — | 記述 | 不要 |

### 2.13 第13節 結論

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再検証 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R13-1 | 14 | 観測した評価範囲では、擬人的な工程仕様全体を保持しないbundleでも品質制約を満たした。品質制約を維持しながら**all-agent token**を小さくした候補に共通していたのは、仕様・証拠・実装・検証・停止を実行時に観測可能な条件として表した境界である。`elapsed_seconds`はこの主張へ含めない | R5-*、R6-*、R7-*、R8-*の統合 | 上記すべて | 複数層（連結しない） | `interpretive_synthesis`（統合）＋`same_condition_observation`（各層内のKPI） | **「品質を支えていたのは境界である」という排他的な因果主張はしない。** 品質を支える要素にはmodelの既定能力、TaskSpec、path別`AGENTS.md`、repository authority、fixtureと対象リポジトリの状態、executorの挙動が残る。**「評価範囲内では」が必須の限定である**（Standard14（反復適応あり）、`gpt-5.6-sol`、Codex CLI、単発作業）。**C125の正式なStandard14集約結果は`N=5`である。これとは別に、未完了の`N=100`追試poolで各case 30件まで実行され、F04の品質未達5件が観測されている（R7-13）。正式な`N=30`結果ではないが、低頻度欠陥が存在しないとはいえない** | ablation＋同条件追加反復＋holdout target＋独立再採点 |

---

## 3. 既存証拠では接続できない主張（再検証候補）

以下は、論文仮組みの中で**主張として書けなかった**か、**限定付きでしか書けなかった**接続である。本文では該当箇所に留保を置いている。

| # | 接続したい主張 | 現在言えること | 不足している証拠 | 再検証分類 | 概算規模 |
| --- | --- | --- | --- | --- | --- |
| 1 | C125の失敗頻度と参照条件との差を正式に評価できる | **低頻度欠陥の有無は既に判明している。** 正式な集約は`N=5`で`70 / 70`だが、未完了の`N=100`追試poolで各case 30件まで実行され、F04で品質未達5件が観測された（正式な`N=30`結果ではない）。同じ証拠水準のC95はB20で2件落ちた | 比較条件を正式に固定したうえでの失敗頻度の推定と、参照候補との差の評価 | 同条件追加反復 | 標準14項目B20、1条件1,400回、換算約`$311` |
| 2 | 品質境界を閉じたうえで費用も下げた | v13 / CLI `0.144.0`の0バイト対照と、v14 / `0.146.0`のC125の換算額を並置できるだけ | 同一互換キーでの0バイト対照 | 同条件追加反復 | 標準14項目`N=5`、70回、換算約`$16`相当 |
| 3 | 各境界は単独で必要である／境界集合が最小である | 版と版の差までしか言えない | 境界ごとの除去条件。**何をablationするかを先に定義する必要がある**（9ファミリー＝630 run、C81以降の寄与7件＝490 run、13 label＝910 run。複数の制御を同じlabelへ統合しているため、単純なlabel単位ablationが妥当かも別途定義が必要） | ablation | 定義次第で490〜910 run |
| 4 | 境界を閉じる順序に必要性がある | 実際に開発が進んだ順序である | 順序入れ替え条件、同時追加条件 | ablation | 条件数に比例 |
| 5 | 指示書は別リポジトリへ移植できる | 停止境界という機構は再現した。14課題全体の成功は成立していない | 正本をそろえたClick条件、および未使用リポジトリ | 同条件追加反復＋holdout target | Click再測定70回＋新target構築 |
| 6 | Click F10の停止は正しい挙動である | 現行契約はscore `1`と評価している | 停止を成功と判定する条件を事前に組み込んだrating revisionと再測定 | 新case family | rating revision＋70回 |
| 7 | 仕様確定の境界は長期・部分曖昧タスクでも働く | 単発課題での観測しかない。該当caseが存在しない | 部分曖昧・複数段のcase family、誤停止と過剰問合せを区別する採点条件 | 新case family | case family設計＋rating revision＋反復 |
| 8 | 制御はmodel系列を跨いで移る | 同系列3 modelで維持されなかった。Claude系は0件 | 別model系列での測定 | 別model / CLI | Claude Code CLI adapter実装（現在保留）＋70回 |
| 9 | 採点は採点者依存でない | 固定契約による監査である。契約欠陥の実例が2件ある | 独立した第三者採点者による再採点 | 独立再採点 | 既存runの再採点（新規実行不要） |
| 10 | 表面圧縮候補の間で動的量を比較できる | 符号の不一致だけが読める | 全候補を同一集計軸へそろえた再集計 | 既存データ再解析 | 保存済みresultからの再集計（新規実行不要） |
| 11 | 指示書本文の注入コストが分かる | キャッシュ済み入力という区分の総額だけが分かる | 入力要素別のtoken計装 | 計装追加 | 計装実装＋再実行 |
| 12 | 委譲がall-agent tokenに占める比率（run単位） | 中央値同士の差の割合（56.4%）だけが算出できる | run単位の`descendant_tokens / all_agent_tokens` | 既存データ再解析 | 保存済みrolloutからの再集計（新規実行不要） |
| 13 | 収支の式の各項が実測されている | 観測されたtoken差を解釈する概念モデルである | 読解cost・追加判断cost・回避costの項別計装 | 計装追加 | 計装実装＋再実行 |
| 14 | `N=5`条件間の数%差がノイズと区別できる | 検定・信頼区間を算出していない | 反復間分布からの区間推定、または反復数の増加 | 既存データ再解析（区間推定）／同条件追加反復（検出力） | 保存済みiteration値からの再解析 |
| 15 | Baselineの工程と判定条件が1対1に対応する（当時の設計として） | 本論文が構成した解釈である | 変換を1つの設計として記録したartifact（存在しない） | 文言限定 | — |
| 16 | 「9つの品質責務」がBaseline作者の意図した分類である | 本論文が本文から抽出した整理である | 当時の責務列挙artifact（存在しない） | 文言限定 | — |
| 17 | 実装runごとのレビュー工程・独立監査がruntimeで保証されている | 常設工程は削除され、rootに対応制御はない。F10と各caseの禁止境界は評価範囲の品質制約である | runtime側のレビュー／独立監査の起動機構 | 対象外（TaskSpecとruntimeの領域。11.2節） | — |
| 18 | 制御の便益が保守費用に見合う | どの制御が何を変えたかまで | 実務利用における利用者価値の測定 | field study | 測定設計から必要 |
| 19 | Baselineの実務利用件数、運用期間、対象タスク範囲、実務成果の品質がどの程度だったか | 公開artifactの存在・blob一致・THE-CAPTION overlay・運用観測に基づく改訂履歴は**検証済み**（R1-7a）。利用の規模と成果だけが未検証 | 運用記録、成果記録、研究用評価と独立した品質記録 | 文言限定（著者提供前提である旨の明示）／または運用・成果記録の追加 | — |
| 20 | 監査・レビュー指摘に基づく自動再修正（差し戻し・再監査・再レビュー）の能力が維持されている | 常設ループは削除され、`RECOVERY`は別種の境界である。`machine_rework_max=1`は同じ責務ではない。**runtimeにも評価課題集合にも同等形がなく、能力は未測定である** | 差し戻しループの能力を測るcase | 新case family | case family設計＋rating revision＋反復 |

---

## 4. 一次資料と要約文書の相違・留保

一次資料を正本として確認した結果、要約文書の記述に対して補正または留保が必要な箇所を記録する。**過去のartifactはin-placeで変更していない。**

> **番号について**: 留保1・留保2は本文からの参照が確定する前に統合され、欠番である。既存の参照を保つため番号を繰り上げていない。

### 相違1: `ControlFreeRepository`に残っているものの記述

- **既存論文の記述**（3.1節、付録A.2、第14節の限界16）: 「root `AGENTS.md`だけを0バイトにし、配下ディレクトリごとの指示書4件はそのまま残した対照（TaskSpecと実行環境設定も残る）」
- **一次資料**: `the-caption-3ce91a4-control-free-repository-r1/manifest.json`と`the-caption-3ce91a4-current-r2/manifest.json`のtarget別SHA-256を照合すると、差分targetは`AGENTS.md`のみ。すなわち`docs/orchestration-process.md`（24,209 bytes）、`docs/prompt-guide.md`（15,421）、`docs/glossary.md`（4,086）、`prompts/plan.md`（4,183）、`implement.md`（2,128）、`audit.md`（5,161）、`review.md`（3,910）も**Baselineと同一のまま残っている**（合計59,098 bytes）。
- **補正**: 既存論文の記述は誤りではないが不完全である。この条件は「擬人的な工程仕様が置かれたまま、それを呼び出すrootの制御だけを外した状態」である。仮組みでは6.1節・11.2.1節・12.10節でこの内訳を明示した（R6-2）。
- **解釈上の帰結**: `-70.80%`というtoken低下は、工程仕様の文書量が減ったことによるものではない。**文書が存在しても、rootの制御がその工程へ入らなければ実行量は生じない**という読み方が可能になる。
- **CFRとC35を混同しない**: CFRは経路の非活性化（文書は残す）、C35は静的artifactの除去（内容を空にする）である。両者は別の操作であり、仮組み11.2.1節でこの区別を明示した。

### 相違2: C35の工程仕様の状態

- **既存論文の記述**（3.1節）: 「rootの実行制御は残し、旧来の役割説明や手順説明は見出しだけの空の受け皿に置き換えた」
- **一次資料**: 該当7 targetは`0`バイト（`git_blob_sha1: e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` = 空blob）である。「見出しだけの空の受け皿」ではなく**完全な空ファイル**である。
- **補正**: 仮組みでは7.2節で0バイトと明記した（R7-5）。なお`non_goals`に「bundle target数の削減または削除tombstoneの導入」が挙げられており、**targetを消さずに内容だけを空にした**理由は、bundle target集合を比較条件として固定するためである。

### 留保3: C35の置換根拠となったcommand evidenceはリポジトリ内にない

- C35のmanifestは「expanded12 × N=5の保存済み観測で成功commandから参照されなかった」と記録しているが、その根拠となるraw command evidenceは**外部のresult registry**にあり、このリポジトリへcommitされていない（基盤規則が「raw execution evidenceをrepositoryへcommitしない」と定めている）。
- したがってR7-5の証拠水準は`artifact_verified`（byte数と0バイト化）と`historical_design_record`（非参照の観測）の複合である。**非参照の観測そのものはmanifestの記述を信頼している。** 仮組み7.2節と13節#6でこの限定を明示した。

### 留保4: 「品質責務9項目」「工程対応表」は本論文の構成

- 1.3節の9項目、3.2節の「対応づけた責務」列、11.1節の変換対応表は、いずれもBaseline本文とC125本文から本論文が構成した整理であり、当時のartifactにこの分類として記録されているものではない。
- また、**9責務からStandard14を導出したという履歴も一次資料から確認できない。** Standard14の正本から確認できるのは、旧12項目へA01とA02を加えて14項目とし、版と評価境界を固定したことである。
- 該当Claim（R1-5、R3-1、R11-1）の証拠水準は`interpretive_synthesis`とし、再検証欄は「文言限定」とした。仮組みでは3節冒頭・3.1節・11.1節末尾でこの限定を明示した。

### 留保5: 設計記録は「人間の組織図の写し取りではない」と述べている

- `docs/prompt-guide.md`は分業を「人間の組織図の写し取りではない」「AI に存在しない制約を捨て、AI 固有の失敗様式に向けて作り直した統治の形」と明示している。
- したがって「人間の開発プロセスをそのままprompt化した」という表現は、**工程・成果物・関所の構造については成立するが、役割分担の設計意図については成立しない**。仮組みでは1.2節でこの区別を明示した（R1-3、R1-4）。
- **この留保は研究の論証を弱めない。** むしろ「AI固有の失敗様式へ向けて設計されたと当時考えられていた工程構造でも、AI実行としては不要な経路を含んでいた」という形で、問いを鋭くする。

### 留保6: Baselineの品質は3段に分けて記述する

- 既存論文と仮組み初版は「品質確保に成功した初期解」と断定していたが、これは後続評価で見つかった欠陥との関係を不明にする。一方「品質を出せていたとも言えない」は研究開始時点の到達を否定しすぎる。
- 仮組みでは次の3段へ統一した（R1-4、R5-2）。(1) 当時の認識、(2) 初期評価の事実（拡張12課題`58 / 60`が4点、品質中央値`100.000`）、(3) 後続評価の事実（Standard14でA01・A02・F07依存関係に残余欠陥）。

### 留保7: 独立監査の削除はレビューと同じ限定を要する

- 11.1節の対応表は、監査SAの行を`VALIDATION_CLOSURE` / `VALIDATION_PLAN` / `TERMINAL`へ対応づけている。しかしこれらが担うのは**必須検証の発行、結果のbind、terminal状態の判定**であり、実装者から独立した契約準拠監査、reward hackingの敵対的検出、範囲逸脱の第三者判定、実装経緯を遮断した完了偽装検査と同じではない。
- 同様に`CONTEXT`は継承範囲を制御するpredicateであり、**独立した監査主体が存在しない状態では、監査SAが持っていた情報非対称性そのものを再現しない**。`PRODUCER`もrootが実装と検証双方のproducerになる経路を禁止していない。
- 仮組みでは11.1節に限定(1)〜(3)を追加し、11.2節をレビューだけでなく独立監査へ拡張した（R11-1）。**レビュー工程について適用した限定と同じものを、監査工程にも適用する。**

### 留保8: 「境界」の数は3つの別集合を指す

- 研究過程で識別された境界ファミリー（**9件**、7.5節A）、C125のroot本文のlabel（**13件**、7.5節B）、`synthesis`が記録するC81以降の寄与（**7件**、7.7節）は別の集合である。
- とくにC43（仕様確定）とC71（validation closure）は`synthesis`の7件に現れないが、`SPEC`と`VALIDATION_CLOSURE`としてC125の本文に載っている。逆にC119とC122は7件に含まれるが、7.5節Aでは別ファミリー（A7 / A8）として数えている。
- **要旨と結論へ単一の「7つの境界」を置かない。** また**ファミリー一覧はKPI低下の一覧ではない**（A3は所要時間`+5.78%`、A6はtoken`+7.44%`、A8は品質`69 / 70`）。仮組みでは7.5節をA / Bへ分割し、要旨・13節#7でこの区別を明示した（R7-1、R7-15）。

### 留保9: 自動再修正ループと`RECOVERY`は置換の関係ではない

- Baselineの自動再修正は、監査SAの停止指摘とレビューSAの重大指摘を起点に実装SAへ差し戻す最大5回のループである（root `AGENTS.md` §停止と自動再修正、`orchestration-process.md` §自動修正ループ）。
- C125の`RECOVERY`が扱うのは`environment-only repair + same required command rerun`だけであり、監査・レビュー指摘に基づく実装修正ループではない。
- したがって11.1節の対応表を「回数による制御を状態による制御へ置換した」と書くことはできない。仮組みでは行を2つに分け、**監査・レビュー駆動の自動再修正ループは常設工程ごと削除された**こと、**`RECOVERY`は別種の環境recovery境界である**ことを明示した（R11-1、限定(4)）。
- `machine_rework_max=1`は評価caseのTaskSpec契約であり、実行時の自動再修正ループの代替ではない。

### 留保10: 「実務利用」は公開artifactで検証できる部分と、著者提供前提にとどまる部分へ分ける

**検証済み（`artifact_verified` ＋ `historical_design_record`、R1-7a）**

- `Kenn-dclxvi/orchestration-prompt`はPUBLICなリポジトリである（2026-06-14作成）。
- PR #18（2026-06-28 merged、head `28fddf7d2734daeca9b9e9756159460c2ec6b09c`）時点の`AGENTS.md`は blob `9d70bc48adc5699f4e986f2ae9bc79dbf623f8db`（5,980 bytes）で、**本リポジトリのBaseline manifestが記録する研究Baselineのroot `AGENTS.md`と一致する**。
- 同refに`overlays/the-caption/`が存在し、READMEが適用順と管理方針を定めている。
- PR #18本文は「プランSA（ケースE）が…実運用ではほぼ自律起動しなかった」を変更理由として記録しており、**運用上の観測に基づく改訂履歴**である。

**同時に確認した相違（R1-7aの表現上限）**

| target | 研究Baseline | 公開PR #18 head | 判定 |
| --- | --- | --- | --- |
| `AGENTS.md` | blob `9d70bc48…` | 同一（root / overlay とも） | 一致 |
| `prompts/{plan,implement,audit,review}.md` | 4 blob | overlay側と同一 | 一致 |
| `docs/prompt-guide.md` | `835aebcd…`（15,421 bytes） | 同一 | 一致 |
| `docs/orchestration-process.md` | `1a25c460…`（24,209 bytes） | `6cf63f29…`（22,203 bytes） | **不一致** |
| `docs/glossary.md` | `14bf17c2…`（4,086 bytes） | 存在しない | **欠落** |

適用は作業用クローンへ配置してから`THE-CAPTION`へマージする経路をとる。**そのうえで「研究Baseline bundle全体が公開されていた」とは書かない**（上表の不一致・欠落による）。

**依然として著者提供前提（R1-7b）**

利用件数、運用期間、対象タスクの範囲、実務成果の成功率、不具合・手戻り・レビュー品質、研究用評価と独立した品質記録は、公開リポジトリにも本リポジトリにも存在しない。

**参照する履歴点**: 現在の`orchestration-prompt/main`はその後の改訂を含むため参照しない。論文が参照するのは上記の固定refである。研究Baseline全体の正本は引き続き本リポジトリの19 path bundle（`the-caption-3ce91a4-current-r2`、`63225d2d…`）であり、**公開`orchestration-prompt`（汎用コア・公開系譜・改訂履歴）と入れ替えない。**

### 留保11: C71の「実質欠落+3件」は現在の解釈では維持されない

- B18（v12）の意味確認では、実質欠落がC69 1件・C71 4件（A02 3件＋A01 1件）と分類され、「C71側で実質的な低得点が3件多い」がC71の`stopped`判定の根拠の一つになった。
- しかし**C69の実質欠落1件もC71の3件と同じ`git diff --check`未実行である**（B18 resultの意味確認表）。`a02-rating-divergence.md`はこの型を「提示していない特定コマンドを採点側が必須化した要求と採点のずれ」であり「本物の品質低下とは言えない」と再分類している。
- したがってv13解釈を当てると、提示条件に照らした実質的な低下として残るのはC71のA01 1件だけであり、**「+3件」は維持されない**。仮組みでは8.6節にこの突き合わせを追加し、13節#9から「効率改善の代償」の例としてのC71を撤回した（R8-8）。
- **過去の判定・score・未解決riskはin-placeで変更しない。** C71の評価状態は`standard14_b18_evaluated / stopped`のままである。
- **ただし補正を広げすぎない。** 補正後に残る差はC71のA01 1件であり、これは効率改善（C69比token中央値`-26.14%`）と同時に観測された低頻度の品質未達の**一観測ではある**。1件だけから一般的なトレードオフは確立しないが、「引用できない」わけでもない。
- また、**品質と実行量のトレードオフ自体は別条件で観測されている**。C33はC32比でtoken中央値`-24.63%`かつ`quality_score`中央値`-6.250`である（同一compatibility key内）。したがって**「本研究は効率改善が品質低下を伴った比較を確立していない」とは書かない。** 3つを別々に扱う: C33 = 品質とtokenの明確なトレードオフ、C71 = 効率改善と同時に観測された低頻度tail failureの一観測、C95 = 少数反復ではtailを除外できないことの証拠。

### 留保12: 自動再修正の責務はruntimeにも評価集合にも同等形がない

- 11.1節の総括は3分類とした。(a) root predicateへ移った責務、(b) runtimeから削除されたが評価課題集合で能力・禁止境界を確認している責務、(c) **runtimeから削除され、現行評価集合でも同等能力を直接確認していない責務**。
- (c)に該当するのは「監査・レビュー指摘に基づく自動再修正ループ（差し戻し・再監査・再レビューを最大5回）」である。`machine_rework_max=1`は評価caseのTaskSpec契約であり同じ責務ではない。
- したがって**この責務を「評価課題集合側へ移った」と分類しない。** 再検証候補20として分離した（R11-1）。

### 留保13: 研究開始前の認識と研究開始後の測定を結合しない

- 研究の経緯は「(1) Baselineが到達点として先に存在 → (2) AI実行として最適かという疑問 → (3) 評価基盤と評価課題集合の構築 → (4) 初期測定」の順である。
- したがって**研究の中で得た拡張12課題の結果（`58 / 60`）を、研究開始時点でBaselineを初期解と考えていた根拠として使えない**。研究開始前の初期解という認識の根拠は著者提供の利用経験（R1-7b）である。公開artifactと改訂履歴はR1-7aが支えるが、**利用規模と成果は支えない**。
- 仮組みでは要旨・1.4節・5.1節・14#1をすべて「研究開始前の認識」「研究開始後の初期測定」の二段へ統一した。12.4節の「このリポジトリの実務利用は対話形態」も著者提供前提である旨を明示した（R1-4、R1-7）。

### 留保14: C125の`N=5`結果は30件規模で否定された

- 仮組みの初版はC125を「現在の設計到達点」とし、残riskをB20未実施と`N=100`未着手だけとしていた。**2026-08-01に`N=100`追試が実施され、pool 30件/caseでF04にscore `2`が5件出て停止した。**
- したがって「F04の誤停止を解消した」「70 / 70」は`N=5`の範囲に限る記述であり、**低頻度欠陥の不在を意味しない**。本文の1.6節・7.7節・11.5節・12.5節・14節#10へ反映した（R9-4）。
- 皮肉な整合として、本文が5.2節・12.5節で述べていた「`N=5`の通過は長期安定性ではない」という主張が、**C125自身の系列で実証された**。論証はこの結果で弱まらない。
- **過去の判定と保存済みresultはin-placeで変更していない。** C125の`adopted / release_projected / runtime_projected`は追試結果で履歴上書きしない。

### 留保15: 中心問いを「Baselineの品質の維持」として定義しない

- 本論文は品質制約を「各品質責務に対応する課題で減点が発生しない」と定義する（2.1節）。一方Baselineは、研究開始後の最初の測定（拡張12課題`58 / 60`）でもこの条件を満たしていない。
- したがって「Baselineによって得た品質を維持しながら実行経路を減らせるか」という問いは、操作的定義と一致しない。実際に行ったのは、(1) 責務の明示と評価課題集合との対応づけ、(2) 残余欠陥を閉じる、(3) その制約下でall-agent tokenを改善する、である。
- 仮組みでは中心問いを「**Baselineが守ろうとしていた品質責務を損なわず、評価で見つかった残余欠陥を閉じながら、AI固有の不要な実行経路を除去できるか**」へ変更した（R2-1）。**「品質を維持しながら」はC43以降の候補間比較に限って使う。**

### 留保16: 研究の出力を前提として引用しない

- 本稿の初期版は、リポジトリ内部の設計原則文書 [`prompt-control-design-principles.md`](prompt-control-design-principles.md) を「研究開始時点で固定されていた設計原則」として引用していた。**これは循環参照である。**
- `git log --follow`で確認すると、同文書の初版は**2026-07-19**（PR #43、Candidate41評価の記録時）であり、`evaluations/results/`の最初のcommitは**2026-07-14**である。すなわち同文書は研究開始より後、C11〜C40の観測から147行として書かれ、現行は298行である。文書自身が「Candidate43からCandidate125までの保存済み観測から得た**現時点の**設計原則」と宣言している。
- 初版に含まれるのは、分岐を先に消す方針、収支の式、品質と実行量の読み替え表である。**「失敗候補を直系継承しない」は同文書に存在せず**、出典は[`candidate81-candidate125-control-findings-synthesis.md`](candidate81-candidate125-control-findings-synthesis.md)の設計原則8である。本稿はこの誤帰属も訂正した。
- `future-roadmap.md`の初版は**2026-07-24**で、これも研究期間内である。
- 仮組みでは各引用箇所へ成立時期を明記し、**§12.2「前提と結論が分離していない」を新設して構造そのものを開示した**。ただし構造は解消していない。

### 留保17: 参考文献[8]への誤帰属を撤回した

- 本稿の初期版は、`AGENTS.md`仕様の策定時期（2025年8月）と採用規模（6万リポジトリ・20ツール）を arXiv:2604.21090 へ帰属させていた。
- **本文を取得して確認したところ、同論文にはいずれの記載もなかった。** 同論文はGitHub上の公開`AGENTS.md` 34件を五原則の枠組みで評価し、37%が構造的完全性の閾値を下回ると報告するものである。
- 出所は検索結果の要約であり、一次資料ではなかった。**当該数値の記述を撤回し、本稿はこれらを主張しない。**

### 留保18: 責務9（ループの有界性）に対応する観測課題がない

- 本稿の初期版は4.6節で責務9を「実装3件（再作業上限の遵守）」で観測していると述べていたが、14 caseの成果条件・禁止境界を走査すると**再作業上限の遵守を採点条件とするcaseは存在しない**。11.1(c)と14節9項は当初から「実行時にも評価課題集合にも同等形が残っていない」と述べており、4.6節だけが食い違っていた。
- 4.6節を11.1(c)へ揃えて訂正した。**したがって9責務のうち1件は、実行時制御としても評価課題としても未測定である。**

### 留保19: 層Aの数値は推論`high`である

- 層A（拡張12課題）の結果は推論`high`、層B・層C・層Dは`medium`である。既存論文2.5節も同じ層分けをしている。仮組みでも層をまたいだ連結はしていない（R4-3）。

### 留保20: 外部文献への誤帰属5件を撤回した

参考文献の本文または全文HTMLを取得して照合した結果、次の帰属が成立しないことを確認し、いずれも撤回した。**出所はいずれも検索結果の要約であり、一次資料ではなかった。**

| 文献 | 撤回した記述 | 実際の内容 |
| --- | --- | --- |
| [2] arXiv:2601.20404 | 「親エージェントの消費のみを集計している」「集計スコープがthreats to validityに挙がっていない」 | token定義は`Total tokens consumed, comprising input tokens, cached input tokens, and output tokens.`だけで、**親限定とも子セッションを含むとも書かれていない。** 独立したLimitations / Threats to Validity節が存在せず、集計範囲への言及がない（節構成はIntroduction / Background and Related Work / Study Design / Results / Research Roadmap / References） |
| [1] arXiv:2511.12884 | 「実務のファイルの大半はリポジトリに関する事実の記述であり、工程の規定ではない」 | 記述的／規定的という区別を立てていない。結論軸は機能的操作への偏りと非機能要件の希少性である。数値（1,925／2,303／62.3%／69.9%／67.7%）は一致 |
| [12] arXiv:2603.13285 | 「フロンティアモデルほど表層的言い換えに頑健である」 | **逆である。** `commercial frontier models remain sensitive to prompt variations, with performance drops comparable in magnitude to those observed in open-weight models`。頑健性の知見はfrontierではなく規模について、かつ`larger models demonstrate greater robustness to paraphrasing perturbations on average, yet remain vulnerable to word-level modifications`という条件付き。投稿は2026-02-27（本稿の`2026-03`はarXiv IDに引かれた誤記） |
| [13][14] | 「format・calibration driftを含む5種のバイアスが整理されている」 | calibration driftは両論文とも扱っていない。[14]は`Expected Calibration Error and Brier Score require token-level logprobs that are not exposed by the majority of providers`として将来課題としており、対象は位置と冗長性の2種のみ |
| [4] arXiv:2606.20512 | 鉤括弧付きの`recent studies disagree` | 原文にこの文言はない。`research disagrees on whether such materials help agent performance`および`Whether these context files help coding agents is still debatable.`。また対比軸はcoverage対**precision**（`per-patch precision remains statistically constant (∼59 %, p=0.119)`）であり、経路長ではない |

- [8] arXiv:2604.21090 は`37%`の分母を訂正した（`34件のうち37%`ではなく`評価対象のfile-model pairのうち37%`）。
- [10] arXiv:2510.04618 は入力側でcontextを反復更新する手法であり、実行環境層への重心移動を支える出典にならないため、当該文の出典を[11]単独へ変更した。
- **留保17（[8]への誤帰属）と本項は同型である。二次的な要約を一次資料として扱わない規律が、外部文献側で複数回破られていた。**

### 留保21: 11.6節の設計指針は一般原則ではない

- 外部査読で「実務家向けの抽象化された実践ガイドライン」の追加を求められ、11.6節を新設した。**同節は新しい測定も新しい主張も追加していない。** 既存Claimを4区分（書き換える／先に書く／書かない／削らない）へ並べ替え、各行へ根拠節を付けたものである。
- **一般的な設計原則として引用できない。** 単一の対象リポジトリ、単一のモデル系列（`gpt-5.6`系）、14課題の範囲の観測である。同節自身が冒頭と末尾でこの限定を宣言している。
- 表内の率は互換キーが異なる比較から集めているため、**行間で大小を比較できない**（留保：R7-1と同じ制約）。
- 10.1節の結果により、この指針は指示書の内容単独に属さない。**指示書とモデルの組についての観測である。**

### 留保22: 経過時間と中心結論の表現を本文で引き下げた

外部査読で、研究者向け草稿への整形時に本文がevidence mapの表現上限を越えていることが指摘され、次を訂正した。

| 越えていた記述 | 訂正後 |
| --- | --- |
| 18束の方向一致に符号確率`2^-18`を当てていた | **削除した。** 一次結果が記録しているのは「18 / 18 Batchで中央値が小さかった」という事実だけで、確率計算はしていない。実行順のランダム化・交互配置がなく、束間独立性も等確率も確認していないため推測統計を当てない |
| 経過時間の差の「向き」をKPIとして読む | **同条件比較における記述として読む**へ引き下げた。追加検証の優先度を決める診断値とする |
| 「直列実行ではtoken増・時間減が成立する機序がない」 | **削除した。** input構成の変化、提供側の処理速度、tool I/Oや待ち時間など、本研究が計装していない要因で起こり得る。本文自身がC116→C118で機序を特定できていないと認めている |
| 「品質を支えていたのは……観測可能な実行境界である」（結論4と最終文） | **R13-1の禁止に反していた。** 「借りた枠組み全体を保持しなくても品質制約は満たせた」「共通していたのは……構造だった」へ引き下げ、モデルの既定能力・TaskSpec・path別`AGENTS.md`・repository authority・fixture・executor挙動が残ることを明記した |
| 「効率を決めるのは……分岐を1つ閉じているか」（1.5節と結論5） | **解釈軸**へ引き下げた。留保23の事後符号化（2類型の混在、判定者依存、非十分性）と両立しない断定だった |
| 「1文がモデルの分岐を1つ増減させ、子セッションの起動を1体増減させる」 | 一対一対応は測っていない。**確率を変え得るという記述**へ改めた |

**経過時間の位置づけは変えていない。** 統制しないことは設計上の選択であり（KPIではなく指標として観測する）、統制の失敗としては記述しない。訂正したのは、統制していない量の向きをpromptの因果効果として読んでいた点である。

**第2回の査読で、同じ意味の主張が別節に残っていることが指摘された。** 文言を消しても機構主張が残っていたため、次を追加で訂正した。

| 残っていた記述 | 訂正後 |
| --- | --- |
| 「作業仮説は……部分的に支持される」（4.3節） | 「記述的に整合する結果が観測された」 |
| 「両指標が同方向なら整合として読む」（4.3節） | 「同方向・逆方向のいずれも追加調査の手掛かりとして記録する」 |
| 「経過時間は直列の往復回数に、tokenは……総量に対応する。両者の乖離は経路のどこが変わったかを示す」（4.3節） | **削除。** 「乖離は未計装の要因を含む追加調査の対象として記録する。経過時間の内訳を観測していないため機序を特定しない」 |
| 「通常の機序は並列化」（7.4d節） | 「あり得る複数の説明の一つ」へ |
| 「経過時間の増加は発行順を固定したことに対応する」（4.3節） | 「発行順の固定と経過時間の増加が同時に観測された。因果として帰属しない」 |
| 「差の向きは……指標としてそのまま使う」（12.4節） | 「記述的な共変動であり、そこから実行経路の機序を読まない」 |
| 「所要時間の向きは……確認している」（12.7節） | 「記述的に整合する共変動を観測している」 |
| 「その記述が実行経路の分岐を1つ閉じているかで効果が決まる」（7.5節） | **解釈軸へ。** 判定基準の再現性・十分条件性・因果的決定因子であることのいずれも確認していないことを明記 |
| 「分岐を1つ閉じる記述は実行量を下げた」（11.6節） | 「本系列でtoken低下と同時に観測された記述」へ。同時観測であり単独の因果効果ではないと明記 |
| 「Lullaらの設定では事実の記述が探索を代替した」（7.5節） | 同論文は探索削減を**説明仮説**として挙げ、execution traceによる確認を将来課題としている。「異なる研究で同じ機構が独立に観測された」とは扱わない |
| 「本研究が示せたのは、どの記述が実行経路の何を変えたかまで」（14節） | 「どの候補差分と、どの品質・token・実行経路の変化が同時に観測されたかまで」へ。単文ablationを実施していないことと矛盾していた |
| 「非比例かつ不連続に動く」（1.2節） | 「非比例・離散的に変化する場合がある」へ |
| 結論4の参照先「11.4節、12.6節」 | 単独因果・最小性の参照先として不適当。「1.6節、12.2節」へ |

### 留保23: 事後符号化は§12.2の限界を解消していない

- [`branch-closure-retrospective-coding.md`](branch-closure-retrospective-coding.md)は、§12.2の構造的限界を**解消していない**。到達したのは限界の所在の具体化である。
- 符号化中に、事前固定した基準では判定できない区別が2つ現れ、全件へ一律に適用した（実行経路と往復の分離、候補単位への集約規則）。**基準は結果参照前に固定したが、無修正では通らなかった。**
- **手作業符号と規則符号が33件中9件で食い違う。** どちらを正とするかで「閉じた」の件数が24件と15件に変わる。本文書は規則側を正とし、両方を開示する。
- 語彙ベースの機械判定は否定表現（「停止理由にしない」）と既存述語の再表現を読めず、`closed`を過大に判定する方向の誤りを持つ。
- **成立前区間を独立検証群として使う設計は成立しない。** 候補indexの状態語彙が研究途中で変わり、成立前33件には`stopped`が0件しかない。さらに全resultを走査すると、成立前で「閉じていない」と符号化された14件のうち親と同一互換条件の比較が保存されているのは5件だけで、欠落は「閉じていない」側へ偏る。**追加作業では回復できない構造上の制約であり、未実施の残作業ではない。**

### 留保24: atomic run経路のEvaluation set identityが層Bと異なる

- 層Bのset identityは`430d1d4b…`、C125のmodel軸resultは`2096d15e…`である。これはatomic run経路でのidentity計算が異なるためであり、`evaluations/AGENTS.md`が「atomic run経路では`N`、coverage、iteration集合、計画順序、`max_workers`をrunの実効互換条件へ含めない」と定めている。同じ`the-caption-standard14-r1`だが、identity値としては別である。**この2つのidentity値を同一視しない。**

---

## 5. 数値のsource一覧（仮組み本文に出る主要数値）

| 数値 | 出所 | 条件 |
| --- | ---: | --- |
| Baseline root `5,980 bytes` | `prompts/baselines/the-caption-3ce91a4-current-r2/files/AGENTS.md.txt` | bundle実体 |
| CFR root `0 bytes` | `prompts/candidates/the-caption-3ce91a4-control-free-repository-r1/files/AGENTS.md.txt` | bundle実体 |
| C5 `7,725` / C35 `3,235` / C41 `3,482` / C43 `3,980` / C71 `4,987` / C81 `5,525` / C125 `10,908` bytes | 各candidate bundleの`files/AGENTS.md.txt` | bundle実体 |
| 工程仕様7 target合計 `59,098 bytes` | Baseline bundleの該当7 file | bundle実体（24,209 + 15,421 + 4,086 + 4,183 + 2,128 + 5,161 + 3,910） |
| C43のlabel数 `9` | `the-caption-3ce91a4-outcome-authority-boundary-r1/files/AGENTS.md.txt` | bundle実体（file全体は見出し1行を含む11行） |
| 層Bの全KPI（7条件） | [層B result](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)、[C71 / C81 result](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md) | `79ed04a4…` |
| 層Aの全KPI（4条件） | [層A result](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md) | `abc7d7a9…` |
| root-only / all-agent内訳（Baseline `3,888,115` / `8,925,798`） | [`v3-all-agent-token-reaccounting`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md) | 層A系、旧rating、`high` |
| SA routing観測（監査SA / レビューSA起動数、40 implementation run） | [`baseline-candidate1…candidate5 result`](../evaluations/results/baseline-candidate1-candidate2-candidate3-candidate4-candidate5-expanded12-global-m24-n5_2026-07-16.md) | `5048fe59…` |
| C98 / C104差 | [C104 result](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md) | 層C |
| C116 / C118差、A02 `N=20` | [C118 result](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | 層C |
| C125の全KPI、C107 / C118 / C122比、F02 / F04診断 | [C125 result](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | 層C |
| C81 / C95 B20、検定値 | [B20 result](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md) | `c5bfcd6d…` |
| C125 Sol / Terra / Luna | [model軸 result](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md) | 3 keyが互いに異なる |
| Click C81 | [Click C81 result](../evaluations/targets/click/results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md) | Click instance、CLI `0.144.0` |
| Click C125 | [Click C125 result](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md) | `39dcb70f…` |
| 表面圧縮系列の静的・動的量 | 各候補result、[`candidate-history.md`](candidate-history.md)、[`control-mechanisms.md`](control-mechanisms.md) | 候補ごとに別key・別集計軸 |
| 料金換算額 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md) | 補助指標 |
| B18のtool call `-30.16%`、モデルステップ`-26.54%` | [C69 / C71 B18 result](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md) | v12、標準14項目。**C43 → C71（層B）の経路診断ではない**（R11-3） |