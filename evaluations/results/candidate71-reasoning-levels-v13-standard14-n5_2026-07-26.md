# Candidate71 reasoning 6水準 Rating v13 標準14項目 各5回

## 結論

Candidate71をreasoning `low`、`medium`、`xhigh`、`max`、`ultra`で新規実行し、既存の`high`と同じRating v13、標準14項目、各`N=5`、global queue `M=24`で記録した。新規5水準はすべて70 / 70件がvalidかつrateableで、excluded attempt 0件、result登録とfinal compact完了だった。

公式score分布は、`low`、`medium`、`high`、`xhigh`、`max`が`4 = 70`、`ultra`が`4 / 0 = 69 / 1`だった。6水準とも`quality_score`中央値は`100.000`だった。`medium`がall-agent `total_tokens`の中央値と合計が最小、`low`が`elapsed_seconds`の中央値と合計が最小だった。`xhigh`以上は`high`よりtokenとelapsedがともに増加した。

`ultra`のA01 iteration 3はRating v13でscore `0`として保存されたが、後の証拠確認で採点偽陽性と判別した。実行したのはsource、test、履歴のread / searchで、実際のtest commandや編集はなかった。search pattern内の`pytest.fixture`をRating v13が`pytest`実行と誤認し、`a01_forbidden_test_operation`にした。最終応答は未固定値を質問し、変更とtestを実行せず停止していた。Rating v13 resultはimmutable historyとして変更しない。

reasoning effortはcomparison conditionであり、6結果のcompatibility keyは異なる。そのため、以下はLayer 4の互換comparisonではなく、reasoning effortだけを変更した水準別の記述的な差である。winner、採用、release、THE-CAPTION本体反映は判断しない。

## 固定条件

- prompt set: `the-caption-3ce91a4-validation-closure-r1`
- bundle SHA-256: `995481ad58ad1bc11628bfd8b8978ed904d62989a28caa87268b30d5c5a58695`
- evaluation set: `the-caption-standard14-r1` revision `r1`
- quality rating: `outcome-abstract-condition-preserving-owner-diagnostic-v13`
- rating contract SHA-256: `d2dd4096911c35257c2866872d071f2ee5137bb3dcb6a7b279853e3ebe581f1f`
- target repository: `THE-CAPTION@3ce91a403f9e0c83f29d56bbe9e7b449b713445d`
- target tree: `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`
- model: `gpt-5.6-sol`
- runtime: Codex CLI `0.144.0`、Python `3.14.5`、memories `false`
- permission: `workspace-write`、approval `never`
- repetition: 14 case × `N=5` = 70 slot / level
- schedule: global queue、`M=24`
- token accounting: all-agent / `v1`
- evaluation set identity SHA-256: `430d1d4b70b7e670d03048954c6ef1ec588da593d562cb832d58bd51ad7b11db`

prompt identity、case、TaskSpec、permission、executor parameter、rating、反復条件はreasoning effort以外を変更していない。各新規campaignは同時実行せず、`low`、`medium`、`xhigh`、`max`、`ultra`の順にそれぞれ`M=24`で実行した。

## 3 KPI

| reasoning | score分布 | `quality_score`中央値 | all-agent `total_tokens`中央値 | `elapsed_seconds`中央値 | 70件token合計 | 70件elapsed合計 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `low` | `4 = 70` | 100.000 | 2,000,274 | 901.850秒 | 9,884,671 | 4,323.913秒 |
| `medium` | `4 = 70` | 100.000 | 1,923,688 | 948.869秒 | 9,475,504 | 4,754.179秒 |
| `high`（既存） | `4 = 70` | 100.000 | 2,131,059 | 1,114.525秒 | 10,863,680 | 5,525.379秒 |
| `xhigh` | `4 = 70` | 100.000 | 2,263,485 | 1,382.917秒 | 11,423,628 | 6,940.946秒 |
| `max` | `4 = 70` | 100.000 | 2,382,990 | 1,851.930秒 | 11,955,598 | 9,100.296秒 |
| `ultra` | `4 / 0 = 69 / 1` | 100.000 | 3,407,392 | 2,188.151秒 | 16,636,231 | 10,721.935秒 |

`high`との差は次のとおりである。

