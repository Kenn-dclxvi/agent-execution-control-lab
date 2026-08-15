# Candidate231 調査許可の簡潔化設計

## 結論

Candidate231はCandidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接の基準とし、Candidate230で人間語へ展開した13項目のうち、F02でtoken差が集中した`EVIDENCE_GATE`だけを短くする。Candidate230はpromptの親にせず、品質を維持できた人間語と、追加検索・部分読み・再確認が残った反例のsourceとして使う。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準promptと正常経路 | Candidate147。必要な実装を決める具体的な観測だけを許可し、必要な事実が揃ったら変更へ進む |
| 保存済みの問題経路 | Candidate230のF02は5 / 5 Score `4`、独立producer起動0件だったが、token中央値`178,886`でCandidate147の`128,236`より`39.50%`大きかった。全文read後に同じ判断の検索や部分readを追加したrunがあった |
| 問題を許した辺 | 展開した説明の中で「追加調査を許可する条件」と「必要な事実が揃った時点で調査を閉じる条件」が離れ、同じ判断の検索・部分読み・再確認を別の必要調査として扱える |
| 変更する条件 | `EVIDENCE_GATE`を、状態、調査の開放条件、変更前の許可範囲、実装方針の確定、追加調査の例外という同じ機能を保った短い人間語へ置き換える |
| 実行不能にする経路 | 一つの実装方針を決める必要な事実が揃った後に、同じ判断のための検索、部分読み、再確認を追加する経路 |
| 維持する正常経路 | 未観測の具体的な値を一つの調査で確定する。missing、unreadable、具体的矛盾、許可範囲内で実現不能、別authorityの明示が観測された場合だけ次の調査を一件許可する |
| 対象外 | 成功runのcommand順を手順化しない。read対象、command、tool、repository構造を固定しない。ほか12項目はCandidate230の人間語を変更しない |
| 評価 | F02 N=5だけを実行する。5 / 5 Score `4`、判断責任者名からの独立producer起動0 / 5件を必須とする。token中央値をCandidate230の`178,886`とCandidate147の`128,236`へ比較する |
| 進行判定 | 品質と担当起動を維持し、token中央値がCandidate230を下回れば、この簡潔化を有効な復元差分とする。Candidate147比`+10%`以内は当面の目安であり、成否条件にはしない |
| 停止条件 | 品質または担当起動に一件でも反例があれば停止する。F02の結果にかかわらず、この評価からStandard14、追加N、採用、release、projectionへ自動的に進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-compact-evidence-admission-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- 変更target: root `AGENTS.md`だけ
- 変更箇所: `EVIDENCE_GATE`だけ
- 維持箇所: ほか12項目はCandidate230と同一byte、ほか17 targetはCandidate147と同一byte
- Candidate230: 人間語と反例のsource。baseline、評価状態、bundle identityは継承しない

## 現在状態

`f02_n5_completed / quality_passed / token_lower_than_candidate230 / criterion_owner_producer_failed_1_of_5 / mechanism_failed / stopped / adoption_not_decided`

## 評価結果

F02は5 / 5件がScore `4`だった。token中央値はCandidate230の`178,886`から`133,657`へ`25.28%`減り、Candidate147の`128,236`との差は`+4.23%`まで縮まった。同じ判断の追加検索または部分readも2 / 5件から1 / 5件へ減った。

一方、1 / 5件で判断責任者名から独立workerを起動した。固定した停止条件に従い、コスト差は保存するがCandidate231を復元差分として採用しない。
