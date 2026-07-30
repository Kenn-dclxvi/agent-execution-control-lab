# Candidate81 / Candidate96 successful validation result projection Rating v14 Medium F02 N=5

## 結論

Candidate81とCandidate96は、F02 r1、Rating v14、Medium、Codex CLI `0.146.0`、各`N=5`で全件score `4`だった。compatibility keyも一致した。

ただし、Candidate96が狙ったsuccess projectionは`0 / 5`だった。全runでfocused testとfull gateの成功stdoutがmodel-visibleなcommand resultへそのまま返った。事前停止条件に従い、Candidate96を`targeted_f02_evaluated / mechanism_gate_failed / stopped`とする。F04、標準14、B20、採用、release、本体反映へ進めない。

Candidate96のtoken中央値はCandidate81比`-11.03%`、elapsed中央値は`-15.78%`だった。しかしsuccess output抑制は成立していないため、この差を設計した機構の効果とは扱わない。

## 固定条件

| 項目 | 固定値 |
| --- | --- |
| case | `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` |
| Evaluation set | `the-caption-planning-first-f02-r1` / `r1` |
| set identity | `9de3130e4252f338cb81ce7ae91d20c1ef9ce05f734360126d9087a5d3e06b4b` |
| Rating | `outcome-terminal-state-evidence-owner-diagnostic-v14` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| Codex CLI / Python | `0.146.0` / `3.14.5` |
| runtime identity | `61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73` |
| repetition | 各`N=5`、iteration `1..5` |
| effective concurrency | `M=5` |
| compatibility key | `63e6b46dac29b2657732b7d6b69826abe2f5ffff28c480ed089f4b2e1e9e650b` |

両profileの差はprofile IDとprompt identityだけである。TaskSpec、case revision、fixture、required validation、rating、model、reasoning、CLI、permission、executor parameter、M / Nは変更していない。

## 一次result

| prompt | bundle SHA-256 | result ID | result content SHA-256 | score `4` |
| --- | --- | --- | --- | ---: |
| Candidate81 | `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220` | `fb33b8b1f6e048babeeb770d14484501` | `c7929d8476c07731b85aa377f5fe13d1b6352b86820c5f60b239fd6eb9e7dcd6` | 5 / 5 |
| Candidate96 | `3ac342bc11b1f0a99bad411ecdebeead671e0b182e21e7ea27cf4f7a84b37d10` | `c721252a3b7f4bf3862095dc049a87ec` | `4bf43fc3eb47cb696221669e2a9e375db01a2a12b0bca7f51d92b8def018f7d0` | 5 / 5 |

required command evidenceの欠落、unexpected changed path、quality failureは両方とも0件だった。

## KPI比較

| KPI | Candidate81 | Candidate96 | C96 - C81 | 変化率 |
| --- | ---: | ---: | ---: | ---: |
| all-agent token中央値 | 290,587 | 258,530 | -32,057 | -11.03% |
| elapsed中央値 | 97.937秒 | 82.481秒 | -15.456秒 | -15.78% |
| all-agent token合計 | 1,541,931 | 1,269,593 | -272,338 | -17.66% |
| elapsed合計 | 477.880秒 | 416.289秒 | -61.591秒 | -12.89% |

N=5のtargeted観測であり、差の一般化や有意差の主張はしない。mechanism gate不通過のため、KPI差をsuccess projectionの効果とも解釈しない。

## Mechanism監査

成功時projectionの成立条件は、全required validation成功時にmodel-visible resultがvalidation identity、exact command、exit codeだけとなり、success stdout / stderrを含まないことである。

Candidate96の全5 runでは次の経路を観測した。

- focused testは各runで直接commandとして1回発行され、model-visible `aggregated_output`は各`23,640` bytesだった。
- full gateは各runで直接commandとして1回発行され、model-visible `aggregated_output`は各`159,575` bytesだった。
- 両command resultにはpytestの成功行、test一覧、coverage等のraw outputが含まれた。
- validationを包み、成功時にidentity、exact command、exit codeだけへ投影するwrapperは生成されなかった。
- Candidate96のmodel-visible required validation outputは合計`916,075` bytesだった。

したがって、success projectionは`0 / 5`、required validation evidenceは`5 / 5`である。

## KPI差の経路診断

Candidate81は全5 runでcommandを計65回発行し、1 runだけfull gateを2回発行した。Candidate96はcommand計49回で、full gate重複は0件だった。required validationのmodel-visible output合計はCandidate81 `1,075,200` bytes、Candidate96 `916,075` bytesである。差の大部分はCandidate81のfull gate再実行1回に対応する。

