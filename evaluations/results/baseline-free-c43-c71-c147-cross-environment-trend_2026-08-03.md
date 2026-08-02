# Baseline / Free / Candidate43 / Candidate71 / Candidate147 試験環境別推移

## 結論

Baseline、ControlFreeRepository（以下Free）、Candidate43、Candidate71を同時に比較できるStandard14 `N=5`環境は、Rating v13 High、Rating v13 Medium、Rating v14 Mediumの3つである。この3環境では、次の傾向が共通している。

1. 品質分布は、BaselineとFreeに低scoreが残り、Candidate43とCandidate71は70 / 70件がscore `4`だった。
2. token中央値とelapsed中央値の順序は、3環境すべてで`Candidate71 < Candidate43 < Free < Baseline`だった。
3. Candidate71のCandidate43比は、tokenが`-29.19%`から`-35.58%`、elapsedが`-5.63%`から`-10.59%`の範囲で小さかった。
4. Candidate147を加えた互換比較はRating v14 Mediumだけである。この環境では5条件中Candidate147の集約tokenとelapsedが最小で、70 / 70件がscore `4`だった。

ただし、rating、reasoning、Evaluation set identity、Agent / CLIが異なる環境間の絶対値は互換比較ではない。環境をまたぐ増減をpromptの改善または悪化へ帰属しない。本書では、同一環境内の順位と、環境を変えても維持された方向だけを横断傾向として扱う。

## 対象と読み方

- 品質は公式score分布を省略せずに読む。`quality_score`中央値が同じでも、低scoreの有無は別の品質情報である。
- tokenはall-agent `total_tokens`、elapsedはStandard14全体の反復別中央値である。
- Rating v10 / v12の連続試験、Rating v13のreasoning水準試験、Rating v14のCandidate147 `N=100`は、共通5条件比較と分けて各promptの安定性推移として扱う。
- `N`、coverage、iteration集合はatomic runのidentityではないが、集約値の標本数として明示する。

## 比較環境

| 環境 | rating | reasoning | CLI | coverage | 対象 | 互換比較の範囲 |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | v10 | High | 0.144 | Standard14、N=5 / B18 | C43 | E1内だけ |
| E2 | v12 | High | 0.144 | Standard14、N=5×18 Batch | C71 | E2内だけ |
| E3 | v13 | High | 0.144 | Standard14、N=5 | Baseline / Free / C43 / C71 | E3の4条件内 |
| E4 | v13 | Medium | 0.144 | Standard14、N=5 | Baseline / Free / C43 / C71 | E4の4条件内 |
| E5 | v14 | Medium | 0.146 | Standard14、atomic N=5 | Baseline / Free / C43 / C71 / C147 | E5の5条件内 |
| E6 | v14 | Medium | 0.146 | Standard14、atomic N=100 | C147 | E5と同じatomic実効条件のsample拡張 |

E3とE4はreasoningだけが異なる記述軸である。E4とE5はrating、Evaluation set identity、Agent / CLI条件が異なる。したがって、E3↔E4およびE4↔E5はLayer 4の互換comparisonではない。

## 共通N=5環境の推移

### Rating v13 High（E3）

| prompt | score分布 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 1 / 0 = 62 / 2 / 3 / 3` | 92.857 | 12,568,833 | 3,628.547秒 |
| Free | `4 / 0 = 65 / 5` | 92.857 | 3,918,502 | 1,308.201秒 |
| C43 | `4 = 70` | 100.000 | 3,109,899 | 1,180.979秒 |
| C71 | `4 = 70` | 100.000 | 2,131,059 | 1,114.525秒 |
| C147 | 未実施 | — | — | — |

### Rating v13 Medium（E4）

| prompt | score分布 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 1 / 0 = 63 / 2 / 1 / 4` | 92.857 | 11,977,774 | 3,568.742秒 |
| Free | `4 / 0 = 65 / 5` | 92.857 | 3,496,976 | 1,250.057秒 |
| C43 | `4 = 70` | 100.000 | 2,716,869 | 1,061.204秒 |
| C71 | `4 = 70` | 100.000 | 1,923,688 | 948.869秒 |
| C147 | 未実施 | — | — | — |

### Rating v14 Medium（E5）

| prompt | score分布 | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | ---: | ---: | ---: |
| Baseline | `4 / 3 / 0 = 65 / 1 / 4` | 92.857 | 13,624,982 | 3,333.567秒 |
| Free | `4 / 0 = 65 / 5` | 92.857 | 3,488,611 | 1,166.296秒 |
| C43 | `4 = 70` | 100.000 | 3,151,442 | 1,091.549秒 |
| C71 | `4 = 70` | 100.000 | 2,030,116 | 988.187秒 |
| C147 | `4 = 70` | 100.000 | 1,447,626 | 852.543秒 |

