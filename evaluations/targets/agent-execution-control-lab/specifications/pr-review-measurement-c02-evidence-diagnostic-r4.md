# Candidate170 C02診断のcollector修復 r4

この仕様は、Candidate170の診断測定でモデル実行後に発生したcollectorの循環importを修復し、同じPRR-C02/r2、同じprompt、同じモデル構成、同じ反復を再実行する条件を固定する。

## 修復範囲

- GitHub Actions run `31299704268`の一次resultを保存する。
- model-visible packet内の`pr_review_measurement_c02_evidence_diagnostic.py`を基底collectorの正しい内容で固定する。
- packet内から回復toolのCLIを実際に起動する試験を追加する。
- workflow、Profile、preflight、Run Result schema、実行toolは新しいrevisionとして追加し、実行済みのr2とr3 artifactを変更しない。
- Candidate170のprompt、fixture、review contract、rating contract、root SonnetとOpus関係レビュー役1人の構成、権限、診断項目は変更しない。

## 完了条件

新しいpacket内で回復toolが循環importなしに起動し、レビュー出力、実行記録、hook記録をsanitized resultへ収集できること。その後の採点結果は新しいRun Resultへ記録し、先行する二件の失敗resultとは別に保持する。

この修復は診断測定の実行環境だけを変更する。Candidate170の改善効果、fresh held-out効果、採用、release、本体反映を示さない。
