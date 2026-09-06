# Candidate274: 実行境界を保持したC147の再構成

## 目的と実行仕様

利用者が承認した方針は、C147を直接の親とし、成果確定・探索制限・検証の完了境界を原文で残し、委任・役割管理の細部だけを削ることである。対象は`the-caption`系列、変更対象はroot `AGENTS.md`だけ。非rootの18対象とsource identityを保持する。C273は失敗反例と補助比較の位置づけであり、直接の親にしない。

本作業の実行者は設計、作成、整合確認、実行前照合、計測、採点、集計のすべてでroot。条件所有者は利用者要求と適用中のリポジトリ指示。成果条件は新しい完全バンドルと、同一Astra medium条件の6ケース各N=5結果の保存である。評価中のprompt変更、評価基盤変更、採点変更、既存の履歴・未コミット作業の変更は許可しない。採用・release・本体反映は別判断とする。

## 作成前の確認

1. **基準と最短正常経路**: 制御なし出発点は`the-caption-3ce91a4-control-free-repository-r1`、直接親・原文・主比較相手はC147 `the-caption-3ce91a4-result-effect-scope-r1`、bundle `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc`。要求成果が未確定なら確認し、成果が確定していれば正本と対象から実装を決め、必要変更、検証、結果の確認を完遂する。
2. **具体的な問題経路**: [C273の保存60run診断](candidate273-astra-n5-token-increase-causal-audit.md)で、F01・F02・F04の変更後外側呼び出しがC147の1回からC273の5〜9回へ増えた。C273 F01 `220b7f9ccdcb4f4b87143f8cc3e65f68`ではfocused pytest・待機・full gate・待機・待機・最終確認を別々に発行した。必須試験自体の回数は変わらず、履歴入力の反復が増加した。初回変更後の区間は全トークン増分の92.47%を占めた。
3. **許可と依存関係**: TaskSpecの必須試験・順序とrepository authorityだけでは、途中結果を受領してモデルが次の試験や待機を発行することを禁止しない。C147の`VALIDATION_CLOSURE`と`VALIDATION_PLAN`は、この返却・再開境界を閉じる。開始identityの結果が影響しないreadまで別判断へ分離する経路は`DECISION_BOUNDARY`が閉じる。これらを逐語保持する。
4. **全変更集合**: C147の13条項から`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`だけを削除し、残る9条項は順序も含め逐語保持する。`SPEC`、`PRODUCER`、`TERMINAL`、`EVIDENCE_GATE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`を残す。復旧は委任管理ではないため削らない。新しい条件、例外、ラベル、参照は追加しない。
5. **再構成の因果関係**: パケット項目・継承量指定、起動名称と返却者の細かな照合、rootの役割の再記述、先行成果に対する独立条項を一つの委任管理群として削る。成果条件・実行者・確定結果の最小の対応は`SPEC`・`PRODUCER`・`TERMINAL`に残る。この群を削って中心の実行境界が維持できるかを測る一つの再構成であり、削除した各条項の独立効果を実証済みとは扱わない。
6. **維持する正常経路**: 必要情報はTaskSpec、許可された対象、適用指示、正本から当該操作の実行者へ届く。必要な検証は個別のコマンドとして実行し、失敗時は後続を止め、未終了なら完了を待つ。結果欠落を推測で補わない。明示された別実行者の指定は`PRODUCER`に残る。パケットの詳細項目を削除しても、情報を読む許可を新たに追加しない。runtimeやadapterの変更は必要ない。
7. **新しい判断と対象外への影響**: 追加条件は0。委任入力の作り方と結果照合の細部には裁量が戻るため、委任を含む経路の品質維持は未検証と明記する。初回6ケースはこの群の全面的な安全性を証明しない。必要な正常情報まで遮断する新しい規則は作らない。
8. **評価条件と診断**: Astra `gpt-6-astra`、reasoning `medium`、CLI `0.153.3`、Python `3.14.5`、Rating v14、全エージェントtoken accounting v1、max_workers 24。C273と同じA01 r2・A02 r2・F01 r3・F02 r1・F04 r2・F07 dependency r1を各N=5、期待Score分布は4が30件、3以下0件。C147 Astra元result `654d171e89a547d9af421ec9ee05ad96`から既に選択済みの同6ケース結果と固定Layer 1を再利用し、非prompt条件の一致を正式receiptで確認してから発行する。C273 `4c15af38e95849db803ed0e6b2abbede`は互換する補助比較とする。推論回数・変更後呼び出し・待機・子エージェントusageは原因診断に限定する。
9. **停止条件**: 実行前に不一致・未確認があれば発行0で停止。invalid、採点不能、Score 3以下では拡張しない。同一6ケースN=5のselection合計中央値でC147比total_tokensとelapsed_secondsがともに減少した場合のみコスト改善方向とする。増加許容幅は0、同値は改善未確認。いずれかが増えれば拡張を止める。経路だけを独立した停止条件にしない。初回通過後のStandard14と追加Nは別段階とし、本作業では6ケースN=5までを実施する。

## 条項間の依存確認

`EVIDENCE_GATE`が参照する`VALIDATION_PLAN`、同節が参照する`METHOD`、検証と完了が使う実行者・状態の定義は残る。削除する4条項のラベルを残存本文が参照していないことを作成時に確認する。C273の限定版`VALIDATION_PLAN`は使わず、C147の全文を使う。実行票の具体コマンドや待機回数を成功runから転記せず、C147が既に持つ許可・依存境界を維持する。

## 状態

作成前設計を先に固定した。評価状態は独立resultへ記録する。C147原文の9条項を残すこと自体を、品質・効率の改善または採用の根拠にはしない。

## 実行前照合

C147の同6ケースの基準result `2c5c5b8c1576471b81f2c05947a92a08`に対し、`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`を通過した。C273で修正済みの固定set・全fixtureの複製を再利用し、6ケースcoverageを正規経路で固定した。

- [実行プロファイル](../evaluations/profiles/candidate274-execution-boundary-core-v14-medium-six-case-astra-m24-n5-cli0153-r1.json)
- Candidate274 pool: `528e1500ee26121a69e72c12a7b121456762717510d52287f1b4d2e26fa7e458`
- bundle SHA-256: `7454c6921e60db3334d8308b9cc016833a6a8588bc2ca4c275d78197780e4e66`
- 生証跡の保存先: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate274-v14-medium-six-case-astra-n5-cli0153-20260905-r1`

CLIは固定aliasの絶対パス・バンドルhashを照合し、各runに固定された経路のみを用いる。C147と非prompt条件を変更せず、不足30件だけを発行する。

## 初回計測結果への導線

[6ケースN=5の一次結果](../evaluations/results/candidate274-c147-astra-medium-six-case-n5_2026-09-05.md)に記録した。30 / 30 Score 4、C273比の大幅増加は解消。C147比トークン+0.80%のため事前コスト条件は不通過であり、追加評価は行わない。
