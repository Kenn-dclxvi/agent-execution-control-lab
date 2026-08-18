# Prompt制御の検討原則

## この文書の役割

この文書は、THE-CAPTION向けのプロンプトへ制御を追加、変更、削除する前に確認する設計原則の正本である。評価基盤のLayer、KPI、スキーマは対象としない。また、特定のCandidateを採用するか、リリースするか、THE-CAPTION本体へ反映するかも、この文書だけでは決めない。

現在の内容には、ControlFreeRepositoryからCandidate222までの保存済み結果と、Candidate214のsource delivery再監査を反映している。Candidateごとの詳細は[`candidate-history.md`](candidate-history.md)と[`prompts/candidates/README.md`](../prompts/candidates/README.md)、Candidate125からCandidate147までの因果関係は[`Candidate125からCandidate147までのプロンプト制御知見`](candidate125-candidate147-control-findings-synthesis.md)を参照する。少数回の試験で得た結果を、未評価の条件へ一般化してはならない。

試行回数は`N`で表す。新しい試験や文書では、`B`を試行回数の意味で使わない。過去のファイル名や題名に残る`B20`は、履歴上の識別子としてそのまま残す。

## 最優先の原則

制御の目的は、モデルに望ましい判断をさせることではない。意図しない動作を実行できる許可、またはその動作へつながる依存関係をなくすことである。

同じ入力を与えられたモデルが、判断や処理順序を変えるだけで問題のある操作をプロンプトの規則に違反せず実行できるなら、その経路は閉じていない。成功率、Score 4の件数、トークン、経過時間が良くても、その制御が効いたとは判定しない。

AIが選べる処理方法を、評価で観測した成功runのcommand、read範囲、tool順、判断順またはmodel stepへ合わせること自体を制御目的にしない。TaskSpecが手段を成果条件として明示した場合、または問題操作のpermissionかdependencyを閉じても正常経路を維持するために必要な場合を除き、処理方法はpermission内でAIが選ぶ実装方法とする。望ましい処理順を直接指示しなければ成立しない案は、prompt制御の設計思想と一致しないためCandidateを作成しない。

比較可能な条件で品質を維持し、all-agent `total_tokens`と`elapsed_seconds`がともに減少した場合は、costの方向が改善したと判定できる。どちらか一方でも増加した場合は、まず増えた指標をcost退行として扱う。対象機序と変更対象外への影響は3 KPI差の原因診断として確認し、独立した合否条件にはしない。tool call数、model step数、read回数、出力量または経路の形は原因診断に使えるが、3 KPIの判定を置き換えない。

設計は次の順で進める。

1. 保存済みtraceから、実際に起きた問題のある操作を特定する。
2. その操作を許していた記述や、そこへ到達させた依存関係を特定する。
3. その許可を削除するか、正常な処理に必要な範囲だけへ狭める。成功した実行のツール順や判断順を、新しい手順として転記してはならない。
4. 正常終了に必要な情報について、誰が持ち、どの経路で渡し、誰がどこまで読めるのかを確認する。問題のある経路を再び開かなくても、その情報が届く必要がある。
5. 問題のある操作をまだプロンプトの規則に違反せず実行できる場合や、正常な処理に必要な情報まで届かなくなる場合は、Candidateを作成しない。

### 必要な情報まで遮断した場合の直し方

たとえば、元資料全体の再読を禁止した結果、レビューに必要な一部分まで読めなくなったとする。このとき、「必要な場合だけ元資料を読んでよい」「先に必要性を判定する」と書き足してはいけない。その書き方では元資料を読む許可が残り、読むかどうかを再びモデルの判断に委ねることになる。

代わりに、実行前に次の内容を決める。

- 必要な値を誰が取得するのか。
- 元資料のどの範囲だけを読めるのか。
- 取得した値を、どの入力としてレビュー担当へ渡すのか。
- rootやレビュー担当が、元資料全体を受け取れないようにする方法。

つまり、「元資料を読む必要があるかを正しく判断させる」のではなく、「必要な人へ、必要な部分だけが最初から届く形にする」。

このように限定した情報の受け渡し経路を、この文書では`carrier`と呼ぶ。

