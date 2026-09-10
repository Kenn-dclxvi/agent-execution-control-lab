# Runtime

target固有のpreflight、Codex CLI実行、schema検証、決定的採点および3 KPI収集を行う。r1からr3は失敗履歴、`run_qualification_v4.py`は成立したN=1基盤である。その固定条件をbaseline N=5とCandidateの段階的評価へ拡張した。実行時の一時workspace、一時home、raw transcriptおよびauth内容はリポジトリへ保存しない。

`prepare_semantic_calibration.py`は、自然文graderを有効化する前の開発用pilotを準備・集計する。標準経路は3件以上の独立AI grader panelであり、採点packetから回答の出自を除き、運営者mapを分離する。全員一致率、名義尺度のKrippendorff's alpha、label分布および不一致一覧を集計するが、人間判断との一致、pilotの合否、適格条件の数値またはgrader適格性を生成しない。従来の人間pilot処理は任意の証拠強化経路として保持する。

`run_ai_grader_panel.py`は固定済み3 memberだけを実行する。`preflight`は評価用の不変`codex-cli 0.148.0`をregistryから解決し、絶対実行path、entrypoint hash、全利用schemaを含む正本、runner、member別packet、map、template、transport schemaおよびstdinをrepository外のrun rootへ固定する。transport schemaはcanonical schemaから生成し、固定値の型と全propertyのrequired指定を発行前に検査する。`run`はreceiptを再構成してdriftを拒否した後、memberごとに別の一時workspaceと`CODEX_HOME`を使い、read-onlyかつ`--ephemeral`で3 slotを同時発行する。raw JSONL、stderr、labelおよびpilot reportはrun rootだけへ保存し、canonical schemaで再検証する。preflight自体はmodel slotを発行しない。

CLI 0.148のJSONL token accountingは`turn.completed.usage`の`input_tokens`と`output_tokens`を合計して`total_tokens`へbindする。`cached_input_tokens`、`cache_write_input_tokens`および`reasoning_output_tokens`は内訳として保持し、総量へ重ねて加算しない。`recover`は、process完了済みでcanonical labelがJSONLに残っているがusage形式差だけで`unrateable`になった固定3件に限り、raw JSONLのhashとidentityを照合して別resultへ回復する。元resultを上書きせず、モデルを再発行しない。
