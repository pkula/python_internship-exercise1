import sys
import copy
import pycountry


def read_csv(file_name):
    #this function read a file line by line and return list contain lines
    with open(file_name, "r") as file:
        lines = file.readlines()
    return lines


def cut_lines(lines):
    #this function cut line to a single data and replace list contain lists 
    lines = [element.replace("\n" ,"").split(",") for element in lines]
    l = copy.deepcopy(lines)
    for i in range(len(lines)-1,-1,-1):
        if len(lines[i]) != 4:
            print("bledna ilosc danych w linijce "+ str(i+1), file=sys.stderr)
            l.remove(lines[i])
    return l


def format_date(lines):
    #this function get all cutted data and then change to format date
    l = copy.deepcopy(lines)
    for i in range(len(lines)-1,-1,-1):
        month = lines[i][0][0:2]
        day = lines[i][0][3:5]
        year = lines[i][0][6:]
        try:
            date = year + "-" + month + "-" + day;
            l[i][0] = date
            int(day)
            int(month)
            int(year)
        except ValueError:
            print("zly format daty w linijce " +str(i+1), file=sys.stderr)
            l.remove(lines[i])
            continue
        if int(day)>32 or int(day)<1 or int(month)>12 or int(month)<1 or int(year)<2000:
            print("zly przedzial daty w linijce "+ str(i+1), file=sys.stderr)
            l.remove(lines[i])
            continue
    return l



def replace_countries(lines):
    # this function get a lines and change region to country (3'letters notation)
    list_countries = []
    if_add = False
    for line in lines:
        for pycountry_city in list(pycountry.subdivisions):
            if line[1] == pycountry_city.name:
                line[1] = pycountry_city.country.alpha_3
                if_add = True
                break
        if if_add:
            if_add = False
            continue
        line[1] = "XXX"
    return lines


def format_CTR(lines):
    # this function change %CTR to numbers
    l = copy.deepcopy(lines)
    for i in range(len(lines)-1,-1,-1):
        try:
            l[i][3] = str(int(round(float(lines[i][2])*float(lines[i][3][0:-1])/100,0)))
        except:
            l.remove(lines[i])
            print("3 lub 4 dana w linijce " + str(i+1), file = sys.stderr)
    return l


def remove_multiplicity(lines):
    # this function combines a record with this same date and city
    new_lines = copy.deepcopy(lines)
    for i in range(len(lines)-1):
        for a in range(i+1,len(lines)):
            if lines[i][0] == lines[a][0] and lines[i][1] == lines[a][1]:
                lines[a][2] = str(int(float(lines[a][2]) + float(lines[i][2])))
                lines[a][3] = str(int(float(lines[a][3]) + float(lines[i][3])))
                lines[i]= 123456789
                break
    for i in range(len(lines)):
        if 123456789 in lines:
            lines.remove(123456789)
    return lines


def conv(date):
    """conversion date to int
    format date: YYYY-MM-DD
    example: conv("1994-07-24")
    """
    return int(date[0:4] + date[5:7] + date[8:])


def arrangment(lines):
    """ this function sort not quick so if you have to convert a big csv
     you must write a function based quick sort or bubble sort 
    """
    for i in range(len(lines)-1):
        for a in range(i+1,len(lines)):
            if conv(lines[i][0]) > conv(lines[a][0]) or conv(lines[i][0]) == conv(lines[a][0]) and lines[i][1] > lines[a][1] :
                t = lines[i]
                lines[i] = lines[a]
                lines[a] = t
    return lines


def write_to_file(file_name,lines):
    with open(file_name, "w") as file:
        for record in lines:
            row = ','.join(record)
            file.write(row + "\n")
