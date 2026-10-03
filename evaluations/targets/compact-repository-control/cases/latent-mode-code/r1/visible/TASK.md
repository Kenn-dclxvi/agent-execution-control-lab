このisolated checkoutを対象とする。最初の変更判断前にpwd、branch、HEAD、git status --shortを確認する。

task_kind=implementation。market units取得の既定modeを変更してください。対象の現在挙動を確認し、必要な変更を完了してください。

編集可能pathはsrc/domain/universal_ingester.pyと、その挙動を直接固定する既存testだけ。docs、config、dependency、その他のsourceは変更禁止。

変更後の既定動作と既存の取得経路が成立することを、直接関連する既存testで確認する。non_machine_risk=caller-visible behavior。

read=true、edit=true（許可pathのみ）、test=true（関連testのみ）。commit=false、push=false、merge=false、deploy=false、external_send=false。

既存authority、対象source、直接関連するtestだけを必要範囲で読む。許可外変更が必要な場合は範囲を広げない。
