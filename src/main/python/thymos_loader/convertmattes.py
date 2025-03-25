import os
import glob
import csv
import polars as pl
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment

def read_thymos_csv(file_path):
    metadata = {}
    data_rows = []
    header = None
    reading_state = "metadata"

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if reading_state == "metadata":
                if len(row) == 0:
                    reading_state = "header"
                elif len(row) >= 2:
                    metadata[row[0]] = row[1]
                elif len(row) == 1:
                    metadata[row[0]] = None
            elif reading_state == "header":
                header = row
                reading_state = "data"
            elif reading_state == "data":
                if len(row) == len(header):
                    data_rows.append([float(cell) if cell else 0.0 for cell in row])

    data = pl.DataFrame(data_rows, schema=[(col, pl.Float64) for col in header])
    return metadata, data

def filter_only_loadcell2(data):
    # return only columns: time, position, loadcell2
    return data.select(["time", "position", "loadcell2"])

def convert_mattes(csv_folder, output_excel_path):
    csv_files = sorted(glob.glob(os.path.join(csv_folder, "*.csv")))

    wb = Workbook()
    ws = wb.active
    ws.title = "Measurements"

    col_offset = 1

    for index, file_path in enumerate(csv_files, start=1):
        metadata, data = read_thymos_csv(file_path)

        # Převod polars -> pandas pro zápis do Excelu
        df = data.to_pandas()

        # Napiš nadpis s číslem
        ws.cell(row=1, column=col_offset, value=str(index)).alignment = Alignment(horizontal="center")

        # Metadata (1 řádek s nadpisem)
        ws.cell(row=2, column=col_offset, value="Measured values from testing machine")
        ws.merge_cells(start_row=2, start_column=col_offset, end_row=2, end_column=col_offset + len(df.columns) - 1)

        # Jednotky
        units = {
            "Time": "s",
            "position": "mm",
            "loadcell1": "N",
            "loadcell2": "N",
            "loadcell3": "N"
        }

        # Napiš hlavičku
        for i, col_name in enumerate(df.columns):
            ws.cell(row=3, column=col_offset + i, value=col_name)
            ws.cell(row=4, column=col_offset + i, value=units.get(col_name, ""))

        # Data
        for r_idx, row in enumerate(df.itertuples(index=False), start=5):
            for c_idx, value in enumerate(row):
                ws.cell(row=r_idx, column=col_offset + c_idx, value=value)

        # Posuň se doprava pro další tabulku
        col_offset += len(df.columns) + 1  # +1 mezera

    wb.save(output_excel_path)


if __name__ == "__main__":

    # TEST convert_mattes
    source_files = ["dev/test_1.csv"]
    target_file = ""
    convert_mattes(source_files, target_file)
    
    # # TEST read_thymos_csv
    # metadata, data = read_thymos_csv("dev/test_1.csv")
    # print(metadata)
    # print(data)
    