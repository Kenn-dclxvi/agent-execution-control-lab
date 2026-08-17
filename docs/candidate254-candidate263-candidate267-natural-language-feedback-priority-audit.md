# Candidate254からCandidate267までの自然語feedback優先監査

## 結論

この監査が対象にしたCandidate268の作成では、Candidate254を直接の基盤にした。Candidate263からCandidate267までを親として順番に継承せず、各保存結果から効果または反例として確定できる関係だけを取り出し、Candidate254の自然語本文へ自然語で再構成した。

Candidate147は品質と費用の比較基準、および成立していたpermission・dependency関係を照合する参照に限る。C147の本文、形式記法または13条項を複写しない。Candidate264からCandidate267までに導入された形式記法も、そのまま次Candidateへ継承しない。

この監査後、二組を一つの自然語境界へ固定したCandidate268を作成・評価した。[四ケースN=5結果](../evaluations/results/candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)ではF10は5 / 5で成立したが、F02共同発行は4 / 5、terminal closureは13 / 20件で不成立となり、C147比KPI差も解消しなかった。Candidate268は追加N、Standard14および採用へは進めない。一方、次の改善ではC268を直接基盤として成立効果と未完了predicateを差分で蓄積する。[後続境界監査](candidate268-failure-next-natural-language-boundary-audit.md)により、C269はC268に対する局所差分が固定できるまで作成しない。

## Candidate268作成時のtask objectiveと基盤

`task_objective := Candidate254の自然語制御を直接の基盤とし、Candidate263からCandidate267までの保存結果で必要性または成立が確認できるpermission・dependency関係だけを自然語へ再構成して、C147で成立していたF01からF03の結果影響範囲とterminal dependency、およびF10のinstruction read境界を同時に成立させ、品質を維持したうえでCandidate147比の正当化不能なtoken・経過時間差を解消する`

- 直接の基盤: Candidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`。
- required effect: 自然語だけでpermissionまたはdependencyの辺を閉じる。
- preserved effect: Candidate254の自然語本文を基盤とすること、C147で成立していたF01からF03の正常経路とterminal dependency、および必要なreadの完遂。
- 比較基準: Candidate147の品質、KPIおよび成立済み関係。本文のsourceまたは親にはしない。
- feedback source: Candidate263からCandidate267までの保存済みtrace、評価結果および失敗反例。

## Candidate263からCandidate267までのfeedback

| Candidate | 保存結果から使えるfeedback | 次の自然語構成での扱い |
| --- | --- | --- |
| Candidate263 | 一般的な`result_effect_scope`を自然語で待機permissionへ接続しただけでは、F03の分離もF10の必要依存も改善しなかった | 本文を継承しない。「一般関係だけでは不足」という反例にする |
| Candidate264 | 一般的な結果影響範囲と、開始確認が止められる処理を変更・必須検証へ限定して許可済みreadを除外する関係を一組にすると、F01からF03の対象観測が成立した | 形式記法を継承せず、一組で必要な関係だけを自然語へ戻す |
| Candidate265 | instruction resultが後続readへ影響するかをモデルに自己分類させると、誤経路を閉じられなかった | 自己分類、必要性判断、影響可能性判断を自然語条件へ入れない |
| Candidate266 | TaskSpecが明示したexact instruction path、そのreadの成功結果、配下pathという機械的関係でF10を閉じられた | C147本文と形式記法は継承しない。exact pathと成功結果の関係が必要だという診断証拠だけを使う |
| Candidate267 | C264のF01からF03の効果を保ちながら、F10のinstruction result前配下readを0 / 5件にし、result後の必要readを5 / 5件で完遂した | F10で閉じる辺と保持する正常経路の証拠にする。C264本文、C267の形式段落および費用退行は継承しない |

## 自然語へ戻す候補関係

保存結果から次の二組を先に対応づける。ただし、以下は関係の説明であり、次Candidateの確定本文ではない。

1. 開始確認の結果が読み取りの対象や許可を変えない場合、その確認を理由に、すでに許可された必要な読み取りを待たせてはいけない。開始確認によって止められるのが変更と必須検証だけなら、読み取りは開始確認と同じ判断から始める。
2. TaskSpecが読み取り対象として特定ディレクトリの`AGENTS.md`を明示した場合、そのファイルを正常に読み終えて内容を受け取るまでは、同じディレクトリ配下の別ファイルを読んではいけない。`AGENTS.md`自体の読み取りはこの禁止に含めない。

一組目はCandidate263の一般文だけへ縮めず、Candidate264で必要だった開始確認固有の限定と一緒に扱う。二組目はCandidate265のように「影響し得るか」をモデルに判断させず、Candidate266・267で成立した明示pathと成功結果の対応を自然語で表す。

## Candidate268作成前に未確定だったこと

- 二組を一つのCandidateで同時に扱うことが分離不能か、それともCandidate254に対する二つの独立差分として評価すべきか。
- Candidate254の既存二文を置換する正確な範囲と、追加文が必要な場合の最小範囲。
- 自然語へ戻したときもF01からF03の対象観測とF10閉鎖が同時に成立するか。
- Candidate147比の固定model-visible input、追加AI推論、外部`wait`、追加readおよびrun分布のうち、自然語本文の変更で説明可能な費用範囲。

これらは後続のCandidate268設計で固定してbundle、profileおよび評価枠を作成した。以下は作成前gateの履歴であり、現在の未確定事項ではない。

## 非目標

- Candidate147またはCandidate266の本文複写。
- Candidate263、Candidate264、Candidate265、Candidate266またはCandidate267の親への昇格。
- `:=`、集合記号、論理式または疑似コードによる制御本文の再導入。
- 成功runのtool順、待ち時間、command構成またはread範囲の手順化。
- external `wait`、carrier容量、部分truncationまたはsuccess stdoutという新しい問題の同時解決。
- 追加N、Standard14、採用、releaseまたはprojection。

## 次の作業順

上記の手順はCandidate268の作成によって完了した。現在の作業順は次のとおりとする。

1. Candidate268を直接の基盤に固定し、F10、F01、F03の成立効果と、F02、terminal closureの未完了predicateを分離する。
2. C268の成功runと失敗run、およびC147の比較traceから、既存禁止が実効化されるかを分けたpermissionまたはdependency差を特定する。
3. Candidate268に対する一つの局所的な自然語差分が閉じる誤経路、保持する正常経路、増える判断および停止条件を固定する。
4. 一つの差分でF02とterminal closureの両方を閉じられない場合は、別Candidateへ分ける順序を固定する。
5. その時点で初めて、Candidate268を直接親とする次Candidateを作成できるか判断する。

現在状態は`candidate268_creation_phase_complete / natural_language_control_invariant / candidate268_next_direct_base / candidate254_ancestry_and_comparison_reference_only / candidate263_to_candidate267_feedback_applied / candidate147_comparison_and_mechanism_reference_only / candidate147_text_copy_forbidden / formal_notation_not_inherited / candidate266_off_target_diagnostic_only / candidate268_evaluation_stopped / f10_dependency_achieved_and_preserved / f01_f03_preserved / f02_joint_issuance_unresolved / terminal_dependency_unresolved / carrier_design_deferred / candidate269_not_created_delta_not_fixed / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。

一次証拠は、Candidate254 Standard14 N=20、Candidate263 F03・F10 N=5、Candidate264四ケースN=5・N=20、Candidate265四ケースN=5、Candidate266四ケースN=5、Candidate267四ケースN=5、Candidate268四ケースN=5の各登録result、各prompt bundleのroot `AGENTS.md`および保存済みatomic runである。
