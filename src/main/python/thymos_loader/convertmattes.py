# from openpyxl import workbook
import csv 
import polars as pl

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

def convert_mattes(source_files, target_file):
    for source_file in source_files:
        # read thymos csv file
        metadata, data = read_thymos_csv(source_file)
        # filter only loadcell2
        data = filter_only_loadcell2(data)
        print(metadata)
        print(data)


if __name__ == "__main__":

    # TEST convert_mattes
    source_files = ["dev/test_1.csv"]
    target_file = ""
    convert_mattes(source_files, target_file)
    
    # # TEST read_thymos_csv
    # metadata, data = read_thymos_csv("dev/test_1.csv")
    # print(metadata)
    # print(data)
    