# Sonnet 5.5 lowで検証の一括化が成立しない理由（r1）

2026-10-09。[C280の指示文を短くする案の検討](c280-compaction-review-r1.md)で残した課題のうち、Sonnet 5.5 lowでC281以降の機序（検証の一括化）が成立しない理由を、保存済みのtranscriptから分解した記録。[設計原則](prompt-control-design-principles.md)の全文を読んだうえで、読み取り専用で分析した。新しいモデル実行はしておらず、Candidateは作成しない。

## 結論

**Sonnet lowで検証が複数の要求に分かれるのは、評価の仕組みがClaudeに渡す課題文の、必須コマンドの発行方法の指定に従った結果である。** プロンプトの検証の項目（一つの外側の呼び出しの中で順に実行する）は、この指定と正面から食い違っており、Claude Codeでは成立できない。

## 事実

### 検証が分かれた実行の分類

変更を伴うrunのうち、変更後に検証のコマンド（`pytest`、`main_verify`、`git diff --check`、`bash -n`、`npm`など）を含む要求が2回以上あった実行を、要求の間に修正（`Edit`、`Write`、書き込みのコマンド）があったかで分けた。

| 段階 | 検証が1要求 | 検証が分かれた | 修正なしの分割（境目の数） | 修正後の再実行など |
| --- | ---: | ---: | ---: | ---: |
| C280 | 23 | 20 | 23 | 0 |
| C284 | 17 | 27 | 32 | 2 |
| C293 | 22 | 23 | 33 | 3 |
| C296 | 24 | 20 | 26 | 0 |

分割のほとんどは、修正をはさまない分割である。C296の分割の形は、`pytest`→`main_verify`（5件）、`pytest`→`pytest`→`diff-check`（5件）、`bash -n`→`main_verify`→`diff-check`（5件）、`npm`→`npm`→`npm`（3件）などで、検証のコマンドを1つずつ別の要求で発行していた。

### 分割の境目は、TaskSpecの必須コマンドの境目と一致する

評価条件の`command_evidence_protocol.required_command_groups_by_case`（ケースごとの必須の検証コマンド）と照らした。

| 段階 | 必須コマンドが2つ以上ある変更run | 検証が分かれたrun | 分割の境目が別の必須コマンドの間 | 同じ要求で必須コマンドを複数のBash呼び出しとして並べたrun |
| --- | ---: | ---: | ---: | ---: |
| C280 | 33 | 20 | 20 | 3 |
| C296 | 34 | 20 | 20 | 0 |

分割したrunは、すべて、別々の必須コマンドの間で分かれていた。

### 課題文の指定

Claude Codeの評価で、モデルへ渡す課題文には、全Candidate共通で次の文が付く（`scripts/run_claude_evaluation.py`の`render_task`、`command_protocol_text_revision`は`claude-bash-separate-command-r1`）。

> TaskSpecのrequired validation commandは1 commandずつ個別のBash tool呼び出しで実行し、compound commandへまとめないでください。

Codexの評価では、同じ目的の文が「列挙順に`tools.exec_command`へ1 commandずつ個別invocation」「1 commandずつ個別の`exec_command`で実行」となっている（`scripts/run_codex_evaluation.py`）。Codexでは、外側の一つの呼び出し（JavaScriptのループ）の中で`exec_command`を個別に発行できるため、プロンプトの検証の項目と両立する（C147のVALIDATION_CLOSUREが、この読み方を明記していた）。Claude Codeでは、`Bash`の呼び出しそのものが外側の呼び出しであり、個別の`Bash`呼び出しを求める指定と、一つの外側の呼び出しの中で実行する指定は、両立しない。

## 解釈

- Sonnet lowは、リポジトリの指示文（`AGENTS.md`）より、課題文の指定に従っている。Opus 5.5 mediumのC289のA02の2件で、検証をまとめた一つの呼び出しが終了コード1を返して減点されたのも、まとめた呼び出しが、この指定の採点（コマンドごとの終了状態）と合わなかった例である。
- したがって、判定表で「Sonnet lowではVが成立しない」とした結果の大部分は、モデルの性質ではなく、評価の課題文の指定による。Vは、Claude Codeでは、この評価の条件のもとでプロンプトから閉じられない。
- プロンプトの検証の項目は、Claude Codeでは費用（固定分）だけになり、Codexでは効果を持つ。

## リポジトリの中で取れる対応と、取れない対応

- **取れない（このリポジトリの解決案にしない）：** 評価の課題文の指定（`render_task`の文）を変えること。これは評価条件の変更であり、プロンプトの比較の変数ではない（`PROMPT_ONLY_COMPARISON`）。変える場合は、利用者が明示的に依頼する評価基盤の別作業となり、変更前後の差をプロンプトの効果として比べない。
- **取れる（設計の候補）：** 指定と両立する形で、モデルへ戻る回数を減らすこと。Claude Codeでは、一つの応答の中に複数の`Bash`呼び出しを並べられる。必須コマンドを個別の`Bash`呼び出しとして、同じ応答の中で並べて発行すれば、課題文の指定を守ったまま、途中の結果ごとにモデルへ戻る経路を閉じられる。C280のSonnet lowでも、3件はこの形だった。Codexでは、従来どおり一つの外側の呼び出しの中で個別に発行する形が、同じ境界を満たす。
  - この形では、前のコマンドが失敗しても、同じ応答に並べた後続のコマンドは実行される（失敗時に後続を止める、が成り立たない）。前のコマンドの結果に依存するコマンド（たとえば`npm ci`の後の`npm run build`）は、並べられない。どの範囲を並べるかの決め方を、必要性の判定に任せずに定められるかが、設計の課題になる。

## 判断の限界

- 分類は、コマンド文字列と、要求の間の修正の有無による簡易な判定である。
- Sonnet low以外のClaudeモデル（Opus 5.5 mediumなど）での検証の分割も、同じ指定の影響を受けていると考えられるが、この記録では数えていない。
- この記録は採用、release、本体反映を決めない。

## 参照

[C280の短縮の検討](c280-compaction-review-r1.md)、[判定表](mechanism-establishment-table-r1.md)、[C284の設計](candidate284-validation-single-call-design.md)、[C290・C291の設計](candidate290-candidate291-root-instruction-validation-exit-design.md)、[C296の結果](../evaluations/results/c296-sol61-low-sonnet55-low-standard14-n5_2026-10-09.md)。
