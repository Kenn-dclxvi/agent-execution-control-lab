import json
from unittest.mock import patch
from src.infra import context_repository as module
class TestContextRepositoryAtomicSave:
    def test_success(self,tmp_path):
        with patch.object(module,'DIR_CURRENT',str(tmp_path)), patch.object(module.os,'replace',wraps=module.os.replace) as replace:
            assert module.ContextRepository().save({'a':1},'2026-04-20') is True
            assert json.loads((tmp_path/'context_20260420.json').read_text())=={'a':1}
            assert replace.call_count==1
            assert not list(tmp_path.glob('*.json.tmp'))
    def test_failure(self,tmp_path):
        target=tmp_path/'context_20260420.json'; target.write_text('old')
        with patch.object(module,'DIR_CURRENT',str(tmp_path)), patch.object(module.os,'replace',side_effect=OSError('replace failure')):
            assert module.ContextRepository().save({'a':1},'2026-04-20') is False
            assert target.read_text()=='old'
            assert not list(tmp_path.glob('*.json.tmp'))
