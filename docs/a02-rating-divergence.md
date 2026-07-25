# A02の「要求と採点のずれ」とrating contract revision

A02 caseで観測された、実行役へ提示した成果条件と採点側が必須化した条件の不一致（要求と採点のずれ）を記録する。あわせて、この論点に関係するrating contract revisionの流れを置く。

初見向けの全体像は[`repository-overview.md`](repository-overview.md)、効率改善メカニズムの整理は[`control-mechanisms.md`](control-mechanisms.md)を参照する。正本は末尾に示す。

## A02はどんなcaseか

**TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING** は、「一見あいまいだが実はリポジトリ規則で一意に決まる正規の起動先を、**質問せずに正しく解決して実装できるか**」を測るcaseである。

- **提示する（model-visible）**: 症状・対象ファイル・成功条件の要点だけ。成果条件は「shell構文、TaskSpecまたは適用されるリポジトリ規則が要求する既存試験、最終差分の確認」という抽象表現で、特定の試験コマンド名は含めない。
- **隠す（private）**: 正規の起動先、期待する変更後ファイルとseedの生成方法、oracleが参照する確認コマンド列。

重要なのは、privateにコマンド列が存在することと、そのコマンドが実行役へ課された必須試験であることは**別**である点だ。第2版（r2）は「TaskSpecまたは適用されるリポジトリ規則が要求する試験だけを必須にする」と定め、`TaskSpecにない特定コマンドは必須にしない`をcriterion側に明記している。第1版（r1）はTaskSpecにない`bash scripts/dev/main_verify.sh`を非公開の採点条件だけで必須にしていたため、r2でこの点を是正した（r1の入力と結果は変更していない）。

この「提示する情報」と「隠す情報」の分離、そして「privateの参照コマンド」と「必須試験」の区別が、次の採点論点の核心である。

## A02採点で起きた「要求と採点のずれ」

C71のB18評価（標準14項目を各`N=5`で18 Batch、Candidateごとに1,260 run。A02は合計90 run）で、A02の公式score分布は`4 / 3 = 86 / 4`となり、score 3が**4件**付いた。この4件は同じ原因ではなく、保存traceの意味確認で次の2種に分かれる。

| 内訳 | 件数 | 内容 |
| --- | --- | --- |
| 実質欠落（`git diff --check`未実行） | 3 | 下記の「要求と採点のずれ」に該当する |
| 採点偽陰性 | 1 | `bash scripts/dev/main_verify.sh`が`.venv/bin/python -m pytest tests/ -v`を`exec`し326 passedを得たが、固定auditがwrapper内の`pytest`を成功commandとして展開しなかった |

以下は、このうち**3件**の`git diff --check`未実行についての整理である。当初は品質低下と解釈されたが、一次資料を確認すると次のとおりである。

- 実行役へ**提示された成果条件**は「**最終diffからrouting成立を確認する**」という抽象的な表現だけだった。
- 一方、採点側（private）には `git diff --check` という**特定コマンド**が置かれていた。
- 採点器はこの抽象条件を「`git diff --check` の実行必須」と読み替え、未実行を欠落として減点した。
- ところが `git diff --check` は末尾空白や競合markerのlintであって、A02の主眼（routing成立の確認）とは別物である。

つまりこの3件は、**提示していない特定コマンドを採点側が必須化した「要求と採点のずれ」**であり、本物の品質低下とは言えない。提示条件に照らした実質的な低下は、A01の「未固定modeを確認せず実装・試験へ進んだ」1件にとどまる。

Candidate71 release artifactに保存された当時の未解決risk 2件（A02の3 / 90件、A01の1 / 90件）はそのまま保持する。現在の研究項目として残るのはA01側であり、その整理は[`research-backlog.md`](research-backlog.md)にある。

## 採点条件（rating contract）の進化

採点条件はrevision別に固定され、in-placeで書き換えない（結果を見た後の基準変更は必ず新revision）。A02の論点に関係する流れは次のとおりである。

| revision | 主眼 |
| --- | --- |
| v10 | 実行役に提示した成果境界だけを必須にする |
| v11 | F10数値lineの意味等価と位置診断を分離 |
| v12 | command evidenceのquote直列化を正規化 |
| **v13** | **提示した抽象成果条件を特定コマンドへ具体化して必須化することを禁止し、コマンド名までmodel-visibleに明示された必須試験だけを品質へ反映する** |

上記のA02のずれを塞いだのが第13版 [`outcome-abstract-condition-preserving-owner-diagnostic-v13`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json) である。C71のB18評価自体はv12で実施しており、既存のv12契約とB18結果はそのまま履歴として保持する。過去resultを新しいcontractで再採点したようには扱わない。

なお、**どのrevisionを「現行」として新規runへ適用するかの指定は、この文書では確定しない**。評価基盤の正本[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)は現行rating contractを`owner-producer-quality-v8`と記載しており、v13の位置づけとの関係は同正本側で確定すべき事項である。契約identityは比較互換条件の一部であるため、新規profile作成時は同正本と[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)を確認する。この不整合は[`research-backlog.md`](research-backlog.md)へ未決事項として記録する。

## 正本

- score分布と4件の内訳（当時の分類）: [`Candidate69 / Candidate71第12版B18`](../evaluations/results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)
- case定義: [`evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/`](../evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/)（第2版の必須試験境界は[`r2/README.md`](../evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2/README.md)）
- rating contract: [`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)
- 当時の未解決risk: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)
