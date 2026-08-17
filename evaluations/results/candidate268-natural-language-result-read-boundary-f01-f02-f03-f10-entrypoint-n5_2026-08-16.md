# Candidate268 自然語result・read境界 F01・F02・F03・F10 entrypoint N=5

## 結論

Candidate268は、Candidate254を直接の基盤としてCandidate264とCandidate267から得た関係を自然語だけで再構成したが、追加N、Standard14、採用、releaseおよびprojectionへは進めない。20 / 20件がvalidかつScore `4`で、F10のinstruction result先行と必要read完遂は5 / 5件だった。一方、C147で成立しC268で保持すべきF02の開始確認と許可済みreadの共同発行は4 / 5件に後退し、validationのnonterminal resultをterminalとして扱わない境界も13 / 20件で保持できなかった。

したがって、F10だけを達成したことをCandidate254系全体の自然語再構成成立とは扱わない。状態は`quality_passed / f10_passed / f01_f03_preserved / f02_mechanism_failed / terminal_closure_failed / unjustified_cost_regression / stopped`である。追加N、Standard14、採用、releaseおよびprojectionへ進めない。

この評価停止はCandidate268の系譜上の破棄を意味しない。次の自然語改善ではCandidate268を直接基盤とし、F10、F01およびF03の成立効果を保持しながら、F02とterminal closureを未完了predicateとしてC268との差分で詰める。Candidate254は系譜と診断比較の参照に限り、次案をC254から作り直さない。

## 目的と比較基準

- 直接の親と実装基盤はCandidate254である。
- Candidate263からCandidate267までは、成立効果と失敗反例を自然語へ戻すためのfeedback evidenceに限る。
- Candidate147は本文の複写元ではなく、機序とKPIの比較基準に限る。
- C268のprompt本文には形式記法、Candidate番号またはC147本文を入れていない。

比較前receiptはCandidate254登録result `4208b6ca016d485684f8df9fadc5b38e`へ固定し、prompt identity以外の条件が一致した後にCandidate268の不足20件だけを発行した。Candidate254とCandidate147のslotは再実行していない。

## ケース別機序

| ケース | 対象境界 | Candidate268 | 判断 |
| --- | --- | ---: | --- |
| F01 | 開始確認と許可済みreadを同じmodel stepから発行 | 5 / 5 | 保持 |
| F02 | 開始確認と許可済みreadを同じmodel stepから発行 | 4 / 5 | 不通過 |
| F03 | 開始確認と許可済みreadを同じmodel stepから発行 | 5 / 5 | 保持 |
| F10 | exact `src/AGENTS.md`のterminal success content result後にだけ配下readを発行 | 5 / 5 | 成立 |
| F10 | instruction result後に必要な配下readを完遂 | 5 / 5 | 成立 |

F02 iteration 4のrun `8e4ed55acc854576b0c880f7adc380c2`は、`pwd`、branch、HEAD、statusの開始確認resultを受け取った後に、四つの許可済みsource / test readを別のmodel stepから発行した。これはC264で確認した効果を自然語へ完全には戻せていない直接反例である。

## モデル再入とterminal境界

従来の狭い定義である外部`wait`呼び出しは0回だった。しかし、これは改善ではない。F01の5件、F02の3件、F03の5件、合計13件でvalidation invocationがnonterminal resultを返した後、同じcellの完了を待ったrunは0件だった。

- 3件は、pending resultをbindしないまま別の`exec`を発行してmodelへ再入した。
- 10件は、nonterminal result後に別tool callを発行せず終了した。

このため、C267で観測した29回の外部`wait`が消えたことをcost改善として採用できない。C268では、合法な待機費用を削ったのではなく、terminal result受領前に先へ進む別の誤経路へ移った。quality scoreは保存workspaceから後に収集したcommand evidenceで必須commandの成功を確認できるため20 / 20 Score `4`となったが、実行時のterminal closure成立を意味しない。

## KPI比較

### 全体

| Candidate | quality | total_tokens | elapsed_seconds |
| --- | ---: | ---: | ---: |
| Candidate147 | 100.0 | 494,706 | 302.929 |
| Candidate254 | 100.0 | 578,975 | 293.129 |
| Candidate268 | 100.0 | 633,513 | 333.267 |
| Candidate268 − Candidate147 | 0.0 | `+138,807`、`+28.06%` | `+30.339`、`+10.02%` |
| Candidate268 − Candidate254 | 0.0 | `+54,538`、`+9.42%` | `+40.138`、`+13.69%` |

C268はC267比ではtoken `-0.45%`、経過時間`-2.41%`にすぎず、N=5の揺れを超える改善とは扱わない。しかもterminal closureを失っているため、この差を採用根拠にできない。

### ケース中央値

| ケース | C147 token / 秒 | C254 token / 秒 | C268 token / 秒 | C268 − C147 | C268 − C254 |
| --- | ---: | ---: | ---: | ---: | ---: |
| F01 | 107,202 / 66.424 | 113,598 / 56.578 | 146,693 / 78.379 | token `+36.84%`、秒 `+18.00%` | token `+29.13%`、秒 `+38.53%` |
| F02 | 128,236 / 100.607 | 184,341 / 85.479 | 184,623 / 98.814 | token `+43.97%`、秒 `-1.78%` | token `+0.15%`、秒 `+15.60%` |
| F03 | 104,320 / 70.866 | 182,945 / 87.773 | 140,781 / 85.899 | token `+34.95%`、秒 `+21.21%` | token `-23.05%`、秒 `-2.13%` |
| F10 | 87,934 / 61.546 | 105,979 / 68.331 | 113,017 / 68.214 | token `+28.52%`、秒 `+10.83%` | token `+6.64%`、秒 `-0.17%` |

C147との差は四ケースすべてのtokenで大きい。C268の目的は単にF10を閉じることではなく、自然語だけで必要な制御を成立させることなので、このKPI差とF02反例を残したまま新しいcarrier制御へ進まない。

## 再入以外の課題

F02は5 / 5件でmodel-visible outputのtruncationを観測し、F03も1 / 5件で観測した。C268の外部`wait`が0回でもF02 token中央値はC147比`+43.97%`だったため、C267のcost退行をモデル再入だけでは説明できない。大きなsource / test readを一つのcarrierへ載せ、必要regionが欠けた後に追加readまたは追加判断へ進めるpermissionは残っている。

ただし、これを直すcarrier差分を次Candidateへ先行させない。まず必要なのは、C147で成立していた開始確認と許可済みreadの共同発行、およびterminal resultを待つ境界を、C268で成立したF10閉鎖と同時に自然語だけで保持できる構成へ進めることである。

## 評価アーティファクト

- 登録result: [`f43e7342001140b38f7f33e5bcb73cac.json`](f43e7342001140b38f7f33e5bcb73cac.json)
- 品質監査: [`candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json`](candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-quality-audit-r1.json)
- 機序監査: [`candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json`](candidate268-natural-language-result-read-boundary-f01-f02-f03-f10-entrypoint-n5-mechanism-audit-r1.json)

最初の`register-selection-result`は`--reference-result-id`と`--cycle`を省略したため、四ケースだけのfixture集合を持つ非互換result `7e238bcbaf93457aa2e153d64ec69fd9`をappend-only registryへ作成した。このresultは比較、本文、採用判断に使用していない。正しい登録resultはCandidate254の完全なcompatibility key `7ca205650dc15458645bef639d86ea2c742095941540def54847ea4593783c70`を持つ`f43e7342001140b38f7f33e5bcb73cac`である。
