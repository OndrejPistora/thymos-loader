from openpyxl import workbook
import csv 
import polars as pl

def read_thymos_csv(file_path):
    metadata = {}
    # data is empty polars table
    data = 
    reading_state = "metadata"

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # read metadata rows one by one
            if reading_state == "metadata":
                if len(row) == 0:
                    reading_metadata = "blank"
                else:
                    metadata[row[0]] = row[1]
            if reading_state == "blank":
                reading_state = "header"
            if reading_state == "header":
                # prepare polars table
                header = row
                reading_state = "data"
            if reading_state == "data":
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
    