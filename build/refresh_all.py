"""
refresh_all.py — regenerate every DB-derived output in one step.

After editing capex_portfolio.db (via DB Browser or import_excel.py --apply),
both the Excel workbook and the website's data file need regenerating, or
they'll disagree with the database and with each other. This is the one
command to run after any database edit:

    python3 refresh_all.py

Equivalent to running build_workbook.py then export_site_data.py, in that
order (the workbook doesn't depend on the site export or vice versa, but
running them together is the routine you actually want after a DB change).
"""
import build_workbook
import export_site_data


def main():
    print("== Rebuilding Excel workbook ==")
    build_workbook.main()
    print("\n== Regenerating site data ==")
    export_site_data.export()


if __name__ == "__main__":
    main()
