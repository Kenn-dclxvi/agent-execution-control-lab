# Candidate128 / Candidate134 F04 targeted result

## 結論

Candidate134のF04 N=5はscore `4 / 3 = 4 / 1`だった。score `3`が1件出たためCandidate134を停止し、追加24件、F02、F07、Standard14へ進めない。

code-shaped lexemeのdirect contentは5 / 5件で取得した。しかし3 / 5件がその後に全target contentへ進み、構文抽出集合も2 / 5件でTaskSpecのcriterion以外の語まで拡張された。低Score 1件は`audit_match_key`と`colSpan`の周辺だけでは既存の上流定義`hasAuditKey`を観測できず、同名定義を追加してlintを失敗させ、buildを実行できなかった。

したがって、意味的anchor空判定の削除だけではPoint 2を閉じない。TaskSpec lexemeは要求箇所へ到達できても、その箇所が参照するTaskSpec未記載symbolのcurrent contentまで保証しない。

## 固定条件

- candidate: `the-caption-3ce91a4-syntactic-lexeme-continuation-r1`
- parent: `the-caption-3ce91a4-required-effect-closure-r1`
- bundle SHA-256: `adcffe5d147d99072a8d5699a721f6f077f44a6a05fcefddd28b49fa293d250f`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- pool: `ec2935e1e479acff8c53fd57c4c3e251529512705849fdde07826d3cba55fa90`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `76699e2e6f154253bf29c4545c2955ca`
- analysis: `f9344b226d814fe1bbd20036f59ce1d6`
- registered result: `57696a3578774fea87b7e7c7ddcdeaa4`
- excluded attempt: 0

比較前に保存済みF04 reference result `cea34faab78149119808da7c59628955`を一意にbindした。prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合し、preflightが5 slotを承認した後だけ発行した。

## 結果

| iteration | run | score | lexeme経路 | artifact変更 | validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `d84a6b233b144933a184e260ead9b755` | 4 | direct後、過剰集合からfull fallback | `hasAuditKey`一行 | 3 / 3成功 |
| 2 | `ba492e5102fb4cb2958d66084cd6de94` | 4 | direct、full fallbackなし | `hasAuditKey`一行 | 3 / 3成功 |
| 3 | `be2654e6c54143198122132748ba3feb` | 4 | 過剰集合からfull fallback | `hasAuditKey`一行 | 3 / 3成功 |
| 4 | `b97129434cf34fff8347e7e5268e0959` | 4 | direct後、全target content | `hasAuditKey`一行 | 3 / 3成功 |
| 5 | `1e4a2a0ab99e4ddfa1e49c2748e7149a` | 3 | directのみ、上流定義未観測 | 重複`hasAuditKey`を追加 | lint失敗、build未実行 |

5件中央値はquality `100.000`、token `177,714`、elapsed `106.048`秒だった。qualityとmechanismの停止条件に到達したため、効率改善の判断には使わない。

## 低Score run

iteration 5はTaskSpecの未解決criterionから`audit_match_key`と`colSpan`を正しく抽出し、両方の全一致箇所と周辺contentを取得した。full fallbackは使っていない。

最初のcontext幅は各一致の前後12行、continuationは前後45行だった。`colSpan`周辺からheader、row cell、空表示の条件分岐は見えたが、150行目の既存`const hasAuditKey = true;`はmodel-visible contentへ入らなかった。agentは同定義が欠落したと判断し、91行目へ新しい`hasAuditKey`を追加した。

`npm ci`は成功した。`npm run lint`は91行目と150行目のblock-scoped variable重複でexit `2`となった。TaskSpecのfail-stopに従いbuildを実行せず終了し、score `3`となった。

この失敗はC131 / C133の「anchorを捨てて全量へ進む」失敗とは異なる。Candidate134のlexeme route自体は使われたが、direct matchから一段先の参照symbol current contentがcoverage集合に含まれなかった。

## 他4件のmechanism

- iteration 2だけが、TaskSpec criterionのlexeme direct contentを使い、全target contentへ進まず完了した。
- iteration 4は両lexemeが一致済みでも`sed -n '1,920p'`を追加した。
- iteration 3は`task_kind`、target path、temporary-output名までlexeme集合へ入れ、不一致を理由にfull fallbackを開いた。
- iteration 1もconstraints由来の語を二回目の集合へ加え、不一致を理由にfull fallbackを開いた。

Candidate134は「各未観測criterion」という入力境界と「不一致時だけfallback」という条件の両方を安定して制御できなかった。

## 解釈と次の境界

次に同じlexeme抽出規則を言い換えるCandidateは作らない。保存traceは二つの別課題を示す。

1. request identity: criterion以外のTaskSpec語を集合へ混ぜず、direct一致済みならfull fallbackを開かない。
2. evidence closure: direct match行が参照するcode symbolの定義current contentを、意味分類なしに同じresultへ含める。

二つを同時に新しいglobal predicateへ入れると、再び複数問題の一括解決になる。次は低Score iteration 5を使い、参照symbolの一段展開が既存Point 2、Point 4 dependency、Point 5 change constructionのどこに属するかを監査する。その監査で既存制御との重複と適用範囲を確定するまで、Candidate135は作らない。

## 状態

`targeted_f04_n5_evaluated / quality_gate_failed / mechanism_gate_failed / score_3_1_of_5 / direct_lexeme_5_of_5 / full_content_fallback_3_of_5 / upstream_definition_unobserved_1_of_5 / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 4 / 5 | fail / stop |
| score `3`以下 | 0 / 5 | 1 / 5 | fail / stop |
| criterion code lexemeのdirect content | 5 / 5 | 5 / 5 | pass |
| criterionだけの構文抽出集合 | 5 / 5 | 3 / 5 | fail |
| 全target content fallback | 0 / 5 | 3 / 5 | fail |
| staleまたは未観測preimageを持つ変更 | 0 / 5 | 1 / 5 | fail |
| 必要変更と3 validation完備 | 5 / 5 | 4 / 5 | fail |
