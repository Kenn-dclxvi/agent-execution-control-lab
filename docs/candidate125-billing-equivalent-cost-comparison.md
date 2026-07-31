# Candidate125課金換算比較

## 結論

Candidate125のStandard14 N=5を、通常input、cached input、cache write、outputへ分解し、GPT-5.6の公開API単価で課金換算した。

THE-CAPTIONの70 run合計では、Candidate125 Solは`$15.5472`だった。これはControlFreeRepositoryの`$25.1562`に対して`-38.20%`、Baselineの`$91.6701`に対して`-83.04%`である。

Candidate125 Solは、root制御を0 byteにしたControlFreeRepositoryより品質を回復しながら、課金換算額も小さかった。ControlFreeRepositoryは70件中65件がscore `4`、A01の5件がscore `0`だった。Candidate125 Solは70 / 70件がscore `4`だった。

本書の最後に、ControlFreeRepositoryを`1.00倍 = 100%`とした比較表を示す。この表を、今回の具体的な効果を読むための結論とする。

## 対象

すべて14 case、各case N=5、合計70 runの保存済みall-agent usageを集計した。

| 対象 | model | score分布 | quality中央値 | result ID |
|---|---|---:|---:|---|
| Baseline | GPT-5.6 Sol | `4 / 3 / 1 / 0 = 63 / 2 / 1 / 4` | `92.857` | `107d31cdae9044d08c0768ffc89d3896` |
| ControlFreeRepository | GPT-5.6 Sol | `4 / 0 = 65 / 5` | `92.857` | `3fb81b94ef1d4770b52bc202bf0a43d8` |
| Candidate125 THE-CAPTION | GPT-5.6 Sol | `4 = 70` | `100.000` | `96fb571308de4c08a7aeed0faefb7d72` |
| Candidate125 Click | GPT-5.6 Sol | `4 / 1 = 65 / 5` | `94.643` | `7560599fef024dfb8011264352707ab8` |
| Candidate125 THE-CAPTION | GPT-5.6 Terra | `4 = 68` | `100.000` | `b328615bd42b4447ad9c7ad6fc93945a` |
| Candidate125 THE-CAPTION | GPT-5.6 Luna | `4 = 67` | `92.857` | `0736e412cd6c49048400ccc8a9993528` |

一次resultは次を参照する。

- [Baseline / ControlFreeRepository Rating v13 Medium Standard14 N=5](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)
- [Candidate118 / Candidate125 Rating v14 Medium Standard14 N=5](../evaluations/results/candidate118-candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md)
- [Candidate125 Sol / Terra / Luna](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md)
- [Click Candidate125 Medium Standard14 N=5](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md)

BaselineとControlFreeRepositoryはRating v13、Codex CLI `0.144.0`である。Candidate125はRating v14、Codex CLI `0.146.0`である。Clickはtarget repositoryとcaseも異なる。本書では、これらを一つの互換KPIにはせず、保存usageを現在の同じ単価へ換算した記述的なcost比較として並べる。

## 課金換算方法

`input_tokens`はcached inputとcache writeを含む。このため、通常inputを次の式で求めた。

```text
通常input = input_tokens - cached_input_tokens - cache_write_input_tokens
```

GPT-5.6各modelの公開API単価は次のとおりである。単位は100万token当たりの米ドルである。

| model | 通常input | cached input | cache write | output |
|---|---:|---:|---:|---:|
| GPT-5.6 Sol | `$5.00` | `$0.50` | `$6.25` | `$30.00` |
| GPT-5.6 Terra | `$2.00` | `$0.20` | `$2.50` | `$12.00` |
| GPT-5.6 Luna | `$0.20` | `$0.02` | `$0.25` | `$1.20` |

公式価格は[Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol)、[Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra)、[Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna)を参照した。

model内の比率は共通である。cached inputは通常inputの`0.1倍`、cache writeは`1.25倍`、outputは`6倍`である。そこで、異なるtoken区分を一つの量として読むために、次の「通常input換算token」も計算した。

```text
通常input換算token
  = 通常input
  + cached input x 0.1
  + cache write x 1.25
  + output x 6
```

reasoning outputはoutput tokenへ含めた。保存rolloutをrequest単位で確認した結果、272K inputを超えるrequestはなかった。このため長文割増は発生していない。

Candidate125のusageではcache writeが明示的に`0`だった。BaselineとControlFreeRepositoryの旧usage schemaにはcache write項目がないため、本集計では`0`として扱った。

ここで示す金額は保存tokenを公開API単価へ掛けた換算値であり、Codexの契約プランに対する実請求額ではない。

## 70 runの課金内訳

各token欄は「token数 / 価格」を示す。

| 対象 | 通常input | cached input | cache write | output | 通常input換算token | API価格換算 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline Sol | 8,281,550 / `$41.4078` | 55,057,408 / `$27.5287` | 0 / `$0` | 757,789 / `$22.7337` | 18,334,025 | **`$91.6701`** |
| ControlFreeRepository Sol | 2,412,903 / `$12.0645` | 14,567,424 / `$7.2837` | 0 / `$0` | 193,598 / `$5.8079` | 5,031,233 | **`$25.1562`** |
| Candidate125 THE-CAPTION Sol | 1,771,526 / `$8.8576` | 4,948,224 / `$2.4741` | 0 / `$0` | 140,516 / `$4.2155` | 3,109,444 | **`$15.5472`** |
| Candidate125 Click Sol | 1,415,510 / `$7.0776` | 5,332,992 / `$2.6665` | 0 / `$0` | 124,771 / `$3.7431` | 2,697,435 | **`$13.4872`** |
| Candidate125 THE-CAPTION Terra | 1,712,543 / `$3.4251` | 7,440,384 / `$1.4881` | 0 / `$0` | 135,964 / `$1.6316` | 3,272,365 | **`$6.5447`** |
| Candidate125 THE-CAPTION Luna | 2,336,543 / `$0.4673` | 13,419,520 / `$0.2684` | 0 / `$0` | 184,475 / `$0.2214` | 4,785,345 | **`$0.9571`** |

