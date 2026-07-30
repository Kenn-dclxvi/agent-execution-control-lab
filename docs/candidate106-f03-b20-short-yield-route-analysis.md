# Candidate106 F03 B20 short-yield経路分析

## 結論

Candidate106で残ったF03の1件は、full validationを未発行のままmessageを挟んだ経路ではない。full validationを含むcustom exec wrapperが開始済みだったが、wrapper outerへ`yield_time_ms=1000`を明示したため1秒でnonterminal resultがmodelへ返り、その再入時に進捗messageを生成した経路である。

Candidate104 / Candidate106のF03各100件を同じ観測軸で再分類した結果、途中message全12件はすべて`yield_time_ms=1000`を明示し、`Script running with cell ID`を返したrunだった。短時間yieldを使わなかった157件の途中messageは0件だった。

したがって、次の制御対象はprompt方式一般やfull validationの発行順ではない。validation wrapperの意図的なearly yieldを許可する判断と、nonterminal再入後に`wait`よりcommentaryを選ぶ判断の二段階である。

## 対象と証拠

- comparison result: [`Candidate104 / Candidate106 F03・F08 N=5 B20`](../evaluations/results/candidate104-candidate106-validation-terminal-wait-v14-medium-f03-f08-continuous-n5-b20-cli0146_2026-07-30.md)
- case: `TC-F03-ATOMIC-CONTEXT-CLEANUP/r2`
- prompt: Candidate104 / Candidate106
- repetition: 各prompt `N=5 × B20 = 100 run`
- Candidate106違反run: `db37cda875434f2abb2bf64d5c20c232`
- campaign: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate104-candidate106-validation-terminal-wait-v14-medium-f03-f08-continuous-n5-b20-cli0146-20260730-r1`
- 機械分類artifact: campaign内`route-deep-dive.json`
- 機械分類artifact SHA-256: `b256799ccfc22bab61166743ad57632b7dd918db8f6be4fc5fad30f21a6268f2`
- 機械分類script SHA-256: `e18da42131d2a2fa7a0989170d7136930e4123fd0bd26065972a8c4c4cb200e7`

raw rolloutと機械分類scriptはverification checkoutまたはCodex session storageへ保持し、このrepositoryへcommitしない。

## event順序の訂正

Candidate106違反runの実順序は次である。

1. focused validationがexit code `0`で完了した。
2. 同じcustom exec wrapper内でfull validationを開始した。
3. wrapper outerに明示した`yield_time_ms=1000`が先に満了した。
4. `Script running with cell ID 4`がnonterminal resultとしてmodelへ返った。
5. modelが「同じ検証票内で進行中」と進捗messageを生成した。
6. full validationがexit code `0`で完了した。

従前のresult文書にあった「message後にfull validationを発行した」という説明は誤りである。required commandの順序とfail-stopは成立していた。違反したpredicateは、nonterminal wrapper result後に進捗messageを挟まないことである。

## 全200件の分類

| prompt | F03 run | outer `yield_time_ms=1000` | `Script running`返却 | 途中message | 1秒yieldなしの途中message |
| --- | ---: | ---: | ---: | ---: | ---: |
| Candidate104 | `100` | `28` | `28` | `11` | `0 / 72` |
| Candidate106 | `100` | `15` | `15` | `1` | `0 / 85` |
| 合計 | `200` | `43` | `43` | `12` | `0 / 157` |

短時間yieldを選んだ後の途中message率はCandidate104の`11 / 28`（`39.3%`）からCandidate106の`1 / 15`（`6.7%`）へ下がった。短時間yield自体の選択率も`28%`から`15%`へ下がった。Candidate106は二段階の両方へ作用したが、どちらも完全には閉じなかった。

`yield_time_ms=1000`は途中messageの十分条件ではない。Candidate104で17件、Candidate106で14件は、同じnonterminal返却後もmessageを生成せずterminal resultへ進んだ。一方、全12違反に共通する直接の再入条件であり、短時間yieldなしの違反は0件だった。

## 原因判定

事実：

- Candidate106本文は「意図的な短時間yieldを使わない」と明記していた。
- 唯一の違反runはwrapper outerへ`yield_time_ms=1000`を明示した。
- nonterminal返却後、terminal resultを待つ前にcommentaryを生成した。
- full validationはcommentary前に開始済みで、最終的に成功した。

解釈：

- C106は望ましい意図を記述したが、outer tool argumentの許可状態とnonterminal再入後の次actionを一意な状態遷移へbindしていない。
- 「terminalまで待つ」は、途中経過を説明してから待つ余地を実行者に残した。違反message自身も「完了まで待つ」と宣言している。
- 実測結果から必要なのは、待機の意図を重ねることではなく、early-yield生成と再入後actionを直接制約することである。

この分析からは、prompt制御でゼロにできない、executor変更が必要、またはpre-validation diff / statusが原因だとは判断しない。pre-validation commandを含むCandidate106 runは3件あり、2件は途中messageなしで完了した。Candidate104の違反11件中9件はfocused前commandが0件だった。

## 次Candidateの最小変更軸

次Candidateを作る場合はCandidate106を直接親とし、`VALIDATION_PLAN`のnonterminal wrapper transitionだけを置換対象にする。設計案は次である。

```text
validation wrapperのouter early yieldを禁止する。outer yield deadlineは内部required commandの
wait deadlineより短くせず、未固定ならouter yield_time_msを指定しない。wrapperがcell ID付きの
nonterminal resultを返した場合、terminalまで許可する次actionは同じcell IDへのwaitだけである。
commentary、進捗報告、判断、別toolを先に発行しない。
```

これは提案であり、Candidate identity、bundle、profile、評価結果、採用状態ではない。次Candidateを作成する場合に、文言をさらに短くするか、tool argumentまで固定するかを作成前gateで決める。
