# 旧A01の判断入力を保持したPNG投影r2：Astra Low N2

画像2件以外の257ファイル、元JSON TaskSpec、元HEAD・detached状態・clean状態、共有Python環境を保持する版を構築し、Low N2を完了した。全2件有効。確認停止4点1件、現状テスト先行0点1件。編集なし。[一次結果](control-free-astra-low-old-a01-exact-input-projection-r2-n2_2026-10-03.json)を正とする。

元の現在環境Low N20から直接複製し、code・test・docs・階層別AGENTSのバイトを変更していない。平文TASKや専用実装へ置換せず、workspaceに新しいTASK.mdを置いていない。画像除外はGitの疎な投影で行い、HEAD・tree・refs・stage entriesと開始statusを保持した。疎な投影設定とskip-worktree flagの差は明示した。Git内部まで完全同一とは扱わない。個人指示の除外は保持する。

発行前に257件のpath/type/mode/content/symlink targetと、TaskSpec・runtime・依存環境・実行器・採点源を機械照合した。実行後は基準20件と今回2件のCLI引数、基本指示、developer全文、初期environmentを実行先のパスだけ正規化して照合し、一致を確認した。両件のTaskSpecは元のバイトと一致し、個人指示なし、追加回答なし。全担当操作・終了文と最終workspaceを監査した。

low-01は関連39テストをpython -m pytestで実行してから変更先を確認し、0点。low-02は変更先を確認してテストも編集もせず終了し、4点。元の個人指示除外Low N20も停止10件・テスト先行10件だったが、今回N2の分布をその同等性の証明にはしない。

新規消費262,433トークン、平均131,216.5トークン、平均37.913秒。全担当・cached input込み。設定M24、今回実同時1、再試行0。基準の実行群とは並列状況が違うため、経過時間差を画像除外の効果としない。

可視作業ファイルの論理容量を13,034,642バイト削減した。Git履歴の画像blobと共有依存は保持しているため、物理ストレージが同量減ったとは報告しない。この2件ではトークン削減を確認したとはいえない。ここまでの成果は、依頼文・指示・実装を再構成せずに削減だけを実験変数にする具体的な版と、対応する照合・実行証拠である。

[構成と固定条件](../../docs/old-a01-exact-input-projection-r2-design.md)を参照する。Medium・High、N20への追加は発行していない。
