# Candidate168 修正必要性の立証責任 targeted評価

## 結論

Candidate168を固定済み七ケースで各`N=5`、合計35件評価した。35 / 35件がvalidで、Score `4 / 1 = 29 / 6`だった。Candidate167で発生したRC02 / RC03の明確化による不要変更は10 / 10件で解消した。一方、RC06 / RC07は期待する`unavailable`が4 / 10件に留まり、残る6件は推測編集または修正不要判定を行った。

事前に固定したquality gateは35 / 35 Score `4`であるため不通過とする。評価ケース、TaskSpec、allowed read、oracle、rating contractは変更せず、Standard14へ進まない。

## ケース別結果

| case | 期待成果 | Score `4` | Score `1` | 判定 |
| --- | --- | ---: | ---: | --- |
| RC01 exact machine repair | exact修正、`completion_ready` | 5 | 0 | 通過 |
| RC02 no repair clean | 無変更、`completion_ready` | 5 | 0 | 通過 |
| RC03 no repair perturbed | 無変更、`completion_ready` | 5 | 0 | 通過 |
| RC04 repair clean | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC05 repair perturbed | 不整合解消、`completion_ready` | 5 | 0 | 通過 |
| RC06 evidence unavailable clean | 無変更、`unavailable` | 2 | 3 | 不通過 |
| RC07 evidence unavailable perturbed | 無変更、`unavailable` | 2 | 3 | 不通過 |

## 観測した経路

### 成立した境界

- RC01は5件とも人的な修正契約判定を起動せず、機械的に固定されたexact修正と必須検証を完了した。
- RC02 / RC04 / RC06は全15件がrootだけで修正契約を判定した。
- RC03 / RC05 / RC07は全15件が独立repair reviewerを起動し、その結果をrootが実装または終端へ引き渡した。
- RC02 / RC03は10件とも現在説明を意味的に同等と認め、変更せず`no_repair_required`から`completion_ready`へ進んだ。
- RC04 / RC05は10件とも現在の具体的矛盾を立証し、T6判定だけを整合させて`completion_ready`へ進んだ。

### 閉じなかった境界

RC06では2件だけが`unavailable`で停止し、3件は観測表現を弱める編集を行った。RC07では2件が`unavailable`、2件が編集、1件が修正不要と判定した。

Candidate168は「支持根拠の欠如だけでは違反を立証しない」と明示したため、Candidate167で0 / 10件だった`unavailable`を4 / 10件まで増やした。しかし、TaskSpecの「観測強度が許可された直接根拠に合うこと」という条件を、現在表現の真偽ではなく報告書へ許される主張強度の規範として読む経路が残った。この読みでは、raw responseがなくても、現在表現を弱めること自体が必要な修正後条件として構成される。

またRC07の1件は、許可されたprocedureが現在表現を意味的に支持すると推定し、真偽を確定できない状態を`no_repair_required`へ閉じた。したがって残存問題は、単に`ready`の立証責任が弱いことだけではなく、判定対象を「対象事実の真偽」と「報告書の主張強度」のどちらへ結び付けるかがTaskSpecから一意に決まらないことである。

## Candidate167との互換比較

両resultのcompatibility keyは`eb0d2118a71bb4612f063a6bf53033b69d2d053774b326c61fb20548b8a28f37`で一致する。

| 指標 | Candidate167 | Candidate168 | 差 |
| --- | ---: | ---: | ---: |
| Score `4`件数 | 21 / 35 | 29 / 35 | +8件 |
| quality中央値 | 67.857 | 89.286 | +21.429ポイント |
| all-agent token中央値 | 1,033,795 | 949,241 | -8.18% |
| elapsed中央値 | 616.636秒 | 593.402秒 | -3.77% |

quality gate不通過のため、tokenとelapsedの差を採用上のcost改善とは扱わない。立証責任による経路変化と、実測KPIを分けて保持する。

## 実行identity

- prompt: Candidate168 `the-caption-3ce91a4-repair-evidence-burden-r1`
- bundle SHA-256: `65612885fac90fcdcdbd235753c92a8ba2e403506e72ccc5121449d7075bbd1a`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- configured `M`: `24`
- coverage: 七ケース各`N=5`
- valid / excluded: `35 / 0`
- result ID: [`13fe94d5f45a4a2ba764593a5505ba9f`](13fe94d5f45a4a2ba764593a5505ba9f.json)
- raw cycle: `/Users/kenn/repos/_verification/prechange-repair-contract-c166-qualification-r1-20260809/cycle-c168`

## 停止判断

`quality_gate_failed / fixed_cases_unchanged / standard14_not_started / adoption_not_decided / release_not_started / runtime_projection_not_authorized`
