# STD14専用素材の工程2完了記録 第3版

2026年10月4日。全14ケースの専用素材、採点接続、局所検証、配送入力と依存環境の固定を保存し、工程2を完了した。モデル試験は0件で、工程3の最終対応判定は実施していない。試験発行は無効のままである。

## Node条件の読み違いの訂正

[工程1の計画](standard14-dedicated-evaluation-plan-r1.md)のNode条件は、旧保存環境の実体・版・hashとローカルcacheを取得し、全推論設定へ同じ環境を固定することである。同計画は旧結果とのコスト比較を別の事前証跡へ分けている。[前版](standard14-dedicated-stage2-continuation-r2.md)では、過去の実行時点のbinary hash・cache manifestとの完全一致証明まで工程2の必須条件として扱った。これは要求より強い条件を置いた読み違いだった。工程1や旧記録は書き換えず、本版で訂正する。

旧receiptに記録されたNode/npmの版と一致する現存実体を取得し、package/lockの旧sourceとのバイト一致を保持した。Node本体とlib、npmの全ファイル、lock指定の内容hashを検証したcacheをリポジトリ外の専用保存先へコピーした。動的共有ライブラリは推移的依存を含む23件のhashへ結び、使用時の変更を拒否する。コピーしたcacheを各実行に独立して展開するため、前の実行によるcache変化を次の条件へ持ち越さない。

[環境固定記録](../evaluations/targets/standard14-dedicated-control/registrations/node-environment-binding-r3.json)には1,947項目、論理量106,275,937 byteを保存した。固定物と独立cacheだけを使用し、offlineのnpm ci、lint、buildがすべて成功した。[推移的依存の固定](../evaluations/targets/standard14-dedicated-control/registrations/node-dynamic-closure-r4.json)と[全推論設定の接続検査](../evaluations/targets/standard14-dedicated-control/registrations/node-setting-connection-r4.json)も保存した。Low・Medium・Highで同じ固定記録を使い、各設定でNode/npmの解決と版を確認した。モデル呼出しは行っていない。

Node本体のみをコピーした初回局所検査は共有lib不足で失敗した。[失敗記録](../evaluations/targets/standard14-dedicated-control/registrations/node-binding-local-attempt-r1.json)を保持し、同じインストールのlibを含めて修正した。成功に見せるために実行ファイルを改変していない。

過去の実行時点の実体・cacheとの同一性は依然として証明していない。版一致や現在の成功をその証明に代用せず、旧結果によるコスト比較は未認定のままとする。この留保と、新しい系列内で全推論設定を同一固定できたことは別の判断である。

## 工程2の受入結果

[受入記録](../evaluations/targets/standard14-dedicated-control/registrations/stage2-completion-r3.json)に、仕様の6受入項目と一次証拠を対応づけた。

| 受入項目 | 保存した証拠 |
| --- | --- |
| 正常参照と個別の誤成果 | 全14ケース、独立コード変異24件、補足48検査。別実装・別応答の受理を含む局所証拠 |
| 操作と最終成果の結合 | 操作・criterionの143検査に加え、保存証拠から採点まで全14正常例と107異常検査が成功 |
| 真の実行による局所確認 | Python・shellの終了証拠、Nodeの固定環境でのoffline install・lint・build。F06の空snapshot回帰と月次両optionの影響を保持 |
| 要求と検査の双方向対応 | 旧criterion 42件の対応、逆参照42件、孤立した品質条件0件 |
| 配送・入力・依存の固定 | root 0 byte、非root原文一致、TaskSpec原文保持と許可SHA置換だけ、14件coverage、漏洩検査、固定Python・CLI・Node/cache |
| ストレージとコード量 | 既存の素材・Git量の記録と、今回追加した依存環境・採点補助の量を分けて保存 |

これは実装者による局所受入であり、工程3の要求対応最終判定を先取りしない。採点接続の合成usageを実モデルのトークン実測へ転用しない。モデル応答の実採点、全担当usageと時間区間の実測成立は、承認された将来の測定で確認する。

[最終固定記録](../evaluations/targets/standard14-dedicated-control/registrations/source-freeze-r3.json)、[発行条件](../evaluations/targets/standard14-dedicated-control/registrations/admission-r3.json)、[引き継ぎ記録](../evaluations/targets/standard14-dedicated-control/registrations/handoff-r3.json)が今回の引き継ぎ先である。工程1の5成果、第1・第2版の固定成果、既存系列、実行器・収集器の原文を保持した。push、PR、mergeは行っていない。

次は工程3である。計画指定のGPT-6 Astra Highによる一回の最終対応判定は未実施であり、現在の工程2の完了と混同しない。工程3通過、実配送条件の照合、新集合の発行前証跡が揃うまで、28件の一件目も発行しない。
