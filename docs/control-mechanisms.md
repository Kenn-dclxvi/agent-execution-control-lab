# 得た知見: トークンを大きく減らせた仕組み

ここでは、これまでの候補開発で観測した「どの制御がトークン消費を大きく減らしたか」を、その因果とともに整理します。前提となる用語は説明を添えて用います。

### 前提となる用語

- **トークン (token)**: 言語モデルが入出力を処理するときの計量単位です。多いほど所要時間と費用が増えます。本リポジトリで扱うのは **all-agent `total_tokens`**、すなわち **root agent（作業を統括する主体）と、そのrunから起動された全SA session（sub-agent、下記のworker）の最終usageを合算した値**です。合算値なので、workerが増えると総量は非線形に膨らみます。
- **prompt control（制御）**: 指示書（AGENTS.md等）に置く不変条件のことです。1つの**label**（見出し付きの制御単位）が1つの**predicate**（「この条件が成り立つときはこう振る舞う」という判定文）を持ちます。labelを足すとモデルの実行経路が変わり、トークンが増減します。
- **worker（SA session）**: モデルが作業を分担するために起動する下位セッションです。1体起動するたびに、その子セッションのusageがall-agent総量へ丸ごと加算されます。
- **model step / tool call**: モデルが一度立ち止まって次の行動を決める単位（step）と、その結果として実際にコマンドやreadを実行する回数（tool call）です。トークン消費はこの2つの回数と強く連動します。

### 大きく減らせた4つのメカニズム（効果の大きい順）

**1. 不要なworker起動そのものを抑える（削減幅が最大）**

因果: all-agent総量はworker1体ぶんのusageを丸ごと加算するため、「root agentだけで完結できる作業なのにworkerを起動する」経路を消すと、総量が最も大きく下がります。

制御の内容: 「criterion ownerを指す語列が現れただけではworkerを起動せず、TaskSpec（作業仕様）が独立したproducer executionを明示的に指定した場合にのみ委譲する」というpredicateに整理しました（Candidate41）。加えて、分散していた実行制御を単一のexecution authority（実行権限の主体）へ統合し直しました（Candidate5、Candidate15）。

観測: worker spawnがほぼ0になり、Candidate35との比較ではtoken合計がCandidate41比で`+50.02%`（=Candidate41側が約1/3少ない）、expanded12ではbaseline比 all-agent中央値で最大`-4,335,047`。品質（`quality_score`）は同水準を維持しました。品質を保ったままトークンを削減できたのはこの系統でした。

**2. workerへ継承するcontextを必要十分まで絞る**

因果: workerに「ここまでの経緯」を広く継承させると、その分だけ子セッションのusageが増えます。担当criterionに不要な情報を渡さなければ減ります。

制御の内容: worker packet（引き継ぎ情報）が十分なら継承を`none`にし、不足時も必要最小限のturnだけ継承する設定にしました（Candidate33）。

観測: Candidate32比でtoken中央値`-24.63%`（約`-959,484`）。ただし継承を絞りすぎた結果、`quality_score`中央値が`-6.250`低下しました。「渡さない情報が判断に不要」と確認できないまま削ると品質を割る、という反例です。

**3. 結論が変わらない場面での再判断・再readを止める**

因果: モデルは作業途中で繰り返しmodel step（次の行動の再検討）に戻ります。この再入自体がトークンを消費するため、「戻っても選択が変わらない」場面での再入を止めると減ります。

制御の内容: 「未発行のinvocation（次に出す指示）の選択を変えないresult間では、モデルへ再入しない」というlabel（`DECISION_BOUNDARY`、Candidate69）と、「artifact変更後に必要な検証を同一waveで一括発行し、全result受領後に一度だけ判断し、成功後は根拠のない追加readをしない」というlabel（`VALIDATION_CLOSURE`、Candidate71）を追加しました。

観測: standard14でCandidate43比 all-agent中央値`-26.21%`・top-level tool call`-26.60%`（Candidate69）、Candidate69比 token合計`-27.93%`・tool call`-30.16%`（Candidate71）。いずれもトークンとstep数を大きく削りましたが、評価上はどちらも事前gate不通過で`stopped`でした。停止理由・現在の解釈・採用状態はcandidateごとに分かれます。

