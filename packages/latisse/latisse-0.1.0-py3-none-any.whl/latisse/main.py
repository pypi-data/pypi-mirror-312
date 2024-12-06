import click
import git
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, DefaultDict, Tuple
import os
import stat
from .hooks import GEN_CHANGELOG

CATEGORIES = {
    'feat': 'Features',
    'fix': 'Bug Fixes',
    'docs': 'Documentation',
    'style': 'Styling',
    'refactor': 'Code Refactoring',
    'perf': 'Performance Improvements',
    'test': 'Tests',
    'build': 'Builds',
    'ci': 'Continuous Integration',
    'chore': 'Chores',
    'revert': 'Reverts',
}

def load_existing_changelog(output: str) -> str:
    """Load the existing changelog content or create a new header if the file does not exist.

    Args:
        output (str): The path to the changelog file.

    Returns:
        str: The existing content of the changelog or a default header.
    """
    changelog = Path(output)
    if changelog.exists():
        return changelog.read_text()
    return "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"

def get_sorted_tags(repo: git.Repo) -> List[git.TagReference]:
    """Retrieve and sort Git tags by commit date.

    Args:
        repo (git.Repo): The Git repository object.

    Returns:
        List[git.TagReference]: A sorted list of Git tags by commit date.

    Raises:
        click.ClickException: If no tags are found or if there's an error fetching tags.
    """
    try:
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
        if not tags:
            raise click.ClickException("No tags found in the repository. Please tag your releases.")
        return tags
    except git.exc.GitCommandError:
        raise click.ClickException("Error fetching tags from the repository.")

def categorize_commit_message(commit_msg: str) -> Tuple[str, str]:
    """Categorize a commit message based on predefined prefixes.

    Args:
        commit_msg (str): The commit message to be categorized.

    Returns:
        tuple: A tuple containing the category and the cleaned-up commit message.
    """
    category = 'Other'
    for prefix, cat_name in CATEGORIES.items():
        if commit_msg.startswith(f'{prefix}:'):
            return cat_name, commit_msg[len(prefix)+1:].strip()
    return category, commit_msg

def gather_changes(repo: git.Repo, tags: List[git.TagReference]) -> List[str]:
    """Gather changes between Git tags and categorize them by commit messages.

    Args:
        repo (git.Repo): The Git repository object.
        tags (List[git.TagReference]): A list of Git tags sorted by date.

    Returns:
        List[str]: A list of changelog entries categorized by type of change.
    """
    new_changes = ["## [Unreleased]"]
    for i, tag in enumerate(tags):
        version = tag.name
        previous_tag = tags[i + 1] if i < len(tags) - 1 else repo.head.commit
        changes: DefaultDict[str, List[str]] = defaultdict(list)

        for commit in repo.iter_commits(f'{previous_tag}..{tag}'):
            commit_msg = commit.message.strip().split('\n')[0]
            category, commit_msg = categorize_commit_message(commit_msg)
            changes[category].append(commit_msg)

        date = tag.commit.committed_datetime.strftime('%Y-%m-%d')
        new_changes.append(f"\n## [{version}] - {date}")
        for category, msgs in changes.items():
            if msgs:
                new_changes.append(f"\n### {category}")
                new_changes.extend(f"- {msg}" for msg in msgs)

    return new_changes

def generate_changelog_content(output: str) -> str:
    """Generate the entire changelog content for the current Git repository.

    Args:
        output (str): The output path for the changelog file.

    Returns:
        str: The full content of the updated changelog, including new changes.
    """
    repo = git.Repo(os.getcwd())
    existing_content = load_existing_changelog(output)

    tags = get_sorted_tags(repo)
    new_changes = gather_changes(repo, tags)

    return existing_content + "\n".join(new_changes)

@click.group()
def cli() -> None:
    """CLI tool to generate and update changelogs for Git repositories."""
    pass

@cli.command()
@click.option('--output', default='CHANGELOG.md', help='Output file for the changelog')
def generate(output: str) -> None:
    """Generate or update a changelog for the current Git repository.

    Args:
        output (str): The file path where the changelog will be written.
    """
    try:
        content = generate_changelog_content(output)
        Path(output).write_text(content)
        click.echo(f"Changelog updated: {output}")
    except click.ClickException as e:
        click.echo(f"Error: {e}")

@cli.command()
def install_hook() -> None:
    """Install the changelog generator as a Git post-tag hook."""
    try:
        repo = git.Repo(os.getcwd())
    except git.exc.InvalidGitRepositoryError:
        click.echo("Error: Current directory is not a git repository.")
        return

    hooks_dir = Path(repo.git_dir) / 'hooks'
    hook_path = hooks_dir / 'post-tag'

    hook_content = GEN_CHANGELOG
    try:
        hook_path.write_text(hook_content)
        hook_path.chmod(hook_path.stat().st_mode | stat.S_IEXEC)
        click.echo(f"Git hook installed: {hook_path}")
    except Exception as e:
        click.echo(f"Error installing Git hook: {e}")

if __name__ == '__main__':
    cli()

