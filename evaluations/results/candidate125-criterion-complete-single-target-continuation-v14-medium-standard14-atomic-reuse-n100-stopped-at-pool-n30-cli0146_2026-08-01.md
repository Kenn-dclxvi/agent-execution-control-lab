# Candidate125 Rating v14 Medium Standard14 N=100追試停止結果

## 結論

Candidate125のStandard14 N=100追試は完了していない。compatible atomic poolを各case 30件まで拡張した時点でF04にscore `2`を5件確認し、その後のN=50 batchをユーザー指示で中断した。

現在状態は`n100_execution_stopped / registered_pool_n30 / score2_observed / n30_selection_result_not_created / n50_partial_unrated_unregistered`である。Candidate125の既存`adopted / release_projected / runtime_projected` stateは、この追試結果で履歴上書きしない。

## 固定条件

- prompt: `the-caption-3ce91a4-criterion-complete-single-target-continuation-r1`
- bundle SHA-256: `60e95bfe7f9e09a0cbb2fb980c54f1cd1bd671c37509976e7e88574adf911435`
- evaluation set: `the-caption-standard14-r1` revision `r1`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model: `gpt-5.6-sol`
- reasoning: `medium`
- Codex CLI: `0.146.0`
- Python: `3.14.5`
- configured max workers: `M=24`
- Candidate125 pool key: `9437d24c1a536cd10f61a17badac01537045862554dec8f43f5477f394d6f830`

prompt、set、case revision、fixture、TaskSpec、rating、model、reasoning、runtime、CLI、permission、executor、token accountingをatomic run単位で固定した。N、iteration集合、coverage、計画順序はexecution provenanceとして分離した。

## 登録済みpoolの状態

既存N=5を再実行せず、不足runだけを追加した。各14 caseに30件、合計420 atomic runが登録済みである。

| scope | score 4 | score 2 | total |
|---|---:|---:|---:|
| 全registered pool | 415 | 5 | 420 |
| F04 | 25 | 5 | 30 |
| F04以外 | 390 | 0 | 390 |

batch-n010の新規65件はすべてscore `4`だった。batch-n030の新規270件はscore `4 / 2 = 265 / 5`だった。全5件のscore `2`は`TC-F04-WEB-AUDIT-COLUMN-VISIBILITY`で発生した。

この420件はpool member数である。case別30件を固定するselection receiptと集約analysisを作成していないため、正式な`N=30 result`とは記載しない。

## F04 score 2の共通経路

対象runは次の5件である。

- `fd0343d8198f433ea1377536b741980e`
- `24520644defc4c9bbd286ebe1220fa67`
- `aaea372253ff44e3a99e029b3f9df141`
- `1664ae1804354e14806eecb6bf904c67`
- `fd11349c90264ed29699065248723057`

全runで`App.tsx`の終端までを取得し、現在の`colSpan={hasAuditKey ? 7 : 6}`と`py-20`はmodel-visibleだった。必要な変更は`const hasAuditKey = true;`をdata依存式へ変える一箇所だけだった。

しかし各runは、正しい`hasAuditKey` hunkと、開始状態に存在しない`colSpan={7}`および`py-24`を前提とする不要なhunkを一つのatomic patchへ入れた。preimage不一致によりpatch全体が失敗し、retryでも観測値ではない`colSpan={6}`を推測した。machine rework上限到達後に変更と3 Node commandを実施せず停止したためscore `2`になった。

これはevidence不足、fixture drift、executor failureではない。変更operationへ入れるcurrent-content operandを観測済みcontentへbindせず、開始状態ですでに充足済みのF04-C2にも変更単位を作ったmodel-visible判断が原因である。atomic applyは失敗を増幅したが、executor変更を解決策にしない。

## 中断したN=50 batch

N=50へ向けた次batchは、ユーザーの停止指示を受けてcontrollerと子processを終了した。停止時点で`attempts.jsonl`は54件、terminal bindingは52件だった。summary、seal、rating、atomic registrationはない。

このpartial batchを品質分布、pool count、N=30またはN=50 resultへ含めない。N=70以降は発行していない。

## 後続判断

F04の5件を作成根拠として、Candidate126の[`criterion-bound change input設計`](../../docs/candidate126-criterion-bound-change-input-design.md)を分離した。Candidate125のN=100追試は再開せず、partial evidenceと登録済みatomic runを保持する。