このため、Candidate96の低いtoken・elapsedは、validation success outputを投影した結果ではなく、重複validationと周辺commandがこの5 runで少なかったことによる可能性がある。prompt文面が再実行判断を抑えた可能性は残るが、本評価だけでは確定できない。

## KPI差の詳細分析

### 反復別方向

| iteration | token差 C96 - C81 | token変化率 | elapsed差 | elapsed変化率 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | -77,989 | -27.79% | -7.863秒 | -9.28% |
| 2 | -114,336 | -31.46% | -20.210秒 | -19.68% |
| 3 | +21,253 | +8.14% | +1.551秒 | +1.78% |
| 4 | -32,057 | -11.03% | -10.865秒 | -11.09% |
| 5 | -69,209 | -20.00% | -24.205秒 | -23.03% |

tokenとelapsedはともに4 / 5反復でC96が小さかった。n=5の対応付き符号順位検定では両KPIとも両側`p=0.125`で、5%水準の有意差とはいえない。方向は単一の外れ値だけではないが、確認試験を省略できる強さでもない。

### full gate重複を除く感度分析

Candidate81 iteration 5はfull gateを2回実行した。影響を除くため、両promptのiteration 5を外してiteration 1〜4だけで中央値を再計算した。

| KPI | Candidate81 | Candidate96 | 変化率 |
| --- | ---: | ---: | ---: |
| token中央値 | 285,631.5 | 253,790.5 | -11.15% |
| elapsed中央値 | 92.660秒 | 84.777秒 | -8.51% |

したがって、token差はfull gate重複1件だけでは説明できない。elapsed差は縮小するが、同じ方向を維持する。

### token内訳

| 内訳 | Candidate81合計 | Candidate96合計 | 差 | 変化率 |
| --- | ---: | ---: | ---: | ---: |
| input token | 1,524,364 | 1,254,479 | -269,885 | -17.70% |
| output token | 17,567 | 15,114 | -2,453 | -13.96% |
| cached input token | 1,246,976 | 1,054,464 | -192,512 | -15.44% |

全token差`272,338`の`99.10%`はinput token差である。最終回答の短文化より、tool resultを含むcontextが後続model stepへ再入力される回数と量の差が支配的だった。

### 実行route

| diagnostic | Candidate81 | Candidate96 | 差 |
| --- | ---: | ---: | ---: |
| command execution | 65 | 49 | -16（-24.62%） |
| read / status / diff系command | 52 | 38 | -14（-26.92%） |
| agent message | 32 | 29 | -3（-9.38%） |
| command output bytes | 1,464,755 | 1,276,318 | -188,437（-12.86%） |
| focused gate | 5 | 5 | 0 |
| full gate | 6 | 5 | -1 |

Candidate96はrequired validationを省略していない。減ったのは、主に変更前のread / search / statusと、Candidate81 iteration 5のfull gate再実行である。

### Candidate81 B20分布との診断比較

2026-07-30朝に完了した最新Candidate81 Standard14 B20のうち、F02の100 runを基準分布として参照した。このcampaignはStandard14 r1、各case `N=5`、global queue `M=24`を20 batch実行した1,400 runである。各batchのF02標本数は5件だが、campaign全体の実行並列数はprofile、`plan.json`、各batchの`global-plan.json`で`max_workers=24`に固定されている。

今回のC81 / C96 F02比較自体は両方`M=5`でcompatibility keyも一致する。一方、B20はStandard14と`M=24`であり、今回のF02単独resultとはevaluation set identity、repetition condition、scheduler条件が異なる。したがってB20を正式なLayer 4比較へ混ぜず、F02 N=5の点推定がC81の保存分布のどこに位置するかを見るdiagnosticに限定する。B20とのscheduler差は、両方M=5である今回のC81 / C96差そのものを説明する理由には使わない。

| KPI | C81 Standard14 B20内F02 100 run | 今回C81 N=5中央値 | 今回C96 N=5中央値 |
| --- | ---: | ---: | ---: |
| token | p25 `257,215` / median `276,628` / p75 `308,594` | `290,587`（経験分位64%） | `258,530`（経験分位26%） |
| elapsed | p25 `91.414秒` / median `98.829秒` / p75 `107.542秒` | `97.937秒`（経験分位46%） | `82.481秒`（経験分位6%） |

