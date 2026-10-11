"""Tests for bookmarks CLI."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from bookmarks.cli import app
from bookmarks.storage import Storage

runner = CliRunner()


@pytest.fixture
def temp_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "bookmarks.json"
    monkeypatch.setattr("bookmarks.storage.DEFAULT_PATH", path)
    return path


def test_add_and_list(temp_storage: Path) -> None:
    result = runner.invoke(app, ["add", "https://python.org", "--tag", "python"])
    assert result.exit_code == 0
    assert "Added" in result.stdout

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "https://python.org" in result.stdout
    assert "python" in result.stdout


def test_add_without_tags(temp_storage: Path) -> None:
    runner.invoke(app, ["add", "https://example.com"])
    storage = Storage(temp_storage)
    bookmarks = storage.load()
    assert len(bookmarks) == 1
    assert bookmarks[0].url == "https://example.com"
    assert bookmarks[0].tags == []


def test_list_empty(temp_storage: Path) -> None:
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No bookmarks" in result.stdout


def test_list_filter_by_tag(temp_storage: Path) -> None:
    runner.invoke(app, ["add", "https://a.com", "-t", "python"])
    runner.invoke(app, ["add", "https://b.com", "-t", "rust"])

    result = runner.invoke(app, ["list", "--tag", "python"])
    assert "https://a.com" in result.stdout
    assert "https://b.com" not in result.stdout


def test_search(temp_storage: Path) -> None:
    runner.invoke(app, ["add", "https://python.org", "-t", "docs"])
    result = runner.invoke(app, ["search", "python"])
    assert result.exit_code == 0
    assert "https://python.org" in result.stdout


def test_remove(temp_storage: Path) -> None:
    runner.invoke(app, ["add", "https://a.com"])
    result = runner.invoke(app, ["remove", "1"])
    assert result.exit_code == 0
    assert "Removed" in result.stdout

    result = runner.invoke(app, ["list"])
    assert "No bookmarks" in result.stdout


def test_remove_missing(temp_storage: Path) -> None:
    result = runner.invoke(app, ["remove", "99"])
    assert result.exit_code == 1
    assert "not found" in result.stdout
