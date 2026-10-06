# STD14の開始履歴を保持する素材別版の実装方針 第1版

2026年10月4日。[工程7の最終判定](standard14-dedicated-stage7-final-verdict-r1.md)で特定した判断材料の欠落を解消するための実装仕様である。実装は未着手であり、この文書は追加の評価モデル実行を許可しない。

必要な成果は、全14ケースの要求・維持条件・難しさを保つ評価代替のうち、開始履歴の対応を満たす別版と、その局所受入証拠である。対象は `standard14-dedicated-control` の履歴構築と設計側の開始照合に限定する。方法は、受入済みの開始treeを変えずに、過去root・ケースseed・Free開始の関係を実物のGit objectとして組み直すことである。元TaskSpec、全42条件、採点、既存の素材・結果・発行前記録、Lowの不再発行、各N2、旧インスタンスを維持する。

## 許容差と維持条件

正本は[開始状態契約第2版](../evaluations/targets/standard14-dedicated-control/registrations/stage7-start-state-contract-r2.json)。工程1のroot0 byteという配置は、既存 `fixture/base/` と実行開始treeについて維持する。新版の構築時だけ、過去treeへ旧root原文を置く。旧本文を現在の指示として適用する変更ではない。

1. 過去rootは旧source `3ce91a403f9e0c83f29d56bbe9e7b449b713445d:AGENTS.md` の5980 byteを、契約に固定したhashで読み取る。58行という数だけを合わせたダミー本文や、新しい開始許可の説明で代替しない。生ログはコピーしない。
2. 正常な専用baseのコード・テスト・文書に過去rootだけを組み合わせ、履歴上のbaseを作る。旧素材の無関係な巨大な履歴を全面コピーしない。新baseの説明は `repository base` として新しい由来を偽装しない。
3. 故障を注入する10件では既存 `seed_operations` と同じ変更だけを適用し、baseを直接の親とするseedを作る。説明は旧と同じ `evaluation fixture seed`。SD14-05・06・11・13は故障注入がなく、seedはbaseの別名とし、空のseedを作らない。
4. seedからrootだけを0 byteにする一つのコミットを作り、説明は旧と同じ `repository authority` とする。これをFree開始とし、余分な `repository start` は置かない。開始時のbranch状態は旧側の固定開始構成へ合わせてdetachedにし、HEADと参照を設計側で記録する。過去の全84件のbranch同一性を確認したという意味ではない。
5. 全14件で新版開始treeのpath・type・mode・content・symlinkが旧専用版の対応する開始treeと一致することを要求する。Git identityと履歴、記録の診断容量だけが変わる。非root正本は旧Free原文を保持する。
6. 月次TaskSpecだけ固定seed SHAを新seedへ機械置換する。それ以外の配送TaskSpecはバイト一致。固定seedの直接親からの月次差分を残し、HEAD^をレビュー対象の代わりにしない。望ましい操作順は指定しない。

commit/tree/blob ID、作業領域パス、容量、baseより古い不要な履歴の切出しは許容する。開始前のroot削除、ケースの故障、baseとseedの同一性、seedの親、実行開始のbranch状態を未宣言の差として消すことは許容しない。過去rootから参照できることと、現在のauthorityとして有効であることは分ける。必要な判断材料がこの履歴範囲で不足すると判明した場合は、許可文を足さず、その必要object・参照と元契約の関係を記録して局所受入を不合格にする。

## 新しく作るもの

既存の `fixture.py`、`fixture/base/`、`cases/*/r1/`、集合、実行設定、実装第6版、旧新resultを変更しない。次の名称は今回固定した作成先であり、作成済みという意味ではない。

