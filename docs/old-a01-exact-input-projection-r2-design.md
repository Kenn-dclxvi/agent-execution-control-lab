# 旧A01の判断入力を保持する素材削減r2

利用者が2026年10月3日に承認した方針に従い、個人指示を除外した現在環境の旧素材を正本とする。小規模r4の依頼文、専用実装、再記述したauthority、unittestへの置換は使わない。

## 固定した構成

対象はthe-captionの旧A01 r2、Free、Astra Low。TaskSpecは現在環境の旧素材N20と同じJSON入力バイト、採点は元oracleとRating14。CLI0.159.0、実行引数、空の個人指示home、固定モデル一覧、共有Python3.14.5とworkspace内venv shim、全担当集計、時間境界、固定M24を再利用する。個人指示を戻さず、新たな停止指示を加えない。

変更対象はimages/MailIcon.pngとsrc/web/market_units_editor/public/mail-icon.pngの2件だけ。通常のgit rmと新commitは使わず、非coneの疎なチェックアウトで作業領域から除く。元HEAD b5c1cc6、HEAD tree、全refs、stageのpath・mode・blob、detached状態、clean状態を保持する。Git内部の疎な投影設定と除外2件のskip-worktree flagは、画像除外を実現する方法の差として明示する。Git内部設定まで完全同一とは呼ばない。

元のtracked file 259件から上記2件を除き、残り257件のpath・type・mode・content・symlink targetを発行前に機械照合した。対象コード、関連test、docs、全てのAGENTS.mdは元のバイトのまま。新しいTASK.mdをworkspaceへ追加しない。画像除外により可視作業ファイルの論理容量は13,034,642バイト減る。元Git履歴に画像blobは残るため、この数値を物理ディスク削減量とは扱わない。

## 発行前照合と試験

元の固定Layer1を複製して投影し、元の実行器のexecute関数をそのまま呼ぶ。元結果・素材manifest・TaskSpec・profile・runtime・共有依存環境・実行器・集計器のhashを保存し、起動時に照合する。declared axisは画像2件の作業領域からの除外と、それを表すGit投影metadataだけである。依頼文やauthorityの意味変更を削減に混ぜない。

新しいfixture投影系列であり、過去のrun poolへ合算せず、prompt比較やLayer4登録は行わない。現在環境の旧素材Low N20を参照として固定するが、fixtureは除外2件とGit投影metadataが違うため、過去の完全互換runを再利用した結果とは扱わない。既存の画像削除r1はHEADが違うため再利用しない。

まずLow N2だけを発行する。低得点をそのまま残し、無効なら追加発行停止、自動再試行なし。今回の実同時数は1、基準N20の実行群構成とは異なるため、経過時間の差を画像除外の因果へ帰属させない。Medium・HighやN20へ自動延長しない。N2の得点分布が基準N20と同等だと主張せず、同じ判断入力と実行依存を保持して実行できたかを先に確認する。

専用保存場所はSN7100のruns/astra-old-a01-exact-input-projection-r2-low-n2-20261003。fixture-manifest.json、comparison-preflight.json、dispatch-plan.json、controller-preflight.jsonと実行証拠を保持する。最初の準備では複製直後のGit indexのstat cache更新が必要だったため、画像の不在確認で停止してモデルを発行しなかった。index更新後に投影を再適用し、全確認成立後にのみ2件を発行した。
