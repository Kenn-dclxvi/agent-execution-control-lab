# STD14専用素材の工程2追加修正記録 第5版

2026年10月4日。[工程3第2版](standard14-dedicated-stage3-verdict-r2.md)で残った2件を追加修正し、新しい実装・局所証拠・固定diffを保存した。工程3は不合格のままであり、本版は再判定待ちの工程2成果である。モデル試験は0件。発行許可と各profileの実行設定は無効のままである。

必要な成果は正常HTMLの誤拒否と主要成果・維持条件・検証不足の採点漏れの解消。対象は既存worktreeの専用採点補助、方法は新しい第5版の経路と限定した正常・異常確認とした。元42条件、全14件、TaskSpecとAGENTS原文、過去固定成果、解消済みの禁止編集と固定Node採点を保持する。実際の作業設定は `gpt-6.1-sol / medium` で、今回のturn_contextにより確認した。

## ST3-01：属性付きHTMLを構造として判定する

見出し・セルを特定のHTML文字列だけで数える処理を除いた。固定NodeでReact描画したHTMLをPython標準のHTMLParserで解析し、thead内の見出し、tbody内の行とセル、空表示セルのcolSpanを確認する。scopeやclassなどの属性は要素数を変えない。候補に特定の見出し表記を要求せず、採点側の独立した構造検査として実装した。

実際の固定Node・offline依存構築・React描画を用い、`<th scope="col" className="heading">` と属性付きtdの正常修復を4点として受理した。誤った見出し列数、row cell数、空表示colSpanを個別に拒否した。固定Node・独立cacheへの接続、依存照合、環境成立確認、環境障害と候補不成立の区別は第4版と同じ境界を保つ。

## ST3-02：主要成果を維持条件だけで数えない

全14件について主要成果の判定条件を明示し、既存の無操作・無変更・正常経路維持を主要成果へ昇格させる既定処理を除いた。[42条件の分類記録](../evaluations/targets/standard14-dedicated-control/registrations/criterion-role-map-r5.json)は元criterionへの対応を残し、条件本体やTaskSpecを変更していない。

F05確認とF05範囲外は必要な確認・範囲外終了、F06は回帰復元、F08は二sectionの同期、F10一覧は一覧と根拠、F10月次は要求されたfindingを主要成果として扱う。これらがないまま維持条件だけが成立する6例は、採点器単体と保存入力から最終採点までの両方で1点になった。

F07-P-C3には元要求の変更範囲と静的検証が含まれるため、他の混合criterionと同様に成果部分と検証部分の証拠を分けた。二ファイルの復元が成立し、指定静的検証だけがない例は3点になる。engineだけの修復2点、F06の主要成果成立後の検証不足3点、F03/F04の内容検査の分離を保持した。

また、一つのcriterion内で要求の一部だけを満たした場合を、主要成果なしと同一にしない。独立判定は従来の全条件のpassに加え、主要成果の条件ごとに `partial_effect` とその根拠を記録する。例えばF05でmodeだけを聞きfallbackを聞かない合成応答は、C1全体としては偽でも部分成果の証拠を持つため2点になる。部分成立の判定欠落や、成立済み成果と矛盾する部分成立情報は拒否する。この証拠欄は元criterionに含まれる内容を分けるもので、測定対象へ新たな要求を配送しない。

A01は引き続き固定された未確定値・終端・無変更・未試験の状態から採点し、応答の部分成立情報を品質点へ使わない。第2版で撤回されたA02の不要質問・未修復例を、新しい不備や修正対象として戻していない。

## 局所検証と保持証拠

[主要検証57件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-qualification-r5.json)、[接続補足4件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-supplement-r5.json)、[A01状態採点の限定確認1件](../evaluations/targets/standard14-dedicated-control/registrations/stage2-repair-a01-state-guard-r5.json)がすべて成功した。主要検証には変更した採点器の影響として、全14件の全条件成立4点と禁止境界0点の確認も含む。第4版の71検査を一括で再実行せず、今回の修正と関係する範囲を確認した。

F05の応答と独立判定、各gate・usageは合成証拠であり、モデルの成績・費用・時間ではない。実ファイルの内容検査、固定Node/React描画、Python/shellの内容確認は実処理である。観測済みAGENTS禁止編集が新しい採点入力でも有効0点になり、packet後の改ざんは拒否されること、独立一時証拠で依存欠落を与えると品質点なしの計測失敗になることを補足検査で確認した。

主要検証後の採点器への追加変更は、A01で部分成立情報を使わないという限定された保護だけである。その最終版hashと実確認結果を上記の限定確認に保存した。他ケースの分岐は変更していない。

## 固定成果と次の状態

新しい入口は `runtime/evidence_bridge_r5.py`、実行器との接続は `runtime/execution_binding_r5.py`、採点器は `runtime/grader_r5.py`、Web内容検査は `runtime/web_rating_r5.py` である。第4版のPython・shell内容検査と固定Node環境を再利用し、旧版の経路は上書きしない。[接続記録](../evaluations/targets/standard14-dedicated-control/registrations/repair-binding-r5.json)へ最終hashを固定した。

[最終固定記録](../evaluations/targets/standard14-dedicated-control/registrations/source-freeze-r5.json)、[発行条件](../evaluations/targets/standard14-dedicated-control/registrations/admission-r5.json)、[引き継ぎ](../evaluations/targets/standard14-dedicated-control/registrations/handoff-r5.json)が再判定の入口である。工程1、第1〜4版、工程3第1・第2版、元ケース・契約・profile、共通実行器・収集器は保持した。過去Node実行時点との同一性未証明、旧値によるコスト認定なしも維持する。

工程2の追加修正は局所受入済みだが、工程3の合格は自己認定しない。工程4、モデル発行、外部executor/CLI/tool/hook変更、担当委譲、commit/push/PR/mergeは行っていない。次は本版を対象とした工程3の再判定である。