ここで示しているのは、評価対象のプロンプトへ「停止せよ」と書く制御例ではない。Candidateを設計する側が、その案を評価へ進めてよいかを判断するための原則である。必要な`carrier`を事前に一つへ定められない案は、C214で禁止した元資料全体の読み取りを再び許してしまうため、`prompt_control_not_demonstrated / candidate_not_created`として棄却する。

ただし、棄却するのはその案だけであり、問題の検討を終了するわけではない。問題は未解決の設計課題として残し、読み取り対象の粒度、情報の取得者、パケットの作り方、rootへ返す出力の範囲を分解し直す。C214のreviewer-side局所境界を維持し、未閉鎖の初回deliveryも閉じる別の構造を見つけるまで、条件文を足したCandidateの作成や評価には進まない。

レビュー制御では、Candidate214で実現した「packet構築後にreviewerが投影元を再読しない」と「別containerの必要観測を残す」という局所境界を維持する。後続のdelivery再監査では、Candidate214でもrootがreview開始前にwhole sourceを受領していたため、rootへの初回mixed-owner deliveryは禁止できていなかった。必要な情報まで遮断した問題と初回deliveryの未閉鎖を、情報の取得者、受け渡し経路、読める範囲、受け取れる出力をsource取得前に限定して解消する。現在の詳しい方針は[`Candidate214経路閉鎖の再制御方針`](candidate214-route-closure-recontrol-direction.md)と[`review carrier bootstrap authority監査`](review-carrier-bootstrap-authority-audit.md)に記録する。

## 設計時に守ること

### どの層で制御するか

比較の出発点は、root `AGENTS.md`を0-byteにし、各パスに適用されるリポジトリの指示だけを残した`the-caption-3ce91a4-control-free-repository-r1`とする。この状態でも、TaskSpecは利用者が求める結果、許可された操作、必要な検証、停止条件を定める。リポジトリ上の正本は正しいパスや配置規則を定め、リポジトリの現在状態は採用できる事実を限定する。これらだけで正常に完了できる処理へ、同じ意味の全体共通labelを重ねてはならない。

制御を置く場所は、次のように分ける。

- 利用者が求める結果、許可、必須操作が未確定なら、TaskSpecまたはスキーマで明示する。
- リポジトリから一意に決まるパス、コマンド、配置規則は、リポジトリ上の正本に置く。
- 操作を発行する時点でモデルから見える条件に基づく許可、依存関係、結果の採用条件、結果の失効条件は、プロンプトで制御できる。
- ツール結果の配送、出力量の上限、操作の不可分性、runtime hookは、プロンプトでは強制できない。これらがなければ解決できない案は`candidate_not_created`として棄却するが、問題を解決済みまたは検討終了とは扱わない。リポジトリ内で制御できる境界へ問題を分解し直す。
- 正しい成果が採点規則のために低得点になる問題は、採点規則で修正する。

### 利用者が求める結果、証拠、変更を分ける

- 利用者が決める結果と、AIが選ぶ実装方法を分ける。未確定の結果をリポジトリの内容から推測して補ってはならない。結果が確定している場合は、リポジトリ上の正本から実装方法を選べる。
- 証拠が十分かどうかを、バイト数、行数、読み取り回数、対象数、呼び出し回数、ラウンド数では判定しない。その証拠を使う判断に必要な事実を観測できたかで判定する。
- `satisfied / unsatisfied / unobserved`を混同しない。`unobserved`は判断材料が足りない状態であり、`unsatisfied`は必要な事実を確認したうえで条件を満たしていない状態である。両者では次に行う処理が異なる。
- 複数の変更結果、対象、相互関係があるタスクでは、個々の変更を始める前に、必要な結果全体を一つの実装方針へ結び付ける。その実装方針には、変更対象、変更条件、維持すべき条件を含める。
- リポジトリを読むのは、未確認の判断項目と、現在不足している事実が特定され、その読み取り結果によって判断を進められる場合に限る。「念のため」の再読、実装方法を選ぶだけの探索、確定済み判断の再確認は行わない。
- 変更の失敗や不足した結果によって無効になるのは、その影響を受けた判断だけである。別の変更結果や、すでに成立した別の操作結果まで一括して未確認へ戻さない。

