# A02の「要求と採点のずれ」とrating contract revision

A02 caseで観測された、実行役へ提示した成果条件と採点側が必須化した条件の不一致（要求と採点のずれ）を記録する。あわせて、この論点に関係するrating contract revisionの流れを置く。

初見向けの全体像は[`repository-overview.md`](repository-overview.md)、効率改善メカニズムの整理は[`control-mechanisms.md`](control-mechanisms.md)を参照する。正本は末尾に示す。

## A02はどんなcaseか

**TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING** は、「一見あいまいだが実はリポジトリ規則で一意に決まる正規の起動先を、**質問せずに正しく解決して実装できるか**」を測るcaseである。

- **提示する（model-visible）**: 症状・対象ファイル・成功条件の要点だけ。
- **隠す（private）**: 正規の起動先、期待するdiff、**必須試験の具体コマンド**。

この「提示する情報」と「隠す情報」の分離が、次の採点論点の核心である。

## A02採点で起きた「要求と採点のずれ」

C71のB18評価（18反復）で、A02に3件の低得点（score 3）が付き、当初は品質低下と解釈された。しかし一次資料を確認すると次のとおりである。

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
| **v13（現行）** | **提示した抽象成果条件を特定コマンドへ具体化して必須化することを禁止し、コマンド名までmodel-visibleに明示された必須試験だけを品質へ反映する** |

上記のA02のずれを塞いだのが第13版 [`outcome-abstract-condition-preserving-owner-diagnostic-v13`](../evaluations/rating-contracts/outcome-abstract-condition-preserving-owner-diagnostic-v13.json) である。既存のv12契約とB18結果はそのまま履歴として保持し、過去resultを新しいcontractで再採点したようには扱わない。

## 正本

- case定義: [`evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/`](../evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/)
- rating contract: [`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)
- 当時の未解決risk: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)
