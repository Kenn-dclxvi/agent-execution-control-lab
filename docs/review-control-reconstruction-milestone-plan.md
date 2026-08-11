# review制御再構成マイルストーン計画

> **位置づけ**: 現行frontier／Candidate作成前／分析進行中／評価未開始

## ゴール

Candidate147までに得た有効な不変条件を保持しながら、operation、predicate、evidence、producer、result、dependency、invalidation、terminalおよびartifact変更許可の定義を一貫した制御構造へ再構成する。

ゴールはCandidate176、Candidate187または他の既存Candidateの再現ではない。ADR9 r2の各ケースについて、model-visibleな契約と入力から期待terminalを導出し、正しいproducer、観測、resultおよび局所効果の経路で成立させる。加えて、Standard14で既存の実行制御を退行させない。

Candidate147の本文、条項数、配置または語列は保持条件にしない。必要であれば既存条項を分割、統合、置換または削除する。条項数、プロンプト量、判断点および実行コストは、制御成立後に測定する結果であり、設計前の制限にしない。

## 完了条件

1. ADR9 r2の全対象runがvalidかつScore `4`となる。
2. 各terminalが、期待するproducer、evidence、resultおよびdependency経路で成立する。
3. 未観測receiptの昇格、root代行、禁止情報配送、無関係なresultによる失効および危険なartifact変更が0件となる。
4. 過去の低頻度失敗に対応する高リスクケースの拡張試験を通過する。
5. Standard14互換試験で品質と既存機序を退行させない。
6. 保存済み基準resultとprompt identity以外の互換条件が一致し、比較前receiptが`ready`となる。
7. 評価、採用、releaseおよびprojectionを別ゲートとして保持する。

## 共通原則

- C147、C176または他Candidateを正解として固定しない。既存Candidateは成功経路、失敗経路および設計仮定を識別する診断証拠として使う。
- C147で成立した挙動を保持対象とするが、C147の定義または文章を逐語維持しない。
- C176で成立したreview admission、情報封鎖、具体的反例およびterminal判断を参考にするが、C176で残った観測result境界の失敗も修正対象とする。
- review要否、evidence充足、review result、terminalおよびartifact変更許可を同じ状態へ縮約しない。
- 全入力の列挙または分類を、terminalごとのdependency証明の代用にしない。
- 設計レビューは方向を成立不能にする具体的反例の確認に限定する。完全性は互換試験で検証する。
- validな低品質runを再実行で置き換えない。
- 拡張試験は結論を変え得るケースだけを選び、適格な既存atomic runを再利用する。

## M1: 過去結果の因果分析

### 目的

過去Candidateが狙った制御、設計時に置いた仮定、実際の結果、成立した部分および誤っていた部分を、Candidate固有の表現ではなく制御境界へ変換する。

### 成果物

- ADR01〜ADR09のterminal別証明責務
- 過去Candidateの設計意図と実結果の対応
- 繰り返し発生した失敗原因
- C147の保持・改訂・分割・削除候補

### 完了条件

- ADR01〜ADR09の全失敗を、有限閉包、具体的反例、反例なし、判断依存入力不足またはpermission否定へ分類できる。
- 原因不明またはCandidate名だけで表した失敗を残さない。
- 設計へ渡す未解決predicateと必要観測を列挙できる。

### 現在状態

`in_progress`

## M2: 制御構造の再設計

### 目的

C147の13条項を保持・改訂・分割・削除へ分類し、operation、predicate、evidence、producer、result、dependency、invalidation、terminalおよびartifact変更許可を一貫した責務構造へ再配置する。

### 完了条件

- 一つの状態遷移を複数条項が競合して所有しない。
- 各terminalの必要条件をCandidate名、case IDまたは期待terminalの参照なしに導出できる。
- evidence発行条件、観測resultの真正性、dependency、result失効およびterminal形成が区別されている。
- 実行方法の自由が独立観測resultの統合許可を意味しない。
- 条項数、追加量または総量を理由に必要な制御を削らない。

## M3: 設計方向の敵対的レビュー

### 目的

設計を成立不能にする一般的な具体的反例を確認する。表現改善、網羅性の追加または試験で判定可能な不確実性だけを理由に設計を循環させない。

### 完了条件

- 未解決のblocking counterexampleがない。
- 設計のtarget、permission、methodまたはstop conditionを変える指摘が残っていない。
- 残余リスクが試験predicateと対象ケースへ対応している。
- reviewの反復で当初の設計軸を増やしていない。

