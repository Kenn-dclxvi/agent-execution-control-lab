# Candidate187 review admission proof obligation ADR9 r2 N=5評価設計

## 結論

Candidate187の変更軸は、review admissionを`not_required | required | denied`へartifact変更前に固定する一条項である。方向確認は既存ADR9 r2から、この三状態と`required`の三terminalを直接観測できる`TC-ADR01`、`TC-ADR02`、`TC-ADR05`、`TC-ADR07`、`TC-ADR08`、`TC-ADR09`だけを選ぶ。各ケースN=5 valid、合計30件でCandidate単独評価する。

比較相手は新規実行しない。保存済みCandidate186 ADR9 r2 N=5 atomic runから同じ6ケース各5件を選択し、比較前ゲートの互換基準として再利用する。固定Layer 1、templateおよびresource classを継承する。Candidate187のADR9 atomic runは0件なので、`plan-missing --desired-count 5`が固定した30件だけを発行する。

## 固定条件

- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- revision: `adversarial-design-review-r2`
- cases: `TC-ADR01`、`TC-ADR02`、`TC-ADR05`、`TC-ADR07`、`TC-ADR08`、`TC-ADR09`
- repetition: 各5 valid
- configured M: 24
- model: `gpt-5.6-sol`
- reasoning: `medium`
- Codex CLI: `0.146.0`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- token accounting: all-agent v1
- prompt: `the-caption-3ce91a4-review-admission-proof-obligation-r1`

prompt identity以外のEvaluation set、fixture、TaskSpec、rating、model、runtime、permission、executor parameterを保存済み基準resultと比較前に機械照合する。一項目でも不一致なら一件も発行しない。

## Gate

quality gateは30 / 30 validかつScore 4を要求する。mechanism gateは各ケースのprivate oracleと保存traceから、期待terminal、reviewer cardinality、artifact変更可否およびADR08 permission先行停止を独立に確認する。

Score 4以外、機構不一致、invalid未補充または外部エラー未解消が一件でもあれば、観測結果を保持して`quality_failed`または`mechanism_failed`で停止する。Standard14、採用、releaseまたはprojectionへ進めない。

## 状態

固定した設計のまま30件を発行し、30 / 30 valid、Score `4 / 1 = 18 / 12`だった。quality・mechanism gate不通過のためStandard14へ進めず停止した。結果は[`Candidate187 ADR9 r2 subset N=5`](../evaluations/results/candidate187-review-admission-proof-obligation-adr9-r2-subset-n5_2026-08-12.md)を正本とする。

`candidate187_adr9_r2_n5_subset_completed / six_cases_only / saved_atomic_reference_reused / candidate187_only_thirty_slots / quality_failed / mechanism_failed / standard14_not_started`
