# target固有ツール

- `pr_review_fixture_tool.py`: model-visible fixtureのread-only取得
- `pr_review_measurement.py`: fixture検証、入力準備、許可field収集、診断採点
- `pr_review_authority_collector.py`: 固定Git treeからroot `CLAUDE.md`とchanged pathの局所`AGENTS.md`を決定論的に選択し、identity receiptを生成
- `pr_review_authority_packet.py`: 選択receiptを固定treeへ再照合し、model-visibleなauthority原文packetを生成
- `pr_review_fixture_tool_r2.py`: r1のfixture取得に加え、検証済みauthority原文packetを`rules`で返すBaseline候補用tool
- `pr_review_repository_snapshot.py`: 固定target treeへ任意のschema v2 caseの変更後本文をoverlayし、`.git`なしread-only snapshotとidentity receiptを生成
- `pr_review_fixture_tool_r3.py`: r2の入力取得に加え、snapshot内のpath一覧とUTF-8本文をread-onlyで返すBaseline候補用tool

これらは`agent-execution-control-lab`固有のcase ID、rule、authority選択を扱うため、ターゲット非依存kernelの`scripts/`へ置かない。authorityとrepository snapshotのreceiptはmodel-visible入力対応を証明するが、case設計の独立qualification、profile、preflight、Baseline admissionを単独では成立させない。
