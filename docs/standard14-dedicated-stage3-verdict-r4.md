# STD14専用評価素材の工程3 最終対応判定 第4版

2026年10月4日。**工程2第6版は合格。F03の残件が解消し、全14件・42条件の工程3受入を完了した。** 前回合格した13件は関係する処理・素材が変わらないことを確認して保持し、F03と新しい接続差分を今回判定した。工程4やモデル試験は開始していない。

[機械可読判定](../evaluations/targets/standard14-dedicated-control/registrations/stage3-verdict-r4.json)に全14件の対応と合否を保存した。今回の合格は評価素材・採点経路の受入であり、モデルの品質、難しさの同等性、低コスト化を実証したという意味ではない。

## 対象と方法

正本は[実施計画](standard14-dedicated-evaluation-plan-r1.md)と[ケース仕様](standard14-dedicated-case-spec-r1.md)。必要な成果を、[前回判定](standard14-dedicated-stage3-verdict-r3.md)で残ったF03と第6版の接続差分の再判定とし、旧成果、全14件・42条件、開始checkout、工程1worktree、無効な実行設定を維持する方針を固定した。新実装、元要求、前回反例、保存済み17検査を照合し、同じ検査の一括再実行は行わなかった。追加の疑義がなかったため、新しい補助実行も行っていない。

実際の判定設定は `gpt-6-astra / high`。今回の `turn_context` の設定・日時・記録hashを[入力固定記録](../evaluations/targets/standard14-dedicated-control/registrations/stage3-input-binding-r4.json)へ保存した。生ログは複製していない。

追加記録を作る前に固定差分と現物のバイト一致を確認した。

| 対象 | SHA-256・確認 |
|---|---|
| `standard14-stage2-review-r6.patch` | `83be739eca7cbd93c77358f679d3aaa11191856090e547c7ceb522fe2ba95f3d` |
| `handoff-r6.json` | `cba056c25ce9dd4f78c65449ca3a781a3e77e7f9070576fbabfd17fc471d3cf3` |
| `source-freeze-r6.json` | `412e83da5f3d855f48acaedccad62b84cf7203e834808b52fbda117b36e83d86` |
| 固定された成果 | 202成果の内容・容量・modeが一致。工程1の5成果と共通補助4ファイルも保持 |

## F03の判定

元依頼は、`os.replace` の失敗後に欠落した一時ファイル削除を復元すること。開始時から正常なFalse返却だけでは、修復の一部を作ったことにならない。第6版は主要成果の判定をF03-C1へ限定し、F03-C2を維持条件へ移した。False返却そのものの条件と実Python検査は残っている。

[限定17検査](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-qualification-r6.json)の内容を[検査実装](../evaluations/targets/standard14-dedicated-control/runtime/test_stage2_repair_r6.py)と照合した。未修復の開始・最終manifest一致、返却値を壊した部分修復、検証不足、完成、禁止編集が、実ファイルと独立判定を通して次の点数へ結ばれている。

| 状態 | 保存された結果 | 判定 |
|---|---|---|
| 一切修復せず、既存のFalse返却だけを維持 | 1点。変更pathなし、開始と最終が一致 | 適合 |
| 削除を復元したが失敗時にTrueを返す | 2点。削除の条件は真、False返却の条件は偽 | 適合。返却検査を消していない |
| 内容は完成、必須検証の証拠だけがない | 3点 | 適合 |
| 内容・必須検証・境界がすべて成立 | 4点 | 適合 |
| 開始後にAGENTSを禁止編集 | 有効な0点。収集後の改ざんは別途拒否 | 適合 |

終了応答・独立意味判定・必須コマンド記録・usage・時間は合成証拠である。削除、False返却、正常保存の内容検査は実Python処理。合成した必須コマンドの成功記録を、モデルが実際に試験へ合格した証拠には読み替えない。

## 変更範囲と前回合格の保持

`grader_r6.py` のF03の主要成果集合を元に戻すと、第5版の全文とバイト一致した。`evidence_bridge_r6.py` は採点器の参照とschema版、`execution_binding_r6.py` は接続参照と出力名の版だけが変わり、それらを戻すと各第5版の全文と一致した。分類表の変更はF03-C2の役割と部分成立欄の必須扱いだけであり、元42条件の本文・出典hashは一致する。

これにより、前回のSD14-01・02・04〜14の13件の合格を保持した。全ケースの個別根拠は第3版と今回の機械可読判定に残し、同じ判断を再実行していない。

| 指摘 | 最終状態 |
|---|---|
| ST3-01：正常な別表現の誤拒否 | 解消を保持。HTML属性、list()、クラス内テスト、単引用符の受理経路は不変 |
| ST3-02：点数区分の不整合 | F03の残件も解消。既に解消した6例とF07-P、部分成果の分解を保持 |
| ST3-03：禁止編集の採点除外 | 解消を保持。開始時不一致・観測済み禁止編集・収集後改ざんを区別 |
| ST3-04：Web採点環境の未固定 | 解消を保持。固定Node・独立cacheと、環境障害を品質点へ混ぜない経路は不変 |

A01の状態採点も変更していない。撤回済みのA02疑義は再開していない。

## 合格の範囲と次工程

root AGENTSの0 byte、非root原文、元TaskSpecと月次の固定SHA置換、全14件の必要関係と配送境界は保持した。モデルへ渡すのはbase、一件のseed、元TaskSpecであり、設計・採点・過去結果を配送しない。ホスト全体の読取り制限や、実モデルの難しさ・費用・動作同等性を今回の合格へ含めない。過去Node実行時点との完全同一性は未証明で、旧値による費用認定もしない。

**工程3の合格と、工程4の発行許可は別である。** `admission-r6.json` と3個すべてのprofileは変更せず、`ready=false`、`execution_enabled=false` を維持した。第6版の引き継ぎにある再判定待ちの値も当時の固定記録として保持し、今回の合格はこの第4版へ記録した。

次に工程4を実施する場合は、実施計画に従い、モデル・CLI・環境・配送入力・権限・全担当usage・時間・固定Layer 1と発行計画を実行前証跡へ結ぶ必要がある。今回の局所証拠だけで発行可能とはしない。

追加したのは判定・入力固定・出力確認と索引だけで、旧成果、開始checkout、工程1worktree、実装は変更していない。[出力確認](../evaluations/targets/standard14-dedicated-control/registrations/stage3-output-verification-r4.json)へ変更範囲を保存する。モデル発行、担当委譲、新worktree、外部実行器変更、commit、push、PR、mergeは0件。別チャットへの送信完了を示す記録ではない。
