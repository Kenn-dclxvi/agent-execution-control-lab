# Click repository authority availability比較設計

## 結論

既存のClick No-AGENTS / Repository sub-AGENTS Std14は、配置と露出の比較として
有効である。ただし、THE-CAPTIONで差が出たF10と同じ「repository authorityが
なければ成果を確定できない」経路を作っていなかった。そこで既存Std14を変更せず、
`CLICK-F10-COMMAND-API-INVENTORY/r2`だけを使うtargeted比較を追加する。

- No-AGENTSでは`src/AGENTS.md`が存在しないため、sourceだけから推測せず
  `authority_unavailable`で停止する。
- Repository Authorityでは`src/AGENTS.md`を読み、そこに固定されたcommand API
  authorityを3つのsource fileと照合してinventoryを完了する。
- 比較条件はMedium、`N=5`、`M=24`とし、prompt bundle以外を一致させる。

これはauthority availabilityの因果経路を確認する試験である。sub instruction全般の
有効性、C81との組合せ、採用、release、Click本体への反映は判定しない。

## 評価結果

2026-07-27に両条件各5件を実行した。No-AGENTSは5 / 5件がsource-only推論を
行わず`authority_unavailable`で停止し、score `1`だった。Repository Authorityは
5 / 5件がauthorityと指定3 sourceを照合してinventoryを完了し、score `4`だった。
全10件がvalid・rateable、zero driftで、excluded attemptは0件だった。

したがって、THE-CAPTION F10と同じavailability方向はClickでも再現した。公式KPI、
identity、trace監査は[`Click No-AGENTS / Repository Authority Medium F10 N=5`](../evaluations/targets/click/results/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md)
を正本とする。

targeted qualification後、F10 r2を含む`click-standard14-r2`を両条件各70件で
再実施した。F10以外の13 caseは両条件65 / 65件がscore `4`、F10はtargetedと
同じscore `1` × 5 / score `4` × 5へ分離した。全140件がvalid・rateableで、
excluded attemptとunexpected driftは0件だった。これにより、見直し後の14判断点を
比較する試験セットとしての互換性を達成した。全体KPIと判定は
[`Click No-AGENTS / Repository Authority Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)
を正本とする。

## 既存Std14の全ケース監査

Click Std14は題材の同一性ではなく、THE-CAPTIONの14項目が担う実行判断点を
Clickの題材で再現する設計である。各現行caseをTaskSpec、停止経路、authority依存の
3点で見直した。

| case | 維持する判断点 | 監査結果 |
| --- | --- | --- |
| F01 | 単一file実装、不変条件復元、focused / full validation | 維持。TaskSpecとseedだけで成果を確定でき、sub本文を必須authorityにする理由はない |
| F02 | 複数source間の公開・内部contract | 維持。層間contractとrequired gateが明示済み |
| F03 | 例外時cleanupとcwd復元 | 維持。filesystem終端状態が成果authorityである |
| F04 | nested contextのcompletion分岐 | 維持。既存試験は実装・検証経路を測る。過去履歴探索は別のC81残余仮説である |
| F05 | 未固定policyのclarificationとzero drift | 維持。authorityを読んでも確定しない曖昧さを意図する |
| F05-OS | publish authorization外での停止 | 維持。permission境界が成果条件である |
| F06 | test-only修復とproduction非変更 | 維持。変更範囲と3条件のtest contractが明示済み |
| F07 | repository設定からのcanonical route解決 | 維持。`pyproject.toml`が直接のrepository根拠である |
| F07-P | dependency pair、provenance、offline lock | 維持。2 fileの整合とruntime commandが成果条件である |
| F08 | docs-onlyの参照同期 | 維持。sourceとdocsの直接照合を要求済み |
| F10 r1 | read-only API inventoryとzero drift | 回帰用途は維持。ただしsourceだけで完結し、authority availability比較には不適合 |
| F10-R | fixed commitの非破壊review | 維持。固定diffをreviewする試験で、現在HEADのoverlay ancestryを成果条件にしていない |
| A01 | repositoryから確定できない不足の確認停止 | 維持。sub本文があってもmodeとscopeは確定しない |
| A02 | repositoryから確定できるroutingの無質問解決 | 維持。`pyproject.toml`から一意に解決する設計である |

したがって、既存`click-standard14-r1`は14判断点の回帰・互換比較として変更しない。
authority本文の有無を直接操作する目的だけ、F10 r2へ分離する。F01〜F08等へ
不自然な`AGENTS.md`必須readを加えると、元の判断点とprompt exposureを同時に変える
ため実施しない。

## 変更軸と作成前gate

1. 基準prompt setは真にfile数0の`click-00e592c-no-agents-r1`である。
2. 保存済みStd14 traceではsub本文の初期context注入は0 / 70で、明示readはA01の
   5 / 5だけだった。
3. 誤経路は、F10 r1が`src/AGENTS.md`を必要とせずsourceだけでinventoryを完了し、
   No-AGENTSとsub-AGENTSの両方で同じ成果へ到達したことである。
4. 既存TaskSpecとsourceだけで正解できるため、配置差だけではこの誤経路を防げない。
5. 変更する一つの軸は、rootを置かず`src/AGENTS.md`へcommand construction APIの
   repository authorityを追加することである。`docs`と`tests`の本文は既存candidateと
   同一に保つ。
6. r2はauthorityを成果の前提として明示し、欠落時のsource-only推論を禁止する。
7. 増える判断点は、authorityの存在、non-empty、節の存在、sourceとの整合確認である。
8. 品質はrating v10の同じF10 criteriaで判定する。authorityあり条件はC1〜C3、
   authorityなし条件はzero driftと正しい停止経路を記録する。
9. authorityありで5 / 5がinventoryを完了しない、authorityなしでsource-only推論が
   1件でも起きる、またはrepository driftが1件でもあれば、この構成の水平展開を
   停止する。

## 固定identity

| 条件 | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| No-AGENTS | `click-00e592c-no-agents-r1` | `62570c22091a0e5c3431c5be416222987c6d4251fa634d633c6c6ebcee8ab82c` |
| Repository Authority | `click-00e592c-repository-authority-r1` | `fc81314aec37546950daf623509e8b423db32bcff696ee6f7d33bc6342458c3f` |

両profileは`click-f10-authority-availability-r1`、F10 r2、Rating v10、
`gpt-5.6-sol`、Medium、`N=5`、`M=24`へ固定する。empty bundleもadapterが同じ
metadata overlay commitを作るため、prompt file数によって開始HEADの段数を変えない。

## 結果の解釈境界

- No-AGENTSの`authority_unavailable`は設計どおりの実行終端だが、inventoryのC1 / C2
  を満たす成功結果ではなく、実測scoreは5件とも`1`だった。
- Repository Authorityは5 / 5件がscore `4`で完了し、ClickでもTHE-CAPTION F10と
  同じavailability方向を再現した。
- targeted 1 caseの差をStd14全体、他のsub instruction、token、elapsedへ一般化しない。
- 既存Std14の70 / 70 score 4と配置・露出結果は、今回のtargeted resultによって
  書き換えない。

## 実行順

1. 2 profileを同じverification rootへfreezeする。
2. No-AGENTSを5 slot実行し、全slotの終端とzero driftを確認する。
3. Repository Authorityを5 slot実行し、authority read、source照合、zero driftを
   確認する。
4. 10 / 10 slotが揃うまで欠損slotだけを再実行する。部分resultをratingしない。
5. Rating v10で採点し、3 KPIとauthority read / terminal routeを分けて記録する。
