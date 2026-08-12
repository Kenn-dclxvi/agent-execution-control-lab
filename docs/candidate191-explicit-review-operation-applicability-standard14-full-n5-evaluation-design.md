# Candidate191 Standard14全14ケース N=5評価設計

> **位置づけ**: M7一般制御退行確認／Standard14全14ケース／各N=5

## 結論

Candidate191で中核定義を再構成したため、Standard14の14ケースすべてを各5件で確認する。Candidate176の保存済みStandard14 N=5 resultを比較基準へ一意にbindし、prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor条件およびLayer 1を維持する。

Candidate191の限定Standard14で取得済みのF02、F03、F04各5件は同じ互換条件を満たすため再利用する。他の11ケースだけを各5件、合計55件追加する。TPOまたは別比較系列は追加しない。

## 固定identity

- profile: `candidate191-explicit-review-operation-applicability-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- prompt: `the-caption-3ce91a4-explicit-review-operation-applicability-r1`
- bundle SHA-256: `6ff3f31585185ca2f08fd63eb19e4d75156425aecc1e1a6da63753768b24a163`
- evaluation set: `the-caption-standard14-r1/r1`
- reference result: `a0702207f03a4cb18c8b501329b74023`
- coverage: 14ケース各5件、合計70件
- reuse: F02、F03、F04の15件
- new slots: 他11ケースの55件
- max workers: `24`

## 完了条件

1. 累積70 / 70 validかつScore `4 = 70`となる。
2. caseごとのrequired outcome、許可されたartifact変更、required validationおよびterminalが成立する。
3. 不要producer起動、terminal補完、context漏洩、検証順序違反、result効果の過剰伝播および危険なartifact変更がない。
4. qualityまたはmechanism不一致が一件でもあればresultを保持して停止し、採用、releaseまたはprojectionへ進まない。

複雑性と効率はM8で測定し、本gateの先行制約または品質判定へ使わない。

## 状態

`candidate191_standard14_design_fixed / all_fourteen_cases / reuse_15 / issue_55_only / no_TPO_series`
