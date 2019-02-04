from csvv import csv
import sys
def run():
    try:
        lines = csv.read_csv("csv.csv")
    except FileNotFoundError:
        print("nie ma pliku,blad fatalny", file=sys.stderr) #tu dopisac zapis bledu do pliku
    else:
        lines = csv.cut_lines(lines)
        lines = csv.format_date(lines)
        lines = csv.format_CTR(lines)
        lines = csv.replace_countries(lines)
        lines = csv.remove_multiplicity(lines)
        print(lines)

        file_name = "news.csv"
        csv.write_to_file(file_name,lines)