### 実行者、結果、レビューの責任範囲を分ける

- 各操作には実行者を一つだけ割り当てる。同じ判断を別の実行者へ割り当て直さない。判断責任者やrisk labelを、実際の実行者の指定として扱ってはならない。
- **Worker選択とコスト判定**: TaskSpecが独立したworkerによる実行を成果条件として明示していない限り、workerを使うかどうかは実装方法である。worker数や役割名そのものを制御の成果にせず、rootが実行する場合にも同じ判断条件、許可、結果の対応関係を保つ。
- rootが実行者でない操作では、rootは入力の準備、受け取った結果の対応付け、最終状態の集約だけを行う。判断をやり直したり、欠けた結果を推測で補ったりしない。
- 結果は、誰が、どの操作で、どの入力に基づいて生成したのか、どの種類の結果なのかを識別できるようにする。条件を満たさなかったという結果も、その操作の確定結果として保持する。
- レビューの`counterexample_found`、`no_counterexample_found`、`unavailable`では、必要な証拠の範囲が異なる。一件の具体的な反例で確定できる結果に、対象全体の完全性や無関係な情報の不足を要求してはならない。
- パケットで渡す情報、レビュー担当が自分で読む情報、rootが受け取る情報を、元資料を読む前に分ける。入力がモデルから見えるというだけで、その情報をパケットへ複製してよいことや、rootへ元資料全体を返してよいことにはならない。
- 元資料が存在すること、依頼の目的、ticket、ownership labelは、読める範囲を制限しない。実際に誰へ何が渡るかを限定していなければ、読み取り権限を制御したことにはならない。

### 結果の影響範囲、検証、完了を分ける

- ある結果によって後続処理を止めるのは、その結果が対象、許可、方法、停止条件を変え得る操作だけにする。タスク全体や、互いに独立していて実行を許可済みの読み取りまで止めてはならない。
- 変更後は、必要な検証項目、実行順、各項目の合格条件、失敗時の停止条件を一つの実行票へまとめる。TaskSpecが正確なコマンドを指定していないことを理由に、リポジトリを追加で探索してはならない。
- 必要な検証結果をすべて受け取ってから、一度だけ完了を判断する。検証成功後に新しい要求が加わっておらず、既存結果も失効していないなら、読み取り、検証、レビューを追加しない。
- 検証していない成果を、成功、完了、採用可能として報告しない。

### 制御文を増やしすぎない

- 一つのlabelには、一つの不変条件だけを持たせる。owner、実行者、runtime identity、結果、証拠、失効条件を一つのlabelへ連結しない。
- 条件を追加するときは、その条件によってなくなる具体的な分岐、再読、再試行、コンテキストの受け渡し、責務の競合を示す。なくなるものを説明できない条件は追加しない。
- 既存の制御と同じ問題を扱う場合は、新しい条件を並べる前に、既存条件の置き換え、統合、削除を検討する。
- 同じ意味に見える文でも、文字列が似ているという理由だけで削除しない。実行判断の近くにある再記述が、その場で必要な制約として働いている場合がある。削除前後の実行経路を比べ、意味が保たれることを確認する。
- 文面が整っていること、抽象的な名前を付けたこと、文字数を減らしたことだけを改善の根拠にしない。

## 経路ごとに分けて評価する

次の分類は、プロンプト内でモデルに選ばせる分岐ではない。保存済みtraceを診断し、変更対象外への悪影響を調べるために使う。

| 経路 | 正常な最短経路 | 主な問題経路 |
| --- | --- | --- |
| 利用者が求める結果が未確定 | 未確定の値だけを利用者へ確認する | リポジトリを読んで値を推測する |
| 実装方法だけが未確定 | リポジトリ上の正本から実装方法を決め、変更へ進む | 正本のパスが未記載というだけで停止する、決定後も探索を続ける |
| 実装と検証 | 必要な証拠を確認して変更し、必要な検証をすべて終える | 一部だけ変更する、検証途中で判断へ戻る、不要な再実行をする |
| 読み取りだけのレビュー | 必要な入力だけを使い、指摘あり、指摘なし、判定不能のいずれかを返す | パケット作成済みの元資料を再読する、対象外を探索する、結果確定後も読む |
| 変更せず終了 | TaskSpecだけで終了を判断する | 不要なリポジトリ探索、変更、試験を始める |

