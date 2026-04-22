"""CLI shim: ``python -m augrade.cli.dashboard``."""

from __future__ import annotations

from ..review import dashboard as _mod


def main() -> None:
    _mod.main()


if __name__ == "__main__":
    main()
