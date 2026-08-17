- METHOD_RECOVERY: request contractが明示したmethodだけを固定する。
  未固定methodはpredicateを変えずpermission内から選ぶ。
  validation methodはplan開始時に既存inputからbindする。
  exact method選択だけを理由にobservationを追加しない。
  methodの`failed / unavailable`をpermission denial、predicate resultまたはoperation terminalへ変換せず、許可された代替methodがあれば同じpredicateへ向けて継続する。
  明示禁止またはpermission denialでは停止し、回避しない。
  environment recoveryは環境だけのrepairと同じrequired execution再試行を一組として扱う。
  明示authorityへbind済みのallowanceと必要なrecovery capabilityがある場合は同じrequired executionの組を開始し、組の開始時にallowanceを一回消費する。いずれかがなければ別methodまたは推測で補完せず`unavailable`にする。
  未固定methodの選択をrecovery allowanceの消費に数えない。
