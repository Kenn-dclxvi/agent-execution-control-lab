# Candidate78 project index navigation設計記録

## 結論

Candidate78はCandidate71を直接sourceとする。Candidate71の11 labelと最短正常経路を変更せず、required outcomeに必要な静的project事実がTaskSpecで未解決の場合だけ、repository-wide探索の前に`docs/reference/project-contexts/the-caption.txt`を索引として参照する。

commandの並列化、read件数、batch方法は固定しない。indexはTaskSpec、path-scoped `AGENTS.md`、対象source / test、git stateを置換しない。

## Candidate作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-closure-r1`（Candidate71）とする。最短正常経路は、TaskSpecが対象を直接固定している場合は対応するpath-scoped authorityとsource / testだけを確認し、一つのproducerで成果を生成し、required validationを一つのwaveで閉じてterminalへ進む経路である。
2. 保存済みCandidate71 rating v13のA02 N=5では、5 / 5 runがrepository-wideな`rg`または`rg --files`を実行し、index本文の直接readは0 / 5だった。各runはscore `4`だったが、all-agent tokenは`156,276〜339,274`に分布した。
3. A02のTaskSpecはcanonical targetをrepository authorityと現行entrypoint実体から解決するよう求める。indexには`src/app/entrypoints/v4_daily_main.py`がcanonical daily entrypointとして記録済みだが、Candidate71のroot `AGENTS.md`に導線がなく、現行のrole promptは0-byteである。実行役はindex自体をrepository探索で発見する必要がある。
4. 追加する一つのpredicateは、`project_index_required := required outcomeに必要なproject / command / architecture / environment / testingの静的事実がTaskSpecで未解決`である。`project_index_required=true`の場合だけindexをrepository-wide探索の前に参照する。
5. このpredicateが消す判断点は、canonical targetまたはproject全体の静的構造を解決するために、まずどのrepository-wide file inventory、README、history、sourceを探索するかという入口選択である。
6. 増える判断点は、未解決事実がindexの扱う静的事実かという1回の分類と、条件成立時のindex readである。index本文の5,868 byteがmodel contextへ増える。
7. 品質は標準14項目各N=5、rating v13で確認する。score `4 = 70 / 70`と全caseの完了を必須とする。A02をtrigger確認、F10 EntryをTaskSpecで対象が閉じたnon-trigger確認とする。
8. KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3つとする。index read、repository-wide探索、tool call、worker起動はdiagnosticとする。A02で広域探索が減る方向と、index追加costだけが増える方向の両方を事前仮説とする。
9. score `4`未満、required validation欠落、unexpected worker、A02のrepository-wide探索が減らない、F10 Entryで不要なindex readが増える、または3 KPIのいずれかが期待と逆方向の場合は停止する。追加predicateをCandidate78へ継ぎ足さない。

## 変更境界

- direct source: Candidate71
- 追加: root `AGENTS.md`の`PROJECT_INDEX` 1 label
- 非変更: 残り18 target、index本文、TaskSpec、evaluation set、rating、permission、executor parameter、THE-CAPTION runtime
- adoption / release / runtime projection: 未実施

## Candidate状態

- candidate number: Candidate78
- prompt identity: `the-caption-3ce91a4-project-index-navigation-r1`
- evaluation status: `standard14_evaluated`
- state: `stopped`
- result ID: `79be353bf88940bda9344d2f341511b9`

## 評価結果

標準14項目各`N=5`は70 / 70件がvalid・rateableかつscore `4`だった。Candidate71比の公式Layer 4中央値差は、quality `0.000`、all-agent token `+184,448`（`+8.66%`）、elapsed `+48.817`秒（`+4.38%`）だった。

A02ではindex先行readが0 / 5から5 / 5へ変わったが、repository-wide探索は5 / 5のままだった。F10 Entryでは不要なindex readを2 / 5で観測した。作成前gate 9の停止条件に該当するため、Candidate78へ追加predicateを継ぎ足さず停止する。

## Evidence

- [Candidate71設計](candidate71-validation-closure-design.md)
- [Candidate71 rating v13標準14結果](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)
- [Candidate71 / Candidate78 rating v13標準14結果](../evaluations/results/candidate71-candidate78-project-index-navigation-v13-standard14-n5_2026-07-26.md)
- [Candidate50対象試験](../evaluations/results/candidate43-candidate50-root-read-batch-targeted-n5_2026-07-21.md)
- [Prompt制御の検討原則](prompt-control-design-principles.md)
