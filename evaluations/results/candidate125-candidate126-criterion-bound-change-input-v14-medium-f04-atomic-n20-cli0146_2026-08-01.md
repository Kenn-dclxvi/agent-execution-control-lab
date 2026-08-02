# Candidate125 / Candidate126 criterion-bound change input targeted結果

## 結論

Candidate126の正式な初段判定をF04 N=5へ訂正した。互換poolから固定した5件はすべてvalidで、score分布は`4 / 2 = 3 / 2`だった。score `2`が一件以上あるため停止する。F02 / F07 preservation、Standard14、採用、release、本体投影へ進めない。

N=5では`colSpan`変更と観測していないstale operandは0 / 5だった。一方、2件が`change_input_ready`を満たせないとして正しい`hasAuditKey`変更も行わず、required Node validationを未実施で停止した。制御は誤patchを減らしたが、false stopを増やしたため採用できない。

実行時には初段を誤ってN=20で発行した。20件は削除せず追加証拠として保持するが、段階判定の正本はN=5 selectionとする。追加15件を含む全体分布は`4 / 2 = 12 / 8`で、N=5と同じ停止判断だった。

## 比較identityとpreflight

- candidate: `the-caption-3ce91a4-criterion-bound-change-input-r1`
- bundle SHA-256: `aab0d8ce078e3c164668ca3121afd82d3f8d3996ec37af3c2006fe0a031d1a7c`
- direct parent: Candidate125
- changed target: root `AGENTS.md`
- changed predicate: `change_input_ready`
- evaluation set: `the-caption-standard14-r1` revision `r1`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` revision `r2`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- configured max workers: `M=24`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- Candidate126 pool key: `a1dbcdede93f7a9077fdf0223089b353e820dd69a2b1e8e863eabacf32da8300`

Candidate125のcompatible F04 poolから既存20 runを選択し、selection `cafd06418e98489189ec46e68af29343`、reference result `dcabb19acdac4338b5cf4265d64af616`へ固定した。基準runは再実行していない。Candidate126の20 slotはprompt identity以外を機械照合した`comparison-preflight.json`の後に発行した。ただし、初段をN=5にすべきところN=20を一括発行した点は運用上の逸脱である。

## Quality結果

初段N=5 selectionは`03b6629063e840199033d2a59676ac45`、analysisは`6a4222174a574eb0b2f7d6b6d0ef5e34`である。

| score | run数 | 比率 |
|---:|---:|---:|
| 4 | 3 | 60% |
| 2 | 2 | 40% |
| total | 5 | 100% |

N=5のscore `2` 2件は、required changed path `App.tsx`なし、`npm ci`・lint・build未実施という同じfailure集合だった。token中央値は`150,947`、elapsed中央値は`89.215秒`である。失敗runが早期停止しているため、このcostを効率改善として解釈しない。

以下は先に発行してしまったN=20全体の追加証拠である。

| score | run数 | 比率 |
|---:|---:|---:|
| 4 | 12 | 60% |
| 2 | 8 | 40% |
| total | 20 | 100% |

score `2`の8件はすべて同じfailure集合だった。

- required changed path `App.tsx`なし: 8
- `npm ci`未実施: 8
- lint未実施: 8
- build未実施: 8

20 runはすべてatomic registryへ登録した。N=20 selection IDは`b793f34ffcc04b9abbc19f0456fb8d2c`、analysis IDは`bc3148ba9c7c4d3c9e3fe3778d7d6fdd`である。all-run token中央値は`144,506`、elapsed中央値は`97.013秒`だった。

## Mechanism結果

| mechanism | 結果 | gate |
|---|---:|---|
| 必要な`hasAuditKey`変更 | 3 / 5 | fail |
| 最初のartifact変更operationで適用成功 | 3 / 5 | fail |
| artifact変更なし | 2 / 5 | fail |
| `colSpan`変更 | 0 / 5 | pass |
| stale current-content operand | 0 / 5 | pass |

N=5の成功3件の最終diffは、`hasAuditKey = true`を`funds.some(...)`へ変える一hunkだけだった。`colSpan`、`py-20`、他pathは変更していない。N=20全体では同じ成功が12件、artifact変更なしが8件だった。

N=20の失敗8件のうち少なくとも5件は、continuation resultの出力切詰めにより現在の`colSpan`を確認できないことを理由に停止した。残る3件もheaderとrowの条件表示または`hasAuditKey = true`までは観測したが、artifact変更とvalidationへ進まなかった。

## 原因解釈

`change_input_ready`は本来、実際に発行する変更単位のcurrent-content operandだけをexact bindする意図だった。しかし保存traceでは、modelが開始状態ですでに充足しているF04-C2も変更前に完全再確認しなければならない条件として読んだ。

その結果、不要なhunkを推測するC125の誤経路は消えたが、output truncation時に必要なF04-C1まで止める別の誤経路へ移った。新predicateが選択肢を減らすだけでなく、開始状態の全criterionを再監査する新しい判断を増やしたことが原因である。

## 停止判断

初段N=5で設計時の停止条件であるscore `3`以下、必要変更の抑止、false stopが一件以上発生した。よって現在状態を`targeted_f04_n5_evaluated / n20_overexecuted_evidence_preserved / quality_gate_failed / stale_hunk_suppressed / required_edit_suppressed / false_stop_regressed / result_registered / stopped`とする。

F02 / F07 N=5、Standard14、B20、採用、release、本体投影は未実施である。同じ`change_input_ready`の語句を微修正した次Candidateは、この結果だけから直ちに作成しない。