100 runから5 runを非復元単純抽出したと仮定し、その5件中央値が観測値以下になる正確確率を計算した。tokenはCandidate96以下が`10.88%`である。B20を元の20 batchに分けた場合も、batch内F02 N=5中央値の`4 / 20`がCandidate96以下だった。Candidate96 tokenは低めだが、保存分布の標本変動として起こり得る。今回のCandidate81 token中央値はB20の64%位置であり、`-11.03%`の差には「C81側がやや高く、C96側がやや低い」組合せが含まれる。

elapsedはCandidate96以下が`0.118%`だった。B20の20 batch中央値は最小でも`87.686秒`で、Candidate96の`82.481秒`以下は`0 / 20`だった。一方、今回のCandidate81はB20の46%位置で中心に近い。したがって、`-15.78%`のelapsed差は保存済みC81分布の標本誤差だけでは説明しにくい。ただし`0.118%`はM=24 B20を参照したdiagnosticであり、M=5 F02に対する正式なp値ではない。

full validation再実行はC81 B20 F02で`5 / 100`だった。この母比率からN=5で再実行が0件になる確率は`76.96%`、1件以上になる確率は`23.04%`である。今回のC81 `1 / 5`とC96 `0 / 5`だけでは、重複抑制効果を識別できない。

以上から、token差は標本誤差と整合する。elapsed差は保存済みC81分布の標本誤差だけとは考えにくい。ただしB20は正式互換比較ではなく、今回のC81→C96も直列実行だったため、elapsed差をprompt因果効果と確定することはできない。結論は「すべて誤差」でも「Candidate96の効果を実証」でもなく、`token=likely_sampling_variation`、`elapsed=shift_observed_but_unattributed`とする。

### 保存traceによるelapsed差の分解

今回のC81 / C96各5 runについて、保存済みCodex event traceからmodel使用量、command経路、validation実時間を抽出した。event単位の時刻は保存されていないため、model処理時間とtool待機時間を秒単位で直接分割することはできない。ただし、command内で計測されたvalidation実時間とmodel token量は分離できる。

| diagnostic中央値 / run | Candidate81 | Candidate96 | 変化 |
| --- | ---: | ---: | ---: |
| elapsed | `97.937秒` | `82.481秒` | `-15.456秒` |
| input token | `286,783` | `255,577` | `-10.88%` |
| output token | `3,803` | `2,953` | `-22.35%` |
| reasoning token | `966` | `604` | `-37.47%` |
| agent message | `6` | `6` | `0` |
| command execution | `13` | `8` | `-38.46%` |
| read / status / diff系command | `11` | `6` | `-45.45%` |
| artifact変更前command | `9` | `5` | `-44.44%` |
| focused＋full validation実時間 | `2.68秒` | `2.69秒` | `+0.01秒` |
| command output bytes | `257,062` | `249,507` | `-2.94%` |

validation実時間はほぼ同じであり、`15.456秒`のelapsed差を説明しない。command output bytesの差も小さい。特にrequired validationのraw outputは、full gateを重複したC81 iteration 5を除けば概ね同一量だった。したがって、Candidate96が意図したsuccess output projectionが成立してelapsedを短縮した、という説明は保存traceと整合しない。

対応する5組では、C96は4組でelapsedが短かった。C96が唯一遅かったiteration 3は、5組中唯一、C81よりinput tokenとoutput tokenの両方が増えたrunだった。一方、iteration 2のC96はC81よりcommandが7件多いにもかかわらず`20.210秒`短かった。command件数だけでは差を説明できず、modelへ投入され処理されたcontext量とmodel出力量の方がelapsed方向と整合する。

C81 Standard14 B20内F02 100 runでも、elapsedとのSpearman順位相関は次のとおりだった。これは因果推定ではなく、保存分布内の共変動を見るdiagnosticである。

| diagnostic | elapsedとの順位相関 `rho` |
| --- | ---: |
| output token | `0.799` |
| reasoning token | `0.673` |
| agent message | `0.456` |
| full gate重複 | `0.357` |
| read / status / diff系command | `0.287` |
| input token | `0.275` |
| command execution | `0.250` |
| artifact変更前command | `0.213` |
| command output bytes | `0.050` |

全100 runではCandidate96 elapsed中央値以下が`6 / 100`だった。一方、reasoning tokenがCandidate96中央値`604`以下のC81 runへ限定すると、Candidate96 elapsed中央値以下は`5 / 13`（`38.46%`）だった。つまりCandidate96のelapsed値はC81全体では低いが、model reasoning量が同程度に少ないrouteの中では異常に低くない。

