# C163 4文版の事前設計

## 目的

C163の5文目がF02の実装・検証経路へ与えた影響を測る。変更軸はC163のroot `AGENTS.md`から5文目をそのまま削除することだけとし、書き換えや代替指示の追加はしない。

## 基準と観測

- 基準プロンプト: `the-caption-3ce91a4-five-verified-lines-integrated-r1`、bundle SHA-256 `4813ccf9fb3813b5b4f48b58a53dc4c8833b9971140a65aadd3b3c76d6bea62b`
- 対象ケース: `TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND` r1
- 既知のC163観測: F02 iteration 4ではfocused pytestが最初に`import pytest`欠落で終了コード2となり、1回の修正後はCSVの改行リテラル誤記で6件失敗した。後続のfull gateと差分確認は発行されていない。
- 対象5文目: 「変更後は、必要なテストと差分確認を一つの実行票として先に固定し、実行中は同じ結果だけを待ち、失敗なら後続を止め、全結果がそろったら追加確認せず一度だけ完了を判断する。」

## 経路と変更の範囲

- F02のTaskSpecが求める最短正常経路は、許可された2 sourceと2 testの変更、focused gateとfull gateの成功、許可外差分がないことの確認である。
- TaskSpecとrepository stateは実装内容・成功条件を定めるが、全検証と差分確認を先に一括固定する順序や、失敗時に後続検証を止める規則を定めない。
- 変更するのはC163 root `AGENTS.md`の5文目だけ。述語・役割の追加や置換はなく、5文目が定める「事前に一つの実行票へ固定」「失敗時に後続停止」「全結果後の一度だけの完了判断」を削除する。
- これにより、失敗を受けた後の実行継続と完了判断が5文目によって制約される経路を取り除く。F02で観測したテスト記述誤り自体を5文目が指示したとは扱わない。
- 他の18 target、TaskSpec、case fixture、採点契約、モデル、reasoning、CLI、runtime、permission、executor条件、token accountingはC163と同一にする。

## 評価と停止

- 4文版をC163の直接子full bundleとして固定し、C163 High Standard14と同じ固定Layer 1およびatomic poolからF02の不足5 runだけを発行する。
- 事前に比較する出力は5 runそれぞれのquality score、focused/full gateの観測、テスト修正回数、検証発行順、終端状態、token数、経過時間とする。
- C163の既存F02 N=5を比較対象として再利用し、既存runは再実行しない。
- 5文目以外の実効条件に不一致があれば発行前に停止する。評価後はF02 N=5の観測結果だけを報告し、別ケースや一般的効果へ拡張しない。
