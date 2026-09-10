# Rating contracts

現行contractは[`general-chat-response-exact-v1.json`](general-chat-response-exact-v1.json)である。

自然文だけを独立graderで採点する方式は[`general-chat-response-hybrid-r2-draft.json`](general-chat-response-hybrid-r2-draft.json)と[`grader出力schema`](general-chat-semantic-judge-output-r1.schema.json)へ分離した。開発用pilotは3件以上の独立AI grader panelを標準経路とし、人間監査は任意の証拠強化経路とする。graderの正式な適格性は別のsealed holdoutで一度だけ判定する。r2は`calibration_required_not_active`であり、現行contract、既存resultの再採点規則、またはformal evaluation authorityではない。
