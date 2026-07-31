# Click Candidate125全文水平適用の設計記録

## 結論

THE-CAPTION Candidate125のroot `AGENTS.md`本文を改変せず、Clickのroot
`AGENTS.md` 1 targetへ水平適用し、Click Standard14 r2を各case `N=5`で実施する。
保存済みClick C81はCodex CLI `0.144.0`、今回の実行環境は`0.146.0`であるため、
tokenとelapsedの互換比較は行わない。今回は現行CLIでのCandidate125単独品質と経路を
登録し、C81との現行CLI比較が必要なら両条件を別試験で再実行する。

## Candidate作成前gate

1. 基準prompt setは`click-00e592c-validation-wrapper-precedence-r1`とする。最短正常経路は、固定TaskSpecとrepository stateから必要な変更を行い、明示required validationを完了して停止する経路である。
2. 保存済みClick C81 Standard14 r2ではF10以外65 / 65件がscore `4`、F10はauthority不在により5 / 5件がscore `1`だった。unexpected driftは0件だった。
3. Candidate125のTHE-CAPTION保存traceで対象にした誤経路は、変更前content不足をterminal absenceへ読み替えるfalse stop、implementation bind後の変更前command再入、検証success後の追加toolである。
4. Click C81にはCandidate125の`EVIDENCE_GATE`、`VALIDATION_PLAN`、criterion-complete single-target continuationがないため、同じ判断境界をpromptだけでは強制できない。
5. 変更軸はClick C81 root本文全体をTHE-CAPTION Candidate125 root本文へbyte-identicalに置換することだけである。Click固有predicateやrepository authorityは追加しない。
6. 消す対象は、変更前evidenceの無制限な追加、単なる取得範囲不足によるfalse stop、validation command選択のための追加repository探索、完了済み実行票後の追加toolである。
7. 増える判断点は、変更前evidence admission、exact target wave、限定single-target continuation、artifact変更後のvalidation planである。
8. 品質維持はClick Standard14 r2の14 case各N=5で確認する。期待分布はF10以外65件がscore `4`、repository authorityを持たないF10 5件がscore `1`である。
9. unexpected drift、required command evidence欠落、F10以外のscore `4`未達、またはF10がsource-only推論へ進んだ場合は品質gate不通過として停止する。

## 固定条件

- set: `click-standard14-r2` / `r2`
- prompt: `click-00e592c-criterion-complete-single-target-continuation-r1`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Agent / CLI: Codex、`0.146.0`
- target runtime: Python `3.14.5`、runtime identity `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`
- rating: `click-outcome-abstract-condition-preserving-v10`
- Case / N / M: `14 / 5 / 24`
- permission: `workspace-write / never`

## 比較境界

保存済みClick C81のCodex CLIは`0.144.0`であり、今回の`0.146.0`と異なる。
同じscore分布は品質維持の参考にはなるが、compatibility keyが異なるため公式3 KPIの
差として比較しない。THE-CAPTION Candidate125 resultもtarget instance、case、ratingが
異なるため同一比較へ混ぜない。

## 非目標

- Candidate125の個別predicateへの因果帰属
- Click C81との非互換KPI比較
- Click向けpromptの採用、release、または`pallets/click`本体への反映
- repository外executor、Codex CLI、tool adapter、runtime hookの変更
