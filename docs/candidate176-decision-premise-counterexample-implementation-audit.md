# Candidate176 判断前提反証経路の実装監査

## 結論

Candidate176の修正版について、一般修正を必要とする具体的反例は確認されなかった。変更していないADR9 r2の初回評価へ進める。

## 初回監査の反例

初回実装では、複数の事実根拠を同一具体instanceへ結び付けるための`support_identity`の一意性が、設計にはある一方で実装promptの成立条件から欠落していた。また、manifestのroot `AGENTS.md`に記録したGit blob identityと、親Candidateのprovenanceが実体に一致していなかった。

`decision_premise_counterexample_established`へ、全`fact_support`が一意な`support_identity`を持ち、複数根拠を使う場合は同一具体instanceへの対応関係を明示する条件を追加した。manifestはCandidate175を直接親とするprovenanceと実体から再生成したidentityへ修正した。

## 再監査

修正版の再監査は`no_counterexample_found`だった。次を確認した。

- 判断前提は、固定一般設計または境界台帳に明示され、その境界判断に必要な事実命題に限る。
- 根拠は、現在review operationの成功観測、または設計より前に固定されたcontract / authorityの明示列挙に限る。
- 各根拠は一意な`support_identity`を持ち、複数根拠は同一具体instanceへ明示的に結び付く。
- 列挙漏れ、open境界、名称、背景知識、より強い設計の可能性から反例を推測しない。
- reviewerが意味上の前提、直接矛盾、設計変更効果を判定し、rootはidentity、schema、receiptの受入だけを行う。
- 具体的反例が成立した後は無関係なmanifest欠落で失効させず、反例不成立時だけ証拠不足を`unavailable`へ写す。
- 明示された判断前提がない候補は`not_applicable`であり、review operation全体を`unavailable`にしない。
- Candidate175のreview operation admission、専用producer、semantic projection、permission-before-operation、およびCandidate173由来の規範predicate経路を保持する。
- Candidate175との差分はroot `AGENTS.md`の`DESIGN_ADMISSION`だけである。

## Identity確認

- prompt identity: `the-caption-3ce91a4-decision-premise-counterexample-r1`
- parent prompt identity: `the-caption-3ce91a4-review-operation-admission-closure-r1`
- AGENTS SHA-256: `03fc778f6e493a8c3d1363c415499b1f486408a83a95696b1c8ac312ffc37dc7`
- AGENTS Git blob: `95c17588700ce79453e8eac6c005b4a0dd1ac340`
- bundle SHA-256: `45c8162191e4c844f33188f492bf56768021a26be5f790d8bb9cf825716d56be`

評価case、fixture、oracle、rating contract、合否条件は変更していない。
