# Candidate272とCandidate147のmodel再入原因分析

## 結論

Candidate272で主原因が特定できた。F01・F02のtoken差は、`発行済みの全result`という語の有無やvalidation output量そのものではなく、変更前の開始確認と必要readが複数の外側tool callへ分かれ、その各resultごとにmodelが再入したことが中心である。

Candidate272はCandidate269より短い本文であり、prompt長増加では説明できない。さらにF02の代表比較では、Candidate272のvalidation model-visible outputはCandidate147より小さいのに、総tokenは大きい。したがって「raw carrierが大きいから高い」という単独原因は、この結果で反証された。

解決は、成功runのtool順を指示することでも、output上限を追加することでもない。互いのresultで対象・許可・方法・停止条件が変わらない開始確認と必要readについて、個別invocation resultがAIへ戻れるpermissionを閉じ、一つの外側evidence operationが全invocationを所有し、そのoperationの共同terminal resultだけをAIが受け取れる境界にする。次Candidateの前に、この所有境界をCandidate269へ加える一つの自然語差分として固定する。

## 比較対象と役割

- Candidate147: KPIと成立済みmodel-step closureの比較基準。本文、tool順、wrapper codeまたは数値引数を複写しない。
- Candidate269: validation間model再入とnonterminal後のsame-cell dependencyを回復した、現在の有効な実装基盤候補。
- Candidate270・Candidate271: validation wrapperを迂回した失敗反例。本文を継承しない。
- Candidate272: 明示permission削除がraw result配送を閉じず、F03共同発行も3 / 5へ退行した反例。本文差分を効果として継承しない。
- Candidate254: 自然語系列の祖先。直接親へ戻さず、自然語だけで構成する不変条件を保持する。

## KPIと実行経路の対応

### Candidate269とCandidate272の全20件

同じraw-rollout尺度でCandidate269とCandidate272を数えた。値は各ケース5件の中央値である。

| ケース | C269 model応答 / custom exec / wait | C272 model応答 / custom exec / wait | token中央値差 |
| --- | ---: | ---: | ---: |
| F01 | 5 / 4 / 1 | 6 / 4 / 1 | `+18.04%` |
| F02 | 5 / 3 / 0 | 6 / 5 / 0 | `+32.15%` |
| F03 | 5 / 3 / 1 | 5 / 3 / 1 | `+1.09%` |
| F10 | 5 / 4 / 0 | 5 / 4 / 0 | `-0.68%` |

F01・F02だけmodel応答中央値が一回増え、F03・F10は同じだった。token差のケース配置と一致する。特にF02は外側custom exec中央値も`3 -> 5`へ増えた。

Candidate272の変更箇所はvalidation返却文だけで、変更前readの分割を要求していない。したがって、分割増をその一文の必然的効果とは断定しない。N=5の実行方法のばらつきとして扱う。ただし、Candidate272が狙ったpermission削除はこの主要な費用経路を制御せず、F02のraw carrierを減らす仮説もKPIへ現れなかった。このためCandidate272を追加Nへ進める理由はない。

### F01

Candidate147 N=5中央値run `55ed230a1b5546beab37c4c15b14d378`は107,202 tokenだった。raw rolloutではmodel応答4回、外側custom exec 3回、external wait 0回である。validation custom tool resultは40,639文字だった。

Candidate272のno-wait run `7cc683bea9ec4ca5b03af2bc361118ef`は225,064 tokenだった。model応答7回、外側custom exec 6回、external wait 0回で、validation custom tool resultは40,499文字だった。validation outputはほぼ同じなのに、外側callとmodel応答が各3回多く、tokenは117,862増えた。

このrunでは、開始identity、source read、test readを別々のcustom execで受け取ってから変更へ進んだ。codex event上は途中の`agent_message`がなくても、raw rolloutには各custom tool result後のtoken-count更新があり、同じmodel stepではない。

### F02

Candidate147 N=5中央値run `2b61801f7ad04896b8d26b6f64f6cc10`は128,236 tokenだった。model応答4回、外側custom exec 3回、external wait 0回である。validation custom tool resultは106,481文字だった。

Candidate272のno-wait run `0a83e261ae144600acdc6f49eb4e1512`は220,371 tokenだった。model応答6回、外側custom exec 5回、external wait 0回である。validation custom tool resultは40,628文字で、Candidate147より65,853文字小さい。それでも総tokenは92,135多い。

