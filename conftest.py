"""Repository-wide pytest collection settings.

Evaluation cases and fixtures under evaluations/targets/ contain the target repositories' own tests as
model-visible material. They are not this repository's tests and need the target's dependencies, so the
full discovery (.venv/bin/python -m pytest -q) skips them. Instance runtime tests (evaluations/targets/*/runtime/)
stay collected.
"""

collect_ignore_glob = [
    "evaluations/targets/*/cases/*",
    "evaluations/targets/*/fixture/*",
]


def pytest_collection_modifyitems(config, items):
    """Skip module-level functions a module imported from elsewhere.

    A script may import a helper whose name starts with ``test`` (for example
    ``from inspect_artifact_r4 import test``); pytest would otherwise collect it as a test
    of the importing module and fail on its arguments. Methods of test classes are kept.
    """
    kept, imported = [], []
    for item in items:
        function = getattr(item, "function", None)
        module = getattr(item, "module", None)
        if getattr(item, "cls", None) is None and function is not None and module is not None \
                and getattr(function, "__module__", module.__name__) != module.__name__:
            imported.append(item)
        else:
            kept.append(item)
    if imported:
        config.hook.pytest_deselected(items=imported)
        items[:] = kept
