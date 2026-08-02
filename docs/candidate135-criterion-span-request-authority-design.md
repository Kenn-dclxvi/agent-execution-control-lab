# Candidate135 criterion span request authority設計

## 結論

Candidate135はCandidate128を直接親とし、Point 2のrequest source boundaryだけを変更する。reference definition一段展開は追加しない。

## Identity

- prompt identity: `the-caption-3ce91a4-criterion-span-request-authority-r1`
- direct parent: Candidate128 `the-caption-3ce91a4-required-effect-closure-r1`
- changed rule: `EVIDENCE_GATE`
- changed axis: continuation検索語の入力authority
- unchanged: 全量fallback、continuation一回、単一target条件、Point 3〜6

## Predicate

`criterion_span`は、TaskSpecの`task_kind_goal_and_done_condition` field内で、明示criterion ID直後から次のcriterion IDまたはfield終端までの原文とする。

`criterion_request_lexeme_set`は各未観測`criterion_span`にそのまま現れるcode-shaped tokenと複数語ASCII Title Case literal labelの全件集合とする。allowed path、validation、temporary output、recoveryなど他fieldの語を混ぜない。

集合が非空なら一回のcontinuation resultの先頭で全memberの完全一致箇所と周辺contentを返す。同じinvocation内の後続として、C128の全未取得content fallbackを許す。reference identifierのdefinition展開は行わない。

## F04 N=5 gate

- valid / rateable: 5 / 5
- score `3`以下: 0 / 5
- criterion外lexeme混入: 0 / 5
- criterion lexeme direct部分: 5 / 5
- continuation二回目、別target、repository-wide search: 0 / 5

全量fallbackとreference definition到達は診断値であり、Candidate135のmechanism成否へ使わない。一件でもscore `3`以下またはsource boundary違反があれば停止する。通過した場合だけ、Candidate136で一意definition一段closureを別軸として検討する。

## 実測結果

F04 N=5はscore `4 / 2 = 4 / 1`だった。criterion外lexeme混入は0 / 5だったが、全criterion lexemeをcontinuation先頭へ置いたのは3 / 5だった。Score 2 runは必要contentを全量取得済みでも変更hunkを構成できず、変更なし・validation未実行で停止した。停止条件によりCandidate136へ進めない。

## 結論表

| 課題 | Candidate135 |
| --- | --- |
| A request source boundary | 評価対象 |
| B reference definition closure | 変更しない、診断のみ |
| 親 | C128 |
| 初段 | F04 N=5 |
| 実測 | score 4 / 2 = 4 / 1、停止 |
