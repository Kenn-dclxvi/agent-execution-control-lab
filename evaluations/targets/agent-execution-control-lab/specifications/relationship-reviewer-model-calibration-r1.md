# 関係レビュー役のモデル校正 r1

## 目的

Workflow Freeでrootだけがレビューした2回の観測を受け、複数pathと適用規則の関係を確認する役割を明示的に一つ置く。その役割のモデルだけをSonnetとOpusで切り替え、品質、全agent token、経過時間を各3回観測する。

## 固定するレビュー体制

- rootは`claude-sonnet-5`とし、入力の調査やfindingの再判定を行わない。
- rootは関係レビュー役を必ず1人だけ起動する。
- 関係レビュー役がread-only fixture toolを使い、PR metadata、changed paths、diff、適用規則、対象本文、review contractを確認する。
- 関係レビュー役は、複数pathの変更と適用規則の組み合わせを含めて4カテゴリを判定し、最終schema全体を返す。
- rootは関係レビュー役の構造化結果を変更せずに最終出力とする。

比較する条件は関係レビュー役のmodel aliasだけであり、`sonnet`と`opus`を各3回実行する。両条件でprompt template、root model、fixture、権限、Action revision、出力schema、採点、timeout、token accountingを一致させる。

## 測定と品質

正式KPIは`quality_score`、all-agent `total_tokens`、`elapsed_seconds`の3件である。subagent数、model routing、rootとsubagentのfixture accessは測定成立を確認する診断情報として保存する。

品質上のmissまたはfalse positiveだけでは後続反復を止めない。要求した関係レビュー役が1人でない、modelが一致しない、rootがfixture toolを使った、関係レビュー役がfixture toolを使わない、全agent tokenまたは経過時間が欠ける、といった場合は測定不成立として同じmodel条件の未発行反復を止める。

PRR-C01/r4は校正に使うためheld-out evidenceではない。この6回だけから一般的なモデル優劣や採用可否を決めない。