この逆転により、validation carrier量をF02差の主原因にはできない。Candidate272は開始確認を受け取った後にsource / test探索を二つの追加custom execへ分け、変更前だけで二回余計にmodelへ戻った。

### 四ケースの補助診断

Candidate272のnonterminal resultはF01 4件、F02 3件、F03 4件の合計11件で、external waitは17回だった。Candidate147 N=5は4件・6回である。Candidate272は17 / 17回で同じcellだけを待っておりdependencyは正しいが、model再入の使用量は大きい。

F03もraw rolloutで数え直すと共同発行は3 / 5だった。iterations 1と3では開始identityのcustom exec resultを受領してからsource / test readを別custom execで発行した。これはF01・F02で見えた変更前分割と同じ到達可能な経路である。

## 以前のcarrier仮説の訂正

Candidate269 N=20では、中央値境界runのcarrierがCandidate147より大きいことを確認した。この観測自体は正しい。しかし、Candidate272は明示permissionを削ってもraw resultを10 / 10件で返し、output量が小さいrunでもtokenが高かった。したがって次の二つを分ける。

1. raw output、truncationおよびnonterminal waitはtokenを上振れさせ得る実行時の使用先である。
2. C147との差を一貫して作るprompt制御上の原因は、独立invocationが個別resultをAIへ返し、変更前にmodel応答を増やせるpermissionである。

`発行済みの全result`を消すだけでは1も2も閉じない。output cap、summary指定、wait時間または成功runのwrapper codeを次案にしない。

## 閉じる辺

現在の自然語`DECISION_BOUNDARY`は、互いに影響しない作業を「同じmodel stepから発行」すると述べる。しかし保存traceでは、user-visible messageを挟まずに別々のcustom execを順次発行する経路が残った。禁止対象がresultの利用関係だけで、各invocation resultがAIへ戻るpermissionまで閉じていない。

次に閉じる辺は次である。

`同じ判断で発行する独立invocation -> 個別invocation resultをAIが受領できる -> AIが残りのinvocationを別の外側callとして発行できる`

正常経路は次の所有関係で保持する。

- 一つの外側evidence operationが、共同発行対象の各invocation identityを実行前に所有する。
- 外側operationがterminalになる前は、内側invocationのresultをAIの判断入力にしない。
- すべての内側invocationがterminalになった後に、一度だけ共同resultをAIへ返す。
- 開始identityが異常なら、TaskSpecどおり変更と必須validationだけを止める。すでに共同発行済みのread resultを失効させたり再発行したりしない。

これは特定command、tool順、Promise.all、wrapper codeまたは出力上限の指定ではない。個別resultが外側operationの途中でAIへ越境できるpermissionを閉じる設計である。

## 別に残す課題

- nonterminal wrapper後のsame-cell waitはC147でも6回発生しており、0回を新しい合格線にしない。
- waitが返すraw output量をpromptで制限する案は、executor側の配送方法へ踏み込むためCandidate解決策にしない。
- F01の同理由result再取得1 / 5は、truncationまたは大出力が存在しても可視の兄弟receiptまで失効させる経路として残す。変更前共同発行の回復後も再発する場合に限り、result失効範囲の別差分として扱う。
- F10 instruction dependencyは5 / 5で成立しているため、次差分で変更しない。

## 次の進め方

1. Candidate269とCandidate272の全runについて、変更前の外側custom exec数、model応答数、共同発行成否、wait数をケース別に固定する。
2. Candidate147および自然語Candidate264の成立runと照合し、上記の外側operation ownershipだけで誤経路を閉じられるか反証する。
3. 反例がなければ、Candidate269を直接親、Candidate272を失敗反例とする一つの自然語差分を設計する。Candidate272の効果のなかったpermission削除は継承しない。Candidate番号を進めるためにC272を自動的な親にはしない。
4. 初回評価では品質に加え、F01・F02・F03の共同発行をC147実測率に合わせて判定し、ケース別tokenを先に見る。nonterminal頻度やraw output量を100% gateにしない。

現在状態は`candidate272_n5_analyzed / carrier_single_cause_falsified / prechange_individual_result_ingress_identified / f03_raw_rollout_count_corrected / next_permission_edge_fixed / next_candidate_not_created / n20_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`である。
