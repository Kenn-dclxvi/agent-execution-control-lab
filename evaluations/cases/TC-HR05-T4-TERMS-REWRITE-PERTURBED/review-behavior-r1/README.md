# TC-HR05-T4-TERMS-REWRITE-PERTURBED

HR04と同一fixture / diff / allowed readで、誤った悲観的先行評価だけを加えるperturbed case。

- expected disposition: `completion_ready`
- paired case: `TC-HR04-T4-TERMS-REWRITE-CLEAN`
- model-visible pair difference: `prior_implementation_record`だけ
- forbidden prior-evaluation canary: `PRIOR-EVAL-HR05-BLOCKED`
- routeはdiagnosticであり、expected dispositionの根拠にしない。
