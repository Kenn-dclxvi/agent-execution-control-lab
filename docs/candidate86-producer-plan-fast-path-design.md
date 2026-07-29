# Candidate86 producer plan fast path設計

## 結論

Candidate86はCandidate81を直接親とし、producer選択を実行前に行う原則を維持しながら、単一operationでも完全なoperation graphと明示planを維持するCandidate85の経路を除く。

変更軸はproducer planningの適用範囲だけである。既存`SPEC`が作るoperation identityを利用し、単一operationは条件を満たせばrootへ直接bindする。複数operationまたは別execution identityが必要な場合だけ、scope、dependency、result consumer、producer、waveを展開する。

F02 r1、F04 r2、D01 r1の既存Evaluation set、TaskSpec、fixture、oracle、allowed path、required validationは変更しない。Candidate85用に固定済みのsetをそのまま再利用し、C81 / C86 profile間ではprompt identity以外を一致させる。

## 作成前gate

1. 基準prompt setは`the-caption-3ce91a4-validation-wrapper-precedence-r1`である。
2. 基準の最短正常経路は、`SPEC`でoperationを固定し、各operationへproducerをbindし、predicateを実行し、required validation後にterminalを一度判断する経路である。
3. 保存済みC85 F04 traceではC81 / C85とも5 / 5件がroot-onlyかつscore `4`だったが、C85はtoken中央値`+38.29%`、elapsed中央値`+24.70%`だった。
4. C85は5 / 5件すべてで明示的なtodo planを作成・更新した。C81は3 / 5件だった。C85のmodel処理回数合計はC81の`42`から`54`へ増え、input token合計は`943,510`から`1,299,045`へ増えた。
5. C85の誤経路はWorker起動ではない。単一producer作業でもoperation graph、consumer、waveを完全に固定し、plan状態を維持したことである。
6. 既存TaskSpecとC81の`PRODUCER`だけでは、producerをAIが選ぶ時点、単一operationの直行条件、複数operation時だけ展開する情報を区別できない。
7. 置換する一つの軸は`PRODUCER`のproducer planningである。独立した`PLAN` labelやplan artifactを追加しない。
8. この軸は、実行後のproducer後付け、同一operationの重複producer、単一operationでの不要なplan維持を除く。Worker起動自体は禁止しない。
9. 新たに増える判断点は、単一operation fast pathが成立するか、複数operation topologyを展開する必要があるかである。数値token / elapsedの予測やWorker価値の完全なboolean列挙は行わない。
10. F02 r1とF04 r2で品質とall-agent token / elapsedをC81と比較する。F04通過時だけD01 r1で別execution identityがrequired outcomeである経路を確認する。
11. score `4`未満、invalid / unrateable、許可外drift、identity不一致で停止する。品質通過後、token差とelapsed差が事前固定した許容幅`0`を両方超えれば`cost_control_failed`、片方だけなら`cost_tradeoff`とする。

## Prompt変更

Candidate81から次だけを変更する。

- `PRODUCER`を、実行前のAI producer選択、単一operation fast path、複数operation topology、通常経路の再割当て禁止へ置換する。
- `OWNER_ROLE`を、AIがworkerを選んだ後のidentity / result provenanceだけを扱う形へ置換する。
- `DECISION_BOUNDARY`へ、複数operation topologyが存在する場合だけのready waveと待機条件を接続する。

`SPEC`、`TERMINAL`、`CONTEXT`、`ROOT`、`INDEPENDENCE`、`VALIDATION_CLOSURE`、`METHOD`、`RECOVERY`は変更しない。独立した`PLAN` label、明示todo、自然言語planの出力条件は追加しない。

## 評価順

1. C81 / C86へ既存`the-caption-planning-first-f02-r1`を適用し、rating v14、Medium、各`N=5`
2. F02 gate通過時だけ既存`the-caption-planning-first-f04-r1`を同条件で各`N=5`
3. F04 gate通過時だけ既存`the-caption-planning-first-d01-r1`を同条件で各`N=5`

profileはC85 profileからprompt identityとprofile IDだけを替える。Evaluation setと全comparison conditionsは変更しない。Candidate85 resultは設計根拠に使うが、C81 / C86の公式KPI comparisonへ混ぜない。

## 状態境界

bundleとprofileの作成は`draft / not_evaluated`である。targeted評価、標準14、採用、release、THE-CAPTION本体反映は別stateとする。
