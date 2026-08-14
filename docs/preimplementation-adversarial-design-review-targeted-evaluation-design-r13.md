# 実装前の情報封鎖敵対的設計レビュー Target評価設計 r13

## 目的

必要な独立reviewを完遂しながら、review sourceのobservable outputをsource読取前にrecipient別・scope別のexact carrierへ閉じられるかを評価する。

## r11からの狭い差分

一般設計、authority、boundary、fixtureの意味、review criterion、allowed disposition、oracleおよび期待terminalはr11から変更しない。TaskSpecへsource外の`review_scope_carrier_contract/v2`を追加する。

同contractは、source containerを読む前に次を固定する。

- rootへ返せるexact structural target
- packetへ配送できるroot observation
- required review scopeごとの必要命題
- 各必要命題を支えるpacket observationまたはreviewer direct observation
- reviewerへ直接返せるexact target
- 対応表にないmanifest target、container、ancestorおよびmixed-recipient outputの禁止
- target missing時の`missing` result

## scope別carrier

| case | reviewer direct carrier |
| --- | --- |
| ADR01、ADR02 | 空集合 |
| ADR03〜ADR06 | `consumer_inventory`、`consumer_contracts` |
| ADR07、ADR09 | `paired-scope-evidence.json` |
| ADR08 | 空集合 |

root carrierはidentity、task contract、authority、boundary normative contract、general design semantic、boundary ledger、required validation、review contract、artifactsおよび必要時のuntrusted prior resultへ閉じる。consumer inventory、consumer contractsおよびhistoryはroot outputへ含めない。

## oracleと停止条件

期待terminalとartifact routeはADR9 r2から変更しない。missing paired evidenceをfixtureへ追加しない。

品質、reviewer cardinality、review result admission、result effect、root delivery、reviewer deliveryおよびforbidden inputを独立に判定する。一件でも不一致なら有効runを保持して停止する。