- **Candidate69の停止（当時のrating v10）**: F10 monthlyのfinding location mismatchが1件残り、score分布`4 / 3 = 69 / 1`で全件score 4のgateに届きませんでした。A02の検証欠落が理由ではありません。
- **Candidate71のv12評価（B18）**: 公式score分布`4 / 3 / 0 = 1,255 / 4 / 1`。v12採点で欠落扱いされたのは、A02の`git diff --check`未実行3件と、A01で未固定modeを確認せず実装・試験へ進んだ1件です。
- **rating v13による現在の解釈**: このうちA02の3件だけが「実行役へ提示していない特定コマンドを採点側が必須化した要求と採点のずれ」として本物の品質低下と区別されます。A01の1件はv13でも品質上の問題として残ります。
- **Candidate71の採用状態**: `stopped`は評価状態であり、これとは別の採用判断で2026-07-23にrelease status `projected`・approval `approved`・runtime projection `projected`となりました（評価と採用は別レイヤー）。

正本はlifecycle軸ごとに分かれる。評価または診断を実施したcandidateの評価状態と停止理由は各candidateの独立したevaluation / diagnostic result、未実施の`not_evaluated`は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列（同indexは一覧と導線でもあり、系譜と観測の整理は[`candidate-history.md`](candidate-history.md)）、release status・approval・runtime projectionは[`prompts/releases/README.md`](../prompts/releases/README.md)と各release READMEを正本とする。rating v13契約は[`outcome-abstract-condition-preserving-owner-diagnostic-v13.json`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json)、A02採点の整理は[`a02-rating-divergence.md`](a02-rating-divergence.md)を参照。

**4. read経路を事前に確定し、一括化・最短化する**

因果: 参照resourceを逐次バラバラにreadすると、read1回ごとにstepとトークンが積み上がります。読む対象と順序を事前に確定して一括readすれば減ります。

制御の内容: 順序依存のないroot readを同一model stepへbatch化する（Candidate50）、あるいは全文sourceを1つに固定し、確定済み証拠のreviewでのみ差分を実行前に合成する（Candidate63）形にしました。

観測: 特定case（F10=月次レビュー確認など）では劇的に減り、Candidate63はtool call 3回・token合計`-52.90%`へ収束。Candidate50もF05/F10で`-40.08%`。ただしCandidate50は探索型のA02で`+15.70%`と増加し、全20 runでは`-2.49%`にとどまりました。局所では強く効く一方、case横断では安定しませんでした。

### 横断的に確認できたこと

1. **表面的なprompt縮約は実行時トークンをほとんど動かさない。** byte数やlabel数を減らすだけの変更（Candidate32・65・66・67・68）では、all-agent tokenは有意に変わりませんでした。効いたのは「worker起動・再判断・read」という実行時の振る舞いを変えたときだけです。
2. **削減幅が最大なのは、処理量そのものを減らす制御。** とりわけ不要なworker起動の抑制が支配的でした。stepやreadの削減はその次に位置します。
3. **トークン削減の評価と、採用の判断は別レイヤーです。** メカニズム2・3・4は品質面で低下や不安定さが出て、評価上は`stopped`（品質gate不通過）と判定されました。ただし評価の`stopped`は採用の可否を決めません。採用・本体適用は、評価結果を踏まえて人が別途判断します。実際、メカニズム3のCandidate71は評価上はgate不通過のままですが、トークン効率を優先する別の採用判断として2026-07-23にTHE-CAPTION本体へ適用されました。本基盤はトークン削減を優劣や採用の根拠とはせず、3つのKPI（`quality_score`・`total_tokens`・`elapsed_seconds`）を並べて示すことに徹します。

なお、上記の数値はそれぞれ比較対象・評価集合・採点条件が異なる場面の観測であり、そのまま相互比較や一般化はできません。互換条件をそろえた比較と個別の一次結果は、Candidate別の経緯を[`candidate-history.md`](candidate-history.md)、一次結果を`evaluations/results/`で参照してください。
