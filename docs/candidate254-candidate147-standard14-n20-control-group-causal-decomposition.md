# Candidate254とCandidate147のStandard14 N=20制御群別原因分解

## 結論

Candidate254のStandard14 N=20は280 / 280件でScore `4`を維持したが、Candidate147との同数比較ではtokenが`+9.33%`、経過時間が`-6.48%`だった。増加を一つの原因へまとめず、次の三群へ分ける。

1. F02とF03の完了待ち、およびF03の開始確認とreadの分離は、AIが追加で動いた実行経路の費用である。完了待ちの頻度差はCandidate254の本文差分へ帰属できない。一方、開始確認とreadの分離については、C147でこの経路を0 / 15件にした`result_effect_scope`の明示的な関係が、C254では自然文の行動説明へ短縮されている。C254 F03で6 / 20件再発した事実は、この関係の欠落を改善候補として扱う根拠になる。
2. F07 canonical、F05二ケース、F07 dependency、F10 monthlyでは、AIの応答回数と主要な実行経路がCandidate147と同じままtokenが増えた。ここは追加手順ではなく、長くなったmodel-visible本文を同じ回数だけ入力する固定費が主な候補である。
3. A01ではCandidate254が不要な開始状態確認を省き、tokenと時間をともに減らした。Candidate254固有の`SPEC`文が、内部状態を利用者向け進捗として出力する経路を閉じた効果と対応する。ただし、一つの文だけを原因とする介入比較はまだ行っていない。

したがって、Candidate254全体をCandidate147へ戻さない。後続では一度、Candidate237でF02について成立済みの`SPEC`出力境界二文だけをC147へ移植したCandidate261を作成したが、これはCandidate254を直接の親にしておらず、本記録が要求するCandidate254の改善にはならなかった。Candidate261の固定済み本文と評価結果は履歴として保持し、現在の設計根拠には使わない。

