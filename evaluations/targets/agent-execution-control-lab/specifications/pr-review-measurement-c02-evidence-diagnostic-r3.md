# Candidate170 C02診断の環境修復 r3

この仕様は、Candidate170の診断測定でモデル開始前に発生した転送漏れを修復し、同じPRR-C02/r2、同じprompt、同じモデル構成、同じ反復を再実行する条件を固定する。

## 修復範囲

- 失敗したGitHub Actions run `31299292912`の一次resultを保存する。
- review jobで必要な`pr_review_measurement_c02_evidence_scope.py`をmodel-visible packetへ追加する。
- workflow、Profile、preflight、Run Result schema、実行toolは新しいrevisionとして追加し、実行済みのr2 artifactを変更しない。
- Candidate170のprompt、fixture、review contract、rating contract、root SonnetとOpus関係レビュー役1人の構成、権限、診断項目は変更しない。

## 完了条件

新しいpacketに診断tool、Candidate170測定tool、collector依存、内容非保存hookが揃い、r3 preflightが固定した一件だけを発行できること。実行結果の品質、token、経過時間、証拠取得操作は新しいRun Resultへ記録し、r2の失敗結果とは別に保持する。

この修復は診断測定の実行環境だけを変更する。Candidate170の改善効果、fresh held-out効果、採用、release、本体反映を示さない。
