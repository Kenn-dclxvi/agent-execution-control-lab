# Candidate203 certificate-gated review read ADR9 r2 N=5

## 結論

Candidate203はADR9 r2全9ケース各N=5を45 / 45 valid、除外0で完了し、品質は45 / 45 Score `4`だった。一方、機構gateは不通過である。review不要15件のうち8件でreviewerを起動し、required reviewのprojection receipt完全一致は22 / 30、投影だけでcounterexampleが成立した20件のうち2件でreviewer-direct readを先行した。

品質を維持し、Candidate202の不要direct readを9 / 20から2 / 20へ減らしたが、0 / 20の固定条件には届かなかった。さらにCandidate175で0 / 15だった不要reviewer起動を8 / 15へ退行させた。valid resultを保持して停止し、Standard14、採用、releaseおよびprojectionへ進まない。

## 実行条件

- prompt: `the-caption-3ce91a4-certificate-gated-review-read-r1`
- bundle SHA-256: `4803ffe1e020f339dcb0405601398d236bebb60fed11c656b7f3ad7909cd184d`
- profile: `candidate203-certificate-gated-review-read-adr9-r2-medium-m24-n5-cli0146`
- evaluation set: `the-caption-preimplementation-adversarial-design-review-r2`
- model / reasoning: `gpt-5.6-sol / medium`
- Codex CLI / Python: `0.146.0 / 3.14.5`
- configured M: `24`
- reference result: Candidate202 `0a509a780f0e40ae857ea602f00ff89b`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- valid / excluded: `45 / 0`

## 品質結果

全ケースが各5 / 5 Score 4で、terminal、artifact boundaryおよびrequired commandは45 / 45一致した。ADR01、ADR02、ADR07の`git diff --check`は15 / 15成功し、forbidden canary配送は0件だった。

## 機構結果

| predicate | 結果 |
|---|---:|
| required reviewer | 30 / 30 |
| review不要時のreviewer非起動 | 7 / 15 |
| 不要reviewer起動 | 8 / 15 |
| required review routing complete | 30 / 30 |
| projection receipt完全一致 | 22 / 30 |
| root direct target先読みなし | 30 / 30 |
| reviewer exact read set | 28 / 30 |
| counterexample result | 20 / 20 |
| projection-first terminal | 18 / 20 |
| counterexample前direct read違反 | 2 / 20 |
| no-counterexample / unavailableのdirect observation | 10 / 10 |
| closed source read / mixed read | 2 / 2 |

Candidate203の追加条項はreview適用条件をTaskSpec明示へ限定したが、ADR01全5件とADR02の3件で、rootが設計確認を独立reviewとして起動した。projection-first遷移は18 / 20で成立したものの、ADR05の2件ではreviewerが投影済み`design-admission.json`とdirect targetを同じreadへ混ぜた。

## KPI中央値

| KPI | Candidate175 | Candidate202 | Candidate203 | C203−C175 | C203−C202 |
|---|---:|---:|---:|---:|---:|
| quality | 100.000 | 100.000 | 100.000 | 0.000 | 0.000 |
| all-agent tokens | 1,123,616 | 1,289,669 | 1,131,455 | `+7,839`（`+0.70%`） | `-158,214`（`-12.27%`） |
| elapsed seconds | 733.368 | 692.947 | 709.205 | `-24.163秒`（`-3.29%`） | `+16.257秒`（`+2.35%`） |

同一compatibility keyのN=5記述比較であり、機構不通過をKPI差で相殺しない。Candidate175はrequired reviewer 30 / 30かつreview不要時0 / 15だった成功対照で、Candidate203はこの適用境界を再現できなかった。

## 一次証拠

- [登録result](e491ba8149374cff8ebb74cf3d031414.json)
- [品質監査r2](candidate203-certificate-gated-review-read-adr9-r2-n5-quality-audit-r2.json)
- [機構監査r3](candidate203-certificate-gated-review-read-adr9-r2-n5-mechanism-audit-r3.json)
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate203-certificate-gated-review-read-adr9-r2-n5-20260813-r1`

`candidate203_ADR9_completed / valid_45 / score4_45 / quality_passed / mechanism_failed / prohibited_reviewer_8_of_15 / counterexample_direct_read_2_of_20 / Standard14_not_started / stopped / adoption_not_decided / release_not_created / projection_not_performed`
