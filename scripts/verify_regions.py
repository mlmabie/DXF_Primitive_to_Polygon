#!/usr/bin/env python3
"""Capture targeted close-up screenshots of specific regions on each dashboard,
so we can spot fine-grained UX/spacing issues that full-page renders hide.

Usage:
    python scripts/verify_regions.py [--bundle out_bundle] [--out out_bundle/verify/regions]
"""
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parent.parent


REGIONS = [
    {
        "name": "dashboard_feature_grid",
        "file": "dashboard.html",
        "viewport": [1440, 1000],
        "selector": ".feature-grid",
    },
    {
        "name": "dashboard_hists_area",
        "file": "dashboard.html",
        "viewport": [1440, 1000],
        "selector_nth": (".chart-grid", 0),
    },
    {
        "name": "dashboard_hists_aspect",
        "file": "dashboard.html",
        "viewport": [1440, 1000],
        "selector_nth": (".chart-grid", 1),
    },
    {
        "name": "dashboard_raw_mix",
        "file": "dashboard.html",
        "viewport": [1440, 1000],
        "selector_nth": (".two-col", 0),
    },
    {
        "name": "dashboard_feature_card_single",
        "file": "dashboard.html",
        "viewport": [1440, 1000],
        "selector_nth": (".feature-card", 0),
    },
    {
        "name": "merge_lab_hero",
        "file": "merge_lab.html",
        "viewport": [1440, 900],
        "selector": ".hero",
    },
    {
        "name": "merge_lab_polygon_cards",
        "file": "merge_lab.html",
        "viewport": [1440, 1000],
        "selector": ".inspection-grid",
    },
    {
        "name": "merge_lab_sidebar",
        "file": "merge_lab.html",
        "viewport": [1440, 1200],
        "selector": ".sidebar",
    },
    {
        "name": "merge_lab_selected_toolbar",
        "file": "merge_lab.html",
        "viewport": [1920, 900],
        "selector": ".selected-toolbar",
    },
    {
        "name": "merge_lab_summary_grid",
        "file": "merge_lab.html",
        "viewport": [1440, 900],
        "selector": ".summary-grid",
    },
    {
        "name": "merge_lab_selected_candidate",
        "file": "merge_lab.html",
        "viewport": [1440, 1000],
        "selector": "#candidateExplain",
    },
    {
        "name": "merge_lab_detail_grid",
        "file": "merge_lab.html",
        "viewport": [1440, 1000],
        "selector": ".detail-grid",
    },
]


def run(bundle_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for spec in REGIONS:
            target = bundle_dir / spec["file"]
            if not target.exists():
                print(f"skip {spec['name']}: missing {target}")
                continue
            context = browser.new_context(
                viewport={"width": spec["viewport"][0], "height": spec["viewport"][1]},
                device_scale_factor=1,
            )
            page = context.new_page()
            page.goto(target.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(400)
            if "selector_nth" in spec:
                selector, idx = spec["selector_nth"]
                locator = page.locator(selector).nth(idx)
            else:
                locator = page.locator(spec["selector"]).first
            locator.scroll_into_view_if_needed()
            page.wait_for_timeout(200)
            if locator.count() == 0 or not locator.is_visible():
                print(f"skip {spec['name']}: selector not visible or missing")
                context.close()
                continue
            dest = out_dir / f"{spec['name']}.png"
            locator.screenshot(path=str(dest))
            print(f"region {spec['name']} -> {dest.name}")
            context.close()
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=REPO_ROOT / "out_bundle")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    out_dir = args.out if args.out is not None else args.bundle / "verify" / "regions"
    run(args.bundle, out_dir)


if __name__ == "__main__":
    main()
