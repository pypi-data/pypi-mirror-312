try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from pathlib import Path

DEFAULT_CONFIG = {
    "changelog_file": "CHANGELOG.md"
}
def load_config():
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        return {}
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)
    config = pyproject_data.get("tool", {}).get("latisse", {})
    config.update(DEFAULT_CONFIG)
    return config