## 1 iteration当たりの価格

Standard14の14 caseを一回ずつ実行したまとまりを1 iterationとする。中央値と、70 run合計を5で割った平均は次のとおりである。

| 対象 | 1 iteration価格中央値 | 5 iteration平均 |
|---|---:|---:|
| Baseline Sol | **`$17.2257`** | `$18.3340` |
| ControlFreeRepository Sol | **`$5.0568`** | `$5.0312` |
| Candidate125 THE-CAPTION Sol | **`$3.0492`** | `$3.1094` |
| Candidate125 Click Sol | **`$2.6968`** | `$2.6974` |
| Candidate125 THE-CAPTION Terra | **`$1.2735`** | `$1.3089` |
| Candidate125 THE-CAPTION Luna | **`$0.1974`** | `$0.1914` |

## cacheの位置付け

cache率だけではcostを判断できない。

| 対象 | cache率 | cached input | 通常input換算token | API価格換算 |
|---|---:|---:|---:|---:|
| Baseline Sol | `86.93%` | 55,057,408 | 18,334,025 | `$91.6701` |
| ControlFreeRepository Sol | `85.79%` | 14,567,424 | 5,031,233 | `$25.1562` |
| Candidate125 THE-CAPTION Sol | `73.64%` | 4,948,224 | 3,109,444 | `$15.5472` |
| Candidate125 Click Sol | `79.02%` | 5,332,992 | 2,697,435 | `$13.4872` |
| Candidate125 THE-CAPTION Terra | `81.29%` | 7,440,384 | 3,272,365 | `$6.5447` |
| Candidate125 THE-CAPTION Luna | `85.17%` | 13,419,520 | 4,785,345 | `$0.9571` |

Baselineはcache率が最も高い。それでもcached inputの絶対量が5,506万tokenあり、通常inputとoutputも大きいため、Solの中で最も高額になった。

Candidate125 Solのcache率はBaselineより低い。しかし、通常input、cached input、outputの絶対量がすべて小さい。その結果、課金換算額はBaseline比`-83.04%`になった。

また、outputは通常inputの6倍で換算される。Candidate125 Solのoutputは全raw tokenの約`2.05%`だが、価格では全体の約`27.11%`を占める。costを見るときはtotal tokenだけでなく、outputの削減も重要である。

## 追加測定

Candidate125のTargeted 5ケース N=5とA02 N=20も同じ方法で集計した。run数とcase構成が異なるため、70 runの結論表には混ぜない。

| 測定 | run数 | 通常input | cached input | cache write | output | API価格換算 |
|---|---:|---:|---:|---:|---:|---:|
| Targeted 5ケース N=5 | 25 | 749,590 / `$3.7480` | 2,097,920 / `$1.0490` | 0 / `$0` | 56,603 / `$1.6981` | **`$6.4950`** |
| A02 N=20 | 20 | 700,641 / `$3.5032` | 1,734,400 / `$0.8672` | 0 / `$0` | 50,783 / `$1.5235` | **`$5.8939`** |

## 読み取れる効果

Baselineからroot制御を外したControlFreeRepositoryでは、70 runの価格換算が`$91.6701`から`$25.1562`へ下がった。差は`-$66.5140`、率は`-72.56%`である。一方、A01は5 / 5件がscore `0`だった。制御をゼロにするだけでは品質境界を維持できなかった。

Candidate125 SolはControlFreeRepositoryよりさらに`-$9.6089`、`-38.20%`となり、70 / 70件でscore `4`だった。今回の保存結果では、必要な制御を追加したことがFreeに対するcost増加になっていない。品質を回復しながら、通常input、cached input、outputの総量を下げている。

TerraとLunaはmodel単価がSolより低いため、raw tokenが増えても価格換算は小さくなる。ただしTerraは2件、Lunaは3件がscore `4`へ到達しなかった。したがって、価格だけでSolと同じ成果を得たとは扱わない。

Click Candidate125はFree比`-46.39%`だった。ClickのF10 5件はrepository authorityがないため、固定契約どおりscore `1`で停止した。他13 caseは65 / 65件がscore `4`だった。

## 結論: ControlFreeRepositoryを基準にした具体的効果

ControlFreeRepositoryの70 run合計`$25.1562`を`1.00倍 = 100%`とする。

| 対象 | 70 run API価格換算 | Free比 | Freeからの増減 | 具体的な効果 |
|---|---:|---:|---:|---|
| Baseline Sol | `$91.6701` | **3.644倍（364.40%）** | **+264.40%** | Freeの約3.64倍を使用し、品質中央値は同じ`92.857` |
| ControlFreeRepository Sol | `$25.1562` | **1.000倍（100.00%）** | 基準 | A01の5件がscore `0` |
| Candidate125 THE-CAPTION Sol | `$15.5472` | **0.618倍（61.80%）** | **-38.20%** | Freeより38.20%低く、70 / 70件がscore `4` |
| Candidate125 Click Sol | `$13.4872` | **0.536倍（53.61%）** | **-46.39%** | authorityがある13 caseは65 / 65件がscore `4` |
| Candidate125 THE-CAPTION Terra | `$6.5447` | **0.260倍（26.02%）** | **-73.98%** | 大幅に低価格だが、score `4`は68 / 70件 |
| Candidate125 THE-CAPTION Luna | `$0.9571` | **0.038倍（3.80%）** | **-96.20%** | 最小価格だが、score `4`は67 / 70件、品質中央値`92.857` |
