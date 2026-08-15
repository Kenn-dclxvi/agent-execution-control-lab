# Candidate230 A02・F02・F03 N=5結果

## 結論

Candidate230は15 / 15件がvalidかつrateableで、15 / 15件がScore `4`だった。判断責任者の記載だけから独立した担当を起動する経路は0 / 10件だった。一方、開始状態の結果に影響されないreadを結果受領後まで未発行にした経路がA02の2 / 5件に残った。作成前に固定した停止条件に従い、`mechanism_failed / stopped`とし、Standard14、追加N、採用、release、projectionへ進まない。

同じ3ケースで比較すると、Candidate228と残存失敗機能はA02の1機能で同数だが、失敗runは5件から2件へ減った。固定した比較順では、利用者提示の別AI訳であるCandidate230の方が仕上げやすい。ただし、C147の「同じmodel stepで発行する」という文を残しただけでは、開始identityとreadを常に同じ判断から発行する境界にはならなかった。

## 一次結果

- registered result: `d90d4257c5c1451ab2119e9fa5367cf8`
- prompt identity: `the-caption-3ce91a4-reader-ai-plain-japanese-translation-r1`
- bundle SHA-256: `b7f9374e6d7d239472b69f4666de20ab5d6ed31bfc3e6bfa6aad12e572768f78`
- compatibility key: `ecad7b450511697e60b62d3b93db7b2fe06dacf667ed8634033e42cba0d8b718`
- valid / excluded / error: `15 / 0 / 0`
- Score: `4 = 15`
- all-agent token中央値: `426,185`
- elapsed中央値: `259.1057391669892`秒

互換なCandidate147の対象3ケースresult `0444608873624c8ab9e39726769f542d`は、token中央値`390,297`、elapsed中央値`238.3117350002285`秒である。Candidate230は記述差としてtoken `+9.20%`、elapsed `+8.73%`だった。機序不通過のため、この差を改善効果として扱わない。

Candidate228の同じ3ケースresult `7ae274532e454377bab8e715c6380b5b`と比べると、token中央値は`-49.64%`、elapsed中央値は`-17.60%`だった。品質は同じであり、A02の機序失敗は5件から2件へ減った。

## 機序判定

A02のiteration 1、2、5では、開始identity確認と必要なreadが一つのcommandまたは同じ判断から発行され、途中の結果を次の発行判断へ使っていない。iteration 3、4では、開始identityの結果がモデルへ返った後に追加readを発行した。A02は`3 / 5 passed、2 / 5 failed`である。

F02とF03では、10件すべてで判断責任者名から起動された独立producerは0件だった。この機序は`10 / 10 passed`である。

## 仕上げやすさ

事前に固定した順序で比較すると、Candidate228と失敗機能数は1機能で同じ、失敗run数はCandidate230が2件、Candidate228が5件である。このためCandidate230を、現時点で仕上げやすい方と判定する。Candidate229はA02だけの補助比較だが、同ケースの失敗は4 / 5件であり、Candidate230の2 / 5件の方が少ない。

残る差分はC147の`DECISION_BOUNDARY`のうち、開始identity結果がreadの対象も権限も変えない場合に、そのreadを開始identityと同じmodel stepから発行する局所規則である。13項目全体の再翻訳は不要で、この局所だけを次の修正対象にできる。

## 状態

`targeted_n5_completed / quality_passed / criterion_owner_producer_gate_passed_10_of_10 / result_effect_scope_failed_2_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`

一次の数値は[登録result](d90d4257c5c1451ab2119e9fa5367cf8.json)、個別採点は[品質監査](candidate230-reader-ai-plain-japanese-translation-targeted-n5-quality-audit-r1.json)、機序のrun対応は[機序監査](candidate230-reader-ai-plain-japanese-translation-targeted-n5-mechanism-audit-r1.json)を正本とする。