| reasoning - `high` | quality中央値差 | token中央値差 | elapsed中央値差 | token合計差 | elapsed合計差 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `low` - `high` | 0.000 | -130,785（-6.14%） | -212.676秒（-19.08%） | -979,009（-9.01%） | -1,201.466秒（-21.74%） |
| `medium` - `high` | 0.000 | -207,371（-9.73%） | -165.656秒（-14.86%） | -1,388,176（-12.78%） | -771.199秒（-13.96%） |
| `xhigh` - `high` | 0.000 | +132,426（+6.21%） | +268.392秒（+24.08%） | +559,948（+5.15%） | +1,415.568秒（+25.62%） |
| `max` - `high` | 0.000 | +251,931（+11.82%） | +737.405秒（+66.16%） | +1,091,918（+10.05%） | +3,574.917秒（+64.70%） |
| `ultra` - `high` | 0.000 | +1,276,333（+59.89%） | +1,073.625秒（+96.33%） | +5,772,551（+53.14%） | +5,196.557秒（+94.05%） |

`medium`は`low`比でtoken中央値`-76,586`（`-3.83%`）、token合計`-409,167`（`-4.14%`）だった。一方、elapsed中央値は`+47.019秒`（`+5.21%`）、elapsed合計は`+430.267秒`（`+9.95%`）だった。同一品質中央値の範囲で、tokenとelapsedの最小水準は一致しなかった。

## 診断

診断値は3 KPIへ追加せず、quality scoreを変更しない。

| reasoning | command protocol violation | owner-producer evidence inadmissible | F10 Monthly数値line |
| --- | ---: | ---: | ---: |
| `low` | 0 | 55 | exact 3 / mismatch 2 |
| `medium` | 0 | 55 | exact 5 |
| `high`（既存） | 0 | 55 | exact 5 |
| `xhigh` | 0 | 55 | exact 5 |
| `max` | 0 | 55 | exact 5 |
| `ultra` | 131 | 46 | exact 5 |

`low`のF10 Monthly数値line mismatch 2件はRating v13ではdiagnostic-onlyであり、提示した成果条件と必須試験の成立に影響しない。

Ultraでは推論設定以外の入力条件を変更していないが、70 runのうち14 runがchild sessionを起動した。他の5水準は全70 runがroot-onlyだった。

| reasoning | childありrun | session合計 | child / additional token合計 |
| --- | ---: | ---: | ---: |
| `low` | 0 / 70 | 70 | 0 |
| `medium` | 0 / 70 | 70 | 0 |
| `high`（既存） | 0 / 70 | 70 | 0 |
| `xhigh` | 0 / 70 | 70 | 0 |
| `max` | 0 / 70 | 70 | 0 |
| `ultra` | 14 / 70 | 92 | 2,515,395 |

Ultraの131件のcommand protocol violationはchild sessionが実行したcommandの機械bind証拠不足を含む。これはKPIへ追加せず、Ultraでだけ観測した実行経路として保存する。

## High / Mediumのcase別挙動差

HighとMediumの保存済み70 runずつについて、custom tool call、assistant message、patch wave、model-visible required commandの発行単位をcase別に再確認した。この節は公式3 KPIへの追加ではなく、reasoning effortによる実行経路のdiagnosticである。

### validation closure

model-visibleな複数required commandが、一つのcustom tool call内から個別`exec_command`として発行されたrunを1-step closureと数えた。両水準ともcommand protocol violationは0件である。

| 複数required command case | High | Medium |
| --- | ---: | ---: |
| F01 domain duplicate asset key | 5 / 5 | 5 / 5 |
| F02 cross-layer history date bound | 5 / 5 | 5 / 5 |
| F03 atomic context cleanup | 5 / 5 | 5 / 5 |
| F04 web audit column visibility | 3 / 5 | 0 / 5 |
| F06 restore empty snapshot contract | 5 / 5 | 5 / 5 |
| F07 canonical V4 runner | 5 / 5 | 5 / 5 |
| F07 dependency provenance pair | 5 / 5 | 5 / 5 |
| 合計 | 33 / 35 | 30 / 35 |

明確なclosure差はF04だけだった。他6 caseはHigh / Mediumとも5 / 5で同じだった。

### 探索、plan、修正wave

保存traceで`rg --files -uu`またはhiddenを含む広域searchをrepository-wide inventory、`update_plan`をplan使用として数えた。

