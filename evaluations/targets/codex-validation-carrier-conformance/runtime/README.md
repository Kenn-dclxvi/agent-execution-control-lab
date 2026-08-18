# Codex validation carrier runtime

target固有のfixture materialization、capability preflight、quality gradingおよびtrace診断は[`adapter.py`](adapter.py)へ置く。

qualification-onlyのplan、preflightおよびwrite-once実行entrypointは[`runner.py`](runner.py)へ置く。この履歴実装はcontrol-free receiptのhashへbind済みなので変更しない。P002 candidate-only用の追記実装は[`runner_p002.py`](runner_p002.py)へ分離し、許可済みProfile class、runtime registrationおよびcandidate bindingを追加照合する。6件のprivate observationは[`register_p002.py`](register_p002.py)でcandidate-only resultへ登録した。

VCC6 P001/P002 N=5の追記実装は[`runner_vcc6_paired.py`](runner_vcc6_paired.py)へ分離する。P002の保存済みiteration 1だけを再利用し、P001の30件とP002の不足24件を同じ54件のglobal queueへ固定する。

60 logical resultの結合、Case別集計および事前cost gateは[`register_vcc6_paired.py`](register_vcc6_paired.py)でwrite-once resultへ登録する。
