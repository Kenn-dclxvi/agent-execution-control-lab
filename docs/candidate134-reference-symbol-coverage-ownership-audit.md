# Candidate134 reference symbol coverage owner監査

## 結論

Candidate135はまだ作らない。Candidate134の低ScoreはPoint 2 Evidence coverageの不足であり、Point 4 DependencyやPoint 5 Change constructionへ新しいglobal predicateを追加する問題ではない。

ただし次Candidateの入力はまだ一つに固定できない。Candidate134には、criterion外の語を集合へ混ぜたrequest identity失敗が2 / 5件、direct matchから既存上流定義へ届かなかったcoverage closure失敗が1 / 5件ある。この二つを同時修正すると、再び複数問題を一Candidateへ混ぜる。

## 用語

reference symbolは、取得したsource式が値や条件を参照するidentifierを指す。F04では`colSpan={hasAuditKey ? 7 : 6}`の`hasAuditKey`が該当する。

reference symbol coverageは、TaskSpecの語に一致した行だけでなく、その行の判定を実際に決めるsymbolのcurrent definitionまでmodel-visible evidenceへ含めることである。

## 低Scoreの因果列

Candidate134 iteration 5は次の順に失敗した。

1. TaskSpecから`audit_match_key`と`colSpan`を抽出した。
2. 両語の全一致箇所と前後12行を取得した。
3. 一回のcontinuationで前後45行へ広げた。
4. header、row cell、`colSpan`式は見えた。
5. 150行目の既存`const hasAuditKey = true;`は見えなかった。
6. `hasAuditKey`が欠落していると誤判定し、91行目へ同名定義を追加した。
7. lintが重複定義を検出し、build未実行でscore `3`となった。

lexeme routeは使われており、全target content fallbackも使っていない。原因はanchor選択ではなく、match contentからその判定を支配する既存definitionまでのcoverageが閉じなかったことである。

## Point 4 Dependencyではない理由

Point 4が扱うdependencyは、TaskSpecのrequired effect同士、または複数artifactの成果関係である。F02のengine / updater、F07のdirect constraint / compiled provenance pairが例である。

今回の`hasAuditKey`は新しいrequired effectではない。F04-C1とF04-C2を実装するsource内部の既存identifierである。これをeffect dependency graphへ追加すると、implementation methodをTaskSpec成果条件へ格上げする。

既存の[`Point 4監査`](candidate131-point4-dependency-audit.md)が定めた再開条件には該当しない。

## Point 5 Change constructionではない理由

重複定義の追加は、未観測の既存definitionを「ない」と扱った結果である。変更operationの削除行や置換前文字列が古かった失敗ではない。

Point 5へ`定義不存在の証明`を追加すると、変更前Evidence coverage全体をchange gateへ複製する。Candidate126 / Candidate132で観測したfalse stopを再導入するため、新しいpreimage gateは作らない。

既存の責務分離どおり、Point 5はPoint 2で受領したcurrent contentへ従属させる。

## Candidate131成功traceとの照合

Candidate131 F04 N=29の変更前commandを再確認した。

- `Audit Key`をrequestに含む: 28 / 29件
- `colSpan`を含む: 28 / 29件
- `hasAuditKey`を含む: 25 / 29件
- 唯一の低Score runは3語をcommandへ含めず、全残存contentへ進んだ。

成功28件ではTaskSpecのliteral label `Audit Key`がほぼ共通の入口だった。このmatchはheader直前の`{hasAuditKey && (`も同じ周辺contentへ入れる。Candidate134はcode-shaped lexemeだけへ限定したため、この入口を集合から落とした。

これはliteral labelが次Candidateとして十分という証明ではない。Candidate134の別2件はTaskSpecのcriterion外から語を追加しており、集合のsource boundary自体を守れていない。member typeを増やす前にsource boundary failureを独立に扱う必要がある。

## 分離した二課題

### A. request identityのsource boundary

期待は未解決criterion原文だけから集合を作ることである。実測では2 / 5件が`task_kind`、target path、temporary-output名などを混ぜ、不一致を理由にfull fallbackを開いた。

これはCandidate134の構文規則が実行判断を安定して制御しなかった失敗である。同じ規則の強調や言い換えだけを次Candidateにしない。

### B. reference symbol coverage closure

source boundaryを守った低Score runでも、code-shaped lexemeだけでは上流definitionへ届かなかった。`Audit Key`のようなTaskSpec literal labelを構文抽出対象へ含めれば今回のsource位置へ届く可能性はある。

ただしStandard14横断では、このmultiword UI label routeの直接対象はF04である。他caseへ一般化できる成立証拠はまだない。F04固有の成功だけでglobal promptへ追加しない。

## 保存fixtureによる取得規則の比較

新しい評価slotを発行せず、C134と同じ固定Layer 1のfixtureへ三つのread-only取得規則を適用した。

| 規則 | F04返却行 | 返却文字 | `hasAuditKey`使用箇所 | 既存definition |
| --- | ---: | ---: | --- | --- |
| code-shaped lexeme前後12行 | 118 / 1,097 | 5,422 | あり | なし |
| 上記＋`Audit Key` literal label | 140 / 1,097 | 7,271 | あり | なし |
| 上記＋一意なreference definition一段 | 165 / 1,097 | 8,032 | あり | あり |
| 全target content | 1,097 / 1,097 | 49,375 | あり | あり |

literal labelを足すだけではdefinitionへ届かない。match行とその前後1行に現れるidentifierのうち、同一target内の宣言またはbindingが一か所だけのものを一段展開すると、`hasAuditKey`のdefinitionを追加できた。返却量は全targetの約16%である。

