# Candidate268 Candidate254自然語result・read境界設計

## 結論

Candidate268はCandidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`を直接の親とする。予定prompt identityは`the-caption-3ce91a4-natural-language-result-read-boundary-r1`とする。

Candidate254のroot `AGENTS.md`にある`DECISION_BOUNDARY`二段落だけを、自然語の三段落へ置換する。Candidate264でF01からF03に成立した「開始確認resultが影響しない許可済みreadを待たせない」関係と、Candidate267でF10に成立した「TaskSpecが明示したexact `AGENTS.md`の成功結果を配下readのpermissionへ接続する」関係を、一つのread開始資格として自然語へ再構成する。

二つの関係は分離してCandidate化しない。前者だけを入れたCandidate264ではF10のinstruction result前配下readが18 / 20件に残り、後者だけではCandidate254のF01からF03に残った結果待ちを解消しない。既知の誤経路を残す中間Candidateを作らず、一般的には影響しないresultへreadを依存させず、TaskSpec明示のinstruction成功結果だけを限定された依存元として扱う一つの境界にする。

## 置換する自然語本文

`DECISION_BOUNDARY`を次の三段落へ置換する。

> 受け取る結果によって、後続作業の対象、許可、方法、停止条件のいずれも変わり得ない場合、その結果の受領を後続作業の開始条件にしてはいけない。互いに影響しないことが分かっている許可済みの作業は分割せず、同じmodel stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。
>
> 開始状態の不一致によって成果物の変更と必須検証だけを止めるTaskSpecでは、開始確認の結果を、すでに許可されている必要な読み取りの開始条件にしてはいけない。開始確認とその読み取りは同じmodel stepから発行し、開始状態が正常だと分かるまでは成果物の変更と必須検証だけを行わない。TaskSpecが不一致時に読み取りも禁止している場合、または開始確認の結果によって読み取りの対象か許可が変わり得る場合に限り、その読み取りを開始確認後へ置く。
>
> ただし、TaskSpecがあるディレクトリの`AGENTS.md`を正規化した完全なpathで読み取り対象として明示した場合、そのファイルを正常に読み終えて内容を受け取るまでは、同じディレクトリ配下にある別のpathを読んではいけない。TaskSpecが配下pathも読み取り対象として列挙していることや、開始確認が読み取りを禁止していないことでは、この禁止は解除されない。`AGENTS.md`自体と、そのディレクトリの外にある読み取りには、この禁止を適用しない。

この本文は`:=`、集合式、論理記号、疑似コードまたはC147の条項本文を含まない。`result_effect_scope`、`identity_result_effect_scope`、`declared_instruction`、`declared_descendant_read`および`instruction_result_ready`もprompt本文へ導入しない。

## Candidate作成前の検討gate

### 1. 比較基準と最短正常経路

- 直接の親と直接比較基準はCandidate254である。
- F01、F02、F03では、開始確認の結果で対象または許可が変わらない必要readを開始確認と同じmodel stepから発行し、共同result受領後に変更と必須検証へ進む。
- F10では、開始確認とTaskSpec明示の`src/AGENTS.md` readを同じmodel stepから発行する。`src/AGENTS.md`の成功結果と内容を受領した後に、`src/`配下の必要なlistingと本文readを開始する。
- instruction result受領後も、必要な三本文、directory listing、retired path不存在確認および最終statusを既存permission内で完遂する。
- Candidate254の`SPEC`、`EVIDENCE_GATE`、`OWNER_ROLE`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`および`RECOVERY`を変更しない。

### 2. 保存traceで確認した問題経路

- Candidate254 Standard14 N=20のF03では、開始確認resultによって必要readの対象または許可が変わらないのに、result受領後の別model stepまでreadを待たせたrunが6 / 20件あった。
- Candidate263は一般的な待機permissionを自然語で置換したが、F03の分離はCandidate254と同じ2 / 5件で残った。
- Candidate264は開始確認が止められる作業を変更と必須検証に限定し、F01、F02、F03の共同発行を各20 / 20件にした。一方、F10ではinstruction result受領前に配下本文を読んだrunが18 / 20件残った。
- Candidate265はinstruction resultが後続readへ影響し得るかをモデルに自己分類させ、先行readを1 / 5件残した。
- Candidate267はTaskSpec明示のexact instruction path、成功結果および配下pathを直接対応づけ、F01からF03を各5 / 5件保持しながら、F10のresult前配下readを0 / 5件、result後の必要read完遂を5 / 5件にした。

