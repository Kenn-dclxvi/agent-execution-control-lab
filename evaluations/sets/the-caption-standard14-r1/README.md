# THE-CAPTION 標準14項目 第1版

## 結論

今後の全体試験は、既存の標準F項目12件へA01とA02を加えた14件で実施する。

旧12項目の評価集合、試験設定、結果は履歴として変更しない。14項目は新しい評価集合`the-caption-standard14-r1`として扱い、旧12項目の結果と互換比較へ混ぜない。

## 構成

| 区分 | 評価項目 | 版 |
| --- | --- | --- |
| F | `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` | `r3` |
| F | `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` | `r1` |
| F | `TC-F03-ATOMIC-CONTEXT-CLEANUP` | `r2` |
| F | `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY` | `r2` |
| F | `TC-F05-CLARIFY-UNITS-MODE` | `r1` |
| F | `TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY` | `r1` |
| F | `TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT` | `r2` |
| F | `TC-F07-CANONICAL-V4-RUNNER` | `r2` |
| F | `TC-F07-DEPENDENCY-PROVENANCE-PAIR` | `r1` |
| F | `TC-F08-CANONICAL-CLI-REFERENCE-SYNC` | `r1` |
| F | `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` | `r1` |
| F | `TC-F10-MONTHLY-FORMAT-TEST-REVIEW` | `r3` |
| A | `TC-A01-LATENT-MODE-POLICY` | `r2` |
| A | `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` | `r2` |

## 固定する境界

- A01とA02を外した12項目だけの実行を、今後の全体試験完了として扱わない。
- 項目固有の原因確認は一部項目だけで実施してよい。ただし、その結果を全体試験完了へ読み替えない。
- 14項目のいずれかの版を変更する場合は、この評価集合を上書きせず新しい版を作る。
- A01とA02の`trial-prompt-input.json`は第1版から変更しない。
- F項目用のコマンド証拠指示はA01とA02へ渡さない。
- 既存実行の採点条件は各resultが固定したrevisionのまま保持する。
- 今後の実行は`outcome-abstract-condition-preserving-owner-diagnostic-v13`を使用する。提示した抽象成果条件を未提示の特定コマンドへ具体化して必須化しない。F10 Monthlyの数値lineとowner-producer evidenceは診断へ保存し、quality scoreには使用しない。
- 各候補を5回評価する場合は、14項目掛ける5回の70件を一つの結果として登録する。

## 最初の実行設定

最初の実行設定は[`candidate43-outcome-authority-boundary-v10-standard14-global-m24-n5-r1.json`](../../profiles/candidate43-outcome-authority-boundary-v10-standard14-global-m24-n5-r1.json)である。

Candidate71 B18の互換baseline / candidate実行設定は、それぞれ[`Candidate69 v12`](../../profiles/candidate69-model-reentry-decision-boundary-v12-standard14-global-m24-n5-r1.json)と[`Candidate71 v12`](../../profiles/candidate71-validation-closure-v12-standard14-global-m24-n5-r1.json)を使用した。case、TaskSpec、permission、executor parameter、反復条件はv10 / v11 profileから変更せず、rating contractだけをv12へ更新した。[B18結果](../../results/candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)は両条件の1,260 / 1,260件を登録した。Candidate71に実質的な品質後退4件があったため停止した。Candidate43 / Candidate69 v11 profileは既存revisionの再現用として保持する。

rating v13の最初の互換比較は、Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71の6 profileで実行した。[結果](../../results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)は各条件70 / 70件、計420 / 420件をvalid・rateableとして登録した。v12以前のresultはこのcomparisonへ混ぜず、winner、採用、release、本体反映は判断していない。

この実行設定は候補43、各項目5回、同時実行上限24へ固定する。[初回結果](../../results/candidate43-outcome-authority-boundary-v10-standard14-n5_2026-07-20.md)は70件すべて有効かつ採点可能で、全件が点数`4`だった。別候補を評価する場合は候補の識別情報だけを替え、評価集合、採点条件、実行環境、権限、反復条件を維持する。

候補41は候補の識別情報だけを替えた[`同条件の実行設定`](../../profiles/candidate41-owner-metadata-delegation-boundary-v10-standard14-global-m24-n5-r1.json)で各5回実行した。[候補41・候補43の結果](../../results/candidate41-candidate43-outcome-boundary-v10-standard14-n5_2026-07-20.md)は両候補とも70 / 70件を登録した。

候補43は同じ実行設定を18回継続し、[`1,260件の実施記録`](../../results/candidate43-outcome-authority-boundary-v10-standard14-continuous-n5-b18_2026-07-20.md)を登録した。これは評価集合や採点条件を変更せず、各14項目掛ける5回の独立結果を18件保存した継続試験である。
