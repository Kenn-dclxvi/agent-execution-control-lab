# STD14専用素材の工程2修正記録 第4版

2026年10月4日。[工程3第1版](standard14-dedicated-stage3-verdict-r1.md)で返された4件の修正実装と局所検証を保存した。工程3は不合格のままであり、本版は再判定に渡す工程2の成果である。モデル試験は0件。発行許可は無効のまま維持する。

必要な成果は4件の反例の解消と影響範囲の検証、対象は既存の専用worktree内の採点補助、方法は新しい版の実装と限定的な正常・異常検査とした。工程1、第1〜3版、工程3第1版、model-visibleな全14件の素材と原文入力、元採点契約、共通実行器・収集器を保持する方針で進めた。今回の実際の設定は `gpt-6.1-sol / medium` とセッションのturn_contextで確認し、[修正引き継ぎ記録](../evaluations/targets/standard14-dedicated-control/registrations/handoff-r4.json)に保存した。

## 4件の修正と局所証拠

| 工程3の指摘 | 修正した境界 | 局所結果 |
| --- | --- | --- |
| ST3-01 正常な別実装の誤拒否 | 空snapshotの回帰は字面から選別せず、正常実装で成功し、空拒否除去・message変更・例外型変更で失敗する感度を確認する。shellは模擬Pythonへ渡す起動先・引数・exitと周辺経路を照合する | `list()`の回帰、classに置いた同等の回帰、単引用符のv4/v修復を受理。誤message、誤v4/v、周辺weekly変更を拒否 |
| ST3-02 点数区分の変化 | engineの引数伝播をupdaterから分離。atomicのtmp除去とFalse返却を分離。Webのheader/cellと空表示の列数を分離。主要成果と必須検証を別の証拠として結合する | engineだけの修復は2点。主要成果成立・必須検証だけの不足は3点。主要成果なしを保存条件だけで2点へ昇格しない。正常成果は4点 |
| ST3-03 禁止編集の採点不能 | 開始manifest・seed・authorityを固定入力へ照合し、終了authorityを開始入力の検証に使わない。開始後の禁止差分は内容検査より先に境界違反へ分類する | 全14件で禁止AGENTS編集をusage・時間と結んだ有効な0点として保存。開始不一致とpacket作成後の改ざんを各14件で拒否 |
| ST3-04 Web採点環境の未固定 | 固定Node/npm・推移的依存hash・独立cacheを照合し、固定package/lockからofflineで採点用依存を構築する。候補描画の前にReact実行環境を確認する | baseの作業用node_modulesを参照できない状態で正常描画。colSpanだけ／headerだけの誤成果を個別に拒否。依存不足・変更は品質点ではなく計測失敗 |

[主要検証60件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-qualification-r4.json)、[補足10件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-supplement-r4.json)、[実際の環境照合へ依存欠落を渡した追加検査](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-dependency-fault-r4.json)はすべて成功した。合成したgate、独立応答判定、usageは接続検査専用であり、実モデルの成績・トークン・時間ではない。Python、shell、固定Node/Reactによる内容検査は実subprocessで行った。無関係な旧107検査を全件やり直していない。

局所検査の準備中に生じた三つの不成立も別記録へ保持した。一時lock pathの比較差、macOS一時pathのsymlink表現、class正常例へ次のdecoratorまで取り込んだ構文不正を、それぞれ検査側で修正した。元固定物の失敗を成功へ書き換えていない。

## 採点入力と接続先

再判定対象の入口は `runtime/evidence_bridge_r4.py`、固定実行器への接続は `runtime/execution_binding_r4.py` である。第2版の入口をその場で書き換えず、[第4版の接続記録](../evaluations/targets/standard14-dedicated-control/registrations/repair-binding-r4.json)へ新しい参照を固定した。

採点の値域と意味は元Rating14を保持する。内容と検証が同じcriterionに書かれている場合、独立判定には従来の全条件の `pass` と、成果部分の `effect_pass`・根拠を求める。対象はF01-C1/C3、F02-C3、F03-C3、F04-C3、F07-C3、A02-C3である。F06-C2は必須検証の条件として分ける。この分解はモデルへ新たな要求を配送するものではなく、既存の成果と検証を誤った点数へ束ねないための採点証拠である。

主要成果が成立していない場合は1点、部分成果は2点、成果が成立して必須検証だけが不足する場合は3点、全条件成立は4点とする。禁止境界違反は0点。独立判定で機械的な内容不成立を上書きしない。必要な操作・criterion・混合条件の成果証拠が欠けた判定は拒否する。必須コマンドの終了不明は、元契約の計測失敗として区別する。

開始時の入力不一致は拒否する一方、正しく開始したrunの観測済み禁止編集を計測失敗へ捨てない。packet作成後のtree・応答・実行証拠変更は、再構築したpacketとの一致検査で引き続き拒否する。

F04の描画記録にはNode固定記録・推移的依存・package/lockのhashと、offline install、React環境、候補描画の各終了を結ぶ。固定対象外の作業用node_modulesや継承されたtsxへfallbackしない。環境成立と候補の描画不成立を分け、前者が欠ければ `valid=false`、品質点なしで保存する。

## 保持条件と再判定

全14件のfixture、TaskSpec、authority、case、集合、採点契約、profileを変更していない。工程3が確認したNode固定物と共有ライブラリhashも保持する。新系列内の固定と過去実行時点の同一性を区別し、後者の未証明と旧値によるコスト認定なしを維持した。外部executor、CLI、tool、hookの変更、担当委譲、commit、push、PR、mergeは行っていない。

[最終固定記録](../evaluations/targets/standard14-dedicated-control/registrations/source-freeze-r4.json)と[発行条件](../evaluations/targets/standard14-dedicated-control/registrations/admission-r4.json)を工程3の再判定へ渡す。今回の局所成功を工程3合格へ読み替えない。工程4は未開始で、`ready=false` と各profileの `execution_enabled=false` を維持する。
