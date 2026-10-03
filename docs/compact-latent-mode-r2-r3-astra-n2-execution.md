# 小規模A01 r2・r3：Astra各N2の比較計測

必要な成果は、[r3の見直し](compact-latent-mode-r3-redesign.md)で戻した判断材料により、同じ実行環境でAstraの停止・テスト先行・推測編集と費用がどう変わるかを確認すること。r2とr3をlow・medium・high各N2、計12件測定する。旧A01の定常再実行やN20への自動延長はしない。

## 発行前に固定した条件

実行前照合は非公開campaignの`comparison-preflight.json`、controllerの照合は`controller-preflight.json`に保存した。fixture revisionを実験変数とする非登録診断であり、prompt比較やLayer4登録に読み替えない。r3ではコード・仕様・局所指示を同時に戻しているため、今回の結果で各要素単独の効果は分離しない。

| 固定条件 | 内容 |
|---|---|
| モデル | gpt-6-astra |
| 推論 | low・medium・high。各版内では推論軸、各推論内ではfixture軸 |
| CLI | 絶対パス・内容ハッシュ・runtime IDを固定した0.159.0 |
| Python | 既存の固定venvの3.14.5。controllerの実体と継承PATHを記録 |
| 権限 | workspace-write、approval never |
| 個人指示 | 実行ごとの空CODEX_HOME、authと固定model catalogだけをコピー。user configとrulesを除外 |
| 機能 | multi_agent有効・最大4、memories・apps・plugins・plugin_sharing無効 |
| 反復・並列 | 各版各設定N2、設定上M24、実際は1件ずつ |
| トークン | 全担当の入力・キャッシュ済み入力・出力を含む既存集計 |
| 時間 | CLI子プロセス開始から終了まで。待機も含める |
| 要求・採点 | TASKと私的oracleはr2・r3でバイト一致 |
| 順番 | low→medium→high。各回r2→r3の順で交互に実行 |
| 停止 | 無効runで続行停止、自動再試行なし。低品質は保持 |

旧r2の保存済みN2は比較基準の識別子とハッシュを照合記録へbindしたが、数値は再利用しない。旧照合には子プロセスへ継承するPATHとPythonの解決経路の固定証拠がなく、今回との完全一致を証明できないためである。両版を今回の共通条件で測り、過去の値を新しいfixture比較へ混ぜない。`python`の不足を一方だけ修正せず、両版で同じPATHを使う。

r2は既存の固定素材をそのまま再利用する。r3も[局所検証済みの固定素材](../evaluations/targets/compact-repository-control/registrations/latent-mode-code-source-freeze-r3.json)を使う。両版それぞれのpath・type・mode・内容ハッシュ、参照set・rating・Free identity、既存executorと全担当集計器のハッシュを発行前に照合した。[専用controller](../evaluations/targets/compact-repository-control/runtime/run_latent_mode_code_paired_n2_r3.py)は既存prepare・execute・gradeを呼び、原版の実行器は変更しない。

## 判断と保存

0点だけで比較を終えず、停止・テスト先行のみ・変更先を補完した編集を実際の操作と差分で分ける。質問送信後も動作を続けた場合は停止へ数えない。キャッシュファイルをsource編集と混同せず、採点不能を0点に変換しない。公開で関連テストを許可している一方、私的oracleでは変更先の解消前のテストを0点にする境界は保持する。

N2は今回指定された初回確認である。既に観測された反例の判断を反復不足で延期しないが、r3の旧A01代替成立や費用改善の再現性をN2だけで確定しない。次のNは[共通の再現性基準](reproducibility-decision-policy.md)と利用者の指示に従う。

生ログと認証は非公開campaignに置き、認証コピーは終了後削除する。モデルの結果、実行前照合、操作監査、全担当usage、費用、fixture差の限界を結果アーティファクトへ保存する。既存N20結果は変更しない。
