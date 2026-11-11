# Fable 5.2 low・Free・STD14 N=5の計測中断（2026-11-10）

認証エラーにより計測を中断した。有効runは0件で、品質・費用・経過時間の集計および正式な評価resultの登録は行っていない。

## 確認できたこと

利用者の確認に基づき、THE-CAPTIONの固定評価セット`the-caption-standard14-r1`を、Free（`the-caption-3ce91a4-control-free-repository-r1`）、モデル`claude-fable-5-2`、推論設定`low`、14課題×5反復の70件として準備した。Claude Code 2.1.288、同時実行上限24、CPU負荷による開始制御を固定した。

評価セットの保管場所からLayer 1を複製し、プロファイル、Layer 1、発行計画、全capsuleの照合が通過した。発行許可は70件。モデルへ追加の応答試験は発行していない。各runの初期化時に実行環境を照合する通常の経路を使用した。

開始後、Claude Codeは`Failed to authenticate: OAuth session expired and could not be refreshed`を返した。確認時点の除外済み試行は60件、異なる予定枠は21件だった。これらはモデル品質の失敗ではなく、認証による外部実行失敗として保持した。発行処理とその子プロセスを停止し、残りの予定枠を自動発行する処理も止めた。

## 保存場所と再開条件

- [実行プロファイル](../profiles/free-claude-fable52-low-standard14-n5-cli2288-shellenv-20261110-r1.json)
- [中断記録](free-claude-fable52-low-standard14-n5_2026-11-10-interruption.json)
- [単価表](../price-tables/api-standard-2026-11-10.json)
- 計測ディレクトリ：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/free-fable52-standard14-n5-20261110-r1`
- 発行前確認記録：`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/free-fable52-standard14-n5-20261110-r1/fable/round-1/cycle/layer1/execution-preflight.json`

Claude CodeのOAuth再認証が必要である。認証の復旧後、同じ承認範囲の各課題5件を満たす不足分だけを新しい発行計画へ固定し、発行前の照合を通して再開する。今回の有効runは0件であるため、必要な有効件数は70件のままである。

単価表へ追加したFable 5.2の価格は、[公式資料](https://platform.claude.com/docs/en/models/fable-5-2/overview)を2026-11-10に確認したもの。100万トークン当たり入力8 USD、出力40 USD、キャッシュ読み取り0.20 USD、5分書き込み10 USD、1時間書き込み16 USD。価格の登録は費用集計の完了を意味しない。

## 後続の認証復旧と実行条件の変更（2026-11-10）

利用者の依頼に基づき、過去のコマンド履歴（チャット`01a1161c-e169-7b12-aef0-ebd496ed23d9`）を確認した。当時は計測用設定ディレクトリへのOAuthログイン後、認証ファイルに優先していたトークンが空の計測用キーチェーン項目を削除して復旧していた。今回も同じ空の項目を確認し、非公開のバックアップを取って除去したうえでOAuthログインをやり直した。既存のブラウザセッションで承認し、CLIの`Login successful`と計測環境での認証済み状態を確認した。今回のCLIは新しい認証情報をキーチェーンへ保存した。

復旧後の発行前照合は通ったが、Claude Code 2.1.288によるFable 5.2の呼び出しは「2.1.290以降が必要」というAPIの400応答で拒否された。除外38試行を保存して発行を停止し、この条件の品質結果は作っていない。

既にMacに存在していたClaude Code 2.1.317のアプリを計測用固定パスへ複製し、実行ファイルのSHA-256と署名を確認した。旧条件とは別のプロファイルと実行条件の集約先を作成し、必要な70件を計画し直した。新しい版では組み込みエージェント`web-fetch`とプラグイン`cc-plugin-privacy@builtin`が増えているため、その観測値も新しい実行条件に固定した。旧版での失敗試行と新しい版での試行は混ぜない。

起動確認では`--max-turns 0`がモデル応答を抑止せず、STD14外の応答が1件発生した。費用はCLI報告で0.072852 USD。この応答は評価run、70件の選択、STD14の品質・費用・時間の集計に含めない。初期化のみの確認と空入力の確認では、モデルへの応答要求は行っていない。

[認証復旧と追加確認の記録](free-claude-fable52-low-standard14-n5_2026-11-10-authentication-recovery.json)に、履歴の参照位置、旧CLIでの除外件数、新しい計測の所在を残した。認証情報の値は記録していない。