この結果から、elapsed差の直接要因はvalidation実行時間やraw stdout量ではなく、低いreasoning / output量を伴う短いmodel routeだった可能性が高い。ただし、Candidate96が変更したのはartifact変更後に発火する`VALIDATION_CLOSURE`だけであり、観測されたcommand削減の中心はartifact変更前のread経路である。したがって、短いrouteがCandidate96の規則から必然的に生じたとは説明できない。分類は`model_work_reduction_observed_but_unattributed`とし、prompt因果効果には昇格させない。

### 解釈

Candidate96のsuccess stdout抑制は0 / 5であり、設計したprojection機構は成立していない。一方、Candidate81 iteration 5はfull gate成功後に「構造化終了コードが欠落した」と判断して再実行した。Candidate96は全runでraw stdoutを受け取ったままexit code 0を採用し、full gateを再実行しなかった。このため、`VALIDATION_CLOSURE`の追記が成功resultの認識を強めたという部分的な行動効果は観測されている。

ただし、変更前readの減少はvalidation success後のprojection規則から直接導けない。prompt差による注意配分、run間の確率変動、C81先行・C96後続の直列実行による時間差を分離できない。したがって、次のように分類する。

- success output projection: `failed`（0 / 5）
- required validation維持: `passed`（5 / 5）
- full gate重複抑制: `observed`（C81 1 / 5、C96 0 / 5）
- input / route削減: `observed_but_unattributed`
- token差: `likely_sampling_variation`
- elapsed差: `shift_observed_but_unattributed`
- elapsed差の直接要因: `model_work_reduction_observed_but_unattributed`
- validation実時間またはraw output量による説明: `not_supported`
- KPI改善の因果確定: `not_established`

### 下振れ側へ寄せるためのC81内分布分析

次の目的はC96の平均差を説明することではなく、品質を維持したままC81の速いrouteへ分布を寄せることとした。C81 Standard14 B20は全1,400 runがscore `4`であり、その中のF02 100 runもすべてscore `4`である。したがってF02の速いrunは品質失敗による短縮ではない。

保存traceの`runner_elapsed_seconds`でF02 100 runを下位25件と上位25件に分けると、次の差があった。ここではrouteとの対応を見るためrunner計測を使い、正式KPI値とは混ぜない。

| diagnostic中央値 | elapsed下位25件 | elapsed上位25件 | 上位 - 下位 |
| --- | ---: | ---: | ---: |
| runner elapsed | `87.730秒` | `114.130秒` | `+26.400秒` |
| input token | `253,420` | `272,784` | `+7.64%` |
| output token | `3,008` | `3,991` | `+32.68%` |
| reasoning token | `636` | `1,118` | `+75.79%` |
| command execution | `11` | `13` | `+2` |
| read command | `5` | `7` | `+2` |
| full gate | `1` | `1` | 中央値差なし |
| command output bytes | `263,665` | `262,500` | `-0.44%` |

raw command output量は上下群でほぼ同じだった。大きく違うのはmodelが生成したoutput / reasoning量である。C81 100 runだけで作ったdiagnostic線形モデルでは、input / output / reasoning tokenがelapsed分散の`65.6%`を説明し、batchを丸ごと除外する交差検証でも`62.7%`を説明した。command routeだけでは`45.0%`、OS負荷・dispatch順・平均同時実行数だけでは`2.4%`だった。環境変数だけの交差検証は予測力を持たなかった。

同じC81 tokenモデルを今回のM=5 runへ適用すると、観測elapsedと予測elapsedの残差中央値はC81 `-5.339秒`、C96 `-6.057秒`で、差は`-0.718秒`だった。今回の約15秒差は、ほぼすべてmodel token workloadの差と対応する。C96固有の高速なexecutor経路は観測されていない。

下側へ寄せるための観測可能なroute条件は次のとおりだった。

| route条件 | run数 | elapsed中央値 | elapsed下位25%に入った割合 |
| --- | ---: | ---: | ---: |
| agent message `<=5` | `9` | `88.312秒` | `8 / 9`（`88.9%`） |
| agent message `=6` | `76` | `99.723秒` | `17 / 76`（`22.4%`） |
| agent message `>=7` | `15` | `109.360秒` | `0 / 15`（`0%`） |
| read command `<=4` | `29` | `95.782秒` | `9 / 29`（`31.0%`） |
| read command `>=8` | `15` | `104.321秒` | `3 / 15`（`20.0%`） |
| full gate 1回 | `95` | `99.417秒` | `25 / 95`（`26.3%`） |
| full gate 2回 | `5` | `126.322秒` | `0 / 5`（`0%`） |

