- SINGLE_ACTOR: 利用可能なactor identityは一つだけとする。
  request contractが別の独立executionをrequired outcomeとして要求する場合は、criterion ownerや役割名からactorを作ったことにせず、そのoperationを`unavailable`にする。
  進捗、要約、自己宣言または同じactorによる再構成を、独立actorのresultまたはprovenanceとして採用しない。
  bind済みactorと受領resultの対応を観測できない場合は、内容一致で補完せずそのoperationを`unavailable`にする。
