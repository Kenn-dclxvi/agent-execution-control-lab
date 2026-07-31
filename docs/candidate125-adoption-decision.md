# Candidate125採用判断

## 結論

Candidate125を採用した。Candidate125と内容同一のreleaseを承認し、THE-CAPTIONへ投影した。

状態は次のように分離する。

| lifecycle | 現在状態 |
| --- | --- |
| evaluation | `standard14_evaluated / quality_gate_passed / a02_terminal_closure_passed / candidate107_token_target_passed` |
| adoption | `adopted` |
| release | `projected` |
| runtime projection | `projected` |

この判断は2026-07-31のユーザーによる明示的な採用・展開依頼に基づく。一次evaluation resultに保存した当時の`adoption_not_decided`は変更しない。

## 判断根拠

Candidate125はStandard14 N=5で70 / 70件がscore `4`だった。token中央値`1,401,225`は正式目標`1,523,137`を`121,912`、`8.00%`下回った。elapsed中央値`846.377秒`もCandidate107比`10.48%`短かった。

targeted試験ではF04 false stop 0 / 5、F02 content wave 5 / 5、F02 token中央値`124,094`を確認した。後続A02 N=20でも20 / 20件がscore `4`で、implementation bind後・変更前command再入は0 / 20件だった。

これにより、Candidate118のA02 terminal closure、Candidate122のcontent-wave cost経路、Candidate124で未完了だったF04 content closureを同時に保持した。

## 受容するrisk

Candidate125のStandard14 B20は未実施である。Candidate81にはStandard14 B20の長期安定性証拠があるため、この証拠量ではCandidate125のほうが少ない。この差を隠さず、明示的な採用判断により受容する。

Candidate125のN=100試験は後日実施予定であり、現時点では`planned / not_started`である。これは投影後の追加安定性評価であり、今回の採用・release・runtime projectionの完了状態とは分離する。

Candidate122比ではtoken中央値が`0.19%`低い一方、elapsed中央値は`2.84%`高い。Candidate122は品質gate不通過であり、C125は品質を70 / 70へ回復したため採用するが、全KPI改善とは主張しない。

## 投影境界

投影ではrelease bundleの19 targetを照合し、Candidate81投影後のTHE-CAPTIONとの差分だけを変更した。実効変更はroot `AGENTS.md`一つである。`docs/how-to/index.md`はCandidate125外の既存更新を保持したため、post-merge照合は実効変更1 / 1、manifest target 18 / 19となった。required validationは`408 passed in 6.36s`だった。THE-CAPTION [PR #345](https://github.com/Kenn-dclxvi/THE-CAPTION/pull/345)、merge commit `2791c21d414d849b376be0d9496fc455f7e10e45`、rollback identity `f12e4cc0e1d9291307a49c151e473e3bc6e92e44`を[`projection.json`](../prompts/releases/the-caption-3ce91a4-criterion-complete-single-target-continuation-release-r1/projection.json)へ固定した。
