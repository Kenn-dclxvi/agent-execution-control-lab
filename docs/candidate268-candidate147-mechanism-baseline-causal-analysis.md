# Candidate268・Candidate147機序基準線と原因分析

## 結論

次Candidateの機序合格線を一律100%にはしない。対象機序ごとに、同じ四ケース各N=5で観測したCandidate147の実測率を基準線にする。Candidate147が100%だった機序だけ100%を要求し、100%でなかった機序を次Candidateだけ100%へ引き上げない。

この基準で見ると、Candidate268の未達は二種類へ分かれる。

1. F02共同発行はCandidate147の5 / 5に対してCandidate268が4 / 5であり、基準未達である。次案ではC268の既存境界を変更する。ただし、C268本文は失敗runの分離をすでに禁止しており、別のprompt準拠な誤経路はまだ特定できていないため、同じ禁止文を追加するのではなく、原因を特定したうえで既存文の置換、配置変更または依存関係の再接続を行う。成功runのtool順は変更内容の根拠にしない。
2. nonterminal resultのterminal dependencyは、Candidate147で観測したnonterminal 4 runすべてが同じ完了を待ったのに対し、Candidate268は13 runすべてで待たなかった。C147にあった一つの外側実行内でvalidationを完遂するcarrierがC268の自然語化で失われ、未完了resultを受け取った後の`wait`指示だけが残った構造差と対応する。

したがって、現在もっとも原因が絞れているのはterminal closureである。F02は基準未達として残すが、追加条件Candidateを作れる原因特定にはまだ届いていない。

## 比較対象と数え方

- 直接の実装基盤はCandidate268とする。
- Candidate147は機序ごとの基準線とKPIの比較対象に限り、本文の複写元にしない。
- F01からF03は、開始identity resultが外側の次判断へ返る前に、開始確認と許可済みreadの両方が発行対象へ固定されたrunを合格とする。
- F10 instruction境界は、exact `src/AGENTS.md`のterminal success content resultより前に`src/`配下listingまたは本文readを発行しなかったrunを合格とする。
- terminal dependencyは、cell IDを伴うnonterminal resultを受けたrunだけを分母とし、そのresultをterminal扱いせず同じ完了だけを待ったrunを合格とする。
- external `wait`が発生しなかった割合とterminal dependencyを混同しない。前者はruntime返却時機を含む診断分布であり、後者はnonterminal resultを受けた後の処理境界である。
- truncationなしの割合はcarrier診断であり、現時点のCandidate作成gateにはしない。

## C147実測に合わせた基準線

| 観測項目 | Candidate147 | Candidate268 | 次Candidateの基準線 | 現在判断 |
| --- | ---: | ---: | ---: | --- |
| F01 開始確認・許可済みread共同発行 | 5 / 5 | 5 / 5 | 5 / 5 | C268は到達 |
| F02 開始確認・許可済みread共同発行 | 5 / 5 | 4 / 5 | 5 / 5 | C268は1件未達 |
| F03 開始確認・許可済みread共同発行 | 5 / 5 | 5 / 5 | 5 / 5 | C268は到達 |
| F10 instruction result先行 | 2 / 5 | 5 / 5 | 2 / 5以上 | C268の5 / 5を観測効果として保持するが、100% gateにはしない |
| F10 result後の必要read完遂 | 5 / 5 | 5 / 5 | 5 / 5 | 両方到達 |
| nonterminal resultのterminal dependency | 4 / 4 | 0 / 13 | 観測したnonterminal runの100% | C268は未達 |
| external `wait`なし | 16 / 20 | 20 / 20 | 機序gateにしない | C268の0 waitはterminal違反を含むため改善扱いしない |
| F02 truncation後の追加readなし | 3 / 5 | 0 / 5 | 現時点では機序gateにしない | carrier課題として診断継続 |

F10のCandidate147 2 / 5は、5件中3件でinstruction result前に配下readが発生したことから算出した。Candidate268の5 / 5はC268で獲得した正の効果だが、C147が100%でなかったこの項目を理由に、次Candidateへ5 / 5を一律の機序合格線として課さない。

external `wait`なしは、同じ四ケース各N=5のCandidate147で4 run・6回のwaitが発生したため16 / 20である。Candidate147 N=100の同じ四ケースではwait発生が60 / 400件だったが、これは異なるNの安定性診断であり、初回N=5の基準線と混ぜない。

## F02共同発行の原因分析

Candidate268 F02の成功4件と失敗1件は、同じcase、fixture、TaskSpec、prompt identityおよびpermissionで実行された。失敗run `8e4ed55acc854576b0c880f7adc380c2`は開始identity確認resultを受け取った後に四つの許可済みreadを発行した。

C268の`DECISION_BOUNDARY`は次の二点をすでに明示している。

- 開始状態の不一致が変更と必須検証だけを止める場合、開始確認resultを許可済みreadの開始条件にしない。
- 開始確認と必要readを同じmodel stepから発行する。

したがって、現在の保存traceから、失敗runがprompt準拠のまま通れる別のpermissionまたはdependency分岐は特定できない。成功4件のcommand分割、command文字列、read順または説明文を次の手順へ転記しても、失敗runを構成不能にはできない。

一方、Candidate147の形式表現は、開始identity resultが影響できるoperation classを変更と必須検証へ限定し、許可済みreadをその集合の外へ直接置いていた。Candidate268は同じ関係を自然語で記述しているが、一件でその対応が実行へ反映されなかった。現段階で言えるのは、自然語化した関係の実行安定性がC147の5 / 5へ届かなかったことまでであり、追加すべき条件まではbindできていない。