対象経路の改善と、非対象経路の悪化を相殺してはならない。まず経路ごとに品質と機序を判定する。変更対象外の経路で、新しい分類、探索、再開、再読、再試行が増えていないことを確認した後に、Standard14の3つのKPIを集計する。

## 制御の価値と評価順序

同一のprompt改善系列では、評価ケース、fixture、TaskSpec、oracle、rating、model、reasoning、runtime、permission、token accountingおよび集計方法を固定し、Candidateのprompt identityだけを変える。固定benchmarkの結果から失敗経路やcost原因を診断し、その診断を次Candidateの一般的なpermissionまたはdependency境界へ反映してよい。この反復利用によってbenchmarkの比較可能性は失われないが、初見またはblindという証拠属性は失われる。両者を混同して、Candidateごとに新しい試験を作ってはならない。

新しいケースまたは評価系列を作るのは、固定benchmarkでは対象機序を観測できないことが事前に確認された場合、評価契約の欠陥を修正する場合、またはtask objective自体が変わった場合に限る。その場合、旧系列と新系列の差をprompt効果として比較しない。別途blind検証が必要なら独立した最終gateとして事前に固定し、各Candidateの設計サイクルとは分ける。固定benchmarkのcase ID、model-invisibleなliteral、oracleまたはexpected resultをpromptへ転記することは、反復利用ではなく試験への個別適合なので禁止する。

制御によるトークンの増減は、次の関係で考える。

```text
トークンの正味差
= 制御文を理解するためのコスト
 + 追加された判断と確認のコスト
 - 回避できた探索、コンテキストの受け渡し、再読、再試行、手戻りのコスト
```

評価は次の順で行う。

1. **実行有効性**: 結果が`valid`か、採点可能か、比較条件が一致しているかを確認する。
2. **品質**: 利用者が求める結果、正しい終了状態、アーティファクトの境界を満たしているかを確認する。
3. **機序**: 変更した条件が、対象とした問題経路を実際に閉じたかを診断する。
4. **対象外への影響**: 変更対象外の経路へ、新しいコストや問題経路を移していないかを診断する。
5. **KPI**: 比較可能な`quality_score`、全エージェントの`total_tokens`、`elapsed_seconds`を比較する。
6. **安定性**: 実行前に決めたN拡張と停止条件を使い、低頻度の失敗がないかを確認する。
7. **採用、リリース、本体反映**: 評価とは分けて、明示的に判断する。

制御差分の因果を説明するには、対象とした機序が実際の挙動とどう対応したかを観測する。ただし、機序の全件成立を一律の合否条件にはしない。機序の成立・不成立と品質再現性の成否が常に一致し、その相関が100％であることを互換する証拠で確認した場合だけ、その機序へ100％成立を要求する。ここで品質再現性との相関が100％とは、機序が崩れたrunでは例外なく品質も再現できず、機序が成立したrunでは例外なく品質を再現できる対応をいう。その対応が確認されていない機序の成立率は、原因を調べる診断値として扱い、1件の不成立だけで追加N、Standard14または比較を自動停止しない。N=5の全件成功だけでは、低頻度の品質失敗がないとは判断しない。品質の中央値が100でも、個別の低Scoreを相殺してはならない。

経路、tool順、model step、worker routing、read回数または個別の機序成立率はKPIではなく、3 KPI差の原因を説明する診断情報とする。これらの診断値だけで品質またはcost判定を反転させず、追加N、Standard14、比較または採用判断を停止しない。診断値が利用者要求の未達、quality rating対象のrequired effect欠落、実行無効または比較条件不一致を直接示した場合は、対応する実行有効性または`quality_score`の判定へ反映し、経路自体を別の合否軸へ昇格させない。

品質を維持した比較で、all-agent `total_tokens`と`elapsed_seconds`がともに減少した場合だけ、cost改善の方向を自動判定する。一方だけが減少し他方が増加した場合、増加した指標はcost退行である。追加costと、品質または必要な正常経路との対応は原因診断として監査するが、経路の形そのものを第4のKPIまたは独立した採用gateにしない。評価基盤は3 KPI、互換条件および診断情報を保存し、採用、releaseおよび本体反映は別の明示判断とする。

