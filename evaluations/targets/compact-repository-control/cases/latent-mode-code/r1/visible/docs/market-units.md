# market unitsの現行仕様

`daily`は有効な日次snapshotを優先し、snapshotの欠落・不正時は現在のCSV値を取得する。`strict`は有効なsnapshotだけを許可し、欠落・不正時はエラーにする。コンストラクタで指定を省略したときの現在のmodeは`daily`。

この文書は現行挙動を記述する。変更を決めた記録はまだない。
