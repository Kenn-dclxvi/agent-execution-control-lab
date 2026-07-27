# Click C81 / C81 + Repository Authority Std14 r2比較設計

## 結論

`click-standard14-r2`をC81全文のみと、同じC81全文へClick repository authorityを
加えた条件で比較する。これにより、C81が有効な状態でもF10 r2のauthority
availabilityが維持されるか、またsub instruction追加が他13 caseへ回帰または
干渉を起こさないかを確認する。

- C81: root `AGENTS.md`へCandidate81全文だけを配置する。
- C81 + Repository Authority: 同じroot本文に加えて`docs`、`src`、`tests`の
  sub `AGENTS.md`を配置する。
- 比較条件はMedium、`N=5`、`M=24`、Rating v10、Std14 r2へ固定する。
- 採用、release、Click本体への反映は別gateとする。

## Candidate作成前gate

1. 基準prompt setは`click-00e592c-validation-wrapper-precedence-r1`である。
2. 基準の最短正常経路はC81制御下でTaskSpecを満たし、required validation後に
   停止する経路である。
3. 保存済みStd14 r2では、root promptを持たないNo-AGENTSのF10だけが5 / 5件
   `authority_unavailable`となり、Repository Authorityでは5 / 5件完了した。
4. C81単体はroot制御を持つがClick command APIを確定するrepository固有authorityを
   持たない。したがって、既存TaskSpecとC81本文だけではF10 C1 / C2を満たせない。
5. 変更する一つの構成軸は、C81 root本文を同一に保ったまま、固定済みの
   Click repository authority 3 fileを追加することである。
6. この軸が変える判断点は、F10で`src/AGENTS.md`のcommand API authorityを
   利用できるかどうかである。
7. 増える判断点はpath-scoped instructionの探索、適用path、sourceとの整合確認である。
8. 品質維持は、F10以外の13 caseが両条件65 / 65件score `4`、F10がC81で
   score `1` × 5、C81 + authorityでscore `4` × 5になることで確認する。
9. F10のsource-only推論、authorityありでの未完了、他caseのquality低下、
   unexpected drift、required command evidence欠落が1件でもあれば互換性を判定しない。

targeted F10はすでにNo-AGENTS / Repository Authorityでqualification済みである。
今回は新しいpredicateを作らず、固定済みauthorityをC81との組合せへ水平展開するため、
同じStd14 r2全体を直接実施する。

## 固定する比較条件

| 項目 | 値 |
| --- | --- |
| set | `click-standard14-r2` / `r2` |
| case | 14、F10のみ`r2` |
| model / reasoning | `gpt-5.6-sol` / `medium` |
| N / B / M | `5 / 1 / 24` |
| rating | `click-outcome-abstract-condition-preserving-v10` |
| runtime identity | `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952` |

両profileはprompt identity以外を一致させる。C81 + Repository Authority bundleの
root `AGENTS.md`は既存C81 bundleとbyte-identical、3つのsub本文は既存Repository
Authority bundleとbyte-identicalにする。

## 解釈境界

- 主比較はC81対C81 + Repository Authorityである。
- No-AGENTS対Repository Authorityのr2結果はbridge evidenceとして参照するが、
  別prompt identityのresultを同一KPI comparisonへ混ぜない。
- F10のquality差はauthority availability、他13 caseは回帰と干渉の有無を示す。
- tokenとelapsedは、F10で停止と成果完成の作業量が異なることを分けて解釈する。
- artifact、評価、採用、release、runtime projectionを別状態として扱う。

## 評価結果

2026-07-27に両条件70 / 70件を完了した。C81単体はF10以外がscore `4` × 65、
F10がscore `1` × 5、C81 + Repository Authorityはscore `4` × 70だった。
全140件がvalid・rateableで、excluded attemptとunexpected driftは0件だった。

C81 + AuthorityはC81比でquality中央値`+5.357`、token中央値`+8.86%`、
elapsed中央値`+11.55%`だった。quality差はF10だけで発生した。同じauthority状態で
C81の有無を比較すると、token / elapsedはauthorityなしで`-27.35% / -17.04%`、
authorityありで`-25.08% / -10.98%`となり、C81の削減方向は維持された。

公式KPI、trace監査、解釈境界は
[`Click C81 / C81 + Repository Authority Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)
を正本とする。