現在の選択的な再構成では、Candidate254を直接の親とする。C147で成立した`result_effect_scope`の一般定義だけでなく、`identity_result_effect_scope = {artifact_change, required_validation}`と`authorized_read ∉ identity_result_effect_scope`を含む開始確認固有の集合関係をCandidate254へ戻す。Candidate254の`SPEC`、`EVIDENCE_GATE`、`OWNER_ROLE`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`およびその他の条項は同一byteで保持する。成功runのcommand順、待ち時間、read範囲またはwrapper構成は追加しない。

## この文書でいう原因の強さ

- **直接確認**: 追加tokenが使われたAI応答、tool結果または待機を生traceで特定できる。
- **対応を支持**: 比較対象で他の主要経路が同じであり、本文差分との対応が強い。ただし、その差分だけを切り替えた比較はまだない。
- **未解決**: tokenの使用先は分かるが、どのprompt差分がその経路を許したかは分からない。

この区別をせず、同時に変わった本文をすべて原因と扱わない。

## 比較対象

- Candidate147 N=20は、登録済みStandard14 N=100 result `e6fc6e10dedd47f5a1d59d114e6e0f57`の保存済みatomic poolから、各ケース20件を固定したselectionを使う。
- Candidate254 N=20は、N=5の70件を再利用し、不足210件を追加した登録result `2e40123a1b0642e3bbddb1812ba4414e`を使う。
- prompt以外の比較条件はcomparison key `60226e5443eee2f26127d089ce73626988b8c7aab3bb3c72b999d3b387875ce1`へ固定済みである。
- 品質は両者とも全件Score `4`である。

## 本文差分の大きさ

変更targetはroot `AGENTS.md`だけである。Candidate147は10,772 bytes、Candidate254は13,628 bytesで、Candidate254が2,856 bytes長い。主な節別差は次のとおりである。

| 制御群 | C147 bytes | C254 bytes | 差 |
| --- | ---: | ---: | ---: |
| 用語説明 | 0 | 449 | `+449` |
| `SPEC` | 1,079 | 1,836 | `+757` |
| `EVIDENCE_GATE` | 2,785 | 3,130 | `+345` |
| `OWNER_ROLE` | 1,011 | 1,790 | `+779` |
| `DECISION_BOUNDARY` | 1,077 | 653 | `-424` |
| `VALIDATION_CLOSURE` | 1,357 | 622 | `-735` |
| その他8節と見出し | 3,463 | 5,148 | `+1,685` |
| 合計 | 10,772 | 13,628 | `+2,856` |

Candidate254はC147へ一文だけ足したbyte列ではない。manifest上の`content_relation.source_prompt_identity`はCandidate253であり、Candidate253の自然文再構成を保持している。設計文書がC147を「直接の基準」としていても、C147とのKPI差には、Candidate253までに再構成された全節の表現差が入る。

## ケース別の原因分解

| ケース | KPI差 | 実行経路の比較 | 原因の現在判定 |
| --- | --- | --- | --- |
| A01 | token `-45.93%`、時間`-45.66%` | C147中央値はAI応答2回、開始状態確認1回。C254中央値はAI応答1回、確認0回で、18 / 20件が確認質問だけで終了 | `SPEC`の出力先閉鎖との対応を支持。保持候補 |
| A02 | token `+27.00%`、時間`-1.17%` | AI応答は両者4回。C254はcommand中央値が7.5から6.5へ減った一方、tool result文字数中央値は206,860から223,109.5へ増えた | 大きいread resultと長い本文の再入力。どの制御差がread量を変えたかは未解決 |
| F02 | token `+2.90%`、時間`-0.80%` | C254は7 / 20件、13回、479,174 tokenを完了待ちだけに使用 | 待機費用は直接確認。prompt差分への帰属は未解決 |
| F03 | token `+30.79%`、時間`+0.75%` | C254は9 / 20件、19回、488,719 tokenの完了待ち。開始確認とreadの分離も6 / 20件 | 二つの追加AI経路を直接確認。分離は、C147で0 / 15件だった経路の再発であり、C147のoperation class別`result_effect_scope`を復元する候補にする |
| F04 | token `-2.91%`、時間`+0.73%` | 品質を維持し、開始確認と結果非依存readを同じAI判断から発行する方向の部分効果を保持 | `DECISION_BOUNDARY`は保持。時間との交換条件なので単独で採用根拠にしない |
| F05 clarify | token `+8.81%`、時間`-7.69%` | AI応答2回、command4回、tool result量はほぼ同じ | 追加手順ではなくmodel-visible入力の固定費との対応を支持 |
| F05 deploy | token `+9.34%`、時間`-6.21%` | AI応答2回、command4回、tool result量はほぼ同じ | 同上 |
| F07 canonical | token `+25.47%`、時間`+16.53%` | AI応答は両者4回。変更前command中央値3回、変更後5回、tool result量もほぼ同じ | 入力tokenの増加を直接確認。節単位の帰属は未完了 |
| F07 dependency | token `+4.35%`、時間`-11.37%` | AI応答4回、command9回で同じ。tool result量はC254の方が少ない | model-visible入力の固定費との対応を支持 |
| F08 | token `+9.16%`、時間`+1.28%` | AI応答は両者4回。C254は変更後command中央値が6回から7回へ増加 | 固定費に加えて変更後確認が一回多い。必要性とprompt上の開放辺は未解決 |
| F10 monthly | token `+3.57%`、時間`-17.41%` | AI応答4回、command11回で同じ。tool result量はC254の方が少ない | tokenは固定費との対応を支持。時間差をprompt効果へは帰属しない |

F01、F06、F10 entrypointを含む残りのケースも全体集計へ含める。ただし、この表では、今回の原因を変え得る経路差を生traceで区別できたケースへ集中する。F10 entrypointのpath-local `AGENTS.md`確認後の対象readは、適用規則で対象または許可が変わり得るため、手数だけを理由に削減しない。

## C147で出現しなかった経路からの逆向き監査

C254で増えた経路について、C147で同じ経路が出ていない場合に、C147が何を閉じていたかを逆向きに調べた。ここで「出現しなかった」とは、単に件数が少ないことではなく、同じ判定基準で0件だったことを指す。

| 調査対象 | C147 | C254 | C147の対処を再利用できるか |
| --- | --- | --- | --- |
| F01 / F02 / F03の開始確認と初回許可readの分離 | C147 targeted N=5は15 / 15件で、開始確認の結果をAIの次判断へ返す前に両方を発行対象へ固定し、分離0 / 15件 | F03は分離6 / 20件 | **できる。** C147は、先行結果が影響できる後続操作の種類を`artifact_change`と`required_validation`へ限定し、許可済みreadへ停止効果を広げなかった。C254ではこの集合関係と「task全体または後続全部へ停止効果を広げない」が落ち、望ましい行動だけが自然文で残っている |
| F02・F03の完了待ち | C147にも存在する。targeted N=5ではF02が2 / 5件、F03が1 / 5件、Standard14全体でも検証後の追加発行が22 / 685件 | C254にも存在する | **そのまま使えるC147固有の解決はない。** C147は未完了結果を受けた後の待ち先を限定したが、途中返却そのものは消していない |
| F08の同じentrypointへの狭い再read | 2 / 20件 | 5 / 20件 | **まだできない。** C147は少ないが0件ではなく、閉鎖機構が証明されていない |
| A01の不要な開始確認 | C147中央値では開始確認後に質問 | C254は18 / 20件で確認せず質問 | **逆方向である。** ここはC254の`SPEC`出力先閉鎖を保持する |
| F07 canonicalの同じ主要経路でのtoken増 | C147も同じ主要経路 | C254は同じAI応答回数と主要command回数で入力token増 | **経路閉鎖の対処ではない。** C147の短い本文は費用の比較対象だが、行動制御として移植するものではない |

F03については、C147の対処と結果の対応が直接記録されている。C145では開始確認とreadが15 / 15件で分離した。C147は`DECISION_BOUNDARY`だけをoperation class別の`result_effect_scope`へ置換し、C147では共同発行15 / 15件、分離0 / 15件、品質15 / 15件、C145比でtoken `-25.97%`、経過時間`-22.34%`となった。これは「成功時のtool順を指示する」対処ではない。先行結果が停止させてよい後続操作の種類を限定し、影響しないreadまで待たせられる依存関係を閉じる対処である。

C254にも「同じAI判断から発行する」という行動文はある。しかし、C147にあった次の関係は逐語でも同等の構造でも保持されていない。

```text
result_effect_scope := 受領結果が対象・許可・方法・停止条件を変え得る未発行operation classの集合
decision_boundary(next_operation) := next_operation.class ∈ result_effect_scope
identity_result_effect_scope = {artifact_change, required_validation}
authorized_read ∉ identity_result_effect_scope
```

したがって、C254へ同じ禁止文を重ねるのではなく、C147で成立していた「どの種類の後続作業だけが先行結果を待つか」という関係をC254の意味体系へ戻すことが、現在特定できた追加制御点である。

## F07 canonicalで確認した固定費

F07 canonicalは、追加のAI判断がないのに大きく増えた対照である。

| 項目 | Candidate147 N=20中央値 | Candidate254 N=20中央値 | 差 |
| --- | ---: | ---: | ---: |
| 総token | 101,060 | 126,802.5 | `+25,742.5` |
| 入力token | 99,510 | 124,636.5 | `+25,126.5` |
| 出力token | 1,898 | 2,175 | `+277` |
| AI応答回数 | 4 | 4 | 0 |
| 変更前command回数 | 3 | 3 | 0 |
| 変更後command回数 | 5 | 5 | 0 |
| tool result文字数 | 164,953 | 165,024 | `+71` |

総token差の大部分は入力tokenである。tool result量とAI応答回数が同じなので、F02・F03のような追加待機では説明できない。Candidate254の長いroot本文と、それによって各応答へ残る長い会話入力が直接の使用先である可能性を強く支持する。ただし、2,856 bytesのうちどの節が何tokenへ変換されたかは、節単位の切替試験なしには確定しない。

F05二ケース、F07 dependency、F10 monthlyも、AI応答回数とcommand回数を増やさずtokenだけが増えた。同じ傾向が複数ケースにあるため、F07だけの偶然とは扱わない。

## A01で保持すべき可能性がある境界

C147のA01中央値経路は、開始workspace、branch、HEAD、clean状態を確認し、その結果を利用者へ報告した後、未指定の既定modeを質問した。C254は18 / 20件でrepository evidenceを発行せず、未指定のmodeだけを一回で質問した。

Candidate254の`SPEC`には、TaskSpecへの固定内容は内部状態であり、固定した事実と内容を利用者向け進捗として出力しない、というC147にない文がある。`spec_ready=false`では変更、test、producer割り当てへ進めず、開始状態を後続作業にも使えない。さらに開始状態を進捗として出力できないため、A01では開始状態resultの受け取り先がなくなる。この構造は、確認を発行しなかった18件と対応する。

ただし、C254はTaskSpecが明示した開始状態の直接観測自体を禁止していない。この一文だけを切り替えた比較もない。したがって「A01改善の唯一の原因」とはせず、圧縮時に消してはいけない保持候補とする。

## C254固有または再構成された制御群の扱い

### 保持する

- `SPEC`の、内部固定状態を利用者向け進捗の受け取り先にしない境界。A01の削減と対応する。
- C147の`DECISION_BOUNDARY`が持つ、先行結果の停止効果を、その結果で対象、許可、方法または停止条件が変わり得る未発行operation classだけへ限定する関係。
- 開始確認がreadを禁じず、結果でread対象または許可が変わらない場合に、許可済みreadを待機対象へ含めない境界。
- `VALIDATION_CLOSURE`と`VALIDATION_PLAN`が持つ、途中結果を新しいAI判断へ返さず、全結果後に一度だけ判断する意味。
- 特定のcommand、wrapper、待ち秒数またはread範囲を指定しない自然文の境界。

### 圧縮候補として監査する

- 449 bytesの用語説明。必要な意味を失わず本文へ統合できるかを確認する。
- `OWNER_ROLE`の`+779` bytes。今回生traceを取得できたC147 250件、C254 275件ではchildまたは追加sessionのtokenは0件で、Standard14 N=20はC254固有の増分効果を示していない。未取得runへ外挿せず、独立したowner語列だけでworkerを起動できない意味も削除しない。
- `SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`METHOD`、`RECOVERY`のうち、C147と意味が同じ説明増分。節ごとの意味対応を作ってから圧縮する。
- `EVIDENCE_GATE`の、狭いcontextでの再readや正確な行位置の再検索を止める追加文。F08で同一entrypointの狭い再readがC254 5 / 20件、C147 2 / 20件にあり、この文だけでは経路を実行不能にしていない。回数制限へ変えず、既存のconsumer境界へ統合できるかを監査する。

