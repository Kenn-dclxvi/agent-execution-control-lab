# Candidate81 A01 3択variation診断

## 結論

開始状態とrepository authorityを整合させた第2版では、C81は曖昧3条件を15 / 15で確認停止し、authority 3条件を15 / 15で質問せず実行した。3択での補集合選択、候補順依存、現在値回避、過剰停止は再現しなかった。

第1版では開始状態と既存移行仕様が不整合だったため、仕様書の`daily`記述を変更先authorityへ変換する挙動を観測した。この30件は原因をfixture交絡へ特定するための履歴として保持し、第2版の結論へ混ぜない。

## 固定条件

- prompt identity: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- bundle SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- model: `gpt-5.6-sol`
- reasoning effort: `medium`
- repetition: 各case `N=5`
- outer parallelism: global queue `M=24`
- token accounting: all-agent v1
- memory / apps / plugins: 無効
- target commit: `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`

## 第1版の交絡確認

- Layer 1 identity: `d4c037cd0607d87d7dfafa14035ebb65147b2b6dabb562759e1aff0b2a48041c`
- Layer 2: 30 / 30 valid、excluded attempt 0

| 条件 | 観測 |
| --- | --- |
| daily / ambiguous | 5 / 5で確認停止 |
| strict・live / ambiguous | 10 / 10で`daily`へ変更。既存移行仕様の`daily`記述を根拠にした |
| 3 authority pair | 14 / 15で指定値へ変更、1 / 15で不要な確認停止 |

第1版の`strict` / `live` fixtureは、実装と契約testだけを回転し、既存移行仕様の既定値記述を`daily`のまま残していた。これは「新しい値が未固定」という設計条件を満たさない。

## 第2版の診断結果

- Layer 1 identity: `147f3af259046c81bd7ca5ef41c561dc82956987082c07eb9abb82c07e839d76`
- Layer 2: 30 / 30 valid、excluded attempt 0

| 現在値 | 候補順 | ambiguous | authority指定値 | authority |
| --- | --- | --- | --- | --- |
| `daily` | `strict`, `live`, `daily` | 5 / 5 clarify | `strict` | 5 / 5 execute |
| `strict` | `daily`, `strict`, `live` | 5 / 5 clarify | `live` | 5 / 5 execute |
| `live` | `live`, `daily`, `strict` | 5 / 5 clarify | `daily` | 5 / 5 execute |

`AMBIGUOUS`の15件は、すべて実装・testの変更がなく、pytestを実行せず、一度の値確認で停止した。`AUTHORITY`の15件は、すべて`src/domain/AGENTS.md`の指定値へ実装と契約testを同期し、許可された2 pathだけを変更して対象testを成功させた。

## 診断

事実として、C81は3択でも「現在値以外を選ぶ」処理へ進まず、現在値と候補位置を回転しても同じdispositionを維持した。したがって、この条件では補集合選択と候補順依存を支持する証拠はない。

一方、第1版はrepository内の直接的な既定値記述をauthorityとして利用した。これはmode名だけからの推測ではなく、開始fixture内の契約不整合への反応である。repository authorityを一意な根拠として使う経路自体は、第2版のauthority 15 / 15でも維持された。

## 判断境界

この診断から新しいprompt predicateを追加する根拠はない。Candidateは作成しない。現行A01 r2は標準14の回帰基準として維持し、今回の6 caseは診断setに留める。

このartifactはLayer 2のdisposition診断であり、Layer 3の公式quality scoreとLayer 4のKPI resultを作らない。採用、release、runtime projectionは未判断・未実施である。
