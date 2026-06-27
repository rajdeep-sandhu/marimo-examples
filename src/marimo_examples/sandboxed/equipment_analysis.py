# /// script
# dependencies = [
#     "duckdb==1.5.4",
#     "fastexcel==0.20.2",
#     "marimo",
#     "polars[pyarrow]==1.42.0",
#     "sqlglot==30.12.0",
# ]
# requires-python = ">=3.14"
# ///

import marimo

__generated_with = "0.23.11"
app = marimo.App(width="full", app_title="Equipment Analysis")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Equipment Transaction Analysis
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    # Upload equipment data file
    file_input = mo.ui.file(
        label="Upload Equipment Transaction Data (`.xlsx`)",
        filetypes=[".xlsx"],
        multiple=False,
    )

    file_input
    return


if __name__ == "__main__":
    app.run()