## 同一環境内の差

負値は、後者のpromptが前者より小さいことを示す。

| 環境 | 比較 | token中央値差 | elapsed中央値差 | 品質上の前提 |
| --- | --- | ---: | ---: | --- |
| E3 v13 High | Free - Baseline | -68.82% | -63.95% | 両方に低scoreあり |
| E4 v13 Medium | Free - Baseline | -70.80% | -64.97% | 両方に低scoreあり |
| E5 v14 Medium | Free - Baseline | -74.40% | -65.01% | 両方に低scoreあり |
| E3 v13 High | C43 - Free | -20.64% | -9.72% | C43だけ70 / 70 score `4` |
| E4 v13 Medium | C43 - Free | -22.31% | -15.11% | C43だけ70 / 70 score `4` |
| E5 v14 Medium | C43 - Free | -9.66% | -6.41% | C43だけ70 / 70 score `4` |
| E3 v13 High | C71 - C43 | -31.47% | -5.63% | 両方70 / 70 score `4` |
| E4 v13 Medium | C71 - C43 | -29.19% | -10.59% | 両方70 / 70 score `4` |
| E5 v14 Medium | C71 - C43 | -35.58% | -9.47% | 両方70 / 70 score `4` |
| E5 v14 Medium | C147 - C71 | -28.69% | -13.73% | 両方70 / 70 score `4` |

事実として、C71対C43の方向は3環境で再現した。C147対C71はE5の一環境だけであり、異なるratingまたはreasoningでも再現するかは未評価である。またE5のcase別tokenでは、C147がC71より高いcaseがF05 clarify、F05 out-of-scope、F06、F10 monthlyの4 / 14件ある。集約値の差を全case一様の低下と解釈しない。

## 環境変更時の絶対値の動き

次表はMediumのE4からE5への記述差であり、互換comparisonではない。

| prompt | score分布の動き | token中央値 | elapsed中央値 |
| --- | --- | ---: | ---: |
| Baseline | `63 / 2 / 1 / 4`から`65 / 1 / 0 / 4` | +13.75% | -6.59% |
| Free | `65 / 5`を維持 | -0.24% | -6.70% |
| C43 | 70 / 70 score `4`を維持 | +16.00% | +2.86% |
| C71 | 70 / 70 score `4`を維持 | +5.53% | +4.14% |
| C147 | E4未実施 | — | — |

Freeは絶対tokenがほぼ同じだった一方、Baseline、C43、C71は異なる幅で動いた。この非一様な変動は、異なるrating / Layer 1 / CLI環境の絶対値をprompt固有の時系列として直結できないことを示す。確定できるのは、各環境内の順位と品質分布である。

## prompt別の長期推移

### Baseline

- E3、E4、E5の全環境で品質中央値は`92.857`だった。
- 低scoreはE3で8 / 70件、E4で7 / 70件、E5で5 / 70件だった。ただしratingが異なるため、件数減少をprompt改善とは扱わない。
- A01の未固定値確認前の実装進行は、各環境で継続して観測された。
- tokenとelapsedは5条件中すべての共通環境で最大だった。

### Free

- E3、E4、E5の全環境で`4 / 0 = 65 / 5`、品質中央値`92.857`だった。
- 低score 5件はすべてA01であり、未固定値の確認前に編集・試験へ進む挙動が3環境で再現した。
- Baseline比ではtoken約69〜74%、elapsed約64〜65%小さかったが、品質gateは通過していない。

### Candidate43

| 環境 | sample | 公式score | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | --- | ---: | ---: | ---: |
| E1 v10 High | N=5 | `4 = 70` | 100.000 | 3,647,298 | 1,353.458秒 |
| E1 v10 High | B18、1,260 run | `4 / 3 / 1 = 1,255 / 4 / 1` | 100.000 | 3,286,761.0 | 1,176.261秒 |
| E3 v13 High | N=5 | `4 = 70` | 100.000 | 3,109,899 | 1,180.979秒 |
| E4 v13 Medium | N=5 | `4 = 70` | 100.000 | 2,716,869 | 1,061.204秒 |
| E5 v14 Medium | N=5 | `4 = 70` | 100.000 | 3,151,442 | 1,091.549秒 |

E1のB18では公式低scoreが5 / 1,260件現れた。保存traceではF10の正しいfindingの行位置不一致と、A01の確認表現を認識しなかった採点偽陰性が記録されている。E3〜E5のN=5では低scoreは観測されなかった。したがって、C43は3つの後続N=5環境で品質を維持したが、N=5だけを低頻度事象ゼロの証明には使わない。

### Candidate71

