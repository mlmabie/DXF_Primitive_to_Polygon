"""CLI shim: ``python -m augrade.cli.merge_lab``."""

from __future__ import annotations

from ..review import merge_lab as _mod


def main() -> None:
    _mod.main()


if __name__ == "__main__":
    main()
