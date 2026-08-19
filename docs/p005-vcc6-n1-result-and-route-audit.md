# P005 VCC6 N=1結果とroute監査

> [!IMPORTANT]
> **結果**: `6/6 valid / Score 4 x6 / mechanism 6/6 / N=5 allowed / no stability claim`

## 結論

P005 `p005-portable-full-agent-codex-validation-terminal-projection-r1`は、固定VCC6のcandidate-only N=1 gateを通過した。P004で失敗したH06もScore 4かつmechanism passとなり、raw nested resultをouter output producerにしない境界がこのrunでは成立した。

N=5実施条件は満たしたが、N=1は効率差や安定性を判断する比較結果ではない。P001からP004までの保存済みrunも再実行していない。

## 集計

| 指標 | P005 N=1 |
| --- | ---: |
| valid | 6 / 6 |
| Score 4 | 6 / 6 |
| mechanism pass | 6 / 6 |
| total tokens | 317,976 |
| median tokens | 50,114 |
| elapsed合計 | 192.665106667秒 |
| elapsed中央値 | 31.04529125秒 |

参考として同じ共有runnerのP004 N=1は302,483 tokens、195.566762168秒だった。P005はtokensが15,493増え、elapsedが2.901655501秒短かったが、1反復の分布差をpromptの安定した効率効果とは扱わない。

## H06 route

P004 H06はraw outer output 8,672 bytes、forbidden raw substringあり、terminal projection 1回でScore 1だった。P005 H06は次の結果になった。

- raw outer output: 342 bytes。
- forbidden terminal output substring: 0件。
- terminal projection: 1回。
- model-visible response between validation results: 0件。
- final response、action、event: すべてoracleとexact一致。

この差は、成功時のwrapper手順を転記した結果ではない。P005はraw nested resultをcarrier-local ownerへ固定し、plan terminal後のterminal projection objectだけへouter projection permissionを与えた。

## 次の境界

次に許可されるのは、同じVCC6、同じLayer 1、同じrunner bytesでP005をN=5へ拡張することだけである。N=5のpreflight前に非prompt条件の完全一致とfresh slotを確認する。Standard14、adoption、releaseおよびtarget本体へのprojectionは未承認である。
