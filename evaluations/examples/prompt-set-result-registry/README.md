# prompt set result registryの例

`set.json`と`fixture/`はEvaluation set sourceの最小例である。`run-capsule.template.json`は1プロンプトセット、1ケース、1 iteration用のRun capsule v2を示す。

実利用では`adapter.argv`を実在executorへ置き換え、`prompt_set_identity`とプロンプト固有の`parameters`を対象バンドルへ結び付ける。同じcycle内では`prompt_set_identity`と`comparison_conditions`を変更せず、`case_id`と`iteration`だけをスロットに合わせる。別のプロンプトセットは別cycleで実行し、同じregistryへ`record-result`する。

この例はschemaとfixture境界の説明用であり、評価済みresult、採用、release、本体反映を表さない。
