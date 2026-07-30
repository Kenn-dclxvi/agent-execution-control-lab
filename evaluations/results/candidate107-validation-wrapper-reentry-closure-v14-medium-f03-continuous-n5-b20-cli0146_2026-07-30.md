# Candidate107 validation wrapper再入closure Rating v14 Medium F03 N=5 B20

## 結論

Candidate107をF03 r2で20 batch、各batch `N=5`、合計100件実行した。100 / 100件がvalid・rateable・score `4`で、登録resultのexcluded attemptは0件だった。

実害として観測していた経路は閉じた。focused validation完了からfull validation完了までの途中messageは0 / 100、required validation再実行も0 / 100だった。cell ID付きnonterminal resultは6件あったが、6 / 6件とも次actionはmessageや判断ではなく、同じcell IDへの`wait`だった。

一方、outer deadlineが内部required commandのwait deadlineより短い設定は4 / 100件だった。作成前に固定したzero gateを満たさないため、現在状態を`targeted_f03_b20_evaluated / quality_gate_passed / wait_only_gate_passed / outer_deadline_gate_failed / result_registered / stopped`とする。Standard14、採用、release、runtime projection、本体反映へ進めない。

## 固定条件

| 項目 | 値 |
| --- | --- |
| prompt | `the-caption-3ce91a4-validation-wrapper-reentry-closure-r1` |
| bundle SHA-256 | `72c6f4b8818065300ca24fd0a42bdf49ce834ae44d4f2406da497f98c064c50d` |
| direct parent | Candidate106 |
| case | `TC-F03-ATOMIC-CONTEXT-CLEANUP/r2` |
| Evaluation set | `the-caption-standard14-r1/r1` |
| set identity | `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33` |
| fixture identity | `5fbbf3e5de7bdb51b8d9586707a63ce6e88b3fad3286f5b00fa984cf080aa52e` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| CLI / Python | Codex CLI `0.146.0` / Python `3.14.5` |
| repetition | `N=5 × B20 = 100 run` |
| execution | global queue、profile上の`M=24` |
| token accounting | all-agent v1 |
| compatibility key | `1c49658de3696219b6bfefb620df32976cc9fde6a1f4460cabea327b1ad33477` |

最初の5件用profileは[`Candidate107 F03`](../profiles/candidate107-validation-wrapper-reentry-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json)である。prompt identity以外の条件はCandidate106 F03 N=5 profileと同一である。

## 実行形

最初は5 slotずつの逐次batchで開始した。ユーザー指示によりbatch 1完了後に切り替え、残り19 batchは4 batch・20 slotを一つのglobal queueへ入れるwaveを4回、3 batch・15 slotのwaveを1回実行した。各planとcomparison conditionsの`max_workers`は`24`を維持した。

切替時に旧campaignのbatch 2でiteration 4を一件開始していたため中断した。このattemptはcontroller exit code `-2`の非terminal実行として保管し、品質採点、result登録、100件の集計へ含めていない。再構成後の登録100件にexcluded attemptはない。

## 品質結果

| 指標 | 結果 |
| --- | ---: |
| valid / rateable | `100 / 100` |
| score `4` | `100 / 100` |
| required command evidence | `100 / 100` |
| focused / full success | `100 / 100` |
| 登録resultのexcluded attempt | `0` |

## Mechanism結果

| 診断 | Candidate106 B20 | Candidate107 B20 |
| --- | ---: | ---: |
| outer `yield-time_ms=1000` | `15 / 100` | `3 / 100` |
| cell ID付きnonterminal result | `15 / 100` | `6 / 100` |
| required validation間の途中message | `1 / 100` | `0 / 100` |
| focused validationを1回実行 | `100 / 100` | `100 / 100` |
| full validationを1回実行 | `100 / 100` | `100 / 100` |

Candidate107でcell ID付きnonterminal resultを返した6件は、直後のactionが6 / 6件とも同じcell IDへの`wait`だった。cell ID mismatchは0件で、途中messageも0件である。したがって、nonterminal再入後のwait-only遷移は今回の100件で成立した。

outer deadline分布は、未指定19件、1秒3件、30秒22件、60秒5件、120秒40件、240秒1件、300秒10件だった。内部waitより短いouter deadlineは4件で、内訳は1秒3件と、内部300秒に対するouter 30秒1件である。

また、outerを未指定にしてもcell ID付きnonterminal resultが4件発生した。outerと個別の内部waitを同値にしても、複数commandの累積時間によってnonterminal返却は起こり得る。このため「outer deadlineを内部wait以上にする」は、wrapperをterminalまで一回で閉じる十分条件ではない。

## KPI診断

Candidate107の100件について、all-agent token中央値は`115,801`、範囲は`87,346〜172,003`だった。elapsed中央値は`87.192`秒、範囲は`60.493〜120.956`秒だった。20個のbatch内中央値の中央値はtoken `115,649.0`、elapsed `88.139`秒である。

Candidate106の保存B20はF03とF08を同じresult coverageへ含み、今回のCandidate107はF03だけである。compatibility keyが異なるため、両者のtoken・elapsed差を正式なLayer 4 KPI比較として扱わない。上表のmechanism件数だけを同じF03 event定義による診断比較とする。

## 判定

事実として、Candidate107はCandidate106で残った途中messageを1 / 100から0 / 100へ減らし、nonterminal返却後のwait-only遷移を6 / 6件で成立させた。

同時に、promptが禁止したouter deadline設定は4 / 100件で再発した。結果として、制御の価値は「nonterminal result自体をゼロにしたこと」ではなく、「nonterminal resultが返っても余計なmessage・判断・別toolへ分岐させなかったこと」にある。outer deadline clauseは狙った保証を提供せず、作成前gate不通過である。

## Result identityと保存場所

- Batch 1 result ID: `ee8f476f6be04452848fb7e8b0bb1662`
- Batch 20 result ID: `e698870a4e0f4817a474c50c3d938930`
- 20 resultのcompatibility key: `1c49658de3696219b6bfefb620df32976cc9fde6a1f4460cabea327b1ad33477`
- campaign summary SHA-256: `bf56a47055ebff6b4ed8fac36a6d209f1cec6ae7b0029014c9162d0e32aa63ae`
- mechanism audit SHA-256: `5f1e09752dac702b7a3a6bc95ca7c45c501bf36142ead3288dd195d3daf512db`
- mechanism audit script SHA-256: `a9c1239a453cc7c7cced88d145c03dafbdc8b5403993efd9908a55bcd08ed417`
- sequential campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate107-validation-wrapper-reentry-closure-v14-medium-f03-continuous-n5-b20-cli0146-20260730-r1`
- parallel-wave campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate107-validation-wrapper-reentry-closure-v14-medium-f03-continuous-n5-b20-cli0146-20260730-r2`

raw rollout、全20 result ID、機械分類artifactはverification checkoutへ保持し、このrepositoryへcommitしない。
