# 工程2修正の採点経路 第4版

第1〜3版の採点補助は履歴として保持する。工程3再判定の対象は次の新しい経路である。

- [evidence_bridge_r4.py](evidence_bridge_r4.py)：開始入力と終了後の禁止操作を分離し、独立判定・内容証拠・必須検証を結ぶ。
- [execution_binding_r4.py](execution_binding_r4.py)：原文を保持した実行器と新採点経路の接続。
- [grader_r4.py](grader_r4.py)：成果と検証を分けた0〜4点の判定。
- [inspect_artifact_r4.py](inspect_artifact_r4.py)、[private_rating_checks_r4.py](private_rating_checks_r4.py)：各criterionの独立内容検査。
- [shell_rating_r4.py](shell_rating_r4.py)：起動先・引数・周辺routingの振る舞い検査。
- [web_rating_r4.py](web_rating_r4.py)：固定Node/cacheを使う描画と、環境障害の区別。
- [test_stage2_repair_r4.py](test_stage2_repair_r4.py)、[test_stage2_repair_supplement_r4.py](test_stage2_repair_supplement_r4.py)：指摘反例と修正影響の局所検査。

モデル試験は発行しない。[固定接続記録](../registrations/repair-binding-r4.json)と[修正文書](../../../../docs/standard14-dedicated-stage2-repair-r4.md)を参照する。
