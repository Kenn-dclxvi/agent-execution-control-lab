- VALIDATION_EXECUTION: action完了とplanの全predicate、順序、個別pass conditionおよびstop conditionが揃った場合だけvalidationをreadyにする。
  protocolがexact methodを明示するvalidationだけ、そのmethod bindingをready条件にする。
  readyなrequired validationを固定順の個別executionとして一つの発行判断から開始する。
  各resultを個別に判定し、non-successまたは`unavailable`を受領したら後続を開始しない。
  個別validationを一つの不可分なresultへ結合しない。
  全完了resultを一度だけ結果消費側へ渡す。
  全件successかつ全result bind済みなら追加observationまたはvalidationを発行せずterminalを判断する。
  欠落、non-successまたはunexpected stateをnonterminalとして保持する。
  このclosureを探索、変更前、review finding、method探索またはrecoveryへ流用しない。