### prompt制御へ変えない

- 完了前返却を避けるための待ち秒数。
- commandを一つのwrapperへまとめる指定。
- 成功runで使われたcommand順またはread順。
- ケースごとの行数、ファイル名または再read回数制限。

これらはAIへ処理方法を指定する案であり、品質を維持しながら少ないtokenと時間で成果を得るという目的から外れる。

## 次の設計判断へ渡す内容

次に許されるのは、Candidate254へ同じ行動条件を追加することではなく、C147で成立していた結果影響範囲の関係をCandidate254へ復元する設計監査である。本文圧縮は別の変更軸であり、この復元Candidateへ混ぜない。

1. Candidate254を直接の親に固定する。
2. `DECISION_BOUNDARY`全体だけを置換し、一般的な`result_effect_scope`、後続作業ごとの`decision_boundary`、開始確認の影響範囲`{artifact_change, required_validation}`、許可済みreadの明示的な範囲外固定を一組で戻す。
3. Candidate254の`DECISION_BOUNDARY`以外は同一byteで保持し、A01と対応した`SPEC`境界、F04で成立した開始確認境界およびvalidation境界を失わない。
4. F01、F02、F03で開始確認と許可済みreadの分離を観測し、F10 entrypointで適用規則がread対象または許可を変え得る正常な分離を別に観測する。
5. 品質、問題経路、正常経路、token、時間を別々に判定する。本文圧縮、完了待ち対策、command、wrapper、待ち時間またはread範囲の指定は行わない。