| 環境 | sample / reasoning | 公式score | quality中央値 | token中央値 | elapsed中央値 |
| --- | --- | --- | ---: | ---: | ---: |
| E2 v12 High | B18、1,260 run | `4 / 3 / 0 = 1,255 / 4 / 1` | 100.000 | 2,118,725.5 | 1,008.883秒 |
| v13 Low | N=5 | `4 = 70` | 100.000 | 2,000,274 | 901.850秒 |
| E4 v13 Medium | N=5 | `4 = 70` | 100.000 | 1,923,688 | 948.869秒 |
| E3 v13 High | N=5 | `4 = 70` | 100.000 | 2,131,059 | 1,114.525秒 |
| v13 XHigh | N=5 | `4 = 70` | 100.000 | 2,263,485 | 1,382.917秒 |
| v13 Max | N=5 | `4 = 70` | 100.000 | 2,382,990 | 1,851.930秒 |
| v13 Ultra | N=5 | `4 / 0 = 69 / 1` | 100.000 | 3,407,392 | 2,188.151秒 |
| E5 v14 Medium | N=5 | `4 = 70` | 100.000 | 2,030,116 | 988.187秒 |

v13ではMediumがtoken最小、Lowがelapsed最小だった。XHigh以上はHighよりtokenとelapsedがともに増えた。Ultraのscore `0`は、search pattern内の`pytest.fixture`をtest実行と誤認したRating v13偽陽性として保存traceで分類されている。

E2のB18では、意味確認後もA02の`git diff --check`未実行3件とA01の未固定mode確認前の実装1件が実質欠落として残った。後続v13 / v14のN=5では70 / 70 score `4`だったが、rating改訂と標本数の差があるため、B18で見つかった低頻度挙動がpromptだけで解消したとは断定しない。

### Candidate147

| 環境 | sample | 公式score | quality中央値 | token中央値 | elapsed中央値 |
| --- | ---: | --- | ---: | ---: | ---: |
| E5 v14 Medium | N=5、70 run | `4 = 70` | 100.000 | 1,447,626 | 852.543秒 |
| E6 v14 Medium | N=100、1,400 run | `4 = 1,400` | 100.000 | 1,394,412.5 | 831.914秒 |

E5からE6は同じatomic実効条件のsample拡張である。N=5からN=100へtoken中央値は`-3.68%`、elapsed中央値は`-2.42%`移動した。N=29以降のtoken中央値は約1.383M〜1.394M、elapsed中央値は824.903〜831.914秒で、一方向の増加はなかった。1,400 / 1,400件がscore `4`だったため、C147にはE5環境内で最も強い品質安定性証拠がある。一方、v13以前の互換試験はなく、環境横断の再現性は未評価である。

## 総合整理

### 事実

- Baseline / Free / C43 / C71の品質群分けとcost順位は、3つの共通N=5環境で同じだった。
- C71はC43より、3環境すべてでtokenとelapsedが小さかった。
- C147はv14 Mediumの同一環境でC71よりtokenとelapsedが小さく、N=100でも全件score `4`だった。
- BaselineとFreeは、reasoningまたはrating / CLIを変えてもA01の低scoreが残った。

### 推測ではなく限定付き解釈

- C43からC71へのcost低下は、一つの試験環境だけに依存しない方向として扱える。
- C147のC71比低下はv14 Mediumでの強い観測だが、環境横断で再現したとはまだ扱えない。
- C43 / C71の過去B18が示すとおり、N=5全件passは低頻度失敗ゼロの証明ではない。C147のN=100は、この点を補う同一環境内の証拠である。

### 判断境界

本書は保存済み一次resultの横断整理であり、新しい一次result、互換comparison、採用判断、release判断ではない。既存resultのstateとCandidate147の別artifactでの採用判断は変更しない。

## 参照result

- [Rating v13 High 共通N=5](baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)
- [Rating v13 Medium 共通N=5](baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)
- [Rating v14 Baseline / Free / C147 N=5](baseline-control-free-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md)
- [Rating v14 C43 / C71 / C147 N=5](candidate43-candidate71-candidate147-v14-medium-standard14-atomic-n5-cli0146_2026-08-03.md)
- [C43 Rating v10 N=5](candidate43-outcome-authority-boundary-v10-standard14-n5_2026-07-20.md)
- [C43 Rating v10 B18](candidate43-candidate69-model-reentry-decision-boundary-v10-standard14-continuous-n5-b18_2026-07-22.md)
- [C71 Rating v12 B18](candidate69-candidate71-validation-closure-v12-standard14-continuous-n5-b18_2026-07-22.md)
- [C71 Rating v13 reasoning 6水準](candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)
- [C147 Rating v14 N=100](candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)
