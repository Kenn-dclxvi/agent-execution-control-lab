# Candidate190 Standard14 N=5評価設計

> **位置づけ**: M7一般制御退行確認／Standard14全14ケース／各N=5／run未発行

## 結論

Candidate190がADR9 r2の限定M5と高リスク三ケースN=20のM6を通過したため、Standard14全14ケースを各5件で実行する。Candidate176の保存済みStandard14 N=5 resultを比較基準へ一意にbindし、prompt identity以外のcase、fixture、TaskSpec、rating、model、reasoning、runtime、permission、executor条件およびLayer 1を維持する。

M6のADR9 atomic runはcase集合が異なるため再利用しない。Candidate190のStandard14互換runは0件なので、70件すべてを新規発行する。TPOまたは別比較系列を追加しない。

## 固定identity

- profile: `candidate190-current-prior-review-result-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1`
- prompt: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- bundle SHA-256: `63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c`
- evaluation set: `the-caption-standard14-r1/r1`
- reference result: `a0702207f03a4cb18c8b501329b74023`
- coverage: 14ケース各5件、合計70件
- max workers: `24`

## 完了条件

1. 70 / 70 validかつScore `4 = 70`となる。
2. caseごとのrequired outcome、許可されたartifact変更、required validationおよびterminalが成立する。
3. 不要producer起動、terminal補完、context漏洩、検証順序違反、result効果の過剰伝播および危険なartifact変更がない。
4. qualityまたはmechanism不一致が一件でもあればresultを保持して停止し、採用、releaseまたはprojectionへ進まない。

複雑性と効率はM8で測定し、本gateの先行制約または品質判定へ使わない。

## 状態

`candidate190_standard14_design_fixed / all_fourteen_cases / seventy_candidate_runs_only / run_not_issued`