## M4: Candidate実装

### 目的

固定した設計をprompt bundleへ実装する。C147への追記だけに限定せず、必要な分割、統合、置換および削除を行う。

### 完了条件

- 設計predicateと実装箇所が一対一または明示された合成関係で対応する。
- 各責務の正本が一つで、旧定義との競合がない。
- bundle identity、manifest、構造試験および実装一致監査が成功する。
- Candidate、評価、採用、releaseおよびprojectionの状態が分離されている。

## M5: ADR9 r2互換N=5

### 目的

保存済みADR9 r2基準resultとprompt identity以外の条件を一致させ、再構成した制御の品質と機序を確認する。中核定義を広く変更する場合は9ケースすべて、変更効果が限定できる場合はその効果境界と必要な対照ケースだけを選ぶ。

### 実行前条件

- 基準resultを一意にbindする。
- case、fixture、TaskSpec、oracle、rating、model、reasoning、runtime、permission、executorおよびLayer 1を機械照合する。
- comparison preflightが`ready`になるまで一件も発行しない。
- 保存済みの互換なatomic runを基準側へ再利用し、Candidateの不足slotだけを発行する。

### 完了条件

- 発行対象が全件validかつScore `4`となる。
- caseごとのexpected terminal、reviewer cardinality、artifact変更可否、情報封鎖およびresult真正性が成立する。
- qualityまたはmechanism不一致が一件でもあれば結果を保持して停止し、M6以降へ進まない。

## M6: 高リスクケースの拡張

### 目的

N=5では検出しにくい低頻度失敗を、過去結果と変更内容から選んだケースだけで確認する。

### 対象選択

- ADR05: 具体的反例と無関係なmissingの分離
- ADR07: 必要観測完了後の`no_counterexample_found`
- ADR09: 判断依存入力不足とreview起動
- ADR01、ADR02: 有限固定効果とreview不要判定に変更が及ぶ場合
- その他: M5結果が追加観測で結論を変え得る場合だけ追加

### 完了条件

- 既存N=5を再利用し、不足分だけをN=20へ追加する。
- N=20で結論を変え得る低頻度リスクが残る場合だけN=50へ追加する。
- 全runでqualityとmechanismが成立する。
- 失敗runは再実行で置き換えず、原因分析へ戻す。

## M7: Standard14互換N=5

### 目的

ADR9拡張通過後、C147までに成立していた一般実行制御を退行させていないことを確認する。中核定義を再構成した場合はStandard14の14ケースすべてを対象とする。

### 完了条件

- 70 / 70 validかつScore `4`となる。
- 不要producer起動、terminal補完、context漏洩、検証順序違反、result効果の過剰伝播および危険なartifact変更がない。
- 不一致が一件でもあれば評価結果を保持して停止する。

## M8: 複雑性と効率の評価

### 目的

制御成立後に、実装の複雑性と実行コストを測る。これらをM2からM7までの設計制限または品質gateとして先行適用しない。

### 測定項目

- prompt総文字数、UTF-8 byte数およびC147からの差
- 条項数、predicate数、状態数および重複責務
- token中央値と経過時間中央値
- reviewおよびsubagent起動数
- evidence invocation数と失敗・recovery数

### 完了条件

- 品質・機序結果と複雑性・効率結果を分けて記録する。
- 圧縮または最適化が必要な場合は新しいprompt identityとし、影響する互換試験を再実施する。

## M9: 評価確定と採用判断

### 目的

品質、機序、安全性、効率および残余リスクを整理し、採用判断へ渡す。

### 完了条件

- 一次result、機序監査、比較artifactおよび設計との対応が揃っている。
- 評価済み、採用済み、release済みおよびprojection済みを混同していない。
- 採用、releaseまたはprojectionは利用者の明示判断なしに進めない。

## 停止と再開

- M1で原因不明の失敗が残る場合はM2へ進まない。
- M3でblocking counterexampleが成立した場合はM2へ戻る。
- M5、M6またはM7でquality・mechanism不一致を観測した場合は、そのrunを保持してM1の原因分析へ戻る。
- M8の複雑性または効率だけを理由に、成立済みの制御を失敗扱いにしない。
- 最適化でprompt identityを変更した場合は、影響する評価gateを未評価へ戻す。

## 現在位置

`M1_in_progress / candidate_not_created / evaluation_not_started / adoption_not_decided / release_not_created / projection_not_performed`