`N=20`は、同じ比較条件で選んだ20件のatomic runを意味する。wave数やbatch数を試行回数として扱わない。model、reasoning effort、runtime、rating、case set、token accountingは比較条件に含める。これらが異なる結果の差を、プロンプトの差へ帰属してはならない。

baselineを新しく実行するのは、Candidate resultが有効かつ採点可能で、保存済みの互換baselineがない場合に限る。mechanism不通過だけをbaseline比較の停止条件にしない。まず、同じimmutable identityと比較条件を持つ保存済みresultを再利用し、不足するslotだけを実行する。コストを合否判定に使う場合は、比較するbaseline、比較条件、許容幅、集計単位を結果を見る前に固定する。

## Candidate125以降から得た、今後も使う知見

この節は、当時の採用判断を書き換えるものではない。今後の設計判断に再利用できる因果関係と、繰り返してはいけない失敗をまとめる。

| 観測したCandidate | 今後も使う知見 | 繰り返してはいけないこと |
| --- | --- | --- |
| C125–C142 | 証拠が十分かどうかは取得量ではなく、判断に必要な事実を確認できたかで決める。変更に失敗しても、未達の必要結果は維持する | 証拠の有無、結果の達成状態、変更の組み立て、復旧処理を一つの全体条件へまとめない。下流の条件を強くするだけでは、部分変更が誤停止に変わる |
| C143–C147 | 必要な結果全体を上流で一つの実装方針へ結び付ける。使い手のいない証拠取得を禁止し、結果の停止効果を影響する操作だけへ限定する。C147はStandard14 N=100で1,400 / 1,400件がScore 4だった | C146を機序不成立だけで停止した判定は履歴として保持するが、今後は同種の経路観測を3 KPI差の診断へ限定する。経路を第4のKPIにせず、失敗したCandidateへ条件を足し続けない |
| C148–C163 | 利用者が求める結果と実装方法の分離、変更前調査の限定、実行者と結果の対応、検証実行票は、個別に行動差を確認してから統合できる。C163はStandard14 N=5で70 / 70件がScore 4だった | 読みやすい一般論を一括して追加しない。C148とC156はコストが改善または同等でも、A01を5 / 5件失敗した。個別に効果を確認していない文を統合しない |
| C164–C176 | レビューの要否、専用の実行者、参照禁止の入力、結果の採用条件、3種類の終了結果を、通常の実装処理と分ける。具体的な反例が一件見つかれば、その判定はそこで確定できる | 明示された規範がない差を、一般知識だけで反例にしない。N=5の通過だけでは、低頻度のcanary混入、無関係な情報不足の優先、結果の汚染を防げたとはいえない。C173 N=50は446 / 450件、C175 N=50は447 / 450件がScore 4で停止した |
| C177–C193 | 情報不足、失敗、先行結果の影響は、その結果によって変わる判断と操作だけへ限定する。対象ケースでは、レビューの証明責任や結果の採用条件を局所化する機序が成立した。C187のTC-TPO04 N=20全件成功は、そのケースに限った証拠として保持する | レビューの外側にある操作、観測、変更、終了を、責務名だけで分割しない。限定ケースの成功をADR9やStandard14へ一般化しない。C191–C193は、C147が実現していた相互に独立した呼び出しの同時発行を維持できず、品質改善と機序成立を両立できなかった |
| C194–C203 | C199は、レビュー内部の責務を分けてもmodel stepを増やさず、44 / 45件をScore 4まで回復した。C200は、パケットへ投影済みの元資料を再読する経路を0件にした。C202とC203は45 / 45件がScore 4だった | ticket、ledger、machine receipt、最小操作集合、「先にcertificateを判定する」という指示は、操作の許可そのものを制限しなければ制御にならない。C200は必要なレビュー担当まで遮断した。C202とC203は品質を満たしたが、不要な読み取りと不要なレビュー担当が残り、機序は成立しなかった |
| C204–C206 | 一度採用した証拠を、値が変わるまで有効としたC206では、rootによる本文の再取得が7件から0件になった | C147の機能を責務名で言い換えても、相互に独立した処理の同時発行は回復しなかった。C204とC205は品質を通過したが機序を通過しなかった。C206もStandard14全体で優位なコスト改善を示せなかった |
| C207–C213 | 結果の種類ごとに必要な証拠と、その証拠を読む実行者を分けると、C207で12 / 20件あった反例発見後の読み取りは、C208 N=5で1件まで減った。パケットの作成元を記録すると、同じ資料を別名で読み直す範囲を狭められる | 状態名、範囲名、処理区分、certificateをモデルに選ばせるだけでは、読み取り権限は閉じない。C208 N=50は449 / 450件がScore 4だったが、23 / 450件で機序が成立しなかった。C209–C213も、必要な読み取りの欠落と不要な読み取りの両方を解消できなかった |
| C214–C222 | C214はpacket構築後の投影元再readを0件にし、別containerの必要paired observationを残した。C216はpacketと重複する範囲の読み取りを0件に保ちながら、必要で重複しない範囲の読み取りを残した。C220はレビュー不要時のreviewer起動を9件から1件へ減らした | C214はrootがwhole sourceを受領した後にcontainer全体をreviewerへ閉じたため、同一containerの必要値carrierを失った。後続再監査ではC214のroot初回whole-source deliveryも未閉鎖だった。C215とC216は「必要な場合」という判断でread permissionを再び開き、C217はmodel-visible inputとpacketへ合法的に渡せる入力を混同した。C218–C220のownership、ticket、observable output、C221のproducer別集合、C222のobservation view定義は、最初のroot whole-source permissionを閉じなかった |

