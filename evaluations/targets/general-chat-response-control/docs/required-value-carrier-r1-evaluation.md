# RequiredValueCarrier r1 評価記録

## 結論

`RequiredValueCarrier r1`は、baselineで観測した「保持必須値を回答へ運ばずに完了する」経路に対し、targeted N=5、固定8 Case各N=5、targeted N=20の全gateを通過した。

これは固定8 Case内の局所Candidate評価通過である。後続のcoverage監査により、C147の13制御を網羅する統合チャットCandidateは未作成であり、総合評価も未開始と判定した。現在解釈は[`C147チャット向けcoverage評価 r1`](c147-chat-coverage-assessment-r1.md)を正とし、採用、release、利用先へのprojectionまたはC147の一般化を意味しない。

## 系譜と差分

- 直接の親: `chat-control-free-r1`
- Candidate: `required-value-carrier-r1`
- 追加差分: 利用者が与えた保持必須値を回答へ運ばないまま、その値に依存する話題を完了できないようにする三文
- 継承しないもの: C147原文、コード変更工程、成功runの文章構成、質問・根拠取得・分担・検証の制御

## baseline

`chat-control-free-core-r1-n5-baseline-r1`は40 / 40件がvalidだった。品質4は36件、品質3は4件で、4件はすべて`GCR-Q02`だった。`GCR-Q02`は品質4が1 / 5件で、残る4件は回答済み集合を正しく選んだ一方、入力の保持必須数値を本文へ運ばなかった。

他の7 Caseは35 / 35件が品質4であり、質問過多、不要な根拠要求、独立話題の停止、受領済み根拠の再要求または内部状態名の露出は観測されなかった。

## Candidate結果

| 評価 | valid | 品質4 | gate |
| --- | ---: | ---: | --- |
| `GCR-Q02` targeted N=5 | 5 / 5 | 5 / 5 | 通過 |
| 固定8 Case各N=5 | 40 / 40 | 40 / 40 | 通過 |
| `GCR-Q02` targeted N=20 | 20 / 20 | 20 / 20 | 通過 |

総合N=5では、`GCR-Q02`が5 / 5件で全保持必須値を運び、他の7 Caseも35 / 35件で品質4を維持した。targeted N=20でも質問、根拠要求または未解決集合を増やさず、20 / 20件で品質4だった。

## KPI

固定8 Case各N=5の平均は、baselineが品質`3.90`、all-agent token `12,257.02`、経過時間`7.892秒`、Candidateが品質`4.00`、all-agent token `12,407.62`、経過時間`7.992秒`だった。

これはN=5の記述統計であり、tokenまたは時間の安定した増減傾向とは扱わない。局所`GCR-Q02`のbaselineとCandidateは別runであり、品質改善以外の差をCandidate効果として確定しない。

## 実行基盤の履歴

- r1: 共有`CODEX_HOME`のskills更新競合とmodel cache互換不一致で8 / 8件が外部失敗した。
- r2: 一時`CODEX_HOME`へ隔離したが、stdout error eventを結果へ保存せず原因を確定できなかった。
- transport probe r1: schemaの`const`にAPIが要求する`type`がなく、一回だけのprobeは`unavailable`となった。同じprobeは再実行していない。
- r3: schema projectionを修理して8件のmodel responseを得たが、CLI JSONLに`usage.total_tokens`がなく8 / 8件を`unrateable`として保存した。
- r4: 有効なbaseline測定前にtoken契約をr2へ改訂し、`total_tokens`がない場合は`input_tokens + output_tokens`、cached inputは二重加算しないことを固定した。これ以降に初めて有効なbaselineを成立させた。

失敗したattemptはCaseまたはCandidateの品質結果として使わず、write-once履歴として保持する。

## lifecycle

- Candidate設計: 固定済み
- 局所targeted N=5: 通過
- 局所固定8 Case N=5: 通過
- 局所targeted N=20: 通過
- C147チャットcoverage: 未完了
- 統合Candidate: 未作成
- 総合評価: 未開始
- 採用資格: なし
- release: 未作成
- projection: 未承認

総合N=20、N=100、採用、releaseおよび利用先への反映は、今回の局所評価通過から発行しない。