match周辺の全identifierを無条件に展開すると、`className`などの反復語を拾い、F04は558行まで増えた。reference expansionには「同一targetでdefinitionが一意」というcardinality境界が必要である。

## Standard14内の別artifactへの適用

同じ固定Layer 1で単一editable targetを持つ実装caseへ適用した。

| case | direct行 | closure後 | 追加行 | 一意definition |
| --- | ---: | ---: | ---: | --- |
| F04 TypeScript / JSX | 140 / 1,097 | 165 | 25 | `hasAuditKey` |
| F06 Python test | 161 / 273 | 196 | 35 | `_ingester`、`units_mode` |
| F07 shell | 105 / 229 | 105 | 0 | `args`はdirect範囲内 |
| F08 Markdown | 0 / 636 | 0 | 0 | 修復対象文字列がfixtureにない |

規則はF04以外でも非空になる。ただしF06で追加したdefinitionが品質維持に必要だった保存失敗はまだない。適用可能性と追加制御の必要性は区別する。

## Standard14を越える汎用性の境界

汎用性はcase数ではなく、次の独立軸で判定する。

### task kind

- implementation: reference definition closureの適用候補。
- non-destructive review / read-only audit: artifact変更predicateを作らないため適用しない。
- boundary disposition: clarificationまたはout-of-scope stopが先であり、content continuationを開かない。

repository内44件のmodel-visible TaskSpecは、`implementation` 28件、`boundary-disposition` 2件、`non-destructive-review` 5件、read-only conformance review 1件を含む。全taskへ一律適用する制御にはしない。

### artifact language

固定fixtureにはPython 120、Markdown 50、shell系6、TypeScript / TSX 4のほか、JSON、INI、plist、CSSなどがある。一意definition一段closureは、少なくとも次を別対応として扱う必要がある。

- TypeScript / Python / shell: symbolの宣言またはbindingを持つため適用候補。
- Markdown / prose: symbol definitionという構造がなく、exact textまたはauthority参照を使う。
- JSON / YAML / TOML等のdeclarative artifact: identifier definitionではなくkey / path bindingを扱う必要がある。
- generated / compiled pair: 同一target一段展開ではなく、TaskSpec明示の複数artifact relationをPoint 4で扱う。

したがって`definition`を言語横断の単一文字列patternへ固定しない。適用可能domainを「同一editable target内で、一意な宣言またはbindingをrepository contentから直接観測できるimplementation task」に限定する。

### target topologyとcardinality

- 単一editable target: 一段closureの候補。
- 複数editable target: Candidate128のinitial content waveを維持し、continuationで別targetへ進まない。
- definition 0件: 不存在と断定せず、既存の同一target fallback条件で扱う。
- definition 1件: 一段だけ追加できる。
- definition複数件: modelに正解を選ばせず、追加展開しない。

### depthとcost

一段目のdefinitionがさらに別symbolを参照しても二段目を開かない。transitive closureはrepository全体探索へ拡大し得るためである。全target contentと同等の返却量になる場合もfocused routeとして成立扱いにしない。

## AとBの固定方法

Aの期待集合はTaskSpec全体ではなく、`task_kind_goal_and_done_condition`内の明示criterion ID直後から、次のcriterion IDまたはfield終端までのspanだけを入力にする。allowed path、temporary output、recovery設定を混ぜたC134 iteration 1・3を機械的に失敗と判定できる。

BはAを通過したmatch行と前後1行だけからreference identifier候補を作る。同一target内で宣言またはbindingが一か所だけのidentifierだけを一段追加する。二段目、複数definition、別targetは開かない。

Aはrequest入力のauthority、Bは返却scopeのclosureである。同じrunでもA pass / B failを許す。C134 iteration 5がその具体例である。

## 再開条件

次の順序で証拠が揃った場合だけPoint 2の次Candidateを作る。

1. source boundary: criterion外のTaskSpec fieldを集合へ混ぜないmodel-visible predicateを、保存traceから一つに固定できる。
2. coverage closure: その同じpredicateが、言語固有parserやcase固有語なしでreference symbol definitionを同一resultへ含める。
3. scope: F04以外の少なくとも一つの実装caseで同じrouteが必要または有効であると保存traceから確認できる。
4. cost: 全target contentと同等のdelivery量へ戻らない。

現在、1は構文上の期待値を固定できたがmodel実行での遵守が未検証である。3はPython / shellにも同じ規則を適用できることまで確認したが、F04外で品質上必要だった失敗traceはない。TaskSpecへ`hasAuditKey`を追加する、F04固有labelをpromptへ書く、executorで参照追跡する案は採用しない。

## 結論表

| 課題 | owner | 実測 | 次Candidate |
| --- | --- | --- | --- |
| criterion外lexeme混入 | Point 2 request identity | 2 / 5 | criterion ID spanを期待値へ固定、実行遵守は未検証 |
| full target fallback | Point 2 request identity | 3 / 5 | 同上 |
| reference symbol未観測 | Point 2 evidence closure | 1 / 5、score `3` | 一意definition一段でF04到達、F06でも非空 |
| 重複定義変更 | Point 2不足の結果 | 1 / 5 | Point 5を増やさない |
| required effect dependency | Point 4 | 新しい反例なし | 再開しない |
| Standard14外の適用domain | implementation × 単一target × 一意binding | language / task kind / topologyで限定 | 全task共通にはしない |
| Candidate135 | 未固定 | F04外の品質上の必要性が未観測 | 未作成 |
