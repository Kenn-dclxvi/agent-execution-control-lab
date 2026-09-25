# C276 実行制御文の比較設計

## 目的

利用者が提示した「実行制御」4項目をC276として固定し、C275と同じStandard14・GPT-6 Luna High・N=5で比較する。これはprompt identityだけを変える固定benchmark比較であり、C276が特定の失敗を防ぐ、品質または費用を改善する、あるいは採用に値すると事前に結論づけない。

## 基準と観測

- 基準プロンプトはC275 `the-caption-3ce91a4-four-verified-lines-ablation-r1`、revision `r1`、bundle SHA-256 `357f684904979c7703a1d9248d3b88ad9a1704eefa4243affc912ff6921cb5ac`。
- C275のF02 iteration 2（run ID `f6ec1150753843669e47bcf3a2e7094f`）では、focused pytestが追加testのimport不足で初回終了コード2となり、修正後の同じpytestは27件成功、全体検証は329件成功した。command protocol違反はなく、最終成果は成立した。訂正前のwrite-once登録値はScore 3、別記録の採点訂正後はScore 4である。
- 同traceは、C276の4項目が解消すべき失敗を証明していない。特に、このrunでは独立workerの分割や重複判定はなく、C275の調査と検証は要求された成果へつながっていた。よってF02の初回失敗をC276の改善根拠にせず、N=5比較で動作と3 KPIを観測する。

## 変更範囲と保持条件

- C276の直接親はC275とする。root `AGENTS.md`だけを利用者提示文で置き換え、残る18 targetはC275とbyte一致させる。
- rootの4項目は一体の実行制御文として扱う。変更対象は「要求結果のbindと質問範囲」「作業開始前の全体方針」「独立作業の対応付け」「方針決定後の探索打ち切り」。これらが相互に分離できる独立実験軸かは本比較で結論づけず、対象外の指示を一切変更しない。
- Standard14のcase、fixture、TaskSpec、rating v14、GPT-6 Luna High、CLI/runtime、permission、executor条件、token accounting、集計方法はC275から維持する。C275の70 runを再実行せず、C276用の不足70 slotだけを発行する。
- prompt bundle、profile、preflight receipt、run、resultはそれぞれ固定identityで作成する。採用、release、runtime projectionは対象外とする。

## 観測と判定

- C276とC275のvalid件数、case別Score、quality score、all-agent `total_tokens`、`elapsed_seconds`を同じ集計単位で並べる。
- C275 traceで観測した結果bind、着手前の方針決定、作業分割、判定の重複、実装方法決定後の追加探索を診断項目として確認する。診断値を第4 KPIまたは独立した停止条件にしない。
- 事前に固定した比較であり、quality低下runを中央値で相殺しない。全件の分布、除外、計測失敗を併記する。比較条件不一致またはpreflight不成立ならslotを一件も発行しない。
- 期待と逆の結果を含め、結果は当該Standard14 N=5・GPT-6 Luna High内の観測としてのみ報告する。Score 4件数、3 KPIまたはtrace診断だけで採用・releaseを判断しない。

## 追加の保存済みControl-Free比較

実行完了後の利用者依頼に基づき、同一comparison keyのControl-Free GPT-6 Luna High result `71a8231c6cc048d0a522aaa43d3a91b6`も追加で比較した。再実行はせず、保存済み70 runからN=5を選択し、C276とmatched execution stratumであることを確認した。品質中央値は`+7.143`ポイント、all-agent token中央値は`-615,814`（`-19.60%`）、elapsed中央値は`-118.553秒`（`-11.36%`）。これは追加の保存済みbaseline比較であり、初回設計のC275直接比較を置き換えず、新しい実験変数や一般的な因果主張も導入しない。
