import click
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from pathlib import Path


def load_config():
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        return {}
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)
    config = pyproject_data.get("tool", {}).get("latisse", {})
    return config

@click.command()
def main():
    """A changelog generator"""
    click.echo("Hello, world!")

if __name__ == "__main__":
    main()
