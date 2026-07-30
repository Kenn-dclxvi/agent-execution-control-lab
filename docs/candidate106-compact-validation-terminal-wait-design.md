# Candidate106 短縮validation terminal待機設計

## 結論

Candidate106はCandidate104を直接親とし、`VALIDATION_PLAN`一規則だけを置換する。

Candidate104の既存実行票制御を維持し、追加する意味を「意図的な短時間yieldを使わない」「nonterminal result後は同じsessionのterminalだけを待つ」の二つへ限定する。Candidate105に含めたwrapper構造、stop condition、result返却、例外処理の再説明は削除する。

## Identityと状態

- candidate number: Candidate106
- prompt identity: `the-caption-3ce91a4-compact-validation-terminal-wait-r1`
- direct parent: `the-caption-3ce91a4-staged-evidence-admission-r1`
- changed target: root `AGENTS.md`
- changed predicate: `VALIDATION_PLAN`の置換
- bundle SHA-256: `127e4246b1c0443c53b44aebcbda31cc3e63cf2a1a640769f47ee77adc8661e1`
- root prompt差: Candidate104比 `+104`文字。Candidate105の`+314`文字から`210`文字削減
- evaluation status: `targeted_f03_evaluated / mechanism_gate_passed / standard14_evaluated / quality_gate_passed / result_registered / adoption_not_decided`
- release: `not_created`
- runtime projection: `not_projected`

## 作成前gate

1. 基準promptはCandidate104とする。
2. 最短正常経路は、Candidate104の既存実行票に従い、required validationと完了判定用diff / statusを順に実行し、全result受領後に一度だけ完了判断する経路とする。
3. Candidate105 Standard14 N=5では、F03の検証後再取得なしがCandidate104の2 / 5から4 / 5へ増えた。一方、Candidate105 minus Candidate104の集約中央値はtoken `+0.70%`、elapsed `+2.65%`だった。
4. F05 clarifyは両promptとも4 command / 2 messageで出力量もほぼ同一だったが、Candidate105はtoken中央値が`+418`だった。Candidate105のroot promptはCandidate104より314文字長く、実行routeを変えないcaseにも読解costが流入した。
5. Candidate104のTaskSpec、repository authority、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`は検証集合、順序、完了後追加tool禁止を既に固定している。追加で必要なのは、外側wrapperへ意図的な短時間yieldを選ぶ判断と、nonterminal受領後に別判断へ戻る経路を閉じることだけである。
6. 置換するpredicateは`VALIDATION_PLAN`一つとし、Candidate104本文へ短時間yield禁止と同一session terminal待機だけを統合する。
7. 消す判断点は、意図的な短時間yieldの選択と、nonterminal result後の進捗報告・別tool選択である。
8. 新たに増える判断点は、受領resultがterminalかnonterminalかというmachine-boundな一つだけである。
9. F03 r2、Rating v14、Medium、N=5で、score `4`、required command evidence、意図的な短時間yield 0、validation中進捗message 0、required validation再実行 0を確認する。
10. いずれかが5 / 5で成立しなければ停止し、Standard14へ進めない。全条件を満たした場合だけStandard14を次の独立評価として判断する。

## 変更する規則

```text
VALIDATION_PLAN: artifact変更後の検証開始前に、required validationと完了判定に必要と確定している
diff / status等を一つの実行票へ順にbindする。検証success後はmodelへ戻らず実行票の残りを発行し、
全result受領後に一度だけ完了を判断する。実行票完了後はTaskSpec追加要求またはresult失効がない限り
toolを追加しない。実行票は意図的な短時間yieldを使わずterminalまで待つ。nonterminal resultが返った場合は、
判断 / 進捗報告 / 別toolを挟まず同じsessionのterminalだけを待つ。
```

## 非目標

- TaskSpec、required validation、evaluation set、fixture、ratingの変更
- commandのshell compound化
- tool result truncation、output cap、raw log保存、executor hookの変更
- validation以外の長時間command制御
- 採用、release、THE-CAPTION本体反映

## 最初の試験

- case: F03 r2
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI: `0.146.0`
- repetition: `N=5`
- profileへ固定する並列上限: `M=24`
- readyなslot: 5件
- 実際の同時実行数: 最大5件
- Candidate104: 新規実行しない。保存済みtraceをmechanism基準として使う

## 評価結果

F03 N=5は5 / 5 score `4`だった。5件すべてでfocused validationとfull validationを各一回だけ実行し、その間にmodel messageを挟まず、required validationも再実行しなかった。検証後のdiff / status再取得も0 / 5であり、作成前mechanism gateを通過した。

続くStandard14 N=5は70 / 70件がvalid・rateable・score `4`で、excluded attemptは0件だった。Candidate104比の5 iteration集約中央値はtoken `-44,115`（`-2.52%`）、elapsed `-59.410`秒（`-6.38%`）だった。Candidate105比ではtoken `-56,372`（`-3.20%`）、elapsed `-84.079`秒（`-8.80%`）だった。

詳細は[`Candidate104 / Candidate105 / Candidate106 Standard14 N=5 result`](../evaluations/results/candidate104-candidate105-candidate106-compact-validation-terminal-wait-v14-medium-standard14-n5-cli0146_2026-07-30.md)を正本とする。

続く[`Candidate104 / Candidate106 F03・F08 N=5 B20`](../evaluations/results/candidate104-candidate106-validation-terminal-wait-v14-medium-f03-f08-continuous-n5-b20-cli0146_2026-07-30.md)は両promptとも200 / 200件がvalid・rateable・score `4`だった。F03でfocused validation完了からfull validation完了までにmessageを挟まなかった割合はCandidate104の89 / 100からCandidate106の99 / 100へ改善した。一方、Candidate106でfull validation開始後のnonterminal wrapper resultとterminal resultの間に進捗messageを挟む対象経路が1件再発した。F03・F08のtokenとelapsedには有意差がなかった。事前のzero-regression gateに従い、現在状態を`targeted_f03_f08_b20_evaluated / quality_gate_passed / route_stability_gate_failed / cost_no_significant_difference / stopped`とする。Standard14 B20、採用、release、runtime projection、本体反映へ進めない。後続のevent順序訂正と二段階原因分析は[`Candidate106 F03 B20 short-yield経路分析`](candidate106-f03-b20-short-yield-route-analysis.md)へ分離する。
