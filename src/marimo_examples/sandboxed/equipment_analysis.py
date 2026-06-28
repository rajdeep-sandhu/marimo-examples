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
    from datetime import date

    import duckdb
    import polars as pl

    return BytesIO, date, duckdb, pl


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
    return upload_result, ux_trans, ux_trans_filename


@app.cell
def _(
    mo,
    upload_result: dict | None,
    ux_trans: "pl.DataFrame",
    ux_trans_filename: str,
):
    if upload_result:
        mo.output.append(mo.vstack([ux_trans_filename, ux_trans]))
    return


@app.cell
def _(duckdb, upload_result: dict | None, ux_trans: "pl.DataFrame"):
    if upload_result:
        conn = duckdb.connect()
        conn.register("ux_trans", ux_trans)
    return


@app.cell
def _(date, mo, ux_trans: "pl.DataFrame"):
    today: date = date.today()
    min_trans_date: date = ux_trans["date_extracted"].min()
    max_trans_date: date = ux_trans["date_extracted"].max()

    # The dataset should not have dates beyond the current date.
    # Raise an exception if it does.
    if max_trans_date > today:
        raise ValueError(
            f"Dataset contains future transactions: "
            f"max={max_trans_date:%Y-%m-%d}, today={today:%Y-%m-%d}"
        )

    start_date_input = mo.ui.date.from_series(
        ux_trans["date_extracted"], value=min_trans_date
    )

    end_date_input = mo.ui.date.from_series(
        ux_trans["date_extracted"], value=max_trans_date
    )
    return end_date_input, start_date_input


@app.cell
def _(end_date_input, mo, start_date_input):
    mo.hstack([start_date_input, end_date_input])
    return


if __name__ == "__main__":
    app.run()
