"""CLI shim: ``python -m augrade.cli.labels``."""

from __future__ import annotations

from ..review import labels as _mod


def main() -> None:
    _mod.main()


if __name__ == "__main__":
    main()
