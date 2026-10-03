import hashlib,json
from pathlib import Path
p=Path("settings.json")
print(json.dumps({"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"passed":json.loads(p.read_text())["version"]==2}))
