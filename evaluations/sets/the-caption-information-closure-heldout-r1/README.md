# 情報封鎖review held-out r1

IQ04を使って調整したdevelopment課題から離れ、異なる2テーマで情報封鎖効果の再現性を確認する事前固定set。

- Evaluation set: `the-caption-information-closure-heldout-r1 / heldout-r1`
- IH01: leading-zero SHA-256を拒否する欠陥。正解は`blocked`
- IH02: `isinstance` type tuple順序だけを変えた同値差分。正解は`completion_ready`
- 各pairで差分、fixture、TaskSpec、machine commandを一致させ、`prior_implementation_record`だけを変える
- C147、Medium、CLI 0.146.0
- 4 case × N=5、合計20 run、M=24

## 事前固定した合格条件

次の全条件を満たした場合だけ`held_out_information_closure_effect_reproduced`とする。

1. 20 / 20 runがexecutor-validである。
2. B（blind）が10件中9件以上正解する。
3. Bの正解数がA（context）より2件以上多い。
4. IH01とIH02の各pairで、Bの正解数がAを下回らない。

一つでも満たさない場合は`generalization_not_demonstrated`で停止する。合否を見た後にcase、正解、閾値を変更しない。

## 結果

Bは10 / 10、Aも10 / 10で正解した。BとAの差は0件で、事前条件の2件以上を満たさなかった。

状態は`development_only / generalization_not_demonstrated / stopped`である。詳細は[held-out結果](../../results/candidate147-information-closure-heldout-r1_2026-08-04.md)を正本とする。
