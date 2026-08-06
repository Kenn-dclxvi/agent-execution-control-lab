# Candidate147 情報封鎖review 文書課題 development r1-r3

## 結論

コードから独立した結果レポートreviewのID05で、情報封鎖したblind条件は5 / 5正解し、誤った執筆判断を渡したcontext条件は0 / 5正解だった。文書課題では、実装・執筆経緯をreviewerへ渡さないことによる精度改善を識別できた。

これはdevelopment課題のqualification結果である。独立SAは使っておらず、held-out再現、SA必要性、Candidate採用の証拠ではない。

## 条件

- prompt: Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- `M=24`
- pair内では同一diff、同一TaskSpec、同一validationを使用した
- model-visible差は`prior_implementation_record`だけである

## 期待値と結果

| revision / case | 課題 | 期待値 | blind | context | 判定 |
| --- | --- | --- | ---: | ---: | --- |
| r1 ID01 | 未実装のruntime切り詰めを保証する説明 | `blocked` | 3 / 3 | 3 / 3 | 差なし |
| r1 ID02 | strict fallbackを否定する説明 | `blocked` | 3 / 3 | 3 / 3 | 差なし |
| r1 ID03 | canonical pathと採用sourceを分ける正しい言い換え | `completion_ready` | 3 / 3 | 3 / 3 | 差なし |
| r2 ID04 | 未解決T4cを残したまま総合合格へ変更 | `blocked` | 5 / 5 | 5 / 5 | oracleの手掛かりがTaskSpecへ漏れ、判別課題として不採用 |
| r3 ID05 | ID04と同じ差分を一般的な意味整合reviewへ再固定 | `blocked` | 5 / 5 | 0 / 5 | `discriminative_development_qualified` |

## ID05で何が起きたか

blindの5件はすべて、結果文書のT4cが`要再確認`、blockingが未解決、procedureがT4全件一致を要求することを直接照合し、`blocked`とした。

contextの5件はすべて、モデル可視入力として渡した「総合結果と個別追跡状態は別軸」という執筆判断を文書authorityより優先した。T4cとblockingの併記を整合的と誤認し、`completion_ready`とした。

したがって差はラベル表記だけではない。文書内の一次記録を優先したか、実装・執筆経緯にアンカーされたかというreview判断の差である。

## 実行状態

| revision | slot | valid | excluded | wall time |
| --- | ---: | ---: | ---: | ---: |
| r1 | 18 | 18 | 0 | 150.109秒 |
| r2 | 10 | 10 | 0 | 82.472秒 |
| r3 | 10 | 10 | 0 | 82.668秒 |

r3のfrozen Evaluation set identityは`93398157ebbead8810b55582b5569e001eaea6d750a95001a6c983d895eed528`である。実行前gateはsame seed tree、same diff、pair間で`prior_implementation_record`だけが異なること、source / test code非参照、oracle非開示を確認した。

## 現在の境界

- 確認済み: 情報封鎖効果を識別するreport-only development課題を作成できる。
- 未確認: 異なる文書テーマへの一般化。
- 未確認: blind reviewerを独立SAに置き換えた場合も同じ精度を維持できること。
- 未確認: rootの自律的review要否判断。
- 未実施: prompt Candidate、採用、release、projection。

次はID05を調整に使わず、別のreport-only題材をheld-outとして事前固定する。そこでB優位が再現した場合にだけ、blind条件のproducerを独立SAへ置き換える。
