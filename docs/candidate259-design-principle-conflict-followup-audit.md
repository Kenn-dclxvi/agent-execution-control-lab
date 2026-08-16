# Candidate259 設計原則衝突の後続監査

## 結論

Candidate259のF04 N=5 result `7453ee7e3e0147d5871918a633d1a134`、品質監査、機序監査および`targeted_gate_passed`という当時の評価状態は変更しない。一方、Candidate259が追加した「同じ変更方針に対する同一artifactの追加readは一度だけ」という条件と、その条件をread invocation数で判定した機序gateは、`docs/prompt-control-design-principles.md`の「証拠が十分かどうかを読み取り回数、呼び出し回数等で判定しない」という正本原則と衝突する。

この衝突により、F04 N=5の通過をCandidate259の一般的なprompt制御成立、採用可能性、release準備またはprojection準備へ拡張しない。Candidate259のbundleと保存済みresultは履歴証拠として保持し、後続Candidateの親本文にはしない。

## 衝突する境界

- 正本原則: 証拠の十分性は取得量や回数ではなく、その証拠を使う判断に必要な事実を観測できたかで判定する。
- Candidate259本文: 同じ変更方針について、正常な一度目の追加read後の同一artifactへの二度目の追加read permissionを一律に閉じる。
- Candidate259機序監査: `additional_prechange_same_artifact_read_count`が0または1であることを通過条件にした。

Candidate254とCandidate258で観測した問題経路は、同じ判断について部分resultを受領した後、そのresultから次のreadへの依存関係を作ったことである。問題はreadの二度目という序数そのものではない。発行前から別の必要判定と観測値へbind済みの合法な複数readまで禁止し得るため、Candidate259の回数条件を一般的なpermission境界として維持しない。

## 保存するもの

- Candidate259のimmutable bundle identityと本文
- F04 5件のatomic run、採点、all-agent token、elapsedおよび機序監査
- F04に限った5 / 5 Score `4`、開始共同発行、相互非依存発行、検証境界の観測
- Candidate254とCandidate258の部分result依存経路を示すcounterexample

## 保存しない解釈

- read回数が一回以内なら証拠取得機序が一般に成立したという解釈
- F04 N=5の通過からStandard14、未評価条件、採用、releaseまたはprojectionへの自動的な一般化
- Candidate259を次Candidateの直接の親または追加条件の土台にすること

## Standard14 N=5測定の位置づけ

利用者の明示依頼により、Candidate259本文を変更せず、既存Standard14 r1の14ケースを各N=5で測定する。既存F04 5件は実効互換条件が一致する場合だけ再利用し、不足65件だけを発行する。

この測定が固定するのは、Candidate259を通常のStandard14経路へ置いた場合の実行有効性、品質、変更対象外経路への影響および3 KPIである。70 / 70件がScore `4`でも、上記の設計原則衝突や回数ベース機序を解消したことにはしない。品質失敗、必要な正常経路の欠落または新しい問題経路が一件でもあれば、その事実を有効なresultとして保持し、repair rerunで消さない。

## 現在状態

Standard14 N=5は70 / 70件がScore `4`で完了した。Candidate147比の中央値はall-agent tokenが`+4.32%`、elapsedが`-6.70%`だった。この測定結果は[別result](../evaluations/results/candidate259-same-artifact-second-continuation-exclusion-standard14-n5_2026-08-15.md)へ保存し、本監査で固定した設計原則衝突を変更しない。

`candidate259_f04_result_preserved / design_principle_conflict_recorded / standard14_n5_completed / quality_passed / adoption_not_decided / release_not_created / projection_not_performed`