成功したCandidateは、後続Candidateが全文を引き継ぐ親として扱わない。そのCandidateが実証した局所的な境界の証拠として使う。失敗したCandidateも、修正条件を足すための親にはしない。再び開いてはいけない許可、必要な処理まで止めた過剰遮断、情報の受け渡し経路の矛盾、モデル任せで強制できなかった分類を示す反例として使う。

## Candidateを作成する前の確認事項

新しいCandidateを作る前に、次の内容をすべて記録する。

1. 比較の基準にするプロンプト集合と、その状態で正常に完了する最短経路。
2. 保存済みtraceで実際に確認した問題経路と、その結果が後続処理へ与えた影響。文面だけを読んだ指摘では代用しない。
3. 問題経路を許している記述または依存関係と、TaskSpec、リポジトリ上の正本、リポジトリの現在状態だけでは防げない理由。
4. 追加、変更、削除する条件と責任範囲の全件。各条件は、明示された入力、リポジトリ上の正本、機械的に対応付けられた結果から直接判定できる必要がある。
5. 各変更によって実行できなくなる具体的な問題経路。モデルが判断順を変えても、同じ問題操作を実行できないこと。
6. 維持する正常経路。必要な情報を誰が持ち、どの経路で渡し、誰がどこまで読めるのか。
7. 新しく増える判断、label参照、例外条件と、変更対象外の経路への影響。
8. 品質、3 KPI、安定性を判定する評価ケース、比較単位、比較条件と、3 KPI差の原因を調べる機序診断。
9. invalid、採点不能、互換条件不一致、quality低下または事前に固定したKPI条件不通過の停止条件。問題経路の再発や正常経路の形だけを独立した停止条件にせず、利用者要求またはquality rating対象のrequired effectが欠ける場合は`quality_score`へ反映する。

一項でも決まっていなければ、Candidateのbundle、profile、評価枠を作成しない。一つのCandidateでは、一つの局所的な失敗機序、または分離できない一つの再構成目的だけを扱う。失敗したCandidateへ修正条件を追加し続けず、最後に機序が成立したCandidateへ戻って、差分を必要最小限にする。

## 現在の方針

レビュー制御はC147を直接の基盤とし、C214で実現したpacket構築後のreviewer再read閉鎖と別containerの必要観測を維持する。C214でもroot初回whole-source deliveryは閉じていなかったため、同Candidateの文面またはroot preread 0件という歴史的集計を、source delivery全体の閉鎖として引き継がない。C215からC222までで試した、必要性、operand、ownership、ticket、work item、observable output、producer別集合またはobservation viewをモデルに分類させる方法は、解決策として引き継がない。

