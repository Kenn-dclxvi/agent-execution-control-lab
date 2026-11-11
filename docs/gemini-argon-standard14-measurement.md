# Gemini 4 Argon LowによるSTD14の計測

2026-11-11の利用者依頼は、FreeとC319をそれぞれSTD14の14ケースで5回ずつ計測することである。対象は合計140件で、Gemini対応の計測基盤整備、使用量の確定、採点、集計、結果登録、最小容量保存、復元照合、作業コピーの後片付けを含む。プロンプトの変更、採用、本体反映は含まない。

## 固定入力と実行経路

- Free: [`free-gemini4-argon-low-standard14-n5-agy155-20261111-r1`](../evaluations/profiles/free-gemini4-argon-low-standard14-n5-agy155-20261111-r1.json)。既存の`the-caption-3ce91a4-control-free-repository-r1`を使う。
- C319: [`c319-gemini4-argon-low-standard14-n5-agy155-20261111-r1`](../evaluations/profiles/c319-gemini4-argon-low-standard14-n5-agy155-20261111-r1.json)。既存の`the-caption-3ce91a4-unconfirmed-location-search-r1`を使う。
- モデルは`gemini-4-argon-low`、推論設定は`low`、Antigravity CLIは`1.5.5`。実行ファイルの絶対パスとSHA-256、利用可能なツール、設定ファイルのSHA-256をプロファイルへ固定する。
- 個人の指示ファイル・追加の規則・追加のエージェント・外部プラグイン・フックが存在しないことを発行前と実行直前に確かめる。既存の組み込みswarmプラグインの有効状態は設定識別値に含め、両条件で共通とする。認証情報は既存のものを利用し、複製しない。
- STD14 r1の固定済みLayer 1を保管場所から複製する。ケース、fixture、TaskSpec、成果品質の基準は変更しない。
- [`evaluation_trial.py`](../scripts/evaluation_trial.py)の`prepare`で各試験を準備し、`run-group --trial <Free> --trial <C319>`で一つの待ち行列へ入れる。並列上限は合計24、CPU使用率による発行制御は既存の`cpu_busy_below` r1とする。
- 各スロットの実行回数上限は1とし、140件を超える自動再試行を行わない。除外が発生した場合は有効件数と不足件数を分けて報告する。

## 使用量とコマンド証拠

利用者が別途承認した基盤確認は、単独実行1件と子エージェントを使う実行1件であり、STD14の成績に含めない。単独実行では終了コード0と7、親子実行では子によるコマンドの終了コード0を取得した。

CLI 1.5.5の終了時`usage`は親会話だけを対象とし、`total_tokens`はキャッシュ読み取りを含まない。`thinking_tokens`は`output_tokens`の内数である。この値をそのまま全エージェントのトークン数として登録しない。

[`antigravity_evidence.py`](../scripts/antigravity_evidence.py)は次を照合する。

1. 親ストリームの開始・終了識別子、重複を除いた完了ステップ、終了時の使用量。
2. 親と全子会話のSQLite内の使用量と、同じステップ番号の会話記録。
3. 固定したCLIのモデル識別値`1419`と、確認実行の`gemini-4-argon-low`との対応。他の識別値は推定で対応づけず除外する。
4. 親の使用量を独立に照合した後、全会話の未キャッシュ入力・キャッシュ読み取り・出力を合算する。思考は追加で足さない。
5. データベース内のツール呼び出しと、同じステップのツール終了記録を対応づける。モデルの応答本文にある成功宣言を終了コードの証拠にしない。

確認実行では、単独17,712トークン、親子52,240トークンを照合した。これらは基盤確認だけの値である。親ストリームに子の本文がない場合でも、子のデータベースと会話記録から計数する。子の欠落、未完了、モデル不一致、使用量不一致、必須コマンドの終了状態欠落は計測失敗として除外する。ブラウザ子エージェントと、識別子を対応づけられない非同期コマンドは未対応として扱い、成功を推測しない。

一次ストリーム、会話データベースのバックアップ、会話記録は非公開の試験領域へ保存する。認証情報と非公開の生ログをGitへ含めない。

## 採点、費用、完了条件

[`Antigravity用の採点契約`](../evaluations/rating-contracts/outcome-terminal-state-evidence-antigravity-collector-v1.json)はv14の成果品質規則を変更せず、証拠収集器だけを差し替える。実際の採点は[`standard14_antigravity_quality_audit.py`](../scripts/standard14_antigravity_quality_audit.py)が共通のケース判定関数を使って行う。担当者と生成者の帰属は診断だけに使う。

費用は[`api-standard-2026-11-11`](../evaluations/price-tables/api-standard-2026-11-11.json)による標準API換算額であり、Antigravityのサブスクリプション請求額ではない。[Google公式料金表](https://aistudio.google.com/docs/pricing#gemini-4-argon)の2026-11-30までの単価、100万トークン当たり入力2 USD、キャッシュ読み取り0.10 USD、思考を含む出力10 USDを使う。使用量を推定で補わない。

採点後は各試験の`finish`を実行する。結果登録だけで完了とせず、最小容量保存、内容と属性を含む復元照合、保護入力の不変確認、作業コピー削除を含む`complete.json`が両試験に揃った時点を完了とする。不足がある場合は`incomplete_saved`とし、140件を達成したとは報告しない。

試験領域: `/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/free-c319-argon-low-standard14-n5-agy155-20261111-r1`。

## 今回の完了と収集処理の修正

[今回の結果](../evaluations/results/free-c319-gemini4-argon-low-standard14-n5_2026-11-11.md)は、両試験の`complete.json`が揃い、各70件の登録、保存、復元照合、保護入力の不変確認、作業コピー削除まで完了した。

140件の最初の収集では85件が有効、55件が除外された。50件は省略されたツール出力から終了コードを取れなかったため、5件は終了済みツールの`ERROR`状態を未完了と扱ったためである。保存された完全出力と会話記録を再照合し、元の記録を残して55件の証拠を追記した。モデルの呼び出しを追加せず、ケース、課題文、プロンプト、推論設定、使用量の定義、実測時間、成果品質の規則を維持した。

再照合には[`antigravity_saved_evidence.py`](../scripts/antigravity_saved_evidence.py)と[`recollect_antigravity_commands.py`](../scripts/recollect_antigravity_commands.py)を使う。後者は、完全出力の参照先が会話とステップ番号に一致し、実行時刻も一致する場合だけ終了記録を受け付ける。ツール出力本文にある成功の文字列は証拠にしない。ツールの終端エラーは未完了と区別し、モデル実行の使用量を欠落なく照合できる場合だけ計数する。

今後の実行には、同じ修正を接続した[`run_antigravity_evaluation_v2.py`](../scripts/run_antigravity_evaluation_v2.py)を指定する。新しいプロファイルではv2と依存する収集コードのSHA-256を固定し、発行前確認を行う。今回のr1の実行は元のアダプタと再照合によるものとして保持する。v2への接続と課題文の同一性はモデルを呼ばないテストで確認し、v2による追加のモデル試験は行っていない。