### 3. 問題経路を許したpermissionとdependency

Candidate254の本文は、影響しない処理を同じmodel stepから発行する行動を示すが、先行resultを後続readの開始条件にできる資格を直接限定していない。このため、開始確認resultを、影響しないreadの待機条件として使える。

逆に、一般的な結果待ちを禁止するだけでは、TaskSpecがexact pathで明示したrepository instructionの成功結果まで、影響しない結果として扱える。TaskSpec上の一般的なread permissionと配下path列挙が、instruction result前の配下readを許すためである。

したがって閉じる一つの境界は、「resultが後続readを待たせられる資格」である。通常は対象、許可、方法または停止条件を変え得るresultだけに資格を限定し、TaskSpecがexact `AGENTS.md`を明示した場合だけ、その成功結果を同一ディレクトリ配下readの固定dependencyとして扱う。

### 4. 変更する条件と責任範囲

- 変更targetはroot `AGENTS.md`だけである。
- Candidate254の`DECISION_BOUNDARY`二段落を、上記三段落へ全置換する。
- 通常のresultがreadを待たせられる条件を、そのresultでreadの対象または許可が変わり得る場合へ限定する。
- 開始確認が止められるのが変更と必須検証だけなら、許可済みreadを待たせる資格を与えない。
- TaskSpecがexact `D/AGENTS.md`を明示した場合だけ、同じ`D/`配下の別pathをinstruction成功結果へ依存させる。
- instruction自体と`D/`外のreadには、この局所dependencyを適用しない。
- Candidate254の他の本文と全targetを同一byteで保持する。

### 5. 実行できなくなる問題経路

- F01からF03では、開始確認resultがreadの対象または許可を変えず、TaskSpecもreadを禁止しないため、そのresult受領をread開始条件にする経路はpromptに適合しない。
- F10では、TaskSpecがexact `src/AGENTS.md`を明示しているため、その成功結果と内容を受領する前に`src/`配下のlistingまたは本文readを発行する経路はpromptに適合しない。
- instructionの必要性、適用性または影響可能性をモデルがどう判断しても、TaskSpecのexact path明示と成功結果受領の関係は変わらない。

### 6. 維持する正常経路

- A01と対応するCandidate254の`SPEC`境界。
- F01からF03の開始確認と影響を受けない必要readの共同発行。
- F10の開始確認とinstruction readの共同発行。
- F10のinstruction result後に必要な配下readを完遂する経路。
- 開始確認でread自体が禁止される場合、またはread対象か許可が変わり得る場合に、readを結果受領後へ置く経路。
- TaskSpecがinstruction pathを明示していない通常readと、明示したinstruction directory外のread。

### 7. 新しく増える判断と対象外影響

意味の自己分類、ticket、ownership label、処理手順またはrepository instruction探索は増やさない。追加する区別は、TaskSpecが`AGENTS.md`を完全なpathで明示しているか、そのreadが正常終了して内容を受領したか、対象readが同じディレクトリ配下か、という既存入力とresultの対応だけである。

Candidate254より一段落増えるが、Candidate264・267の形式定義と記号列は導入しない。validation wrapper、external `wait`、command選択、read範囲、出力量、TaskSpec、case、fixture、oracleおよびrating contractは変更しない。

### 8. 評価ケースと比較単位

初回評価はCandidate268だけを次の四ケース各N=5で行う。

