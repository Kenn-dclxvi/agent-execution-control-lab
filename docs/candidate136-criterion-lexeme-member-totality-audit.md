# Candidate136 criterion lexeme member totality監査

## 結論

C136 Score 3の直接原因は、`criterion_request_lexeme_set`の入力範囲ではなくmember抽出規則の退行である。

Candidate134はcode-shaped lexemeを、`_`、`.`、`/`のいずれかを含むASCII token、またはASCII小文字の直後にASCII大文字が現れるtokenと明示していた。この規則では`audit_match_key`と`colSpan`が機械的に集合へ入る。

Candidate135はcriterion外fieldの混入を止める際、この有限規則を未定義の「code-shaped token」という略語へ置き換えた。その結果、camelCaseの`colSpan`をcode-shapedと扱うかがmodelの意味判断へ戻った。C135・C136の保存済み10件では、3 member全部を検索したのは7件、`colSpan`脱落は2件、lexeme検索自体を使わない全量経路は1件だった。

次軸は新しいanchorやcoverage拡張ではない。criterion spanというC135のauthorityを保持し、そのspanから抽出するmemberの文字形規則を有限に戻すことである。

## 保存traceの集計

F04のcriterion spanから期待するmemberは次の3件である。

- `audit_match_key`: `_`を含むASCII token
- `colSpan`: ASCII小文字`l`の直後にASCII大文字`S`
- `Audit Key`: 複数語ASCII Title Case literal label

| Candidate | 全3 memberを検索 | `colSpan`脱落 | lexeme検索なし | criterion外field由来語 |
| --- | ---: | ---: | ---: | ---: |
| C135 | 3 / 5 | 1 / 5 | 1 / 5 | 0 / 5 |
| C136 | 4 / 5 | 1 / 5 | 0 / 5 | 0 / 5 |
| 合計 | 7 / 10 | 2 / 10 | 1 / 10 | 0 / 10 |

C135の`colSpan`脱落runはScore 2だった。全target content自体は受領していたため、脱落だけをそのrunの唯一原因とはしない。しかし充足済み`colSpan`を変更へ戻す誤判定と同時に発生した。

C136の`colSpan`脱落runはScore 3だった。全量後続のmodel-visible配送が空表示cellへ届かず、`colSpan` effectを未観測として正しい一行変更後にvalidation前停止した。こちらはmember脱落が低Scoreへ直接接続した。

## C134との因果比較

Candidate134の規則は次のように有限だった。

```text
criterion_code_lexeme_set :=
  criterion IDを除くASCII tokenのうち、
  `_`、`.`、`/`のいずれかを含むもの、または
  ASCII小文字の直後にASCII大文字を含むものの全件集合
```

F04 N=5ではdirect lexeme contentが5 / 5だった。C134の問題はcriterion外field由来語を2 / 5で混ぜたsource boundaryと、参照definitionまで届かないcoverageだった。`colSpan`自体の抽出規則ではない。

C135はsource boundaryをcriterion spanへ狭め、literal labelを追加した。この二点は維持すべきである。一方、文字形規則を略語へ縮めたことは別変更であり、C134の抽出完全性を継承できていなかった。

したがって、次Candidateで同時に複数問題を解く必要はない。C136を直接親として、`code-shaped token`という一語だけを有限な文字形定義へ展開する。

## 次の有限規則

```text
criterion_request_lexeme_set :=
  各未観測criterion_spanに原文のまま現れる次の全member
  1. criterion IDを除き、`_`、`.`、`/`のいずれかを含むASCII token
  2. ASCII小文字の直後にASCII大文字が現れるASCII token
  3. 2語以上のASCII Title Case literal label
```

意味、重要度、criterionとの関連性でmemberを選別しない。synonym、TaskSpec外の語、他fieldの語を追加しない。reference identifierのdefinition展開も追加しない。

「全件」は、該当文字形のmemberを一つでも省略できないという意味である。target内で一致しないmemberがあっても集合から消さず、既存の同一invocation内fallback条件へ渡す。

## 汎用性

この規則はF04固有symbolの列挙ではなく、Standard14の複数形式を同じ文字形で扱う。

| 形式 | 例 | 規則 |
| --- | --- | --- |
| snake / constant | `asset_key`、`JP_STOCK` | `_` |
| dotted module | `src.app.entrypoints.v4_daily_main` | `.`と`_` |
| path | `docs/reference/system.md`、`./run.sh` | `/`または`.` |
| camelCase | `colSpan` | 小文字→大文字 |
| PascalCase | `MarketUnitsSnapshotError`、`ContextRepository` | token内部の小文字→大文字 |
| literal UI label | `Audit Key` | 複数語Title Case |

適用条件はC135から変えない。単一editable targetのimplementationで、一回のcontinuationが許可された場合だけである。複数editable target、review、clarification、boundary dispositionへ新しいsearchを開かない。

Standard14に現れる具体例は適用範囲の確認に使うだけで、promptへcase名、path、symbolを固定しない。`-`だけを含む語はcriterion IDや自然文との境界が曖昧なため今回の規則へ追加しない。必要な反例が出た場合に別軸で扱う。

## 既存Pointとの関係

- Point 1 Authority: 変更しない。
- Point 2 Evidence coverage: member抽出の文字形だけを修復する。
- Point 3 Effect state: C136の三値bindを保持する。
- Point 4 Dependency: 変更しない。
- Point 5 Change construction: 変更しない。
- Point 6 Closure / recovery: C128を保持する。

全量fallbackやreport deliveryを制御対象にしない。まずfull fallback前のdirect member集合が完全であることだけを検証する。

## 次Candidateのgate

次Candidateを作る場合はC136を直接親とし、F04 N=5、M=24から開始する。

- score `3`以下: 0 / 5。一件でも出た時点で停止する。
- criterion外field由来member: 0 / 5。
- `criterion_request_lexeme_set`の期待3 member: 5 / 5。
- lexeme検索なしの全量直行: 0 / 5。
- 未充足effectの必要変更: 5 / 5。
- 充足済みeffectの変更: 0 / 5。
- initial patch失敗: 0 / 5。
- required validation完備: 5 / 5。

通過後もF04だけで汎用性を確定しない。F02は複数editable targetなので新規continuation対象外であり、preservation確認に使う。F07は単一target caseと複数target dependency caseを分け、適用経路と非適用経路の両方を各N=5で確認する。

## 結論表

| 論点 | 実測 | 判定 |
| --- | --- | --- |
| criterion外field混入 | C135・C136とも0 / 5 | C135 boundaryを保持 |
| 全member抽出 | C135 3 / 5、C136 4 / 5 | 不安定 |
| `colSpan`脱落 | 合計2 / 10 | vagueな`code-shaped`が原因 |
| C134の有限規則 | F04 direct lexeme 5 / 5 | 再利用可能 |
| effect-local admission | C136で必要変更5 / 5、充足済み変更0 / 5 | 保持 |
| 次の変更軸 | member文字形定義だけ | Candidate作成可能 |
