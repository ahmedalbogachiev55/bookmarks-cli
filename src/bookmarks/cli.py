"""Bookmarks CLI entry point."""

import webbrowser

import typer
from rich.console import Console
from rich.table import Table

from bookmarks.storage import Storage

app = typer.Typer(
    name="bm",
    help="Simple bookmarks manager for the terminal.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def add(
    url: str = typer.Argument(..., help="URL to save."),
    tag: list[str] = typer.Option([], "--tag", "-t", help="Tag (repeatable)."),
) -> None:
    """Add a bookmark."""
    bookmark = Storage().add(url, list(tag))
    console.print(f"[green]Added[/green] #{bookmark.id}: {bookmark.url}")


@app.command("list")
def list_bookmarks(
    tag: str | None = typer.Option(None, "--tag", "-t", help="Filter by tag."),
) -> None:
    """List all bookmarks."""
    bookmarks = Storage().load()
    if tag:
        bookmarks = [b for b in bookmarks if tag in b.tags]
    if not bookmarks:
        console.print("[yellow]No bookmarks found.[/yellow]")
        return
    table = Table("ID", "URL", "Tags")
    for b in bookmarks:
        table.add_row(str(b.id), b.url, ", ".join(b.tags))
    console.print(table)


@app.command()
def search(query: str = typer.Argument(..., help="Search text.")) -> None:
    """Search bookmarks by URL or tag."""
    q = query.lower()
    results = [
        b
        for b in Storage().load()
        if q in b.url.lower() or any(q in t.lower() for t in b.tags)
    ]
    if not results:
        console.print("[yellow]Nothing found.[/yellow]")
        return
    for b in results:
        console.print(f"#{b.id} {b.url} [dim]{', '.join(b.tags)}[/dim]")


@app.command()
def remove(bookmark_id: int = typer.Argument(..., help="Bookmark ID.")) -> None:
    """Remove a bookmark."""
    if Storage().remove(bookmark_id):
        console.print(f"[green]Removed[/green] #{bookmark_id}")
    else:
        console.print(f"[red]Bookmark #{bookmark_id} not found.[/red]")
        raise typer.Exit(code=1)


@app.command()
def open(bookmark_id: int = typer.Argument(..., help="Bookmark ID.")) -> None:
    """Open a bookmark in the browser."""
    bookmarks = Storage().load()
    match = next((b for b in bookmarks if b.id == bookmark_id), None)
    if match is None:
        console.print(f"[red]Bookmark #{bookmark_id} not found.[/red]")
        raise typer.Exit(code=1)
    webbrowser.open(match.url)
    console.print(f"[green]Opened[/green] {match.url}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
