# 得た知見: トークンを大きく減らせた仕組み

ここでは、これまでの候補開発で観測した「どの制御がトークン消費を大きく減らしたか」を、その因果とともに整理します。前提となる用語は説明を添えて用います。記述はCandidate166までの保存済みresult（2026-08-04時点）を対象とします。

### 前提となる用語

- **トークン (token)**: 言語モデルが入出力を処理するときの計量単位です。多いほど所要時間と費用が増えます。本リポジトリで扱うのは **all-agent `total_tokens`**、すなわち **root agent（作業を統括する主体）と、そのrunから起動された全SA session（sub-agent、下記のworker）の最終usageを合算した値**です。合算値なので、workerが増えると総量は非線形に膨らみます。
- **prompt control（制御）**: 指示書（AGENTS.md等）に置く不変条件のことです。1つの**label**（見出し付きの制御単位）が1つの**predicate**（「この条件が成り立つときはこう振る舞う」という判定文）を持ちます。labelを足すとモデルの実行経路が変わり、トークンが増減します。
- **worker（SA session）**: モデルが作業を分担するために起動する下位セッションです。1体起動するたびに、その子セッションのusageがall-agent総量へ丸ごと加算されます。
- **model step / tool call**: モデルが一度立ち止まって次の行動を決める単位（step）と、その結果として実際にコマンドやreadを実行する回数（tool call）です。トークン消費はこの2つの回数と強く連動します。

### 大きく減らせたメカニズム

1〜4は削減幅の大きい順、5〜6はその後の系列で加わった別軸です。

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

制御の内容: 「未発行のinvocation（次に出す指示）の選択を変えないresult間では、モデルへ再入しない」というlabel（`DECISION_BOUNDARY`、Candidate69）と、「artifact変更後に必要な検証を同一waveで一括発行し、全result受領後に一度だけ判断し、成功後は根拠のない追加readをしない」というlabel（`VALIDATION_CLOSURE`、Candidate71）を追加しました。Candidate81では同labelを置換し、root producerの複数required validationについて、後段の「順に」「1 commandずつ個別」を一つのcustom wrapper内のbind順・個別`exec_command`発行として固定しました。

観測: standard14でCandidate43比 all-agent中央値`-26.21%`・top-level tool call`-26.60%`（Candidate69）、Candidate69比 token合計`-27.93%`・tool call`-30.16%`（Candidate71）。いずれもトークンとstep数を大きく削りましたが、評価上はどちらも事前gate不通過で`stopped`でした。停止理由・現在の解釈・採用状態はcandidateごとに分かれます。

- **Candidate69の停止（当時のrating v10）**: F10 monthlyのfinding location mismatchが1件残り、score分布`4 / 3 = 69 / 1`で全件score 4のgateに届きませんでした。A02の検証欠落が理由ではありません。
- **Candidate71のv12評価（B18）**: 公式score分布`4 / 3 / 0 = 1,255 / 4 / 1`。v12採点で欠落扱いされたのは、A02の`git diff --check`未実行3件と、A01で未固定modeを確認せず実装・試験へ進んだ1件です。
- **rating v13による当時のrunの現在解釈**: このうちA02の3件だけが「実行役へ提示していない特定コマンドを採点側が必須化した要求と採点のずれ」として本物の品質低下と区別されます。A01の1件はv13でも当該runの品質上の問題として残り、過去scoreやrelease riskは変更しません。
- **A01の現在運用上の位置づけ**: 投影済みCandidate81を使い、現在値と候補順を回転した3択variation r2を追加診断しました。曖昧条件15 / 15件は変更と試験の前に確認停止し、authority条件15 / 15件は指定値へ正しく変更して関連testを成功させました。過去の1件は取り消さず、現在は非再現の監視項目とします。未固定値を確認せず変更したfresh traceを再観測した場合だけ診断を再開し、現時点では新しいprompt predicateや常設gateを追加しません。
- **Candidate71の採用状態**: `stopped`は評価状態であり、これとは別の採用判断で2026-07-23にrelease status `projected`・approval `approved`・runtime projection `projected`となりました（評価と採用は別レイヤー）。
- **Candidate81の安定化と採用状態**: Rating v13 Medium標準14項目は70 / 70 score `4`で、複数required commandの1-step closureはCandidate71の30 / 35から35 / 35へ改善しました。token中央値は`-0.30%`、elapsed中央値は`+5.78%`であり、効率改善ではなくprompt動作安定性の結果です。その後の2026-07-27の明示判断でrelease status `projected`・approval `approved`・runtime projection `projected`となりました。
- **Candidate125の現在の採用状態**: Candidate118のA02 terminal closureを保持し、一つのeditable targetが全未解決変更criterionを所有する場合だけ同targetへの限定continuationを許可しました。Rating v14 Medium Standard14 N=5は70 / 70 score `4`、A02 N=20はbind後再入0件、token中央値はCandidate107目標比`-8.00%`でした。2026-07-31の明示判断でrelease status `projected`・approval `approved`・runtime projection `projected`となりました。Standard14 B20未実施riskは保持します。2026-08-01のN=100追試はregistered poolを各case30件へ拡張した時点でF04 score `2`を5件確認し、N=50 partial batchを中断しました。N=30 selection resultは未作成です。この追試は当時のN=5評価と投影の事実を取り消しませんが、「N=5の通過は低頻度failureの不在を意味しない」ことを示しました。
- **Candidate147が現在の投影対象**: 上のF04低頻度failureを受けて、Candidate126〜Candidate142では変更直前のgateを厳しくする方向を試しましたが、部分変更を閉じるほど`false stop`（成果を完成できるのに保守側へ倒れて停止すること）が増える構造が確認されました。そこでCandidate143で成立済みのCandidate118へ戻り、required outcome全体を上流でimplementationへbindし直し、Candidate145でconsumerのないevidence取得を閉じ、Candidate147で停止範囲を限定しました（下記メカニズム5）。Candidate147のStandard14 N=100は1,400 / 1,400件がscore `4`で、2026-08-03の明示判断でrelease status `projected`・approval `approved`・runtime projection `projected`となり、公開版`the-caption`へ投影済みです。この系列の詳細は[`candidate125-candidate147-control-findings-synthesis.md`](candidate125-candidate147-control-findings-synthesis.md)を参照。

