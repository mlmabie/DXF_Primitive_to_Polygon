#!/usr/bin/env python3
"""Render the generated dashboards with a headless browser and screenshot them
at multiple viewport widths so UX/spacing issues can be audited visually.

Usage:
    python scripts/verify_dashboards.py [--bundle out_bundle] [--out out_bundle/verify]

Outputs one PNG per (dashboard, viewport) pair plus a short manifest.json
that records the console errors and bounding-box checks for each render.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import ConsoleMessage, sync_playwright


REPO_ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    {"name": "dashboard", "file": "dashboard.html"},
    {"name": "merge_lab", "file": "merge_lab.html"},
]

VIEWPORTS = [
    {"label": "w1920", "width": 1920, "height": 1200},
    {"label": "w1440", "width": 1440, "height": 980},
    {"label": "w1100", "width": 1100, "height": 900},
]


def run(bundle_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for page_spec in PAGES:
            for viewport in VIEWPORTS:
                target = bundle_dir / page_spec["file"]
                if not target.exists():
                    print(f"skip {target}: missing")
                    continue
                context = browser.new_context(
                    viewport={"width": viewport["width"], "height": viewport["height"]},
                    device_scale_factor=1,
                )
                page = context.new_page()
                console_errors: list[str] = []

                def _on_console(msg: ConsoleMessage) -> None:
                    if msg.type in {"error", "warning"}:
                        console_errors.append(f"[{msg.type}] {msg.text}")

                page.on("console", _on_console)
                page.goto(target.as_uri(), wait_until="networkidle")
                page.wait_for_timeout(400)

                full_name = f"{page_spec['name']}_{viewport['label']}.png"
                full_path = out_dir / full_name
                page.screenshot(path=str(full_path), full_page=True)

                viewport_name = f"{page_spec['name']}_{viewport['label']}_viewport.png"
                viewport_path = out_dir / viewport_name
                page.screenshot(path=str(viewport_path), full_page=False)

                overflow = page.evaluate(
                    """() => {
                        const doc = document.documentElement;
                        return {
                            scrollWidth: doc.scrollWidth,
                            clientWidth: doc.clientWidth,
                            scrollHeight: doc.scrollHeight,
                            clientHeight: doc.clientHeight,
                            horizontalOverflow: doc.scrollWidth - doc.clientWidth,
                        };
                    }"""
                )

                manifest.append(
                    {
                        "page": page_spec["name"],
                        "viewport": viewport["label"],
                        "viewport_size": [viewport["width"], viewport["height"]],
                        "screenshot_full": full_name,
                        "screenshot_viewport": viewport_name,
                        "console": console_errors,
                        "overflow": overflow,
                    }
                )
                context.close()
                print(
                    f"rendered {page_spec['name']} @ {viewport['label']} -> {full_name} "
                    f"(overflowX={overflow['horizontalOverflow']}, console={len(console_errors)})"
                )
        browser.close()

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, default=REPO_ROOT / "out_bundle")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    out_dir = args.out if args.out is not None else args.bundle / "verify"
    run(args.bundle, out_dir)


if __name__ == "__main__":
    main()
