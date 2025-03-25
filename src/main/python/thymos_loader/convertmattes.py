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
                    data_rows.append(row)

    # use Float64 for all columns
    data = pl.DataFrame(data_rows, schema=header)
    
    return metadata, data

def convert_mattes(source_files, target_file):
    pass
    


if __name__ == "__main__":

    # source_files = []
    # target_file = ""
    # convert_mattes(source_files, target_file)
    
    metadata, data = read_thymos_csv("dev/test_1.csv")
    print(metadata)
    print(data)
    