F02について次に必要なのは、本文の同義反復ではなく、C268の成功4件と失敗1件を分けるmodel-visibleな入力、適用中の別instruction、発行対象の構成またはresult dependencyが存在するかの確認である。差を特定できた場合は、その差を許したC268の既存境界を置換または再配置する。差を特定できない場合はF02だけを根拠に推測の変更を加えず、原因を特定済みのterminal carrier変更を先に進める。

## terminal closureの原因分析

C147とC268は、一般的なterminal条件とnonterminal result後の待機禁止事項をどちらも持つ。しかし、validationの結果をモデルへ返すcarrierが異なる。

Candidate147の`VALIDATION_CLOSURE`は、rootがproducerの場合、順序のある全required validationを一つのcustom exec wrapper内で個別`exec_command`として発行し、全件が完了してから一度だけmodelへ返す構造を固定していた。これにより、通常は途中resultを外側modelへ返さず、wrapper自体がnonterminalになった場合だけ同じcellを待つ関係になっていた。

Candidate268の自然語本文は、各validationを区別できる個別実行にし、途中でmodelへ戻らないことを要求する一方、全件を一つの外側実行へ束ねるcarrierを固定していない。その後の`VALIDATION_PLAN`には、cell ID付きnonterminal resultなら同じcellへの`wait`だけを行うとあるが、これはnonterminal resultがmodelへ返った後の禁止であり、途中resultを返さない実行構造そのものではない。

開いている関係は次のように整理できる。

`validation ticket -> 個別invocationを外側carrierへ束縛しない -> 個別resultがmodelへ返る -> nonterminal resultを受け取る -> wait指示を守らず別toolまたはfinalへ進める`

C268ではこの経路が13 runで現れ、3件は別`exec`へ進み、10件は追加toolなしで終了した。C147では同じ四ケースでnonterminalになった4 runすべてが同じ完了を待った。これはC147の基準線が100%だった項目なので、次Candidateでも、実際にnonterminal resultを受けたrunについて100%のterminal dependencyを要求できる。

ただし、成功runのwait回数、待ち時間またはcommand順を指示へ転記しない。分析から次設計へ渡せるのは、個別validationを一つの外側terminalへ束縛するcarrierの欠落であり、external waitを0件にすることではない。

## KPI差との対応

Candidate268のroot本文は14,607 bytes、Candidate147は10,772 bytesで、C268は3,835 bytes、35.60%大きい。四ケース合算ではC268がC147比でtoken `+28.06%`、elapsed `+10.02%`だった。全四ケースのtoken中央値がC147より28.52%から43.97%高いため、固定model-visible入力の増加は全体差と整合する。ただし、byte差だけでtoken差の全量を因果帰属しない。

F02ではCandidate147が2 / 5件でtruncation後の限定追加readを行ったのに対し、Candidate268は5 / 5件でtruncationを観測し、token中央値はC147比`+43.97%`だった。これは固定入力差に加え、carrier容量未拘束がF02の局所増加へ対応する証拠である。

terminal closureを守らなかったC268の0 waitは、合法な再入費用を削減した結果ではない。terminal dependencyを回復すると、外側carrierを回復せず単にwait指示だけを強めた場合はmodel再入とtokenがさらに増える可能性がある。したがって、terminal closureの次差分は、待機命令の反復ではなく、一つの外側terminalへ個別validationを束縛する自然語上の関係を対象にする必要がある。

## 分析から固定する次の順序

1. terminal closureは原因となるcarrier欠落まで特定できたため、C268上で最初に設計可能性を検討する。
2. F02はC147基準5 / 5に未達である。原因を特定した後、C268の既存共同発行境界を置換、再配置または別dependencyへ接続する。同じ禁止文だけを追加するCandidateにはしない。
3. F10 instruction先行はC147基準2 / 5以上とし、C268の5 / 5を100%必須gateへ自動昇格させない。
4. external waitなしとtruncationなしは、C147が100%でないため一律100% gateにしない。terminal dependencyとcarrier診断から分離する。
5. 次Candidate bundle、profileおよび評価枠はまだ作成しない。まずterminal carrierの自然語差分が、C268のF01からF03とF10正常経路を遮断せず、問題経路を構成不能にするかを作成前gateで確認する。

現在状態は`analysis_complete / candidate268_direct_base / c147_per_mechanism_baseline_fixed / blanket_100_percent_gate_forbidden / f01_f02_f03_baseline_100_percent / f10_instruction_baseline_40_percent / f10_completion_baseline_100_percent / terminal_dependency_conditional_baseline_100_percent / external_wait_absence_not_mechanism_gate / truncation_absence_not_mechanism_gate / terminal_carrier_gap_identified / f02_legal_failure_route_not_identified / candidate269_not_created`とする。

## 一次証拠

- [`Candidate147 F01・F02・F03 N=5`](../evaluations/results/candidate145-candidate147-result-effect-scope-v14-medium-f01-f02-f03-atomic-n5-cli0146_2026-08-02.md)
- [`Candidate147 Standard14 N=5`](../evaluations/results/candidate125-candidate145-candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)
- [`Candidate267・Candidate264・Candidate147 cost再入原因監査`](candidate267-candidate264-candidate147-cost-reentry-causal-audit.md)
- [`Candidate268四ケースN=5`](../evaluations/results/candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)
- [`Candidate268機序監査`](../evaluations/results/candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)
- Candidate147およびCandidate268の保存済みatomic runとcompact trace