正本はlifecycle軸ごとに分かれる。評価または診断を実施したcandidateの評価状態と停止理由は各candidateの独立したevaluation / diagnostic result、未実施の`not_evaluated`は[`prompts/candidates/README.md`](../prompts/candidates/README.md)の状態列（同indexは一覧と導線でもあり、系譜と観測の整理は[`candidate-history.md`](candidate-history.md)）、release status・approval・runtime projectionは[`prompts/releases/README.md`](../prompts/releases/README.md)と各release READMEを正本とする。rating v13契約は[`outcome-abstract-condition-preserving-owner-diagnostic-v13.json`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json)、A02採点の整理は[`a02-rating-divergence.md`](a02-rating-divergence.md)を参照。

**4. read経路を事前に確定し、一括化・最短化する**

因果: 参照resourceを逐次バラバラにreadすると、read1回ごとにstepとトークンが積み上がります。読む対象と順序を事前に確定して一括readすれば減ります。

制御の内容: 順序依存のないroot readを同一model stepへbatch化する（Candidate50）、あるいは全文sourceを1つに固定し、確定済み証拠のreviewでのみ差分を実行前に合成する（Candidate63）形にしました。

観測: 特定case（F10=月次レビュー確認など）では劇的に減り、Candidate63はtool call 3回・token合計`-52.90%`へ収束。Candidate50もF05/F10で`-40.08%`。ただしCandidate50は探索型のA02で`+15.70%`と増加し、全20 runでは`-2.49%`にとどまりました。局所では強く効く一方、case横断では安定しませんでした。

**5. 「結果を待つ」範囲を、その結果で変わる操作だけへ限定する**

因果: メカニズム3は「戻っても選択が変わらないなら再入しない」でしたが、逆に「安全のためにすべての操作を結果待ちにする」制御を足すと、待つたびにmodel stepが1つ増え、その分だけcached input（前回までの入力を再送する扱いのトークン）が積み上がります。過剰な停止それ自体がコストになります。

制御の内容: まずCandidate145で、「その観測値を使って未確定の判断を動かせる相手（consumer）がいる場合だけrepository readを許す」というlabelを置きました。念のための再読、実装方法だけを探す探索、成立済み判断の再確認、報告のためのreadは閉じます。その上でCandidate147が、resultの停止効果をtask全体へ広げず、「そのresultがtarget・permission・method・停止条件を実際に変え得る未発行operation classの集合」だけへ限定する`result_effect_scope`へ`DECISION_BOUNDARY`を置換しました。開始時のidentity確認はartifact変更と必須検証を止めますが、TaskSpecで既に許可されたreadは止めません。

観測: Candidate145はStandard14 N=5で70 / 70件score `4`と品質を保った一方、Candidate125比でtoken中央値`+13.74%`・elapsed`+31.04%`とコストが増えました。原因は開始identityの確認を別stepへ分離したことでした（F01 / F02 / F03で15 / 15件が別step発行）。Candidate147はこれをCandidate145比でtoken中央値`-9.17%`・elapsed`-23.13%`（F01 / F02 / F03の集約ではtoken`-25.97%`、変更前model step中央値が3 caseとも`2 → 1`）まで戻し、安全境界を緩めずにコストを回収しました。残存riskとして、F06のauthority追加readが21 / 100件残っています（発生群のtoken中央値`160,327`は非発生群`104,230`より`53.82%`高い）。

