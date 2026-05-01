"""Interactive review surfaces: dashboard, merge lab, and label tooling.

These are the review-side tools. They are kept in a subpackage so the
core extraction and library can be understood and audited without
reading through ~2500 lines of HTML generator.

None of the generated artifacts (dashboard.html, merge_lab.html,
merge_lab_data.json, dashboard_assets/) are tracked by git. Regenerate
with `python -m augrade.cli.pipeline <dxf> <out>` or the individual
CLI shims.
"""
