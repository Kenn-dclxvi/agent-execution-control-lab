# 候補319 リリース

## 結論

候補319（C319）を、そのままの内容でリリースした。C316のリリース（[`the-caption-3ce91a4-receive-form-file-read-range-release-r1`](../the-caption-3ce91a4-receive-form-file-read-range-release-r1/README.md)）の後継である。

リリース状態は`released`、承認状態は`approved`である。THE-CAPTION本体へは投影していない（`not_projected`）。

承認は、2026-10-15の利用者の判断（「これを採用したい」）による。同じ日に、利用者の指示で、C319の「# 実行制御」を利用者の共通指示（`~/.claude/CLAUDE.md`の「# 実行制御」の節と`~/.codex/AGENTS.md`の全文）に置いた。これはTHE-CAPTION本体への投影ではなく、このリポジトリの外での適用として記録する。

## 識別情報

- リリース識別子: `the-caption-3ce91a4-unconfirmed-location-search-release-r1`
- 元候補: `the-caption-3ce91a4-unconfirmed-location-search-r1`
- 元候補の固定commit: `98cad61929b2429beac45ab8f54b5e6480a4a0d5`
- bundle SHA-256: `516945120d2952c0508da76e715c7ea01446f9917175a0be0c0572ccfafb450c`（元候補と同じ）
- 本文: root `AGENTS.md`の「# 実行制御」6項目。ほかの18対象はTHE-CAPTIONの現在の内容のまま

## C316からの変更

| 項目 | 変更 | 理由 |
| --- | --- | --- |
| 1行目の2文目（C318） | 「既存の状態…は、依頼や指示がそれらから結果を決めるよう指定していない限り、結果を決める根拠にならない」 | ClickのF07-Pで、TaskSpecが既存のlockと隣接groupから意図を解決するよう指定しているのに、CodexがC316の2文目を理由に利用者へ確認して止まった（累積N=20でSol 11 / 20、Astra 10 / 20） |
| 2行目に1文を追加（C319） | 「指示や正本は、依頼が名指ししたものと作業ツリーで見つかったものだけを使い、存在を確かめていない場所を指定して探さない」 | Codexが存在しない`.agents`・`.codex`を指定して探し、ClickのF06でその失敗を環境failureと見なして止まった。同じ探索はTHE-CAPTIONのFreeでも起きていた |

## 評価範囲

FreeとC316と比べた（各4モデル、N=5）。

| 対象 | 品質 | 費用のFree比 | 費用のC316比 |
| --- | --- | --- | --- |
| THE-CAPTION Standard14 | 4モデルとも4点70件 | 4モデルとも幅より下（−9.66%〜−35.11%） | Sol以外の3モデルで幅の中。Solは+29.34%だが、計測の時間帯のキャッシュの状態による（作業の量はC316より少ない） |
| Click Standard14 r4 | Sonnetの1件（Freeでも起きるF06の判断の落とし穴）以外は4点 | 4モデルとも幅より下（−2.55%〜−23.55%） | 4モデルとも幅の中（−3.21%〜−0.07%） |

- C316で起きていたClickのF07-Pの誤った停止と、F06の探索の失敗による停止は、C319では0件だった。
- Codexで存在しない場所を指定して失敗する探索は、THE-CAPTIONのSolでFree 20件、C316 13件に対してC319は1件（各70件中）。作業ツリーにある階層ごとの指示を読む動作は変わらなかった。

## 未解決risk

- THE-CAPTIONのStandard14とClickのStandard14 r4の範囲で、各4モデルN=5の観測である。
- THE-CAPTIONのStandard14には、依頼が結果を既存の状態に委ねるケースがない。1行目の変更の効果はClickでだけ確認した。
- C316との費用と経過時間の比較は、計測の時間帯が違う。
- ClickのF06でSonnetがテストを足さずに終える判断の落とし穴は、Freeでも起きており、この変更では扱っていない。
- 個人の共通指示として全プロジェクトに置いた場合の効果は計測していない。

## 承認状態

- リリース準備: `complete`
- リリース状態: `released`
- 採用承認: `approved`
- 本体反映: `not_projected`
- 承認根拠: 2026-10-15の利用者の判断
- リポジトリ外での適用: `~/.claude/CLAUDE.md`の「# 実行制御」の節と`~/.codex/AGENTS.md`の全文を、このリリースのroot `AGENTS.md`と同じ文面にした（2026-10-15）
- ロールバック: C316のリリース（`the-caption-3ce91a4-receive-form-file-read-range-release-r1`）の本文へ戻す

## 根拠

- [C319 4モデル（THE-CAPTION）](../../../evaluations/results/c319-four-models-standard14-n5_2026-10-15.md)
- [ClickのC319 4モデル](../../../evaluations/targets/click/results/click-c319-four-models-standard14-r4-n5_2026-10-15.md)
- [ClickのCodexでC316だけに出た失敗の分析](../../../evaluations/targets/click/results/click-c316-codex-failure-mechanism-analysis_2026-10-15.md)
- [ClickのF06で起きた失敗の分析](../../../evaluations/targets/click/results/click-f06-failure-analysis_2026-10-15.md)
- [候補318の設計記録](../../../docs/candidate318-c316-delegated-state-source-design.md)、[候補319の設計記録](../../../docs/candidate319-c318-unconfirmed-location-search-design.md)
- [候補319 manifest](../../candidates/the-caption-3ce91a4-unconfirmed-location-search-r1/manifest.json)