agent message数はmodel decision roundの完全な計測値ではなく、visible trace上のproxyである。ただし、C81 / C96 N=5でもC81には7 messageが2件あり、C96には0件だった。単純なcommand数はelapsedと単調関係ではない。速いrunにも個別commandが多い例があるため、command上限を置くのではなく、read結果ごとにmodelへ戻る判断回数を減らす必要がある。

以上から、下側へ寄せる制御候補の優先順位を次とする。

1. artifact変更前に、TaskSpecとrepository authorityから既知のidentity、authority、source、test readを一つのinspection waveへ完全にbindする。相互非依存readはshell compound commandへ結合せず、同一model stepから個別発行する。
2. inspection wave後の追加readは、既存resultでは判定不能なpredicateを一つ明示できる場合だけ許可する。単なる再確認、別表現での再検索、既読範囲の再読は行わない。
3. required validationのexact commandとexit code `0`がbind済みなら、wrapper独自のreceipt不足を理由に同じfull gateを再実行しない。これは5 / 100の高elapsed tailを直接除く候補である。
4. diff / statusなど、完了前に必要と確定しているcompletion evidenceはrequired validationと同じcompletion closureへ事前bindする。各result後にmodelへ戻って次の証拠を追加しない。
5. 中間説明を減らすこと自体を目的にせず、inspection、変更判断、completionのdecision boundaryだけで説明する。reasoning tokenの直接上限は品質を損なう可能性があるため設けない。

成功stdout抑制は優先候補にしない。上下25件でcommand output bytesがほぼ同じであり、Candidate96でもprojectionが成立しなかったためである。M=24の利用も維持する。並列数はcampaign完了時間を短くするが、C81内の個別runを下側へ寄せる説明変数ではなかった。

次Candidateを作る場合の主仮説は、`successful validation result projection`ではなく、`inspection / completion decision-round closure`とする。TaskSpecは変更しない。まずF02 N=5でinspection wave、追加read理由、full gate一回、completion evidence事前bindingがtrace上で成立することを確認する。mechanismが成立した場合だけ、保存済みC81 Standard14 B20と互換なcandidate-only Standard14 B20へ進み、中央値だけでなくp75、p90、最大値、IQR、agent message、追加read、validation再実行率を比較する。

Candidate96の追加runは行わない。success projectionのmechanism gateが不成立であり、下側routeの分析からもstdout projectionを再試験する根拠は得られなかった。次の検証対象は、別identityのinspection / completion closure Candidateである。Candidate81は保存済みB20を再利用し、不足するcandidate側だけを最大24並列で実行する。

## 設計上の所見

Candidate96は、promptが生成するwrapper内でraw resultを受け取り、modelへ返す内容を制御できることを前提にした。しかし実際のCodex CLI経路では、agentがrequired commandを直接発行し、tool transportがraw stdout / stderrをcommand resultとしてmodelへ返した。

したがって、「success stdout / stderrを返さない」というprompt規則だけでは、raw outputがmodel contextへ入る前の境界を支配できない。この点はCandidate90〜Candidate93で観測したoutput ingress境界と同型である。

ユーザーが固定した境界に従い、TaskSpecは変更しない。評価計測は本mechanism監査で改善した。開発環境側のexecutor変更にも進めない。将来再開する場合は、promptまたはpromptが生成するartifactだけで、required commandのexact identityとexit codeを保ったままraw output投入前にprojectionできる実在の発行形式を先に単発traceで実証する必要がある。

## 実行provenance

- Candidate81 final archive SHA-256: `7123a7e50a8f4e3029fc3ad7ed8f460665ccfdf118e5542e5a31efa5d9143248`
- Candidate96 final archive SHA-256: `78684f699f5e5fa2bf14908aac8bb610da82d3d6f439aaf21fbcb23ac480e85f`
- C81では5 slot実行後、汎用Standard14 collectorがF02 set identityを拒否した。slotは再実行せず、既存のF02固定collector設定でLayer 3以降を再開した。
- C96は開始前に同じF02固定collector設定へcontrollerを修正し、5 slotを一度だけ実行した。
- 事後監査では、mechanism gateをCandidate96単独で判定でき、Candidate81 B20の保存traceも存在したため、今回のCandidate81 5 slot新規実行は不要だったと判断した。今後の評価順序はcandidate-only mechanism gate、保存baseline再利用、不足slotだけの最大24 campaign queueとする。

## 状態境界

- Candidate96: `targeted_f02_evaluated / mechanism_gate_failed / stopped`
- Candidate81: 採用・release・projection済み基準を維持
- F04 / Standard14 / B20: 未実施
- Candidate96 adoption / release / projection: 未実施
- TaskSpec変更: なし
- executor adapterまたは開発環境変更: なし
