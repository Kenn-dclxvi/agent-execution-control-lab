# 論文仮組みのevidence map

> [!IMPORTANT]
> **位置付け**: この文書は[`execution-control-research-paper-reframed-draft.md`](execution-control-research-paper-reframed-draft.md)の各主張と一次資料の対応表である。契約、評価状態、採用、release、本体反映の正本ではない。数値と識別子はリンク先の一次artifactを正本とする。
>
> **作成方針**: 数値は一次result（`evaluations/results/`および`evaluations/targets/*/results/`）とprompt bundleの実体から取得した。要約文書（`candidate-history.md`、`control-mechanisms.md`、`candidate81-candidate125-control-findings-synthesis.md`、既存の`execution-control-research-paper.md`）は所在の索引としてだけ使い、数値の正本としては使っていない。一次resultと要約文書の相違は第4節へ記録した。
>
> **新規測定は行っていない。** 既存証拠で接続できない主張は第3節へ再試験候補として分離した。
>
> **作成日**: 2026-08-01（研究状態は2026-07-31時点）

---

## 1. 用語の定義

### 1.1 証拠水準

| 水準 | 定義 |
| --- | --- |
| `established_same_condition` | 同一compatibility keyの保存済みresultで、宣言した変更軸以外が機械照合されている観測 |
| `supported_repeated_observation` | 同一条件の反復（B18 / B20など）または複数campaignで方向が一致した観測 |
| `exploratory` | 単一campaign、少数反復、または単一caseの観測。方向の記述にとどまる |
| `historical_design_record` | 当時のprompt本文、manifest、設計文書に記録された設計意図または判断の記録。効果の測定ではない |
| `descriptive_cross_layer` | compatibility keyが異なる条件の並置。効果量として読めない記述的比較 |
| `unverified` | 該当するcase、result、測定条件が存在しない |

### 1.2 再試験欄

| 値 | 意味 |
| --- | --- |
| 不要 | 現在の表現が保存済み証拠の範囲に収まっている |
| 文言限定で対応 | 追加測定なしで、限定語または留保の明示によって成立させる |
| 同条件再試験が必要 | 同一compatibility keyでの追加実行が必要 |
| 長期反復が必要 | B20規模（1条件1,400回）以上の反復が必要 |
| holdout targetが必要 | 未使用のcaseまたは未使用のtarget repositoryが必要 |
| 独立採点が必要 | 固定契約による監査ではなく、独立した第三者採点者が必要 |

### 1.3 主要なcompatibility key