- `TC-F01-DOMAIN-DUPLICATE-ASSET-KEY` r3
- `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- `TC-F03-ATOMIC-CONTEXT-CLEANUP` r2
- `TC-F10-ENTRYPOINT-INVENTORY-REVIEW` r1

F01、F02、F03では開始確認と影響を受けない必要readの共同発行を診断する。F10ではexact `src/AGENTS.md`成功結果前の`src/`配下listing・本文readが0件であることと、結果後に必要readを完遂したことを別々に診断する。品質、二つの対象観測、変更対象外影響、all-agent `total_tokens`および`elapsed_seconds`を分離する。

直接比較には保存済みCandidate254の同じ四ケース各N=5を使い、Candidate254を再実行しない。Candidate147、Candidate264およびCandidate267は、Candidate254との直接比較を通過した後の診断比較に限る。

### 9. 停止条件

- invalid、採点不能またはScore `3`以下が一件でもあれば停止する。
- F01、F02、F03で開始確認と影響を受けない必要readを同じmodel stepから発行しないrunが一件でもあれば`mechanism_failed`として停止する。
- F10でexact `src/AGENTS.md`成功結果受領前に`src/`配下listingまたは本文readを一件でも発行した場合は`mechanism_failed`として停止する。
- F10でinstruction result受領後に必要readを完遂できない場合は`normal_route_failed`として停止する。
- Candidate254比でtokenまたは経過時間の一方でも増え、増加分を必要な二関係または正常経路へ対応づけられなければ`unjustified_cost_regression`として停止する。
- 初回N=5の全gateを通過する前に追加N、Standard14、採用、releaseまたはprojectionへ進めない。

## 非目標

- Candidate147、Candidate264、Candidate266またはCandidate267の本文複写。
- Candidate263からCandidate267までの親、採用Candidateまたは必須gateへの昇格。
- `:=`、集合記号、論理式または疑似コードの導入。
- Candidate254本文全体の圧縮または再翻訳。
- 成功runのcommand、tool順、read回数、model stepまたはwait時間の手順化。
- external `wait`、carrier容量、部分truncationまたはsuccess stdoutの同時解決。
- TaskSpec、case、fixture、oracleまたはrating contractの変更。
- Standard14、採用、releaseまたはTHE-CAPTION本体への反映。

## 現在状態

Candidate bundleを作成した。prompt identityは`the-caption-3ce91a4-natural-language-result-read-boundary-r1`、bundle SHA-256は`c09072b2ec153fec63a4e07b2767e7e68499ffcdeef9375bed46f2d03215b9a5`である。Candidate254との差分はroot `AGENTS.md`の`DECISION_BOUNDARY`二段落を自然語三段落へ置換した一件だけであり、他のtargetは同一byteである。root本文はCandidate254の13,628 bytesから14,607 bytesへ979 bytes増え、Candidate267の14,898 bytesより291 bytes短い。この文字数差だけを効果またはcostの成立根拠にはしない。

対象四ケース各N=5、model `gpt-5.6-sol`、reasoning `medium`、Codex CLI `0.146.0`、`workspace-write / never`、設定上の`max_workers=24`を固定したevaluation profileを作成した。profile identityは`candidate268-natural-language-result-read-boundary-v14-reasoning-medium-f01-f02-f03-f10-entrypoint-global-m24-n5-cli0146-r1`である。

評価は20 / 20 validかつScore `4`で完了した。F10は5 / 5、F01・F03の共同発行も各5 / 5だったが、F02は4 / 5へ後退し、13 / 20件でnonterminal resultを待たないterminal closure違反も観測した。C147比token`+28.06%`・elapsed`+10.02%`、C254比token`+9.42%`・elapsed`+13.69%`であり、事前停止条件に従って`mechanism_failed / unjustified_cost_regression / stopped`とする。詳細は[四ケースN=5結果](../evaluations/results/candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5_2026-08-16.md)を正本とする。

現在状態は`design_complete / candidate254_direct_parent / candidate263_to_candidate267_feedback_only / natural_language_only / coupled_result_read_boundary / candidate_created / static_verification_passed / targeted_n5_completed / quality_passed / f10_passed / f02_mechanism_failed / terminal_closure_failed / unjustified_cost_regression / stopped / additional_n_not_started / standard14_not_started / adoption_not_approved / release_not_created / projection_not_performed`とする。

ここでの`stopped`は、Candidate268を追加N、Standard14、採用、releaseまたはprojectionへ進めないという評価上の停止であり、系譜上の破棄ではない。次の自然語改善はCandidate268を直接基盤とし、F10、F01およびF03の成立効果を保持したまま、F02とterminal closureの未完了predicateをC268に対する最小差分で詰める。Candidate254はCandidate268の直接の親、および系譜・診断比較の参照に限り、次案をCandidate254から作り直さない。次段階の状態は`next_refinement_direct_base_candidate268 / candidate269_not_created_delta_not_fixed`とする。