**6. 制御ゼロの状態へ、行動が変わると確認できた文だけを足す**

因果: 1〜5は既存の指示書を改訂する方向でしたが、root指示書が0 byteの条件（Free）を基準にすると、「1文足すと実行経路がどう変わるか」を1軸ずつ切り分けられます。効く文だけを残せば、短い指示書でトークンと品質の両方を改善できます。

制御の内容: Candidate148・Candidate152・Candidate156のように複数項目をまとめて足す試験では品質gateを通せませんでした（いずれもA01が5 / 5件score `0`）。そこで、変更前調査を不足情報だけへ絞る（Candidate157）、利用者が決める結果とAIが選ぶ実装方法を分ける（Candidate158）、変更前に方針を1つへまとめる（Candidate159）、独立作業の担当・判定対象・必要結果を対応づけて再判定を禁じる（Candidate161）、必要なテストと差分確認を実行票として先に固定する（Candidate162）の5文を、それぞれ単独追加のN=5で行動変化を確認してから、Candidate163で統合しました。

観測: Candidate163のStandard14 N=5は70 / 70件score `4`（Freeは65 / 70件、A01の5件がscore `0`）。Free比でall-agent token中央値`-15.85%`、API価格換算`-14.01%`、elapsed`-5.74%`で、3指標とも5 / 5 iterationで低下しました。特にA01はtoken`-78.93%`（指定値を推測実装せず質問停止へ変わったため）です。ただしこれは5文セット全体の結果であり、個々の文の因果効果はセット試験からは分離できません。また、誤実装が質問停止へ変わった作業量差を含むため、`-14.01%`を一般的な料金削減率としては扱いません。Candidate163の採用は未判断です。

なお、Candidate164からCandidate166のreview admission系（reviewの要否と担当をどこで決めるか）は、現時点でtoken削減の観測ではなくroutingの成立可否を見ている段階です。Candidate165はCandidate147比でtoken`+75.79%`・elapsed`+34.99%`、Candidate166は品質未判定・Standard14未実施で、いずれも採用未決定です。

### 横断的に確認できたこと

1. **表面的なprompt縮約は実行時トークンをほとんど動かさない。** byte数やlabel数を減らすだけの変更（Candidate32・65・66・67・68）では、all-agent tokenは有意に変わりませんでした。効いたのは「worker起動・再判断・read」という実行時の振る舞いを変えたときだけです。
2. **削減幅が最大なのは、処理量そのものを減らす制御。** とりわけ不要なworker起動の抑制が支配的でした。stepやreadの削減はその次に位置します。
3. **トークン削減の評価と、採用の判断は別レイヤーです。** メカニズム2・3・4は品質面で低下や不安定さが出て、評価上は`stopped`（品質gate不通過）と判定されました。ただし評価の`stopped`は採用の可否を決めません。採用・本体適用は、評価結果を踏まえて人が別途判断します。実際、メカニズム3のCandidate71は評価上はgate不通過のままですが、トークン効率を優先する別の採用判断として2026-07-23にTHE-CAPTION本体へ適用されました。本基盤はトークン削減を優劣や採用の根拠とはせず、3つのKPI（`quality_score`・`total_tokens`・`elapsed_seconds`）を並べて示すことに徹します。
4. **安全側の制御を足すとコストは増える。減らすのは「足す」ではなく「効く範囲へ絞る」。** Candidate143からCandidate145は品質と安定性を得た代わりにCandidate125比でコストが増え、それを回収したのは新しいgateの追加ではなく、既存gateの適用範囲を限定したCandidate147でした（メカニズム5）。逆に、変更直前のgateを積み増したCandidate126からCandidate142では、部分変更を閉じるほど`false stop`が増えました。
5. **品質とKPIが良くても、狙った制御が実際に働いた証拠にはならない。** Candidate146はF01 / F02 / F03で15 / 15件score `4`、Candidate145比でtoken`-4.50%`でしたが、再監査すると狙った共同発行は親のCandidate145で既に15 / 15件成立しており、増分が当該制御に帰属しないため停止しました。判断は品質gate・コストgateとは別に、保存traceで挙動が変わったかを見るmechanism gateで行います。
6. **N=5の通過は低頻度failureの不在を意味しない。** Candidate125はStandard14 N=5で70 / 70件score `4`でしたが、N=100追試の途中（各case30件時点）でF04にscore `2`が5件出ました。tail安定性は反復数を伸ばして初めて判定できます。

なお、上記の数値はそれぞれ比較対象・評価集合・採点条件が異なる場面の観測であり、そのまま相互比較や一般化はできません。互換条件をそろえた比較と個別の一次結果は、Candidate別の経緯を[`candidate-history.md`](candidate-history.md)、一次結果を`evaluations/results/`で参照してください。