| ラベル | key | 固定条件 |
| --- | --- | --- |
| 層B | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` | set `the-caption-standard14-r1` r1（identity `430d1d4b…`）/ target `THE-CAPTION@3ce91a4` / `gpt-5.6-sol` `medium` / Codex CLI `0.144.0` / rating v13（`d2dd4096…`）/ `workspace-write`・approval `never` / 14 case × `N=5` / global queue `M=24` / all-agent v1 |
| 層A（expanded12 v9） | `abc7d7a9a4db052f417a200e5c7b873e39edb27bc5d564163fbb150f560100a4` | set `the-caption-expanded12-f04r2-f10r3-r2`（`de4d1dea…`）/ `gpt-5.6-sol` `high` / Codex CLI `0.144.0` / rating v9 / 12 case × `N=5` / `M=24` |
| 層A（expanded12 旧rating） | `5048fe5980ee008cc3a0343712fff40fada3e129d9fbdd2b2ee802954f96f30e` | set `the-caption-revision-2-expanded12-r1` / `gpt-5.6-sol` `high` / `N=5` / `M=24` |
| 層C（B20） | `c5bfcd6dcc52b99e7a3dabda966dcb00640e4eeed8c969753992545c87a8490c` | set `the-caption-standard14-r1` r1 / `gpt-5.6-sol` `medium` / rating v14 / Codex CLI `0.146.0` / 各1,400件 / `M=24` |
| 層C（atomic reuse N=5） | 各resultの`固定条件とidentity`節を正本とする（rating v14 `9d01b7ee…` / CLI `0.146.0` / fixture `bb9eb7f5…` / runtime `61b26e61…`） | Evaluation set identity `2096d15e…`（atomic run経路） |
| 層D（model軸） | 3 resultで互いに異なる（modelがkeyに含まれる） | 上記層C条件のうち`model`だけをSol / Terra / Lunaへ変更。preflightで差分が`$.comparison_conditions.model`と`$.profile_id`だけであることを機械照合 |
| Click C125 | `39dcb70f20256935b2e257e57cda1cba0c1f15d41ca77bb4e5b4c13734484472` | set `click-standard14-r2` r2（`bbba58d8…`）/ rating `click-outcome-abstract-condition-preserving-v10` / `gpt-5.6-sol` `medium` / Codex CLI `0.146.0` / 14 case × `N=5` / `M=24` |

---

## 2. Claim対応表

### 2.1 第1節 背景：Baselineの到達点

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1-1 | 1.1 | Baselineは人間の開発工程（指示書化・実装・監査・レビュー・差し戻し・完了判定・PR）を役割と関所として写している | prompt本文の工程と役割の限定列挙 | `prompts/baselines/the-caption-3ce91a4-current-r2/files/AGENTS.md.txt`（§役割・§指示書草案・§SA起動と分離・§停止と自動再修正・§完了判定・§PR作成）、`files/docs/orchestration-process.md`（§基本方針・§SA利用ケース・§自動修正ループ）、`files/prompts/{plan,implement,audit,review}.md` | Baseline bundle `63225d2d…`（19 path） | `historical_design_record` | 「工程・成果物・関所の構造を写している」まで。工程が人間の職能配分の写しであるという意図は主張できない（R1-3） | 不要 |
| R1-2 | 1.1 | 親エージェントは実装・修正・テスト実行・監査・レビュー相当の品質確認・指示書作成を直接行わない | prompt本文の禁止列挙 | Baseline root `AGENTS.md` §役割2行目、`orchestration-process.md` §基本方針 | 同上 | `historical_design_record` | prompt上の規定であり、tool levelの強制ではない（`orchestration-process.md` §制約が明記） | 不要 |
| R1-3 | 1.2 | Baselineの設計記録は、この分業を「人間の組織図の写し取りではない」と明示し、AI固有の失敗様式（確証バイアス・迎合・reward hacking）へ向けた設計として7点の理由を挙げていた | 設計理由の原文 | `files/docs/prompt-guide.md` §AI最適化の設計理由 | 同上 | `historical_design_record` | 当時の設計意図の記録である。設計理由の妥当性が測定されたわけではない | 不要 |
| R1-4 | 1.2, 1.4 | Baselineは「工程構造を移植し、各工程の目的をAI固有の失敗様式へ再設計した初期解」であり、その工程構造がAI実行として最適かは未計測だった | R1-1〜R1-3、および当時のtoken集計がroot-onlyだった事実 | 上記＋`evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md` | 混在（設計記録＋層A） | `historical_design_record` | 「未計測だった」は集計範囲の事実として言える。「最適でなかった」は測定後の別主張（R5-1、R5-3）へ分ける | 不要 |
| R1-5 | 1.3 | Baselineが守ろうとした品質責務は9項目として限定列挙できる | prompt本文の該当節 | Baseline root `AGENTS.md` §入力境界・§作業単位化・§停止と自動再修正・§完了判定・§出力、`orchestration-process.md` §停止条件・§各工程の確認範囲・§指摘分類、`prompts/audit.md` §指摘、`prompts/implement.md` §ルール、`prompts/review.md` §レビュー観点、`docs/prompt-guide.md` §原則 | 同上 | `historical_design_record` | 本文から取り出した整理であり、Baseline作者が「9項目」と宣言した記述ではない。整理の粒度は本論文の構成である | 文言限定で対応（「本論文が本文から取り出した整理」と明示済み） |
| R1-6 | 1.4 | Baselineは拡張12課題60回で score `4 / 3 = 58 / 2`、`quality_score`中央値`100.000`だった | 一次resultのscore分布 | [`baseline-control-free-repository-c35-c41-…-v9-expanded12-n5_2026-07-19.md`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md) | 層A（`abc7d7a9…`）、rating v9、`high` | `established_same_condition` | この12課題・rating v9・推論`high`の範囲。標準14項目では`92.857`（R5-1） | 不要 |

### 2.2 第2節 研究疑問

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R2-1 | 2.1 | 中心問いは「品質を維持しながらAI固有の不要な実行経路を除去できるか」である | 問いの定義 | 本論文の定義。関連: `docs/prompt-control-design-principles.md`、`prompts/CLAUDE.md`のcandidate作成前gate | — | — | 問いの定義であり測定主張を持たない | 不要 |
| R2-2 | 2.2 | 静的量と動的量が一致するかは実測可能な副問いである | 静的量（bytes）と動的量（token）の両方が保存されている | prompt bundleの`AGENTS.md.txt`実体、各resultのtoken | 層A・層B | — | 問いの定義 | 不要 |
| R2-3 | 2.2 | 「何を削除すると品質が壊れるか」は0バイト条件で測れる | R6-1 | 下記 | 層B | — | 問いの定義 | 不要 |
| R2-4 | 2.2 | 「品質を支える最小の実行境界」は候補系列で特定できる | R7-* | 下記 | 層B・層C | — | 問いの定義。「最小」の証明はablation未実施のため成立しない（R7-14） | 不要 |
| R2-5 | 2.2 | promptとexecutorの責務境界は実測可能である | R8-3 | 下記 | 層C | — | 問いの定義 | 不要 |

### 2.3 第3節 評価設計

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R3-1 | 3.1, 3.2 | Baselineの品質責務は、model-visibleな成果条件・許可path・禁止変更・必須検証をもつ14 caseへ変換されている | 各caseの`trial-prompt-input.json`と`README.md`、責務との対応 | `evaluations/cases/TC-{F01 r3, F02 r1, F03 r2, F04 r2, F05-CLARIFY r1, F05-OUT-OF-SCOPE r1, F06 r2, F07-CANONICAL r2, F07-DEPENDENCY r1, F08 r1, F10-ENTRYPOINT r1, F10-MONTHLY r3, A01 r2, A02 r2}`、[`the-caption-standard14-r1`](../evaluations/sets/the-caption-standard14-r1/README.md) | set identity `430d1d4b…`（層B）／`2096d15e…`（atomic経路） | `historical_design_record` | 対応表の「責務番号」列は本論文が作った対応付けである。case作成時に責務番号でtraceされていたわけではない | 文言限定で対応（本論文の対応付けである旨を明示済み） |
| R3-2 | 3.3 | Standard14は双方向の失敗を対にしており、「常に止まる」挙動を高く評価しない設計である | case READMEの設計意図 | `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2/README.md`（「A01の対照項目であり、曖昧に見える入力へ常に質問を返す挙動を高く評価しない」）、`TC-F01/r3`（成果達成後の許可外risk停止を禁止）、`TC-F03/r2`（未指定条件を停止理由にしない）、`TC-F07-CANONICAL/r2`（未変更のdefault pathを未完了理由にしない）、`TC-F04/r2`（誤停止の観測） | 各case revision | `historical_design_record` | A01 / A02の対は明示された設計である。他caseの「双方向性」は revision deltaの禁止条項から読み取った整理である | 文言限定で対応 |
| R3-3 | 3.4 | Standard14は作業種類・実行制御境界・失敗方向の3軸で範囲を示せる | 各caseの`task_kind`と成果条件 | 同上、[`evaluations/cases/README.md`](../evaluations/cases/README.md) | 同上 | `historical_design_record` | 軸の分類は本論文の整理である。網羅性の主張ではない（R3-6） | 不要 |
| R3-4 | 3.1, 4.5 | model-visible / private境界が厳密に分離されている | 各caseのvisibility boundary記述、基盤規則 | 各case README §提示範囲 / §Visibility boundary、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §Model-visible境界 | — | `historical_design_record` | 規則としての分離である。破れの実例は R8-6 | 不要 |
| R3-5 | 3.1 | 有効な実行はすべて0〜4で採点し、採点不能を認めない | rating contractの`unrateable_or_null_score_is_allowed_for_valid_run: false` | [`v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json)、[`v13`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json) | v13 / v14 | `established_same_condition` | 契約上の規定。計測失敗（コマンド終了状態を取得できない実行）は除外扱いで別 | 不要 |
| R3-6 | 3.5 | 長期・複数段の作業、段階的に変化する仕様、複数人の合意形成、障害対応、正のrecovery scenarioはStandard14に含まれない | 該当caseの不存在 | [`research-backlog.md`](research-backlog.md) 項目11（「未着手・該当caseなし」）、`RECOVERY`項目（「未完了・効果未測定」）、`evaluations/cases/`のcase一覧 | — | `unverified` | 「含まれない」ことは列挙で確定できる。含めた場合の挙動は不明 | holdout targetが必要（新case family設計） |
| R3-7 | 3.6 | 採点契約は版で固定し、結果を見た後の基準変更は新しい版とする | 契約ファイル群と基盤規則 | `evaluations/rating-contracts/`（v1〜v14）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §Immutable history | — | `established_same_condition` | 規則と実体の一致まで | 不要 |
| R3-8 | 3.6 | v14はA01を「応答本文・疑問符・質問語を使わない」terminal-state evidenceで判定する | 契約本文 | [`v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json) `boundary_rules.TC-A01-LATENT-MODE-POLICY.state_evidence.response_text_policy`、`rater_input.forbidden` | v14 | `established_same_condition` | A01についてのみ確認済み。他caseの判定が同水準で観測可能条件へ落ちているかはcase単位でしか確認していない（R12-7） | 文言限定で対応 |

### 2.4 第4節 測定基盤

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R4-1 | 4.1 | 評価は4 Layerに限定され、各Layerは前段artifactを変更しない | 基盤規則 | [`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §4 Layer、[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md) | — | `established_same_condition` | 規則としての境界 | 不要 |
| R4-2 | 4.2 | 互換条件が全一致しない結果を同一比較へ混ぜない | 基盤規則と各resultの固定条件節 | [`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §Compatibility、各result | — | `established_same_condition` | 規則と実体の一致まで | 不要 |
| R4-3 | 4.2, 9.3 | 層をまたいだ削減率の連結を行わない | 各層のkeyが異なること | 層Bのkey `79ed04a4…`（rating v13 / CLI `0.144.0`）と層Cのrating v14 / CLI `0.146.0` | — | `established_same_condition` | 記述方針。連結した数値は本論文に存在しない | 不要 |
| R4-4 | 4.4, 5.3 | root-only集計ではBaselineがC5より`615,701`少なく見えていたが、all-agentではBaselineが`3,185,357`多い。Baselineのall-agentに占める委譲分は56.4% | 再集計resultの両集計値 | [`v3-all-agent-token-reaccounting_2026-07-16.md`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md)（Baseline root-only `3,888,115` / all-agent `8,925,798`、C5 `4,503,816` / `5,740,441`） | 層A（`5048fe59…`系）、rating旧版、`high`、拡張12課題 | `established_same_condition` | 56.4%は「この12課題・`N=5`・`high`の中央値から計算した比」である。標準14項目での比は算出していない | 同条件再試験が必要（層Bでの委譲比率を出す場合） |
| R4-5 | 4.3 | 3指標の中央値の実効標本数は`N`であり、70回は同質な70独立標本ではない | 集計方法の定義 | 各resultの中央値表記（「5反復中央値」）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) | — | `established_same_condition` | 集計単位の記述 | 不要 |
| R4-6 | 4.1, 13 | 基盤は`winner`、改善・悪化の断定、採用可否、release判断、projection判断を出力しない。評価は観測、採用は判断である | 基盤規則と実際の状態分離 | [`evaluations/AGENTS.md`](../evaluations/AGENTS.md) §3 KPI末尾、[`candidate125-adoption-decision.md`](candidate125-adoption-decision.md)、[`prompts/releases/README.md`](../prompts/releases/README.md)、C125 resultの`adoption_not_decided` | — | `established_same_condition` | 規則と実体の一致まで | 不要 |

### 2.5 第5節 Baselineの測定

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R5-1 | 5.1, 5.2 | Baselineは層Bで`4 / 3 / 1 / 0 = 63 / 2 / 1 / 4`、品質中央値`92.857`、token中央値`11,977,774`、所要時間中央値`3,568.742`秒、70件合計`64,096,747` / `18,583.648`秒。減点はA01 4件、A02 2件、F07依存関係1件 | 一次resultのKPI表と低得点表 | [`baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)（result ID `107d31cdae9044d08c0768ffc89d3896`） | 層B `79ed04a4…` | `established_same_condition` | この7条件・`N=5`の観測。所要時間は記述値（R12-15）。F07 canonicalで4 attemptを`command_evidence_incomplete`により除外し再実行している点を併記する必要がある | 不要 |
| R5-2 | 5.1, 5.4 | Baselineは範囲逸脱・reward hacking・完了偽装・対象外操作に起因する減点0件で、落ちたのは推測の禁止・停止の義務・必須検証の非省略だった | 低得点表の失敗内容と責務の対応 | 同上 §低得点、R1-5の責務列挙 | 層B | `exploratory` | 「0件」は保存された失敗内容の分類にこの3類型が現れないことを意味する。責務ごとの独立検証ではない | 文言限定で対応 |
| R5-3 | 5.3 | Baselineのall-agent tokenの56.4%が委譲先セッションの消費だった | R4-4 | [`v3-all-agent-token-reaccounting_2026-07-16.md`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md) | 層A（拡張12課題、`high`、旧rating） | `established_same_condition` | 層Aの数値である。層Bの`11,977,774`に対する内訳ではない。**この2つを掛け合わせない** | 同条件再試験が必要（層Bでの内訳を主張する場合） |
| R5-4 | 5.3 | 実装SAへの必須委任を外して選択可能にすると、40 implementation runすべてが親直接を選び、実装目的の委譲は0件だった。監査SA / レビューSA起動はC2の35 / 17からC5の25 / 16へ | 一次resultのrouting観測 | [`baseline-candidate1-…-candidate5-expanded12-global-m24-n5_2026-07-16.md`](../evaluations/results/baseline-candidate1-candidate2-candidate3-candidate4-candidate5-expanded12-global-m24-n5_2026-07-16.md) §Prompt execution design / §SA routing observation | 層A（`5048fe59…`）、`high`、拡張12課題 | `exploratory` | 拡張12課題・`N=5`・旧rating。「実装の担当者を分ける段はAI実行では選ばれない」は、この60 runの観測に限定した記述 | 同条件再試験が必要（層Bで再現を主張する場合） |

### 2.6 第6節 削除実験

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R6-1 | 6.2 | ControlFreeRepositoryは層Bでtoken中央値`3,496,976`（Baseline比`-70.80%`）、所要時間`1,250.057`秒（`-64.97%`）、score分布`4 / 0 = 65 / 5`で、A01が5 / 5件0点 | 一次resultのKPI表・差分表・低得点表 | [同上 層B result](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)（result ID `3fb81b94ef1d4770b52bc202bf0a43d8`） | 層B `79ed04a4…` | `established_same_condition` | この条件の観測。所要時間は記述値 | 不要 |
| R6-2 | 6.1, 12.10 | ControlFreeRepositoryはBaseline bundleの19 pathのうちroot `AGENTS.md`の1 targetだけを空ファイルへ置換した条件であり、擬人的な工程仕様（`orchestration-process.md` 24,209 / `prompt-guide.md` 15,421 / `glossary.md` 4,086 bytes）と4つのロールプロンプト（4,183 / 2,128 / 5,161 / 3,910 bytes）はBaselineと同一のまま残っている | manifestのtarget別SHA-256の照合、bundle実体のbyte数 | `prompts/candidates/the-caption-3ce91a4-control-free-repository-r1/manifest.json`（`scope`: 「root AGENTS.mdの1 targetだけを空fileへ置換し…残り18 targetをbaselineと同一に保つ」）と`prompts/baselines/the-caption-3ce91a4-current-r2/manifest.json`の照合結果: 差分target = `AGENTS.md`のみ | bundle `999769800a…` vs `63225d2d74…` | `established_same_condition` | bundle実体から確定できる。**既存論文3.1節・付録A.2はこの条件を「配下ディレクトリごとの指示書4件はそのまま残した」と記述しており、工程仕様7ファイルの残存に言及していない**（第4節の相違1） | 不要 |
| R6-3 | 6.2, 6.4 | 削除では品質責務1・2（推測の禁止と停止の義務）が閉じない。「lean」の最適点は0ではない | R6-1、R6-6、およびC43で減点が0になったこと（R7-7） | 層B result、層A result | 層B・層A | `supported_repeated_observation` | 2つの層で同方向。ただし層Aは`1 / 60`、層Bは`5 / 5`で欠陥の頻度が違う。「削除では閉じない」までが上限で、「必要制御の集合が一意に定まる」ことは示していない | 不要 |
| R6-4 | 5.2, 6.4 | C81のroot本文は`5,525 bytes`（Baseline `5,980 bytes`の約`0.92`倍）だが、token中央値は`1,917,979`対`11,977,774`で約`6.2`分の1である | bundle実体のbyte数と同一keyのtoken | `prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1/files/AGENTS.md.txt`（5,525 bytes）、Baseline `files/AGENTS.md.txt`（5,980 bytes）、層B result | 層B `79ed04a4…`（同一key内での比較） | `established_same_condition` | 静的量と動的量の不一致を同一key内で確認した観測 | 不要 |
| R6-5 | 6.2 | 品質中央値の一致を「品質が同じ」と読み替えない。BaselineとCFRは中央値`92.857`が一致するがcase score分布と全case得点率（`92.500%`対`92.857%`）は一致しない | score分布と得点率の算出 | 層B result §3 KPI（分布）。得点率は`259 / 280`と`260 / 280`から算出 | 層B | `established_same_condition` | 得点率は分布からの算術。一次resultに得点率列は存在しない | 不要 |
| R6-6 | 6.3 | 層Aでも同型の結果。Baseline `58 / 2` token中央値`10,826,033`、CFR `59 / 1` `2,808,523`（`-74.06%`）、C35 `60 / 0` `4,565,773`、C41 `60 / 0` `2,861,019`。C41はCFRより`+1.83%`大きい | 一次resultのKPI表 | [`baseline-control-free-repository-c35-c41-…-v9-expanded12-n5_2026-07-19.md`](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md) | 層A `abc7d7a9…`、rating v9、`high` | `established_same_condition` | 層Bと同方向だが別key。`1 / 60`から`0 / 60`を低頻度誤経路一般の解消へ一般化しない | 不要 |

### 2.7 第7節 実行境界の抽出

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R7-1 | 7.5, 要旨 | 効いた6境界はいずれも「モデルが実行時に観測できる状態・証拠・結果に対する条件」として書かれている | 各候補のroot本文のpredicate形式 | C43 / C71 / C81 / C104 / C116 / C118 / C122 / C125のroot `AGENTS.md.txt`、[`candidate81-candidate125-control-findings-synthesis.md`](candidate81-candidate125-control-findings-synthesis.md) | 層B・層C | `supported_repeated_observation` | 「観測可能条件で書かれている」は本文の形式から確定できる。「観測可能性が効果の原因である」は反例系列（R8-4）との対照からの解釈であり、単文効果としては示していない | 不要 |
| R7-2 | 7.1 | 層Bの7条件は指示書以外の条件（課題、作業指示、fixture、必要な検証、採点契約、実行環境、`M`、`N`）がすべて一致している | resultの固定条件節と「6 profileはprompt identity以外を一致させた」記述 | 層B result §固定条件、[`C71 / C81 result`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)（「両profileの差は`profile_id`と`prompt_set_identity`だけ」） | 層B `79ed04a4…` | `established_same_condition` | 設定値の一致であり、実行時交絡（実行時刻・同時実行数・キャッシュ・提供側負荷）の排除ではない（R12-15） | 不要 |
| R7-3 | 7.1 | 結果は一つの勝者に収束しない（token最小はC81、所要時間と合計最小はC71、`4 = 70`はC43・C71・C81、1回で出し切れた率最良はC81） | 層Bの2 result | 層B result、C71 / C81 result | 層B | `established_same_condition` | 記述的な比較。優劣・採用の順位ではない | 不要 |
| R7-4 | 7.1 | Baselineとの差分（CFR `-70.80%`〜C81 `-83.99%`） | resultの差分表 | 層B result §Baselineとの差 | 層B | `established_same_condition` | 同一key内の記述的差分。個々の一文の効果ではない（R7-14） | 不要 |
| R7-5 | 7.2, 13 | C35以降のbundleでは擬人的な工程仕様7 target（合計59,098 bytes）が0バイトへ置換されており、その根拠は「expanded12 × N=5の保存済み観測で成功commandから参照されなかった」ことである | manifestの`change_reason`・`changed_targets`とbundle実体のbyte数 | `prompts/candidates/the-caption-3ce91a4-root-control-only-r1/manifest.json`（`changed_targets`に7 targetを列挙、`change_reason`に非参照の観測を明記）、C41 / C43 / C71 / C81 / C125 bundleの同7 targetが0バイト | bundle `f53fbf3649…`ほか | `historical_design_record` | manifestに記録された判断根拠である。**根拠となったcommand evidence自体はraw run logであり、このリポジトリへcommitされていない**（第4節の留保2）。byte数と0バイト化は実体から確定できる | 文言限定で対応 |
| R7-6 | 7.2 | C43のrootは10行のラベル（`SPEC / PRODUCER / TERMINAL / CONTEXT / OWNER_ROLE / ROOT / INDEPENDENCE / METHOD / RECOVERY`）からなり、各ラベルが1つのpredicateを持つ | root本文 | `prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1/files/AGENTS.md.txt`（3,980 bytes）、[`prompt-control-design-principles.md`](prompt-control-design-principles.md) | bundle実体 | `established_same_condition` | 本文の構造として確定できる | 不要 |
| R7-7 | 7.3(1) | C43は`spec_ready`のpredicateを置換し、A01の減点を`0`、point分布を`4 = 70`、token中央値をBaseline比`-77.32%`にした。変更理由はC42のA01失敗形（選択肢の補集合からstrictへ固定して書き込みと試験を実行した）である | resultのKPI・低得点表、manifestの`problem` / `change_reason` | 層B result、`the-caption-3ce91a4-outcome-authority-boundary-r1/manifest.json` | 層B `79ed04a4…` | `established_same_condition`（KPI）＋`historical_design_record`（変更理由） | 版と版の比較。1つのpredicate置換であることはmanifestの`scope`（root `AGENTS.md`の既存SPECだけを置換）から確定できるが、そのpredicate単独の効果量は測っていない | 不要 |
| R7-8 | 7.3(2) | C71はC43比でtoken中央値`-29.19%`、所要時間`-10.59%`、70件token合計`-31.18%`、品質`4 = 70`維持 | resultのKPI差 | 層B result（「Candidate71とCandidate43の直接差は、token合計`-4,293,560`（`-31.18%`）、elapsed合計`-554.844`秒（`-10.45%`）」） | 層B | `established_same_condition` | 同一key内の差分。所要時間は記述値 | 不要 |
| R7-9 | 7.3(3) | C81はC71比でtoken`-0.30%`、所要時間`+5.78%`、品質`4 = 70`維持。1回で出し切れた率はF04の`0 / 5 → 5 / 5`により`30 / 35 → 35 / 35` | C71 / C81 resultのKPI表と1-step closure診断表 | [`candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md`](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md) | 層B `79ed04a4…` | `established_same_condition`（品質・診断値）／`exploratory`（数%の差） | 「安定化と所要時間の増加を同時に観測した」まで。因果は主張しない。数%の差は検定・信頼区間なし | 不要 |
| R7-10 | 7.4(4) | C104はC98比でtoken中央値`-6.48%`、所要時間`-9.77%`、品質70 / 70件が4点 | 一次resultのKPI差表 | [`candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md`](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md)（`-121,141`（`-6.48%`）、`-100.745`秒（`-9.77%`）） | 層C（v14 / CLI `0.146.0`） | `established_same_condition` | 固定Standard14 `N=5`の記述差。一般的効果・採用を意味しない（result本文が明記） | 不要 |
| R7-11 | 7.4(5) | C116は`required outcome`と`implementation choice`を別状態に分け、A01とA02を安定分離した | 一次result、C125 root本文の該当predicate | [`candidate116-candidate118-…_2026-07-31.md`](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §6、C125 root `AGENTS.md.txt` §SPEC | 層C | `established_same_condition`（C116のStandard14 70 / 70）／`historical_design_record`（分離の設計意図） | 「A01とA02を一つの条件で安定分離できなかった」（C112〜C115）はsynthesisの記述であり、本表では一次resultへ個別に当てていない | 文言限定で対応 |
| R7-12 | 7.4(6) | C118はA02 `N=20`で20 / 20件が4点、確定後・変更前のコマンド再入`0 / 20`（C116は`5 / 20`・計7コマンド）。Standard14 tokenはC116の`1,599,779`から`1,718,725`へ`+7.44%`、所要時間は`982.872 → 841.648`秒（`-14.37%`） | 一次resultのKPI表と診断 | [`candidate116-candidate118-…_2026-07-31.md`](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | 層C（atomic reuse `N=5`） | `established_same_condition` | 機構成立とcost改善が別であることを示す観測。result本文も「tokenの増分はinput側にあり、command総数の増加では説明できない」と記録している | 不要 |
| R7-13 | 7.4(7) | C125はStandard14 70 / 70件が4点、token中央値`1,401,225`（C107目標`1,523,137`を`8.00%`下回る、C118比`-18.47%`、C122比`-0.19%`）、所要時間中央値`846.377`秒（C107比`-10.48%`、C118比`+0.56%`、C122比`+2.84%`）。F04誤停止`0 / 5`、F02一括取得`5 / 5`（token中央値`124,094`）、A02 `N=20`が20 / 20・再入`0 / 20` | 一次resultのKPI比較表・targeted mechanism節・A02節 | [`candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md`](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)（result ID `96fb571308de4c08a7aeed0faefb7d72`） | 層C（atomic reuse `N=5`）。Standard14 70件のうち25件は登録済みatomic runの再利用、45件が新規実行 | `established_same_condition` | `N=5`の観測。**C95が`N=5`を通過してB20で落ちた事例と同じ証拠水準**。「全指標がC122より改善」とは言えない（所要時間`+2.84%`）。数%の差に検定・信頼区間なし | 長期反復が必要（B20） |
| R7-14 | 7.6, 12.5 | 境界の追加順序、同時追加、ablationは測っていない。したがってこの順序が必要条件であるとは主張しない | 該当resultの不存在 | `evaluations/results/`に順序入れ替え・同時追加・ablation条件のresultが存在しない | — | `unverified` | 「測っていない」ことの記述 | 同条件再試験が必要（ablationおよび順序入れ替え） |
| R7-15 | 7.7 | C125は7つの制御（C81 / C104 / C116 / C118 / C119 / C122 / C125）を一つの指示書へまとめたものである | root本文のラベル対応とsynthesis | C125 root `AGENTS.md.txt`（`VALIDATION_CLOSURE` / `EVIDENCE_GATE` / `SPEC` / `VALIDATION_PLAN` / `METHOD`）、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §結論 | bundle `60e95bfe7f…` | `established_same_condition`（本文の対応）／`historical_design_record`（系譜） | 本文に対応するラベルが存在することは確定できる。各制御の寄与分は分離していない | 同条件再試験が必要（寄与分の分離） |

### 2.8 第8節 効かなかった仮説

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R8-1 | 8.1 | 表面圧縮8候補のうち7件で実行時tokenが増加または実質不変だった（静的`-1.43%`〜`-39.12%`に対し動的`-2.33%`〜`+31.36%`） | 各候補の一次result | C32 / C49 / C54 / C64 / C65 / C66 / C67 / C68の各result（`evaluations/results/candidate43-candidate6{3,4,5,6}-…`ほか）、[`candidate-history.md`](candidate-history.md)、[`control-mechanisms.md`](control-mechanisms.md) | 候補ごとに異なるkey・課題範囲 | `exploratory` | **この列は候補ごとに集計軸が違う（中央値・70件合計・単一課題F10が混在）。候補間の横断比較には使えない。** 読み取れるのは符号の不一致だけ | 同条件再試験が必要（同一集計軸への再集計） |
| R8-2 | 8.2 | 委譲条件の細分化（C82〜C89）は工程分解の誤りを修復しなかった。C87はD01で親候補比token`-51.06%`だがStandard14全体ではC81比token`+6.09%`、所要時間`+1.35%` | 一次resultとsynthesis | [`candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §2、[`research-backlog.md`](research-backlog.md) §2 | 層C（Standard14）／D01は別case set | `established_same_condition`（C81 / C87 Standard14）／`descriptive_cross_layer`（D01との並置） | 局所改善と全体コストの乖離まで。`-51.06%`はC86比であり、Standard14の`+6.09%`と同一比較ではない | 不要 |
| R8-3 | 8.3 | 実行環境側の性質を指示書へ書いても成立しない。C96は成功時stdoutが全5件でモデルへ返り、C97は全5件で成功後に別の`git status`を発行した（completion closure `0 / 5`） | 一次resultと診断 | [synthesis](candidate81-candidate125-control-findings-synthesis.md) §3、C96 / C97の各result、[`candidate97-decision-round-closure-design.md`](candidate97-decision-round-closure-design.md) | 層C | `exploratory` | 各`N=5`の観測。「promptで一切制御できない」ではなく「この条件で狙った投影・締めが成立しなかった」まで | 不要 |
| R8-4 | 8.4 | C95は`N=5`を通過したがB20（1,400回）で`4 / 2 / 1 = 1,398 / 1 / 1`。token`+4.49%`（Holm補正後`p=0.002325`）、所要時間`+5.53%`（`p=0.000019`）でC81より有意に悪化。C81側は`1,400 / 1,400`が4点。command protocol violationはC95のみ19件 / 10 run（McNemar `p=0.001953`） | B20 resultの品質表・検定結果 | [`candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md) | 層C B20 `c5bfcd6d…`。実行順を奇数batch C81→C95、偶数batch C95→C81で交互化 | `supported_repeated_observation` | 本研究で検定を適用した唯一の比較。score `4`件数の差2件はMcNemar `p=0.5`で有意ではないが、事前品質gateは4点未満を1件も許容しない | 不要 |
| R8-5 | 8.5 | 量による証拠の打ち切りは成立しない。C123は正常なdetached HEADを未確定と誤分類し、C124はF04の誤停止を2件出しF02の一括取得も崩した | 一次resultとsynthesis | [synthesis](candidate81-candidate125-control-findings-synthesis.md) §7、[`candidate123-preterminal-result-round-closure-design.md`](candidate123-preterminal-result-round-closure-design.md)、[`candidate124-incomplete-content-continuation-design.md`](candidate124-incomplete-content-continuation-design.md) | 層C | `exploratory` | 各targeted `N=5`の観測 | 不要 |
| R8-6 | 8.6, 10.3 | 抽象的な成果条件を採点側で特定コマンドへ具体化すると実体のない減点が出る。C71 B18のA02 score 3の4件のうち3件がこのずれだった。v13で塞ぎ、v14で`not_required_unless_model_visible`として明文化した。同型の事例がClick側でも1件（A01の`resilient_parsing`字句監査で4件） | 個別事例の分析と契約本文 | [`a02-rating-divergence.md`](a02-rating-divergence.md)、[`candidate69-candidate71-…-b18_2026-07-22.md`](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)、[`v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json) `boundary_rules.TC-A02…`、[`click-c125-…_2026-07-31.md`](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md) | B18はv12。Clickは別instance・別rating | `established_same_condition`（契約本文と事例）／`exploratory`（偏りの方向） | 「この偏りは効率化された側を不利にする方向を持つ」は2事例からの解釈である。偏りの大きさは定量化していない | 不要 |
| R8-7 | 8.7 | 失敗候補を直系継承せず、最後に成立した親（C122）へ戻して成功predicateだけを別軸で再検証した | manifestの`baseline_identity`と系譜 | `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1/manifest.json`（`baseline_identity: the-caption-3ce91a4-prechange-evidence-wave-closure-r1` = C122）、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §5 / 設計原則8 | bundle実体 | `historical_design_record` | 系譜の事実。「この作り方が結果に効いた」は解釈 | 文言限定で対応 |

### 2.9 第9節 後続設計

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R9-1 | 9.1 | C81以降の系列は7つの軸へ分解された探索として読める | synthesisの系列見取り図と各result | [synthesis](candidate81-candidate125-control-findings-synthesis.md) §系列全体の見取り図、[`candidate-history.md`](candidate-history.md) | 層C | `historical_design_record` | 軸の分類は本論文とsynthesisの整理である。番号順の系譜ではないことはmanifestの`baseline_identity`から確認できる | 不要 |
| R9-2 | 9.2, 13 | C125は現在の設計到達点であり終点ではない。Standard14 B20未実施、`N=100`は`planned / not_started`、一次結果は`adoption_not_decided`で、別状態として`adopted / release_projected / runtime_projected`が記録されている | resultのstatus、synthesis、採用判断 | [`candidate118-candidate125-…_2026-07-31.md`](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) §結論のstatus列、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §現在状態と残るrisk、[`candidate125-adoption-decision.md`](candidate125-adoption-decision.md) | 層C | `established_same_condition` | 状態の記述。**採用は`N=5`通過を長期安定性の確定として扱ったものではない** | 長期反復が必要（B20） |
| R9-3 | 9.4 | 現在残るriskは、C125 B20未実施、`N=100`未着手、Terra / Luna未採用、`CONTEXT`・`RECOVERY`ペンディング、部分曖昧・長期タスク未着手、model / CLI更新時の再測定範囲未着手、Claude Code CLI系列保留である | backlogとsynthesisの状態表 | [`research-backlog.md`](research-backlog.md) §状況サマリー、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §現在状態と残るrisk | — | `established_same_condition` | 記録された状態の列挙 | 不要 |

### 2.10 第10節 modelおよびtargetへの依存

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10-1 | 12.9 | 全評価結果は`gpt-5.6`系列 / Codex CLIであり、Claude系modelでの測定は0件である | 全resultのmodel欄 | `evaluations/results/`の各result §固定条件、[`research-backlog.md`](research-backlog.md) §8（Claude Code CLI executor: 保留）、[`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md) | — | `unverified`（Claude系） | 「0件」の記述 | holdout targetが必要（別model系列・別CLI） |
| R10-2 | 10.1, 13 | C125のmodelだけを変えると、Terraは68 / 70（token`+23.81%`、所要時間`-12.73%`）、Lunaは67 / 70（品質`-7.143`、token`+136.06%`、所要時間`+13.29%`）。Lunaの未達3件はすべてA01でrequired value未解決のまま試験へ進み、1回あたり`650,395`〜`870,391` tokenを使った | 一次resultのKPI表と未達内訳、preflightの機械照合 | [`candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md`](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md)（Sol `96fb5713…` / Terra `b328615b…` / Luna `0736e412…`） | modelはkeyに含まれるため3 resultは互換キーが異なる。modelだけを事前宣言した変更軸とし、preflightで`$.comparison_conditions.model`と`$.profile_id`以外の差分がないことを機械照合 | `descriptive_cross_layer`（KPI差）／`established_same_condition`（条件の機械照合） | 「同一系列内の3 model・各`N=5`で維持されなかった」まで。「model一般への依存」ではない。**「C43が閉じた境界がLunaで再び落ちた」という接続は、A01の失敗形が同一（未解決値のまま試験へ進行）であることに基づく解釈である** | 文言限定で対応 |
| R10-3 | 10.2 | Click側でC81はcontrol-free比token中央値`-28.79%`、所要時間`-12.62%`、品質70 / 70件が4点。モデルステップ`-35.06%`、キャッシュ済み入力`-33.92%`。変更前の履歴探索はcontrol-freeの`0 / 10`に対しC81が`4 / 10` | 一次resultと残余経路分析 | [`click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md`](../evaluations/targets/click/results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md)、[`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md) | Click instance、CLI `0.144.0`、rating別（instance固有） | `established_same_condition`（Click instance内）／`descriptive_cross_layer`（対象リポジトリ側との関係） | Click内での比較。`quality_score`の絶対値をinstance間で比較しない（`evaluations/CLAUDE.md`の規則） | 不要 |
| R10-4 | 10.2 | C125本文を1バイトも変えずにClickへ移すと`70 / 70`が有効、分布`4 = 65` / `1 = 5`、品質中央値`94.643`、token中央値`1,348,515`、所要時間`786.007`秒。`1`点の5件はすべてF10で`authority_unavailable`停止 | 一次resultの全体結果表 | [`click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md`](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md)（result ID `7560599fef024dfb8011264352707ab8`）、[`click-c125-full-portability-design.md`](click-c125-full-portability-design.md) | Click C125 `39dcb70f…` | `established_same_condition` | 「停止境界という機構は別リポジトリでも作動した」まで。**14課題全体の成功は成立していない。** 停止が正しい挙動であるという読みは、事前に採点契約へ組み込んでいない | 同条件再試験が必要（正本をそろえた条件、および停止を事前に契約へ組み込んだ再測定） |
| R10-5 | 10.2 | Click C81（CLI `0.144.0`）とClick C125（`0.146.0`）は互換キーが一致しないため、tokenと所要時間の差は算出できない | 両resultの固定条件 | Click C81 result、Click C125 result（「compatibility keyが異なるため、tokenとelapsedの差は算出しない」） | — | `established_same_condition` | 比較不成立の記述 | 同条件再試験が必要（現行CLIで両者を再実行） |
| R10-6 | 10.3 | 未知のtarget一般への移植性は示していない。ClickはC125に対する独立な外部検証集合でもない | 測定範囲とClick観測の設計利用 | [`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md)（残余経路の観測が後続候補設計へ接続）、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §7 | — | `unverified` | 「示していない」の記述 | holdout targetが必要 |

### 2.11 第11節 考察

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R11-1 | 11.1 | Baselineの各工程と、変換後の判定条件を1対1で対応づけられる。削除された工程（プランSA、レビューSA、実装SAへの必須委任）は責務の置き場所が変わり、残った工程（検証、完了判定）は発行単位と結果のbind状態として残った | Baseline本文とC125本文の対応 | Baseline root `AGENTS.md`・`orchestration-process.md`・4ロールプロンプト、C125 root `AGENTS.md.txt`（`SPEC` / `PRODUCER` / `TERMINAL` / `CONTEXT` / `VALIDATION_CLOSURE` / `VALIDATION_PLAN` / `RECOVERY`）、Standard14のF10（レビュー責務の受け皿） | bundle実体 | `historical_design_record` | **この対応表は本論文が構成した解釈である。** 各行が「意図的な置換」として記録されているのはC35（7 target置換）、C43（SPEC置換）、C118（terminal化）などの個別manifestに限られる。全体を1つの変換として設計した記録はない | 文言限定で対応（「本論文が構成した対応」と明示） |
| R11-2 | 11.2 | Baselineは品質責務と工程を同じ文章で表現しており、工程を削ると責務も消え、責務を守るために不要な工程を払い続ける状態だった | R6-1（工程削除で責務が落ちる）、R5-3 / R5-4（不要な委譲） | 層B result、`v3-all-agent-token-reaccounting`、`baseline-candidate1…candidate5` result | 層B・層A | `exploratory` | 2種類の観測の統合による解釈。単一実験による検証ではない | 不要 |
| R11-3 | 11.3, 要旨 | KPI低下は費用削減ではなく、5条件を満たす場合に「不要な実行経路の減少」として読める。該当する観測はBaseline→C43、C43→C71、C98→C104、C118→C125、Click control-free→C81である | 各比較のKPI・分布・診断値 | 該当する各一次result（R7-7、R7-8、R7-10、R7-13、R10-3） | 各層内 | `established_same_condition`（各比較個別）／`exploratory`（5条件という枠組み） | 5条件は本論文が定義した読み取り規準である。各比較は同一key内で成立するが、**層をまたいだ連結はしない** | 不要 |
| R11-4 | 11.3 | 5条件を満たさない例として、C33はtoken中央値`-24.63%`だが`quality_score`中央値も`-6.250`低下した | 一次result | [`candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md`](../evaluations/results/candidate33-worker-context-sufficiency-owner-producer-v5-expanded12-global-m24-n5_2026-07-18.md)、[`control-mechanisms.md`](control-mechanisms.md) メカニズム2 | 層A系（拡張12課題、旧rating） | `established_same_condition`（当該key内） | この条件の観測。層Bの数値と連結しない | 不要 |
| R11-5 | 11.4 | 正味token差 = 制御文の読解cost + 追加された判断・確認cost − 回避できた探索・context継承・再読・再試行・手戻りcost | 各系列の符号の一致 | [`prompt-control-design-principles.md`](prompt-control-design-principles.md)、既存論文第10節、R8-1 / R7-8 / R8-4 | 複数層 | `exploratory` | 観測を整理する枠組みである。3項を個別に計装して測定したわけではない | 同条件再試験が必要（項別の計装） |
| R11-6 | 11.5 | 指示書が制御できるのは、返された結果をどう分類し次に何を選ぶかまでである | R8-3 | 上記 | 層C | `exploratory` | C90〜C97・C105〜C111の失敗範囲まで。「原理的に不可能」ではない | 不要 |
| R11-7 | 11.6 | 制御はmodelと実行環境へ強く結合しており、CLI版更新で比較が失効し、model変更で品質とコストが維持されなかった。B20の概算は1条件約`$311`、2条件約`$622` | R10-2、R10-5、換算単価による外挿 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、[`research-backlog.md`](research-backlog.md) §12 | — | `descriptive_cross_layer`（結合の観測）／`exploratory`（費用外挿） | 金額は換算値の線形外挿で、実測でも実請求額でもない。人間の時間を含まない | 不要 |
| R11-8 | 11.7 | 料金換算では14課題×5回ぶんがBaseline `$91.6701`、0バイト対照`$25.1562`、C125 Sol `$15.5472`、Terra `$6.5447`、Luna `$0.9571`。同一互換キーで成立する比較はBaselineと0バイト対照（`3.64倍`）だけである。C125の`0.62倍`を制御による費用削減として読まない | 換算の集計と単価、各条件の互換条件 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、各一次resultのtoken内訳 | Baselineと0バイト対照はv13 / CLI `0.144.0`（同一key）。C125系はv14 / `0.146.0` | `established_same_condition`（`3.64倍`）／`descriptive_cross_layer`（他の行） | **補助指標であり研究の指標ではない。** 単価に依存し実請求額でもない。指示書単体の注入コストは算出できない | 同条件再試験が必要（v14 / CLI `0.146.0`での0バイト対照） |

### 2.12 第12節 限界

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R12-1 | 12.1 | Standard14は候補の生成・選別に繰り返し使ってきた課題集合であり、C125の`70 / 70`は未使用課題による独立確認ではない。Clickも独立な外部検証集合ではない | 基盤規則と設計利用の記録 | [`evaluations/cases/README.md`](../evaluations/cases/README.md)（「このセットでpromptを調整した結果を、そのまま未使用caseでの最終確認結果とは扱わない」）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)（「tuningに使ったcaseを同一revisionのheld-out evidenceとして扱わない」）、[`click-c81-medium-residual-analysis.md`](click-c81-medium-residual-analysis.md) | — | `established_same_condition` | 反復適応を除外できないことの記述 | holdout targetが必要 |
| R12-2 | 12.2 | 主targetは非公開1件、公開targetは`pallets/click` 1件で、後者では14課題全体の成功が成立していない | 各resultのtarget欄、R10-4 | 各result §固定条件、[`evaluations/targets/README.md`](../evaluations/targets/README.md) | — | `established_same_condition` | 測定範囲の記述 | holdout targetが必要 |
| R12-3 | 12.3, 9.2 | 最大反復は1,400回（B20）。C125はB20未実施、`N=100`未着手であり、`70 / 70`はC95がB20で落ちた事例と同じ証拠水準にある | B20 resultとC125 resultのstatus | [`C81 / C95 B20`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md)、[`C118 / C125`](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)、[synthesis](candidate81-candidate125-control-findings-synthesis.md) §現在状態 | 層C | `established_same_condition` | 証拠量の記述。C81のB20で代替しない | 長期反復が必要 |
| R12-4 | 12.4, 3.5 | 14課題はすべて単発で、部分的に曖昧な長期作業のcaseもevaluation setも存在しない。この未測定領域は実務利用（対話形態）に当たる | 該当caseの不存在とbacklogの記述 | [`research-backlog.md`](research-backlog.md) §11（「未着手・該当caseなし」「このリポジトリの実務利用は対話形態であり、この条件は実利用へ近い」） | — | `unverified` | 未測定であることの記述 | holdout targetが必要（新case family設計＋rating revision） |
| R12-6 | 12.6 | 信頼区間、課題ブロック考慮の効果量、課題別の反復分布は算出していない。検定を適用したのはB20規模のC81 / C95比較だけである | 各resultの統計記述 | 各result（検定はB20 resultのみ）、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md) | — | `established_same_condition` | 統計処理の範囲の記述 | 同条件再試験が必要（推測統計を行う場合） |
| R12-7 | 12.7, 4.6 | 採点は独立した盲検の第三者ではなく、固定契約による監査である | 基盤規則と各resultの採点記述 | [`evaluations/cases/README.md`](../evaluations/cases/README.md) §採点、各result（「採点は独立blind quality raterによるものではない」） | — | `established_same_condition` | 採点方式の記述。契約欠陥の実例はR8-6 | 独立採点が必要 |
| R12-8 | 12.11, 8.1 | 表面圧縮系列の動的量は集計軸が不統一で、候補間の横断比較ができない | 各候補resultの集計単位 | 各候補result | — | `established_same_condition` | 集計軸の不統一の記述 | 同条件再試験が必要（同一軸への再集計） |
| R12-11 | 11.6 | 保守費用の概算は換算値の線形外挿で、実測でも実請求額でもなく、人間の時間を含まない | 換算方法 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md) | — | `exploratory` | 外挿であることの記述 | 不要 |
| R12-12 | 11.6 | 制御の便益（確認して止まる、誤停止しない、手戻りが減る、待ち時間が短い）を利用者側の価値として測っていない | 測定範囲 | 3 KPIの定義（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)） | — | `unverified` | 未測定であることの記述 | holdout targetが必要（実務利用の測定設計） |
| R12-13 | 11.7 | `$25.1562`（v13 / `0.144.0`）と`$15.5472`（v14 / `0.146.0`）の差`-38.20%`は互換キーが違うため制御の効果量ではない | 両条件の互換条件 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、各一次result | — | `descriptive_cross_layer` | 並置にとどまる | 同条件再試験が必要 |
| R12-15 | 12.8 | 所要時間はprompt差から分離されていない。`M=24`の共有待ち行列で実行順のランダム化・交互配置・時刻ブロック化をしておらず、負荷も記録していない。例外はC81 / C95 B20の交互実行だけである | 各resultの実行スケジュール記述 | 層B result（「5つの新規campaignは同時実行せず、Baseline、CFR、C5、C35、C43の順に実行した」）、B20 result（「奇数batchはC81→C95、偶数batchはC95→C81」） | — | `established_same_condition` | 交絡が残ることの記述。`elapsed_seconds`は記述値として扱う | 同条件再試験が必要（`M=1`および順序統制） |
| R12-17 | 11.7 | 指示書単体の注入コストは算出できない。キャッシュ済み入力`$2.4741`（総額の`15.91%`）は複数要素が混在した区分の換算額である | 換算の内訳 | [`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)、既存論文7.5節 | 層C（C125 Sol） | `established_same_condition`（区分総額）／`unverified`（指示書単体） | 区分総額までが上限。root指示書の寄与は分離できない | 同条件再試験が必要（入力要素別のtoken計装） |
| R12-20 | 12.13 | この文書は仮組みであり、いずれの状態についても正本ではない | 文書の位置付け | 本文書の冒頭 | — | — | 記述 | 不要 |

### 2.13 第13節 結論

| Claim ID | 論文節 | 主張 | 必要な証拠 | 一次資料 | compatibility key／条件 | 証拠水準 | 現状の表現上限 | 再試験 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R13-1 | 13 | 品質を支えていたのは擬人的な工程全体ではなく、仕様・証拠・実装・検証・停止を区切る観測可能な実行境界であり、この境界へ再構成することで評価範囲内では品質を維持しながら不要な実行経路とKPIを削減できた | R5-*、R6-*、R7-*、R8-*の統合 | 上記すべて | 複数層（連結しない） | `supported_repeated_observation`（境界の抽出）／`established_same_condition`（各層内のKPI） | **「評価範囲内では」が必須の限定である。** 評価範囲 = Standard14（反復適応あり）、`gpt-5.6-sol`、Codex CLI、単発作業、最大`N=5`（C125）。この限定を外した一般化は成立しない | 長期反復・holdout target・独立採点がいずれも必要 |

---

## 3. 既存証拠では接続できない主張（再試験候補）

以下は、論文仮組みの中で**主張として書けなかった**か、**限定付きでしか書けなかった**接続である。本文では該当箇所に留保を置いている。

| # | 接続したい主張 | 現在言えること | 不足している証拠 | 必要な再試験 | 概算規模 |
| --- | --- | --- | --- | --- | --- |
| 1 | C125の`70 / 70`は長期的にも安定である | `N=5`で70 / 70。同じ証拠水準のC95はB20で2件落ちた | 1,400回規模の反復 | 長期反復が必要 | 標準14項目B20、1条件1,400回、換算約`$311` |
| 2 | 品質境界を閉じたうえで費用も下げた | v13 / CLI `0.144.0`の0バイト対照と、v14 / `0.146.0`のC125の換算額を並置できるだけ | 同一互換キーでの0バイト対照 | 同条件再試験が必要 | 標準14項目`N=5`、70回、換算約`$16`相当 |
| 3 | 各境界は単独で必要である | 版と版の差までしか言えない | 境界ごとのablation条件 | 同条件再試験が必要 | 6境界 × 70回 = 420回程度 |
| 4 | 境界を閉じる順序に必要性がある | 実際に開発が進んだ順序である | 順序入れ替え条件、同時追加条件 | 同条件再試験が必要 | 条件数に比例 |
| 5 | 指示書は別リポジトリへ移植できる | 停止境界という機構は再現した。14課題全体の成功は成立していない | 正本をそろえたClick条件、および未使用リポジトリ | 同条件再試験＋holdout targetが必要 | Click再測定70回＋新target構築 |
| 6 | Click F10の停止は正しい挙動である | 現行契約はscore `1`と評価している | 停止を成功と判定する条件を事前に組み込んだrating revisionと再測定 | 同条件再試験が必要 | rating revision＋70回 |
| 7 | 仕様確定の境界は長期・部分曖昧タスクでも働く | 単発課題での観測しかない。該当caseが存在しない | 部分曖昧・複数段のcase family、誤停止と過剰問合せを区別する採点条件 | holdout targetが必要 | 新case family設計＋rating revision＋反復 |
| 8 | 制御はmodel系列を跨いで移る | 同系列3 modelで維持されなかった。Claude系は0件 | 別model系列での測定 | holdout targetが必要 | Claude Code CLI adapter実装（現在保留）＋70回 |
| 9 | 採点は採点者依存でない | 固定契約による監査である。契約欠陥の実例が2件ある | 独立した第三者採点者による再採点 | 独立採点が必要 | 既存runの再採点 |
| 10 | 表面圧縮候補の間で動的量を比較できる | 符号の不一致だけが読める | 全候補を同一集計軸へそろえた再集計 | 同条件再試験が必要 | 既存resultからの再集計（新規実行不要の可能性あり） |
| 11 | 指示書本文の注入コストが分かる | キャッシュ済み入力という区分の総額だけが分かる | 入力要素別のtoken計装 | 同条件再試験が必要 | 計装実装＋再実行 |
| 12 | 委譲がall-agent tokenに占める比率は標準14項目でも56%程度である | 拡張12課題・`high`・旧ratingでの比率である | 層Bまたは層Cでのroot / worker別token内訳 | 同条件再試験が必要 | 既存runの診断値再集計の可能性あり |
| 13 | Baselineの各工程と変換後の判定条件が1対1に対応する | 本論文が構成した解釈である | 変換を1つの設計として記録したartifact（存在しない） | 文言限定で対応（解釈である旨の明示） | — |
| 14 | 「9つの品質責務」がBaseline作者の意図した分類である | 本論文が本文から取り出した整理である | 当時の責務列挙artifact（存在しない） | 文言限定で対応 | — |

---

## 4. 一次資料と要約文書の相違・留保

一次資料を正本として確認した結果、要約文書の記述に対して補正または留保が必要な箇所を記録する。**過去のartifactはin-placeで変更していない。**

### 相違1: `ControlFreeRepository`に残っているものの記述

- **既存論文の記述**（3.1節、付録A.2、第14節の限界16）: 「root `AGENTS.md`だけを0バイトにし、配下ディレクトリごとの指示書4件はそのまま残した対照（TaskSpecと実行環境設定も残る）」
- **一次資料**: `the-caption-3ce91a4-control-free-repository-r1/manifest.json`と`the-caption-3ce91a4-current-r2/manifest.json`のtarget別SHA-256を照合すると、差分targetは`AGENTS.md`のみ。すなわち`docs/orchestration-process.md`（24,209 bytes）、`docs/prompt-guide.md`（15,421）、`docs/glossary.md`（4,086）、`prompts/plan.md`（4,183）、`implement.md`（2,128）、`audit.md`（5,161）、`review.md`（3,910）も**Baselineと同一のまま残っている**（合計59,098 bytes）。
- **補正**: 既存論文の記述は誤りではないが不完全である。この条件は「擬人的な工程仕様が置かれたまま、それを呼び出すrootの制御だけを外した状態」である。仮組みでは6.1節・12.10節でこの内訳を明示した（R6-2）。
- **解釈上の帰結**: `-70.80%`というtoken低下は、工程仕様の文書量が減ったことによるものではない。**文書が存在しても、rootの制御がその工程へ入らなければ実行量は生じない**という読み方が可能になる。

### 相違2: C35の工程仕様の状態

- **既存論文の記述**（3.1節）: 「rootの実行制御は残し、旧来の役割説明や手順説明は見出しだけの空の受け皿に置き換えた」
- **一次資料**: 該当7 targetは`0`バイト（`git_blob_sha1: e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` = 空blob）である。「見出しだけの空の受け皿」ではなく**完全な空ファイル**である。
- **補正**: 仮組みでは7.2節で0バイトと明記した（R7-5）。なお`non_goals`に「bundle target数の削減または削除tombstoneの導入」が挙げられており、**targetを消さずに内容だけを空にした**理由は、bundle target集合を比較条件として固定するためである。

### 留保3: C35の置換根拠となったcommand evidenceはリポジトリ内にない

- C35のmanifestは「expanded12 × N=5の保存済み観測で成功commandから参照されなかった」と記録しているが、その根拠となるraw command evidenceは外部のresult registry（`/Users/kenn/repos/_verification/…`）にあり、このリポジトリへcommitされていない（基盤規則が「raw execution evidenceをrepositoryへcommitしない」と定めている）。
- したがってR7-5の証拠水準は`historical_design_record`である。byte数と0バイト化はbundle実体から独立に確認できるが、**非参照の観測そのものはmanifestの記述を信頼している**。

### 留保4: 「品質責務9項目」と「Baselineの工程対応表」は本論文の構成

- 1.3節の9項目、3.2節の責務番号列、11.1節の変換対応表は、いずれもBaseline本文とC125本文から本論文が構成した整理であり、当時のartifactにこの分類として記録されているものではない。該当Claim（R1-5、R3-1、R11-1）の証拠水準は`historical_design_record`とし、再試験欄は「文言限定で対応」とした。

### 留保5: 設計記録は「人間の組織図の写し取りではない」と述べている

- `docs/prompt-guide.md`は分業を「人間の組織図の写し取りではない」「AI に存在しない制約を捨て、AI 固有の失敗様式に向けて作り直した統治の形」と明示している。
- したがって「人間の開発プロセスをそのままprompt化した」という表現は、**工程・成果物・関所の構造については成立するが、役割分担の設計意図については成立しない**。仮組みでは1.2節でこの区別を明示し、研究の出発点を「工程構造を移植し、各工程の目的をAI固有の失敗様式へ再設計した初期解」と述べた（R1-3、R1-4）。
- **この留保は研究の論証を弱めない。** むしろ「AI固有の失敗様式へ向けて設計されたと当時考えられていた工程構造でも、AI実行としては不要な経路を含んでいた」という形で、問いを鋭くする。

### 留保6: 層Aの数値は推論`high`である

- 層A（拡張12課題）の結果は推論`high`、層B・層C・層Dは`medium`である。既存論文2.5節も同じ層分けをしている。仮組みでも層をまたいだ連結はしていない（R4-3）。

### 留保7: atomic run経路のEvaluation set identityが層Bと異なる

- 層Bのset identityは`430d1d4b…`、C125のmodel軸resultは`2096d15e…`である。これはatomic run経路でのidentity計算が異なるためであり、`evaluations/AGENTS.md`が「atomic run経路では`N`、coverage、iteration集合、計画順序、`max_workers`をrunの実効互換条件へ含めない」と定めている。同じ`the-caption-standard14-r1`だが、identity値としては別である。**この2つのidentity値を同一視しない。**

---

## 5. 数値のsource一覧（仮組み本文に出る主要数値）

| 数値 | 出所 | 条件 |
| --- | ---: | --- |
| Baseline root `5,980 bytes` | `prompts/baselines/the-caption-3ce91a4-current-r2/files/AGENTS.md.txt` | bundle実体 |
| CFR root `0 bytes` | `prompts/candidates/the-caption-3ce91a4-control-free-repository-r1/files/AGENTS.md.txt` | bundle実体 |
| C5 `7,725` / C35 `3,235` / C41 `3,482` / C43 `3,980` / C71 `4,987` / C81 `5,525` / C125 `10,908` bytes | 各candidate bundleの`files/AGENTS.md.txt` | bundle実体 |
| 工程仕様7 target合計 `59,098 bytes` | Baseline bundleの該当7 file | bundle実体（24,209 + 15,421 + 4,086 + 4,183 + 2,128 + 5,161 + 3,910） |
| 層Bの全KPI（7条件） | [層B result](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)、[C71 / C81 result](../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md) | `79ed04a4…` |
| 層Aの全KPI（4条件） | [層A result](../evaluations/results/baseline-control-free-repository-c35-c41-outcome-quality-owner-diagnostic-v9-expanded12-n5_2026-07-19.md) | `abc7d7a9…` |
| root-only / all-agent内訳 | [`v3-all-agent-token-reaccounting`](../evaluations/results/v3-all-agent-token-reaccounting_2026-07-16.md) | 層A系、旧rating、`high` |
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
| B18のtool call `-30.16%`、モデルステップ`-26.54%` | [C69 / C71 B18 result](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md) | v12、`high`系、標準14項目 |
