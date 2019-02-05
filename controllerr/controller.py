from csvv import csv
import sys


def option(opt):
    file_to_open = "csv.csv"
    file_to_save = "new_scv.csv"
    if len(opt) > 1:
        for i in range(1,len(opt),2):
            if opt[i] == "--file":
                file_to_open = opt[i+1]
            if opt[i] == "--file":
                file_to_open = opt[i+1]
            if opt[i] == "--sfile":
                file_to_save = opt[i+1]
    return [file_to_open,file_to_save]

def run(opt):
    files = option(opt)
    file_to_open = files[0]
    file_to_save = files[1]
    try:
        lines = csv.read_csv(file_to_open)
    except FileNotFoundError:
        print("critical error- do not find a choosed file", file=sys.stderr)
    else:
        lines = csv.cut_lines(lines)
        lines = csv.format_date(lines)
        lines = csv.format_CTR(lines)
        lines = csv.replace_countries(lines)
        lines = csv.remove_multiplicity(lines)
        lines = csv.arrangment(lines)
        for line in lines:

            print(line)

        file_name = "news.csv"
        csv.write_to_file(file_to_save,lines)
