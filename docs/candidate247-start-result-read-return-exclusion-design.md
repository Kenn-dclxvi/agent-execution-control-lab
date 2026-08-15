# Candidate247 開始確認result後のread着手許可の閉鎖

## 結論

Candidate247はCandidate147を直接の基準とし、開始状態の確認resultによって対象、許可、必要性が変わらないと既に分かっているreadを、そのresultをAIへ返した後まで未着手にできる許可を閉じる。Candidate246はF04の検証境界を成立させた人間語のsourceとして使うが、直接の親にはしない。

置換する`DECISION_BOUNDARY`は次の一文とする。

> 開始状態の確認結果によって対象、許可、必要性が変わらないと既に分かっている読み取りは、その結果をAIへ返してから着手してはならない。

これはread command、tool、発行順または同時実行方法を指定しない。開始確認resultをAIへ返した後に、影響を受けない必要readを新しく選んで着手できるpermissionだけを閉じる。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate246は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 開始状態の確認と、そのresultで対象、許可、必要性が変わらないと確定済みのreadを、確認resultがAIへ返る前に着手し、共同result後に一度だけ次を判断する |
| 保存済み問題経路 | Candidate246 F04の5 / 5件で、開始状態の確認だけを最初のcustom tool callから発行し、そのresultをAIへ返した後に`App.tsx`のreadを別発行した |
| 基準挙動 | 互換なCandidate147 F04の5 / 5件では、開始状態の確認と`App.tsx`等のreadを最初の一つのcustom tool call内から発行した |
| 問題経路の影響 | Candidate246は検証境界を5 / 5件で通過した後も総使用token中央値が`183,187`で、Candidate147より21.18%多かった。custom tool call中央値はCandidate147の4件に対してCandidate246は5件だった |
| 許していた辺 | Candidate246の一文は開始確認をread未着手のまま完了することを禁じたが、確認resultをAIへ返した時点を境界へ含めず、返却後にreadを新しく着手する経路が5 / 5件残った |
| TaskSpec等で防げない理由 | TaskSpecは開始drift時にartifact変更とrequired commandを止めるが、readを禁止せず、開始確認resultをAIへ返す前に必要readへ着手するかを定めない |
| 置換する条件 | Candidate246の`DECISION_BOUNDARY`一文だけを上記一文へ置換する。Candidate246で成立した`VALIDATION_CLOSURE`とその他の人間語をbyte同一で保持する |
| 消える問題経路 | 開始確認resultをAIへ返した後に、resultで変わらない必要readを新しく選んで別発行する経路 |
| 判断順を変えた場合 | readの対象、許可、必要性が開始resultで変わらないと既に分かる限り、確認だけを先に判断してもresult返却後の着手は許可されない |
| 維持する正常経路 | driftがreadを禁止する、read対象を変える、またはreadの必要性を変える場合はreadを先に着手しない。不要なreadを新たに要求しない。Candidate246の検証境界を維持する |
| 情報の所在と経路 | TaskSpecが開始時点の確認、drift時の停止対象、read許可pathを持つ。新しいrepository read、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | 開始resultでreadの対象、許可、必要性が変わるかというC147既存境界だけを人間語で保持し、新しい判断材料や例外は増やさない |
| 評価 | F04 N=5。5 / 5件Score `4`、開始確認resultがAIへ返る前の必要read着手5 / 5件、Candidate246の検証機序維持5 / 5件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質、開始確認/read機序、Candidate246の検証機序に一件でも反例があれば停止する。全機序を通過しても総使用token中央値がCandidate147より多ければ、残るF04コスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-result-read-return-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`一文だけ
- 維持target: `DECISION_BOUNDARY`以外の全targetと全文をCandidate246と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / start_result_read_mechanism_failed_5_of_5 / validation_mechanism_failed_3_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