Candidate261とCandidate262はCandidate254を親にしなかったため対象外の診断証拠とし、Candidate263は上記四関係のうち開始確認固有の集合関係を固定せず一般条件だけを置換したため、この復元を実施したCandidateとは扱わない。

## Candidate264での実施結果

上記1〜5だけをCandidate264 `the-caption-3ce91a4-start-identity-result-effect-scope-restoration-r1`として実施した。Candidate254を直接の親にし、`DECISION_BOUNDARY`以外を同一byteで保持した。初回評価は固定したF01、F02、F03、F10 entrypoint各N=5だけを発行した。

- 20 / 20件がvalidかつ採点可能で、すべてScore `4`だった。
- F01とF02は、開始確認と許可済みreadの共同発行を各5 / 5件で保持した。
- F03は、Candidate254の共同発行3 / 5件、分離2 / 5件から、Candidate264の共同発行5 / 5件、分離0 / 5件へ改善した。
- F10 entrypointは、局所instructionのresult後にentrypoint本文を読む必要な正常経路がCandidate254の3 / 5件からCandidate264の2 / 5件へ悪化した。
- 四ケース合算中央値はCandidate254比でtoken `-16.38%`、経過時間`+4.97%`だった。

したがって、対象としたF03の機序成立と品質結果は保持する一方、F10の正常経路悪化と正当化できない経過時間増加により、固定済み停止条件へ該当する。追加N、Standard14、採用、releaseまたはprojectionへ進めない。本文圧縮、完了待ち対策、command、wrapper、待ち時間、read範囲の指定、Candidate261・262・263の修正も、この実施結果へ追加しない。

現在状態は`n20_control_group_decomposition_completed / c147_absence_reverse_audit_completed / candidate254_direct_parent_fixed / full_start_identity_result_effect_scope_restoration_executed_as_candidate264 / candidate264_quality_passed / candidate264_target_mechanism_passed / candidate264_normal_route_regressed / candidate264_unjustified_cost_regression / candidate264_stopped / fixed_model_visible_input_cost_supported / a01_spec_boundary_retained / f02_f03_wait_cost_confirmed / f07_same_route_input_regression_confirmed / whole_revert_rejected / candidate261_candidate262_off_target / candidate263_incomplete_restoration / standard14_not_started / adoption_not_approved`とする。

一次証拠は、Candidate147 N=20 selection `8981e3e14a6e4f10b0844feac45b5bd9`、analysis `8468f192f0284fe3b5173c0a6d1789d2`、Candidate254 N=20 result `2e40123a1b0642e3bbddb1812ba4414e`、Candidate264の登録result `1a64c1b2429c4e89aff3aedd6836944e`、Candidate264機序監査`candidate264-start-identity-result-effect-scope-restoration-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json`、各selectionの保存済みatomic run、`codex-events.jsonl`、`execution.json`、Candidate147、Candidate254およびCandidate264のbundle本文である。
