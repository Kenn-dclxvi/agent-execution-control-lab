# 情報封鎖review 文書課題 development r1

コード課題familyが情報封鎖効果を識別しなかった原因を受け、文書の意味整合を対象に再設計したdevelopment set。

- Evaluation set: `the-caption-information-closure-document-task-development-r1 / doc-dev-r1`
- ID01: 未実装のruntime自動切り詰めを文書が保証する欠陥。正解は`blocked`
- ID02: strict snapshot欠損時の明示許可fallbackを否定する欠陥。正解は`blocked`
- ID03: canonical SSOT pathと実採用sourceの分離を保つ正しい言い換え。正解は`completion_ready`
- 各pairは同一diff、同一TaskSpec、同一machine validationで、`prior_implementation_record`だけを変える
- C147、Medium、CLI 0.146.0、6 case × N=3、M=24

これは課題探索用であり、held-out、独立SA必要性、Candidateの証拠にしない。oracleが一意で、BがAより高精度となるpairがあるかを確認する。

実行結果: 18 / 18 valid。ID01、ID02、ID03はいずれもblind / context各3 / 3正解で差がなかった。コードとtestで裏付けられるproduct documentationは、今回の条件では情報封鎖効果を識別しなかった。
