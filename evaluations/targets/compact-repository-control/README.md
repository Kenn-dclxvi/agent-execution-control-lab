# 小規模リポジトリによる制御評価

STD14相当14件と追加6件を小さなファイル群で確認する独立系列。[設計とSTD14との対応](../../../docs/compact-repository-control-series-design.md)を正本とする。実アプリのSTD14合格へ読み替えない。

[初回のローカル確認](registrations/local-qualification-r1.json)に続き、[Free初回測定](results/free-sol61-low-core20-n1_2026-10-01.md)で20件の実行と全担当usage取得が成立した。追加6件はすべて4点で、Freeの品質失敗とトークン削減は確認していない。採点不備1件を留保し、品質比較の基準化は未完了である。下表のr1は初期固定版として保持し、現行の実測設定は後段から参照する。

| 対象 | 正本 |
| --- | --- |
| 登録情報 | [現行descriptor](target-r3.json)、[20件版](target-r2.json)、[初期固定版](target.json) |
| ケース | [ケース索引](cases/README.md) |
| 固定集合 | [core20-r1](sets/core20-r1.json) |
| 採点 | [成果契約](rating-contracts/outcome-r1.json) |
| 初期試験設定 | [Free Sol 6.1 low N=1](profiles/free-sol61-low-n1-r1.json) |
| Free入力 | [固定identity](prompts/baselines/free-r1/identity.json) |
| 展開・採点 | [fixture_tool.py](runtime/fixture_tool.py) |
| 内容固定 | [固定ハッシュ](registrations/source-freeze-r1.json) |
| 成果記録 | [結果索引](results/README.md) |

## 2026-10-01のFree測定

[実測結果と限界](results/free-sol61-low-core20-n1_2026-10-01.md)では、20件の実行が成立し、追加6件はすべて4点だった。機械採点の残る1件は空の確認事項の表記を誤拒否したため、品質比較の基準化は保留する。旧版は上記索引と固定ハッシュに保持する。

現行の実測設定は[profile r3](profiles/free-sol61-low-n1-r3.json)、[集合r2](sets/core20-r2.json)、[採点契約r2](rating-contracts/outcome-r2.json)、[内容固定r3](registrations/source-freeze-r3.json)。実測前の旧設定は[profile r2](profiles/free-sol61-low-n1-r2.json)、[内容固定r2](registrations/source-freeze-r2.json)へ保持する。展開と採点の履歴は[採点器r2](runtime/fixture_tool_r2.py)、[採点器r3](runtime/fixture_tool_r3.py)、実行器は[r2](runtime/run_free_r2.py)と[r3](runtime/run_free_r3.py)。

将来の再測定へ向けた[採点器r4の局所修正](registrations/local-grader-question-representation-fix-r1.json)はモデル未実行である。初回のローカル確認は[r2](registrations/local-qualification-r2.json)、修正後の確認は[r3](registrations/local-qualification-r3.json)へ保持する。

## 実コードによるA01の小規模化

[r2・r3のAstra各N2比較結果](results/free-astra6-reasoning-latent-mode-code-r2-r3-n2_2026-10-03.md)を保存した。12件すべて有効で、過去のKPIを混ぜずに今回の共通条件で測定した。

[r2・r3のAstra各N2計測](../../../docs/compact-latent-mode-r2-r3-astra-n2-execution.md)は同一環境で両版を測る非登録診断。固定した[実行条件](profiles/README.md)、[集合](sets/README.md)、[採点契約](rating-contracts/README.md)を参照する。

[用途と入力固定を復元したr3](../../../docs/compact-latent-mode-r3-redesign.md)を作成した。9ファイル・14,412バイト、局所15テスト成功。既存r2のN20結果は保持し、r3でモデル差が戻るかは未測定である。

[依存関係を戻したr2の設計](../../../docs/compact-latent-mode-dependency-r2-design.md)と[内容固定](registrations/latent-mode-code-source-freeze-r2.json)を追加した。Astra low・medium・high各2回の非登録診断として、同一fixtureで停止と推測編集の分岐を観測する。

[r2の測定結果](results/free-astra6-reasoning-latent-mode-code-r2-n2_2026-10-01.md)では、lowは停止1件・現状テスト1件、mediumは現状テスト2件、highは推測編集2件。旧A01を再実行せず、小規模素材で3経路を観測した。

[設計記録](../../../docs/compact-latent-mode-code-trial-design.md)に基づき、[専用コードケース](cases/latent-mode-code/r1/case.json)、[一件集合](sets/latent-mode-code-r1.json)、[採点契約](rating-contracts/latent-mode-code-r1.json)、[Free独立二回の設定](profiles/free-sol61-low-latent-mode-code-n2-r1.json)、[実行器](runtime/run_latent_mode_code_r1.py)、[内容固定](registrations/latent-mode-code-source-freeze-r1.json)を追加した。core20の入力と採点は変更していない。

[Free実コード試験の結果](results/free-sol61-low-latent-mode-code-n2_2026-10-01.md)は独立二回とも0点で、実行と全担当usageが成立した。可視素材は7件・3,378バイト。旧20件の採点不備とこの独立試験の成立は別に扱う。

[GPT-6 Astra lowのFree独立測定](results/free-astra6-low-latent-mode-code-n2_2026-10-01.md)も2 / 2件が0点となった。モデル以外の設定を共通に固定した別のモデル軸の記録として保持する。

[旧A01と小規模版の各N20比較](results/free-astra6-reasoning-latent-mode-code-r2-n20_2026-10-01.md)では、旧Lowが20件すべて停止した一方、小規模版Lowは停止1件・テスト先行15件・推測編集4件だった。旧試験の推論設定別の停止差を維持できておらず、代替としての採用はできない。
