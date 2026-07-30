# Candidate99 判断証拠境界の設計

## 結論

Candidate99はCandidate98を直接親とし、predicate判断へ流入できる証拠の境界を一規則だけ追加する。

tool、読取回数、command順序は固定しない。TaskSpec、repository authority、対象artifact、required evidenceへbindされた入力でpredicateを判定できる間は、履歴、広域探索、無関係なtool outputをそのpredicateの判断材料へ追加しない。不足時だけ、未取得証拠とその消費先predicateを先に固定して入力範囲を広げる。

## Identityと状態

- candidate number: Candidate99
- prompt identity: `the-caption-3ce91a4-decision-evidence-boundary-r1`
- direct parent: `the-caption-3ce91a4-validation-completion-sheet-r1`
- changed target: root `AGENTS.md`
- changed predicate: `EVIDENCE_SCOPE`の追加
- evaluation status: `not_evaluated`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate98とする。
2. 最短正常経路は、TaskSpec、適用authority、編集対象、成果判定に直接必要な現在実体を読み、変更predicateを一度判断し、C98の実行票で検証と完了証拠を閉じる経路とする。
3. 保存済みC81 Standard14 B20のF07 100件では、elapsedが`57.155〜149.407秒`、tokenが`103,590〜321,388`へ分布した。最短traceはcommand 6件・message 4件、最長traceはcommand 21件・message 6件だった。最長側だけが追加の局所authority、検証script、tests、src、`git log`、文字列履歴、完了証拠の再取得を判断入力へ入れた。command出力は`212,315 → 229,995 bytes`で差は`+8.3%`にとどまる。
4. Candidate98 Standard14のF07 N=5でも、elapsedは`75.625〜132.423秒`、tokenは`135,619〜250,722`、commandは9〜17件に分かれた。fixture identityがC81 B20と異なるためKPIの正式比較には使わないが、変更前の判断入力が反復ごとに広がる経路は両promptで観測した。
5. F07 TaskSpecはcurrent authority、`run.sh`、周辺routing維持、required validationを既に指定する。現在実体から変更predicateを判定できた後の履歴・広域探索を禁止する境界はTaskSpecにもCandidate98にもない。
6. 追加するpredicateは、判断入力をbind済みのTaskSpec範囲、repository authority、target artifact、required evidenceへ限定し、不足時だけ未取得証拠identityとconsumer predicateを先にbindして入力追加を許す`EVIDENCE_SCOPE`一つとする。
7. 消す判断点は、現在実体で変更predicateを判定できた後に、履歴、広域検索、検証script本文、無関係なtool outputをさらに判断材料へ入れるかという分岐である。
8. 新たに増える判断点は、bind済みpredicateに未取得のrequired evidenceがあるかという一分岐だけである。これはTaskSpec、authority、target artifact、required evidence identityから直接判定し、将来riskや探索の利便性から作らない。
9. 品質と狙った境界はF07 r2、Rating v14、Medium、CLI `0.146.0`、candidate-only `N=5`で確認する。5 / 5 score `4`、required command evidence 5 / 5、root-only、履歴入力0件、predicateへbindされない広域探索0件、理由を先にbindしない追加入力0件を必須とする。
10. 一件でも品質未達、必要証拠欠落、許可外変更、履歴または広域探索の流入、境界確認不能があれば停止する。targeted gate通過前にStandard14またはB20へ進めない。

## 境界制御としての位置付け

この規則が制御するのはcommand名や読取回数ではなく、predicateが消費できる入力の所属である。

- TaskSpecはrequired outcome、permission、target、required validationを定める。
- repository authorityとtarget artifactは現在の判断事実を供給する。
- `EVIDENCE_SCOPE`は、そのpredicateへ流入できる証拠と、入力範囲を広げられる条件を定める。
- executorのoutput cap、tool result配送、atomicityは対象外とする。

したがって、同じ証拠を一括または個別に読む方法はexecutorへ残す。現在入力で判定不能なら追加readを許すが、その前に未取得証拠identityと消費先predicateを固定する。単なる利便性、念のため、将来の可能性は入力拡張の根拠にしない。

## 非目標

- TaskSpec、repository authority、required validationの変更
- read command、tool call、message、tokenの上限設定
- 特定pathやF07固有commandのprompt本文への列挙
- 成功stdoutの配送制御
- Candidate97の再利用または改訂
- 採用、release、THE-CAPTION本体反映

## 次の評価境界

評価を開始する場合は、実行前に基準resultを一意にbindし、C81 B20で固定されたLayer 1、全fixture identity、TaskSpec、case revision、rating、model、reasoning、CLI、permission、executor parameter、設定上の`M=24`、`N=5`を機械照合する。完全一致のpreflight receiptがない場合は一件も発行しない。

targeted F07で品質と境界が5 / 5成立した場合だけ、同じ固定Layer 1のStandard14へ進める。B20はStandard14の品質とcase別経路を確認した後の別gateとする。
