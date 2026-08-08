# target固有ツール

- `pr_review_fixture_tool.py`: model-visible fixtureのread-only取得
- `pr_review_measurement.py`: fixture検証、入力準備、許可field収集、診断採点
- `pr_review_authority_collector.py`: 固定Git treeからroot `CLAUDE.md`とchanged pathの局所`AGENTS.md`を決定論的に選択し、identity receiptを生成
- `pr_review_authority_packet.py`: 選択receiptを固定treeへ再照合し、model-visibleなauthority原文packetを生成
- `pr_review_fixture_tool_r2.py`: r1のfixture取得に加え、検証済みauthority原文packetを`rules`で返すBaseline候補用tool
- `pr_review_repository_snapshot.py`: 固定target treeへschema v2 caseの変更後本文をoverlayし、`.git`なしread-only snapshotとidentity receiptを生成するr1履歴tool
- `pr_review_repository_snapshot_r2.py`: r1の境界を保ったままschema v3を追加許可し、fixture revisionとの一致も検証するqualification用tool
- `pr_review_repository_snapshot_r3.py`: 同じread-only境界でschema v4を固定し、r4変更後本文をoverlayするqualification候補用tool
- `pr_review_qualification.py`: PRR-C01/r3のfixed profileとpreflightを再照合し、Core Baseline qualificationの入力準備、許可field収集、採点を行う
- `pr_review_fixture_tool_r3.py`: r2の入力取得に加え、snapshot内のpath一覧とUTF-8本文をread-onlyで返すBaseline候補用tool
- `pr_review_fixture_tool_r4.py`: r3のread-only境界を保ち、`rules`で規則identity・本文catalogとauthority原文を同時に返すqualification候補用tool
- `pr_review_fixture_tool_r5.py`: r4の入力境界に固定eligibility取得を加え、純正code-reviewの事前判定をmodel-visibleにする新Baseline候補用tool
- `pr_review_code_review_qualification.py`: 純正相当Core Baselineの入力準備、Action出力の許可field収集、workflow trace確認、採点を行う
- `pr_review_code_review_qualification_r2.py`: 初回失敗に対し、`Agent`許可とcollector依存同梱を追加した履歴上のenvironment recovery tool
- `pr_review_code_review_qualification_r3.py`: 同じrepetitionへsubagent lifecycle、tool batch、fixture access、permission denialの計測を追加するinstrumented recovery tool
- `pr_review_code_review_qualification_r4.py`: project設定を通常名でartifact転送し、review job内で配置するenvironment recovery tool
- `pr_review_subagent_hook.py`: Claude Code hook入力から内容を除き、event identity、時刻、agent identity、tool種別だけを原子的に記録する
- `pr_review_workflow_free_calibration.py`: Workflow Freeのpreflight再照合、入力準備、任意subagent構成の診断trace、全agent token収集、品質と測定成立を分けた採点を行う
- `pr_review_relationship_role_calibration.py`: 関係レビュー役を1人に固定したSonnet／Opus条件のpreflight、agent別fixture access、model routing、全agent token、品質と測定成立を収集する
- `pr_review_control_free_qualification.py`: PRR-C02、C03、C05、C06の固定profileを再照合し、control-free資格確認の入力準備、全agent token収集、採点を行う
- `pr_review_control_free_qualification_r2.py`: schema出力の引用とreview job用collector依存の同梱を修復した同一資格確認スロットのenvironment recoveryを行う
- `pr_review_subagent_hook_r2.py`: command内容を保存せず、loopや複合command内の`./fixture-tool`呼出しも検出する
- `pr_review_control_free_qualification_r3.py`: C05/r1を除外した3ケースsetとfixture-tool計測r2を固定して資格確認する

これらは`agent-execution-control-lab`固有のcase ID、rule、authority選択を扱うため、ターゲット非依存kernelの`scripts/`へ置かない。authorityとrepository snapshotのreceiptはmodel-visible入力対応を証明するが、case設計の独立qualification、profile、preflight、Baseline admissionを単独では成立させない。