次のCandidate作成へ進めるのは、最初のreview source取得より前に、既存入力だけからrootへ返せるexact projection、reviewerが直接観測するexact target、各resultを受領できるproducerおよびpacket carrierを一意に固定でき、whole-source invocationがprompt準拠で構成できない場合だけである。その境界を閉じた後も、C214とC222で品質を満たせなかった必要値がreviewerへ届き、必要reviewを完遂できなければならない。確定できない案は棄却し、条件付きでwhole-source permissionを戻すCandidateは作成しない。TaskSpec、case、fixtureまたはoracleの変更で不足を補わず、prompt内で閉じられる情報の所有と受け渡し構造を分解し直す。

C222はC221の`root_operation_set`をpre-review authorityから削除してもroot whole-source deliveryが20 / 20に残ったため、同集合への再分類を唯一の原因とする仮説を棄却した。現在は、packet構築に必要なliteral値がreviewer専有値と同じcontainerにあり、rootのreadがprojectionとwhole outputの両方を実行できる結合を未閉鎖の辺として扱う。以後の結果は[`review carrier bootstrap authority監査`](review-carrier-bootstrap-authority-audit.md)の累積閉鎖台帳へ、検証仮説、反証経路、棄却範囲、残存辺、正常carrierへの影響を追記して次へ接続する。

## 主要な一次参照

- [Candidate43 / Candidate50 targeted](../evaluations/results/candidate43-candidate50-root-read-batch-targeted-n5_2026-07-21.md)
- [Candidate69 / Candidate71 validation closure](../evaluations/results/candidate69-candidate71-validation-closure-v10-standard14-n5_2026-07-22.md)
- [Candidate98 / Candidate104 evidence admission](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md)
- [Candidate116 / Candidate118 implementation bind terminal closure](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [Candidate125からCandidate147までのprompt制御知見](candidate125-candidate147-control-findings-synthesis.md)
- [Candidate147 Standard14 N=100](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
- [Candidate163 Standard14 N=5](../evaluations/results/candidate163-free-five-verified-lines-integrated-v14-medium-standard14-n5-cli0146_2026-08-04.md)
- [Candidate173 ADR9 r2 N=50](../evaluations/results/candidate173-concrete-counterexample-adjudication-adr9-r2-n50_2026-08-10.md)
- [Candidate175 ADR9 r2 N=50](../evaluations/results/candidate175-review-operation-admission-closure-adr9-r2-n50_2026-08-14.md)
- [Candidate187 TC-TPO04 N=20](../evaluations/results/candidate187-review-admission-proof-obligation-tpo04-n20_2026-08-12.md)
- [Candidate191 ADR9 r2 N=5](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5_2026-08-12.md)
- [Candidate200 ADR9 r2 N=5](../evaluations/results/candidate200-projected-review-read-closure-adr9-r2-n5_2026-08-13.md)
- [Candidate202 ADR9 r2 N=5](../evaluations/results/candidate202-review-admission-routing-receipt-adr9-r2-n5_2026-08-13.md)
- [Candidate204からCandidate222までの系譜](../prompts/candidates/README.md)
- [Candidate208 ADR9 r2 N=50](../evaluations/results/candidate208-result-kind-evidence-domain-adr9-r2-n50_2026-08-13.md)
- [Candidate214 ADR9 r2 N=5](../evaluations/results/candidate214-packet-source-container-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate216 ADR9 r2 N=5](../evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md)
- [Candidate217 ADR9 r2 N=5](../evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate220 ADR9 r2 N=5](../evaluations/results/candidate220-review-observable-output-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate221 ADR9 r2 N=5](../evaluations/results/candidate221-review-source-authority-closure-adr9-r2-n5_2026-08-14.md)
- [Candidate222 ADR9 r2 N=5](../evaluations/results/candidate222-review-source-observation-view-adr9-r2-n5_2026-08-14.md)
- [review carrier bootstrap authority監査](review-carrier-bootstrap-authority-audit.md)
