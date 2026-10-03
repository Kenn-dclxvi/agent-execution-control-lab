# 小規模作業ケース

固定集合は14件のSTD14相当確認点と追加6件である。対応と観測できない範囲は[設計記録](../../../../docs/compact-repository-control-series-design.md)を参照する。

| ケース | 内容 | 本文 |
| --- | --- | --- |
| CRC-01 | 重複キーの排除 | [可視入力](core20-r1/CRC-01/visible/TASK.md)、[固定条件](core20-r1/CRC-01/case.json) |
| CRC-02 | 層をまたぐ日付の一致 | [可視入力](core20-r1/CRC-02/visible/TASK.md)、[固定条件](core20-r1/CRC-02/case.json) |
| CRC-03 | 保存と一時状態の解消 | [可視入力](core20-r1/CRC-03/visible/TASK.md)、[固定条件](core20-r1/CRC-03/case.json) |
| CRC-04 | 表示列の整合 | [可視入力](core20-r1/CRC-04/visible/TASK.md)、[固定条件](core20-r1/CRC-04/case.json) |
| CRC-05 | 結果に必要な単位の確認 | [可視入力](core20-r1/CRC-05/visible/TASK.md)、[固定条件](core20-r1/CRC-05/case.json) |
| CRC-06 | 本番操作の範囲外停止 | [可視入力](core20-r1/CRC-06/visible/TASK.md)、[固定条件](core20-r1/CRC-06/case.json) |
| CRC-07 | 空スナップショットの正しい扱い | [可視入力](core20-r1/CRC-07/visible/TASK.md)、[固定条件](core20-r1/CRC-07/case.json) |
| CRC-08 | 正本の実行入口 | [可視入力](core20-r1/CRC-08/visible/TASK.md)、[固定条件](core20-r1/CRC-08/case.json) |
| CRC-09 | 依存の宣言と固定版の対応 | [可視入力](core20-r1/CRC-09/visible/TASK.md)、[固定条件](core20-r1/CRC-09/case.json) |
| CRC-10 | CLIと参照文書の対応 | [可視入力](core20-r1/CRC-10/visible/TASK.md)、[固定条件](core20-r1/CRC-10/case.json) |
| CRC-11 | 入口の欠落を指摘するレビュー | [可視入力](core20-r1/CRC-11/visible/TASK.md)、[固定条件](core20-r1/CRC-11/case.json) |
| CRC-12 | 月次形式を検査するレビュー | [可視入力](core20-r1/CRC-12/visible/TASK.md)、[固定条件](core20-r1/CRC-12/case.json) |
| CRC-13 | 暗黙モードを推測しない | [可視入力](core20-r1/CRC-13/visible/TASK.md)、[固定条件](core20-r1/CRC-13/case.json) |
| CRC-14 | 解決できる方法は正本から選ぶ | [可視入力](core20-r1/CRC-14/visible/TASK.md)、[固定条件](core20-r1/CRC-14/case.json) |
| CRC-15 | 部分変更を完了にしない | [可視入力](core20-r1/CRC-15/visible/TASK.md)、[固定条件](core20-r1/CRC-15/case.json) |
| CRC-16 | 古い検証結果を流用しない | [可視入力](core20-r1/CRC-16/visible/TASK.md)、[固定条件](core20-r1/CRC-16/case.json) |
| CRC-17 | 具体的な反例と無関係な不足を区別する | [可視入力](core20-r1/CRC-17/visible/TASK.md)、[固定条件](core20-r1/CRC-17/case.json) |
| CRC-18 | 許可された情報だけを出力する | [可視入力](core20-r1/CRC-18/visible/TASK.md)、[固定条件](core20-r1/CRC-18/case.json) |
| CRC-19 | 失敗の影響を関係する成果へ限定する | [可視入力](core20-r1/CRC-19/visible/TASK.md)、[固定条件](core20-r1/CRC-19/case.json) |
| CRC-20 | 既存の対象外変更を保持する | [可視入力](core20-r1/CRC-20/visible/TASK.md)、[固定条件](core20-r1/CRC-20/case.json) |

## 実コードを使う独立試験

[CRC-A01-CODE r3](latent-mode-code/r3/case.json)は、日次と再計算・監査の用途、日付別入力固定、取得元と正本、台帳利用側の既定値依存を戻した専用素材。[見直し記録](../../../../docs/compact-latent-mode-r3-redesign.md)と[局所検証](../registrations/latent-mode-code-source-freeze-r3.json)を参照する。モデル未測定で、r2は保持する。

[CRC-A01-CODE r2](latent-mode-code/r2/case.json)は、呼出しへの既定値伝播とstrictの例外条件を戻した別版。[専用集合r2](../sets/latent-mode-code-r2.json)へ固定し、r1の結果は保持する。

[CRC-A01-CODE r1](latent-mode-code/r1/case.json)は、変更後modeが未指定のまま試験へ進む誤経路を、実行可能な取得処理・仕様・既存テストで測る。core20の集合へ追加せず、[専用の一件集合](../sets/latent-mode-code-r1.json)へ固定する。

[CRC-A01-CODE r4](latent-mode-code/r4/case.json)は、コードとテストをr3のまま保持した依頼文の関係だけの診断。[設計と条件](../../../../docs/compact-latent-mode-task-r4-diagnostic.md)を参照する。旧試験の代替としては未採用。
