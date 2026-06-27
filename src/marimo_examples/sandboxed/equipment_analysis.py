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
def _():
    from io import BytesIO

    import duckdb
    import polars as pl

    return BytesIO, pl


@app.cell
def _(mo):
    file_input = mo.ui.file(
        label="Upload Equipment Transaction Data (`.xlsx`)",
        filetypes=[".xlsx"],
        multiple=False,
    )

    file_input
    return (file_input,)


@app.cell
def _(BytesIO, pl):
    def file_to_df(file_input) -> dict:
        """
        Returns the filenme and a polars dataframe from a .xlsx file uploaded via mo.ui.file.

        params:
        file_input: The file input element's value.
        """

        # Get first result for single file upload
        result = file_input.value[0]
        filename: str = result.name
        content: bytes = result.contents
        df: pl.DataFrame = pl.read_excel(source=BytesIO(content))

        return {"filename": filename, "data": df}

    return (file_to_df,)


@app.cell
def _(file_input, file_to_df, pl):
    upload_result: dict | None = None

    if file_input.value:
        upload_result = file_to_df(file_input)
        ux_trans_filename: str = upload_result["filename"]
        ux_trans: pl.DataFrame = upload_result["data"]
    return (ux_trans,)


@app.cell
def _(ux_trans: "pl.DataFrame"):
    ux_trans
    return


if __name__ == "__main__":
    app.run()