- A01はrepository-wide inventoryがHigh 4 / 5、Medium 0 / 5だった。両水準とも変更やtestへ進まず、未固定値を質問して終了した。
- A02はrepository-wide inventoryがHigh 3 / 5、Medium 0 / 5だった。両水準とも5 / 5で成果条件を満たした。
- F07 canonicalはplan使用がHigh 4 / 5、Medium 0 / 5、repository-wide inventoryがHigh 3 / 5、Medium 1 / 5だった。custom tool call平均はHigh 6.0、Medium 4.4だった。
- F02はHigh iteration 3だけpatchが3 waveに分かれ、初回実装後にtest assertionの修正とformat修正を行った。Mediumは5 runすべて1 patch waveだった。custom tool call平均はHigh 8.2、Medium 7.0だった。

一方、F05 clarification / out-of-scopeは両水準とも各run 1 custom tool call、2 assistant messageで一致した。全体でもHigh / Mediumはともに70 / 70 score `4`、child session 0 / 70、command protocol violation 0、owner-producer evidence inadmissible 55、F10 Monthly数値位置exact 5 / 5だった。

### 考察

事実として、Highは一部caseで広域探索、plan更新、修正waveがMediumより多かった。Mediumのtoken中央値とelapsed中央値がHighより小さかったことは、この追加経路と整合する。ただし、保存traceだけからreasoning effortが各追加行動の直接原因だとは確定しない。

また、Highが一律に安定していたわけではない。1-step closureの差はF04に限定され、Highも2 / 5で逐次model再入を残した。MediumはF04で0 / 5だったが、他6 caseではHighと同じ35件中30件をclosureした。したがって、F04は一般的な推論不足ではなく、`npm ci`、lint、buildに対する「順に」「個別」の解釈とreasoning effortが相互作用した可能性が高い。

後続の[Candidate81 standard14 result](candidate71-candidate81-validation-wrapper-precedence-v13-medium-standard14-n5_2026-07-26.md)では、MediumのF04が5 / 5、複数required command case全体が35 / 35 closureとなり、70 / 70 score `4`を維持した。targeted F04 N=10でも10 / 10だった。この後続証拠は、reasoning levelを上げるのではなく、後段の「順に」「1 commandずつ個別」をwrapper内の発行順とinvocation単位へpromptで固定する方が、同一課題の挙動安定化に直接対応したことを示す。これはCandidate81の評価範囲内の判断であり、別課題への一般化や採用、release、本体反映を意味しない。

## 保存artifact

| reasoning | result ID | compatibility key | comparison conditions SHA-256 |
| --- | --- | --- | --- |
| `low` | `cae2cd0d060a4691a252990dae8cd7f3` | `62e313df117725112dae68c4743a63f279d1c9f4d8f0e829e8ddb59e909c6339` | `1717a29c5d784a7f05bed321d2846190f48ab70f5dce6e0f9c58eb221df3bebc` |
| `medium` | `267130a37c3544c7bb6e39c94f03c6e4` | `79ed04a45971db8ffc2287aea064af8b448008da510d27ceefd70862e0ad40d8` | `f76bf65fef7dbedd26cc7afaa66e7a4fe1af60f968d37eb88e72091dd91fcbbb` |
| `high`（既存） | `1b3d8048c391460eae8234e083494763` | `7426ecd03421590549c30a4e16373722153ceefc00280bc305eedb1aa0955633` | `2a0178f296d603f9db3db726ea853104eb2faf94a1cad70aaa8c2b8b00683564` |
| `xhigh` | `6422f299022046c9bd12dccdcc998b4e` | `b59e96317b95839c0c06a169ab25d39eae825dc27513ebfabd635a6fb891da03` | `565a45cc9d3b4655be95dac6b7aab138a2eafb783c184c9e40fee5c4a0631b4d` |
| `max` | `f0aa35f2bb04451e8473b409d9adc2bd` | `a007429ae724cd36d821ef54f629dd3b5798608533ad9792b11c0f2540e6c461` | `b47b3eeb804ea3c8995faa84fb4da9233dfbb8c9505a8d35e655a8347db06198` |
| `ultra` | `ce9dc3e24daf473a847a5afbaf723c0a` | `efb722bc66d1e69c39f3ff07a1a3e757e63d0dbc058f5bf483f01ff87388a436` | `e48a8457337b3dde0ebb57d2f63a937dbfafea99bfc822b5eca06cb50cec6d50` |

- result registry: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/result-registry-v3`
- campaign root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs`

新規5水準の各campaignに`batch-001/compact/final-compact-receipt.json`を保存した。raw execution evidenceはrepositoryへcommitしない。
