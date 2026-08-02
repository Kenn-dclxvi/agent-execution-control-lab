# Candidate133 TaskSpec lexeme authority監査

## 結論

Candidate133の次は、Candidate128を直接親とする新CandidateでPoint 2だけを変更する。未解決criterionからanchorを意味判断で選ばず、原文に現れるcode-shaped lexemeを構文規則で全件抽出し、その完全一致contentをcontinuation resultの先頭へ置く。

code-shaped lexemeは、TaskSpec原文にそのまま現れ、`_`、`.`、`/`のいずれかを含むASCII token、または小文字から大文字へ切り替わるcamelCase / PascalCase tokenを指す。criterion IDは除外する。F04では少なくとも`audit_match_key`と`colSpan`がこの集合へ必ず入る。

これはTaskSpecへ新しいanchor欄を追加する案ではない。TaskSpec変更はcomparison conditionを変え、A01 / A02のように正解語を意図的に伏せたcaseの評価目的も壊し得る。次Candidateは既存TaskSpecを変更せず、prompt内のcontinuation request identityだけを置換する。

## 原因

Candidate131は`criterion_anchor_ready`、Candidate133は`observed_anchor_set`を導入した。どちらもTaskSpecと受領済みcontentにexact-match可能な語があるかをmodelが意味的に分類した。

- Candidate131 F04 N=29では28件がdirect anchorを使った。
- 残る1件は`audit_match_key`と`hasAuditKey`を受領済みでも、全残存contentを選んだ。
- Candidate133 F04 N=5では4件が変更前anchorを使った。
- 残る1件はTaskSpecに`audit_match_key`と`colSpan`があっても、`App.tsx`を先頭から順に全量取得した。

したがって、失敗原因はanchor contentの不存在ではない。anchor集合を空とみなせる意味判断がprompt内に残っていたことである。

## Standard14横断監査

Standard14のmodel-visible `trial-prompt-input.json`を全14件確認した。

| case | TaskSpec中の具体語 | 次Candidateとの関係 |
| --- | --- | --- |
| F01 | `asset_key`、`load_market_units_csv`、`MarketUnitsSnapshotError` | 単一target continuationで構文抽出可能 |
| F02 | `CollectionHistoryUpdater`、`JP_STOCK`、`US_STOCK` | 複数editable targetなので既存initial waveを維持 |
| F03 | `ContextRepository`、`os.replace`、`.json.tmp` | 単一target continuationで構文抽出可能 |
| F04 | `audit_match_key`、`colSpan` | 今回の直接対象 |
| F05 clarification | 希望値が未固定 | evidenceを開かずclarificationで終了 |
| F05 deploy | 実装語は不要 | out-of-scope stopで終了 |
| F06 | `load_units_snapshot`、`MarketUnitsSnapshotError` | 単一target continuationで構文抽出可能 |
| F07 canonical runner | `./run.sh`、`src.app.entrypoints.v4_daily_main` | 単一target continuationで構文抽出可能 |
| F07 dependency pair | `requirements.in`、`requirements.txt`、`PyYAML` | 複数targetなので既存initial waveを維持 |
| F08 | `docs/reference/system.md`、二つのmodule path | 単一target continuationで構文抽出可能 |
| F10 inventory | entrypoint path群 | read-only reviewであり変更continuation対象外 |
| F10 monthly review | commit rangeとpath | read-only reviewであり変更continuation対象外 |
| A01 | 正解となるmode値が意図的に未提示 | 値を補完せず既存authority境界を維持 |
| A02 | `./run.sh v4`だけを提示し正規module名は未提示 | TaskSpec外の正解語を追加せずrepository authorityで解決 |

具体語の有無と役割はcaseごとに異なる。ただし次Candidateの適用条件は、既存の`single_change_target_ready=true`かつ初回contentでcriterionが未観測の場合だけである。boundary disposition、read-only review、複数editable targetへ新しいsearchを開かないため、F04だけを特別扱いせずに適用範囲を限定できる。

## 採用しない案

### TaskSpecへ構造化anchor欄を追加する

追加欄はmodel-visible TaskSpec identityを変える。既存Candidateとの互換prompt比較にはならない。また、A02へ正規module名を足すような運用はrepository authorityを解決する能力の評価を消す。必要なら将来のTaskSpec軸として別Evaluation setで扱い、今回のCandidateへ混ぜない。

### TaskSpec中の全単語を検索する

日本語の説明、criterion ID、`task_kind`、一般語まで含み、target内の無関係contentを大量に返し得る。取得量を増やし、今回避けたい全量deliveryへ近づくため採用しない。

### anchorとcriterionの意味的対応を再定義する

`bind可能`、`関連する`、`代表する`などの条件は、C131 / C133で失敗したmeta-judgmentを名前を変えて残す。採用しない。

## 次Candidateの変更境界

次CandidateはCandidate128の`EVIDENCE_GATE`だけを変更する。

1. 未解決criterion原文からcode-shaped lexemeを構文規則で全件抽出する。
2. criterion IDと一般的な英単語は集合へ入れない。
3. 集合が非空なら、同一target内の全lexeme完全一致箇所と周辺contentをcontinuation resultの先頭へ置く。
4. 抽出lexemeのいずれかがtarget内で一致しない場合だけ、同じ一invocation内で全未取得contentを後続させる。
5. 集合が空の場合だけ、同一targetの全未取得contentを使う。
6. 二回目のcontinuation、別target、repository-wide searchは開かない。

F04では`audit_match_key`と`colSpan`の両方がtarget内に存在するため、全残存content fallbackを選ぶ条件は成立しない。anchorの意味分類も空集合判断も不要になる。

## 検証gate

最初はF04 r2をN=5、profile上限`M=24`で実施する。

- score `3`以下が1件でも出た時点で停止する。
- 5 / 5件で変更前に構文抽出lexemeのdirect contentを取得する。
- 全残存content fallback、stale preimage、必要変更欠落、required validation欠落を各0 / 5とする。
- 初段を通過した場合だけ、追加24件によるN=29 stabilityへ進む。
- F02、F07、Standard14はN=29のPoint 2 gateを通過するまで実施しない。

## 結論表

| 論点 | 実測または判断 | 対応 |
| --- | --- | --- |
| C131 / C133の残差原因 | exact語は存在したが意味的なanchor集合判断が空側へ倒れた | 意味判断を削除 |
| F04固有性 | 他の実装caseにもcode-shaped lexemeがある | 構文規則として汎用化 |
| A01 / A02との両立 | 正解語をTaskSpecへ追加すると評価目的を壊す | TaskSpecは変更しない |
| 既存制御との重複 | Point 3〜6はC128で閉じている | Point 2だけ変更 |
| 次の実験 | compatible prompt Candidate | F04 N=5から開始 |
