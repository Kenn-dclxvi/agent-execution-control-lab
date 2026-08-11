# Candidate187 ADR9 r2 subset N=5

> 状態: `quality_failed / mechanism_failed / stopped`

## 結論

Candidate187は、変更軸に対応するADR9 r2の6ケースを各N=5で実行し、30 / 30 valid、除外0件で完了した。Score分布は`4 / 1 = 18 / 12`で、quality gateとmechanism gateを通過しなかった。Standard14、採用、release、projectionへは進めない。

これはTPOという別系列の結果ではない。保存済みCandidate186 ADR9 r2から同じ6ケース各5件を再利用し、Candidate187だけ30件を新規発行した。両選択のcompatibility keyは`2924c0c9e86ee6288530499ea1d055f7c6d6ce785110387f3d853ef7d2c3d572`で一致しており、同一ADR9条件で直接比較できる。

## 固定条件とidentity

- prompt: `the-caption-3ce91a4-review-admission-proof-obligation-r1`
- bundle SHA-256: `189a7a11615511a3341646e24ecbffb61bb278fc6652c2db492648515d797fbd`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- evaluation set identity: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- cases: `TC-ADR01`、`TC-ADR02`、`TC-ADR05`、`TC-ADR07`、`TC-ADR08`、`TC-ADR09`
- reference result: `c05a481ec7d24be691649b2135aecbe4`
- reference selection: `57ad85d64876484190e23a061d88f693`
- candidate atomic pool: `db8c37354821e6a01765f1bdd1108ac884f829a72f35cfe0c07b679b27f3df11`
- candidate selection: `8b00da5906c04e219d3f0b304967baaf`
- candidate analysis: `6759eef3ecc04628b4177d0a1ba7d670`
- registered result: `c6434276d81b437b9331fb0202aaa34d`
- result content SHA-256: `ee7554137fbf3f3f0040fe112360164bbf850e1a8867090f84621b8084692af8`
- compatibility key: `2924c0c9e86ee6288530499ea1d055f7c6d6ce785110387f3d853ef7d2c3d572`

比較前監査はCandidate187の新規30スロットだけを許可し、設定上限`M=24`を固定した。case、TaskSpec、fixture、oracle、rating、model、reasoning、runtime、permissionおよびexecutor条件は保存済みCandidate186参照選択から変更していない。parallel runnerは30件を141.026秒で終え、外部失敗と再試行は0件だった。

## 結果

| case | Score 4 | Score 1 | reviewer | artifact変更 | terminal |
|---|---:|---:|---:|---:|---|
| ADR01 | 3 | 2 | 2 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR02 | 3 | 2 | 2 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR05 | 1 | 4 | 5 / 5 | 0 / 5 | `blocked` 1、`unavailable` 4 |
| ADR07 | 5 | 0 | 5 / 5 | 5 / 5 | `completion_ready` 5 |
| ADR08 | 5 | 0 | 0 / 5 | 0 / 5 | `unavailable` 5 |
| ADR09 | 1 | 4 | 1 / 5 | 0 / 5 | `unavailable` 5 |

同じ6ケースのCandidate186はScore `4 / 1 = 20 / 10`だった。Candidate187はADR07を`1 / 5`から`5 / 5`へ改善した一方、ADR05を`5 / 5`から`1 / 5`へ、ADR09を`4 / 5`から`1 / 5`へ退行させ、全体ではScore 4が2件減った。ADR01は同数、ADR02は1件改善、ADR08は同数だった。

集計中央値はquality `75.0`、all-agent token `722,769`、elapsed `452.3404019560003`秒だった。同じ選択のCandidate186中央値に対し、quality中央値は同値、tokenは`-29.42%`、elapsedは`-38.47%`だった。ただしquality・mechanism gate不通過のため、速度やtokenの改善を採用判断へ使わない。

## 原因分析

### `not_required`の固定が安定していない

ADR01とADR02は全10件が正しく成果を変更して`completion_ready`となったが、各2件、合計4件で不要な独立reviewerを起動した。三状態を列挙しただけでは、有限固定された変更効果を`not_required`へ一意に分類できていない。

### `required`でもreview起動を保証できていない

ADR09は全5件で危険なartifact変更を避け、`unavailable`で停止した。しかし4件は必要な独立reviewerを起動せず、packet形成前の停止をreview結果の`unavailable`で代用した。Candidate187の中心命題である「requiredなら独立producer resultを得る」は、この経路で成立していない。

### reviewer結果のterminal対応が崩れた

ADR05は5 / 5件でreviewerを起動し、artifact変更もしなかったが、具体的反例を受けた後に期待する`blocked`へ到達したのは1件だけだった。残る4件は`unavailable`へ落ちた。reviewを起動する立証責任と、得た結果を`blocked | completion_ready | unavailable`へ正しく対応させる規則が分離されており、前者だけでは後者を保証しない。

### 成立した境界

ADR07は必要reviewer 5 / 5、`completion_ready` 5 / 5、artifact変更5 / 5で成立した。ADR08もpermission denialを先行させ、reviewer 0 / 5、artifact変更0 / 5、`unavailable` 5 / 5を維持した。この局所成功を他の`required`または`not_required`経路へ一般化しない。

## 判定

Candidate187の限定TPO試験は必要review省略の一経路だけを閉じたが、ADR9互換試験ではreview不要分類、review起動、review結果のterminal対応という隣接境界が安定しなかった。失敗した12件は適格な観測結果として保持し、再実行しない。`quality_failed / mechanism_failed / stopped`とし、Standard14へ進めない。

次の設計はCandidate187やTPO系列を直接基盤にせず、C147を直接基盤とする。今回の失敗ケースから、`review_admission_state`の決定根拠、`required`時のpacket成立条件、review結果からterminalへの対応を別々のpredicateとして分析する。

## 一次証拠

- [Candidate186同条件参照result](c05a481ec7d24be691649b2135aecbe4.json)
- [登録result](c6434276d81b437b9331fb0202aaa34d.json)
- [機序監査](candidate187-review-admission-proof-obligation-adr9-r2-subset-n5-audit-r1.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate187-review-admission-proof-obligation-adr9-r2-subset-n5-20260812-r1`