| 作成先（ターゲット配下） | 必要な結果 |
|---|---|
| `runtime/fixture_history_r2.py` | 既存baseとseed情報から上記履歴を構築する専用実装。既存展開経路はそのまま残す |
| `cases/SD14-01/r2/`〜`SD14-14/r2/`、`sets/dedicated14-r2.json` | 新fixture identityへ結ぶ14件。元要求・42条件・故障内容を変更しない |
| `registrations/history-material-r2.json` | 元版と新版の全14件のobject・親・alias・差分・正本・TaskSpec置換対応、許容差の実物hash |
| `runtime/start_state_contract_r2.py` | 11項目の形式照合に加え、実物・直接親・branch・開始前状態を設計側で照合する実装。モデルは起動しない |
| `runtime/test_history_material_r2.py` | 以下の正常・不正な局所証拠を検査する。モデル応答を作らない |
| `registrations/history-material-qualification-r2.json`、`registrations/history-material-handoff-r2.json` | 検査の実結果と、未実施・受入待ちの区別、固定diff・全入力hash |

採点の意味と実装第6版は再利用し、新しい採点基準を作らない。新ケース版との接続に機械的なパス写像が必要なら新しい接続用ファイルに分離し、既存14件の判定へ影響させない。実行profile・dispatch plan・`ready=true` は作成しない。既存の旧側開始記録へ容量2項目を補完することもない。

## 局所受入で必要な証拠

担当は実際の `gpt-6.1-sol / medium` を記録した実装チャット一つとし、次の結果だけを一度保存する。評価モデル・外部executorは呼ばない。今回、新しいチャットや代理担当は作っていない。

| 判定対象 | 正常な証拠 | 拒否する反例 |
|---|---|---|
| 全14件・42条件と開始tree | 元専用版の固定開始treeとの完全一致、条件原文と役割の維持 | 許可外path・mode変更、authority追加、ケース欠落 |
| 過去rootとFree化 | 本文hash一致、rootだけの削除、Freeで0 byte | 同じ行数だけのダミー、空差分、開始treeへの旧指示残置 |
| 直接親とalias | 10件はbase→seed→Free、4件はbase＝seed→Free | 祖先だけ合う余分なコミット、空seed、別parent |
| 月次の指定差分 | 新seed^..seedに所定の月次故障。SHA置換以外のTaskSpec一致 | HEAD^を対象にする、誤SHA、許可や解答の文言追加 |
| 開始実物の照合 | dispatch前に観測したHEAD・branch・status・manifestと固定入力の対応 | 偽のtrue宣言、異なるbranch、汚れた開始tree、実行後観測の代用 |
| 記録と容量 | 11項目と型、nested manifestの実物一致、同じ範囲・時点の測定 | 9項目、余分な構築情報、boolの整数扱い、同じ値でも異なる測定範囲 |
| 配送境界 | 開始tree・一件のseed・元TaskSpecのみ。非公開契約・採点・報告が配送対象外 | gate成功label、開始許可文、過去結果、oracleへの参照の新規配送 |

開始実物の観測はモデルへ追加する指示ではなく、評価側の別記録にする。開始後のHEAD・cleanや、start.jsonとlaunch.jsonが同じ自己申告を持つことを開始前証明にしない。局所検査用の仮のdispatch identityは実際の発行記録と分ける。

ソースと採点は変えないため、工程3と工程6の無関係な検査を全件再実行しない。新版の履歴と入力接続に影響する検査、およびその具体的な拒否例を実施する。変更した部分が既存検査の前提へ影響したと判明した場合だけ、その検査を追加する。過去の72失敗を再実行したり、旧モデル操作を再発行したりしない。

## 次の判定と限界

実装後は実際の `gpt-6-astra / high` へ設定を結び、固定差分と局所結果を使って、今回変更する履歴と入力接続を一回だけ最終確認する。受入済みのコード本文・42条件・保存失敗検出は、変更されていなければ保持する。

局所受入が成立しても、難しさと低コスト認定は未成立である。旧r2と専用r1の実測値は、それぞれ当時の素材の観測として残す。新しい履歴素材へ再ラベルして比較したり、過去の事前ゲートを有効化したりしない。今後の実測を検討する場合も、未完了要件、再利用可能な保存証拠、比較条件と費用判断の範囲を別途固定する必要がある。今回の追加試験は0件で、Low再発行・N拡張の許可はない。
