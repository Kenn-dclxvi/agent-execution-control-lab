# 累積削減版r7：snapshot関連テストの準備共通化

目的は、r5に累積した画像・未参照資料除外と処理分離を維持し、実際に読まれるsnapshot関連テストの入力量を減らすこと。r6の一般テスト共通化はトークン・時間を減らせなかったため含めない。対象はtests/unit/test_market_units_snapshot.py一ファイルに限定する。

元のパス作成・ディレクトリ生成・CSV準備の反復と、同じ日付によるledger生成を共通関数へ置換する。各テストの名前、parametrizeの入力、CSV・JSON、日付、default・strictの指定と例外・期待値を保持する。共通関数を機械展開したASTが元の全文ASTと完全一致することを確認する。default指定の欠落、snapshotの欠落・不正、strictの拒否と明示的なlive CSV許可の判断根拠を削除しない。読む順や停止を促す指示は加えない。

r5の固定素材を複製し、変更一ファイル以外の205ファイル、除外55件、元TaskSpec、Free、全指示・仕様、CLI0.159.0、Astra Low、共有Python・依存、元oracle・Rating14、permission、集計・時間境界を維持する。派生Git HEAD・tree・stageは短縮に伴う差として事前宣言し、r5 HEADを親とするdetached・cleanと既存refsを保持する。別素材系列で、旧run poolへの合算とLayer4登録は行わない。

元39テストの収集ID・成否を両素材で照合し、実行前証跡保存後に並列Low N2、M24・実同時2だけを発行する。再試行とN20への自動延長はしない。個人指示と追加回答を含めない。確認後の待機も従来の時間境界に含め、差し引かずに記録する。有効な低得点は保持する。
