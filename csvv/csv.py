import pycountry
import copy
import sys

def read_csv(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    return lines



def cut_lines(lines):
    lines = [element.replace("\n" ,"").split(",") for element in lines]
    l = copy.deepcopy(lines)
    for i in range(len(lines)-1,-1,-1):
        if len(lines[i]) != 4:
            print("bledna ilosc danych w linijce "+ str(i+1), file=sys.stderr)
            l.remove(lines[i])
    return l


def format_date(lines):
    l = copy.deepcopy(lines)
    for i in range(len(lines)-1,-1,-1):
        month = lines[i][0][0:2]
        day = lines[i][0][3:5]
        year = lines[i][0][6:]
        try:
            int(day)
            int(month)
            int(year)
            date = year + "-" + month + "-" + day;
            lines[i][0] = date
        except ValueError:
            print("zly format daty w linijce " +str(i+1), file=sys.stderr)
            l.remove(lines[i])
            continue
        if int(day)>32 or int(day)<1 or int(month)>12 or int(month)<1 or int(year)<2000:
            print("zly przedzial daty w linijce "+ str(i+1), file=sys.stderr)
            l.remove(lines[i])
            continue
    print(len(lines))
    print(len(l))
    return l



# funkcja bierze liste miast i zwraca liste panstw w notacji 3 literowej
def replace_countries(lines):
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
    l = copy.deepcopy(lines)
    for i in range(len(lines)-1,-1,-1):
        try:
            l[i][3] = str(int(round(float(lines[i][2])*float(lines[i][3][0:-1])/100,0)))
        except:
            l.remove(lines[i])
            print("3 lub 4 dana w linijce " + str(i+1), file = sys.stderr)
    return l




def remove_multiplicity(lines):
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







def write_to_file(file_name,lines):
    with open(file_name, "w") as file:
        for record in lines:
            row = ','.join(record)
            file.write(row + "\n")
