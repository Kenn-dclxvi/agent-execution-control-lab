import json, os, tempfile
def save(data, path):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".json.tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        os.replace(tmp, path)
        return True
    except Exception:
        os.unlink(tmp)
        return False
