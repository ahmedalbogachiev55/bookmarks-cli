# bookmarks-cli

Simple bookmarks manager for the terminal.

## Install

```bash
pip install -e .
```n
## Usage

```bash
bm add https://python.org --tag python
bm list
bm list --tag python
bm search python
bm remove 1
bm open 1
```n
Bookmarks are stored in `~/.bookmarks.json`.

## Development

```bash
uv sync
uv run pytest
```n
## License

MIT
