"""モード判断を残し、ledger組立だけを資産計算側へ移す。"""
import ast
import copy

def separate(source, assets):
    original = ast.parse(source)
    cls = next(n for n in original.body if isinstance(n, ast.ClassDef))
    fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'build_shadow_ledger')
    assert len(fn.body) > 2 and isinstance(fn.body[1], ast.Assign)
    assert fn.body[1].targets[0].id == 'units_resolution'
    lines = source.splitlines(keepends=True)
    block = ''.join(lines[fn.body[2].lineno-1:fn.end_lineno])
    main = ''.join(lines[:fn.body[2].lineno-1]) + '        return self._assemble_shadow_ledger(active_date, units_resolution)\n' + ''.join(lines[fn.end_lineno:])
    method = '\n    def _assemble_shadow_ledger(self, active_date: str, units_resolution: UnitsResolution) -> ShadowLedger:\n' + block
    helper = assets.rstrip('\n') + '\n' + method
    helper_cls = next(n for n in ast.parse(helper).body if isinstance(n, ast.ClassDef))
    added = helper_cls.body[-1]
    assert isinstance(added, ast.FunctionDef) and added.name == '_assemble_shadow_ledger'
    expanded = ast.parse(main)
    newcls = next(n for n in expanded.body if isinstance(n,ast.ClassDef))
    newfn = next(n for n in newcls.body if isinstance(n,ast.FunctionDef) and n.name == fn.name)
    assert ast.dump(newfn.body[-1], include_attributes=False) == ast.dump(ast.parse('return self._assemble_shadow_ledger(active_date, units_resolution)').body[0], include_attributes=False)
    newfn.body = newfn.body[:-1] + copy.deepcopy(added.body)
    assert ast.dump(expanded, include_attributes=False) == ast.dump(original, include_attributes=False)
    for name in ['__init__','run','_resolve_market_units','_load_live_market_units','_load_fund_config']:
        old = next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name==name)
        new = next(n for n in newcls.body if isinstance(n,ast.FunctionDef) and n.name==name)
        assert ast.dump(old,include_attributes=False)==ast.dump(new,include_attributes=False)
    assert helper.startswith(assets.rstrip('\n'))
    return main, helper, {'moved_block_bytes':len(block.encode()),'expanded_source_ast_equal':True,'mode_signature_and_resolution_preserved':True}
