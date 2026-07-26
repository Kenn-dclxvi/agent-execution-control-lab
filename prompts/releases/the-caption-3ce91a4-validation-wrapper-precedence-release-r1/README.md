# 候補81 リリース

## 結論

候補81の実効変更を、THE-CAPTIONへ投影した。

リリース状態は`projected`、承認状態は`approved`である。

候補81はRating v13、reasoning effort `medium`、標準14項目N=5でquality gateとprompt stability gateを通過した。今回の承認は、2026-07-27の明示的な本体適用依頼に基づく。

## 識別情報

- リリース識別子: `the-caption-3ce91a4-validation-wrapper-precedence-release-r1`
- 元候補: `the-caption-3ce91a4-validation-wrapper-precedence-r1`
- 元候補の固定commit: `e52e029a3da3eeab055856d624535c73132aea40`
- 内容SHA-256: `919e2d4c53a487efde9d87ab182ea9b576c082c29ac81eb46fb7a442fb837220`
- 内容関係: 候補81と同一内容のリリーススナップショット
- 候補81から変更した対象: なし
- 現在投影済みの候補71との差: root `AGENTS.md`だけ

## 評価範囲

- 採点条件: `outcome-abstract-condition-preserving-owner-diagnostic-v13`
- model / reasoning effort: `gpt-5.6-sol` / `medium`
- 評価集合: `the-caption-standard14-r1`第1版、14項目掛ける5回、合計70件
- valid / rateable: `70 / 70`
- 公式点数分布: `4 = 70`
- Candidate71比quality中央値: `0.00%`
- Candidate71比all-agent token中央値: `-0.30%`
- Candidate71比elapsed中央値: `+5.78%`
- 複数required command caseの1-step closure: `35 / 35`。Candidate71は`30 / 35`
- F04の1-step closure: 標準14項目`5 / 5`、targeted試験`10 / 10`

## 未解決risk

- quality、token、elapsedの比較はRating v13、reasoning effort `medium`、標準14項目N=5の範囲に限定する。
- elapsed中央値はCandidate71比`+5.78%`であり、速度改善は確認していない。
- F04の安定化は合計15件で観測したが、targeted試験と標準14項目は条件が異なるため一つのKPIへ集約しない。
- command evidence protocol v1での結果であり、異なるruntimeまたはprotocolへ一般化しない。

## 承認状態

- リリース準備: `complete`
- リリース状態: `projected`
- 採用承認: `approved`
- 本体反映: `projected`。`main`へのmergeで有効化済み
- 承認根拠: 2026-07-27の明示的な本体適用依頼

## 投影結果

- 投影前commit / 巻き戻し先: `2f550a88dfa5b7b24ff653b8fab8cd2ef150d360`
- 投影した実変更対象: root `AGENTS.md`一つ
- 検証: `git diff --check`、`bash ./scripts/dev/verify_change_set.sh`、`401 passed in 6.75s`
- 統合後release対象一致: `18 / 19`
- 一致しない対象: `docs/how-to/index.md`一つ
- 不一致理由: C43投影後のTHE-CAPTION本体更新であり、C81の変更対象外のため現行内容を保持
- THE-CAPTION PR: [#343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343)
- 統合commit: `592e73aae4f5cf71964efea0d49836e8c894cbbc`
- 投影記録: [`projection.json`](projection.json)

## 根拠

- [投影記録](projection.json)
- [THE-CAPTION PR #343](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/343)
- [候補81 標準14項目N=5](../../../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)
- [候補81 F04 N=10](../../../evaluations/results/candidate71-candidate81-validation-wrapper-precedence-v13-medium-f04-n10_2026-07-26.md)
- [候補81設計記録](../../../docs/candidate81-validation-wrapper-precedence-design.md)
- [候補81 manifest](../../candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1/manifest.json)
