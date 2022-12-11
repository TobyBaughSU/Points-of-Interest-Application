from tree_sort import tree_sort

FILENAME = "POIs.txt"
ENQUIRY_FILENAME = "enquiries.txt"

def get_input(query: str = "",
              numOnly: bool = False,
              numMin=None,
              numMax=None,
              acceptBlank: bool = False,
              rawStr: bool = False):
    if not rawStr:
        query += ": "
    while True:
        try:
            inp = input(query)
            if not acceptBlank and len(inp) == 0:
                raise IndexError
            if numOnly and len(inp) > 0:
                inp = int(inp)
                if type(numMin) == int:
                    if inp < numMin:
                        raise ArithmeticError
                if type(numMax) == int:
                    if inp >= numMax:
                        raise ArithmeticError
        except ValueError:
            print("Please enter a number")
        except ArithmeticError:
            print("Please enter a value within range")
        except IndexError:
            pass
        else:
            return inp

def parse(string: str) -> dict:
    # 0: id, 1: name, 2: type, 3: description
    names = ("id", "name", "type", "description")
    lst = string.split(",")

    dict = {}
    for i in range(0, 4):
        dict[names[i]] = lst[i]
    dict["id"] = int(dict["id"])

    return dict


def add_poi() -> None:
    name = get_input("Enter a POI name")
    type = get_input("Enter a POI type")
    desc = get_input("Enter a POI description")

    with open(FILENAME, "r") as file:
        lines = file.readlines()
        if len(lines) == 0:
            id = 0
        else:
            prevId = int(parse(lines[-1])["id"])
            id = str(prevId + 1)
            if lines[-1][-1] != "\n":
                id = "\n" + id
    with open(FILENAME, "a") as file:
        file.write(f"{id}, {name}, {type}, {desc}")

def linear_search_poi(id: int, lines: list, useLineNum: int = False):
    for lineNum, line in enumerate(lines):

        if lineNum == id: # skips this as it was already tried in the main search
            continue

        if id == parse(line)["id"]:
            if useLineNum:
                return lineNum
            else:
                return line.rstrip("\n")
    return -1

def search_poi(id: int, useLineNum: int = False):
    with open(FILENAME, "r") as file:
        lines = file.readlines()
    try:
        if parse(lines[id])["id"] == id:
            if useLineNum:
                return id
            else:
                return lines[id].rstrip("\n")
        else:
            raise IndexError
    except IndexError:
        return linear_search_poi(id, lines, useLineNum)  # tries a linear search as a fallback

def user_search_poi() -> None:
    id = get_input("Enter the POIs ID", numOnly=True)
    out = search_poi(id)
    if out == -1:
        print("Query not found")
    else:
        print(out)

def search_poi_name(query: str) -> list:
    out = []
    with open(FILENAME, "r") as file:
        for line in file.readlines():
            name = parse(line)["name"]
            if query.lower() in name.lower():
                out.append(line.rstrip("\n"))
        return out

def user_search_poi_name() -> None:
    query = get_input("Enter the POIs name")
    out = search_poi_name(query)
    if len(out) == 0:
        print("Query not found")
    else:
        for i in out:
            print(i)

def list_sort(e: str) -> str:
    return parse(e)["name"].lower()

def list_poi() -> None:
    with open(FILENAME, "r") as file:
        lines = file.readlines()
        lines = tree_sort(lines, list_sort)

        for line in lines:
            line = line.rstrip("\n")
            print(line)

def delete_line(lineNum: int, file: str = FILENAME) -> None:
    with open(file, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines[:lineNum] + lines[lineNum+1:]:
            file.write(line)

def user_delete_poi():
    id = get_input("Enter a poi ID to delete", numOnly=True, numMin=0)
    lineNum = search_poi(id, useLineNum=True)
    if lineNum == -1:
        print("Query not found")
    else:
        delete_line(lineNum)
        print(f"Successfully deleted POI {id}")

def make_enquiry():
    enquiry = get_input("Please enter an enquiry")

    with open(ENQUIRY_FILENAME, "a+") as file:
        file.seek(0)
        lines = file.readlines()
        if len(lines) != 0:
            if lines[-1][-1] != "\n":
                enquiry = "\n" + enquiry
        file.seek(0, 2)
        file.write(enquiry)

def answer_enquiry() -> None:
    with open(ENQUIRY_FILENAME, "r") as file:
        lines = file.readlines()
    if len(lines) == 0:
        print("There are currently no enquiries")
    else:
        for number, line in enumerate(lines):
            line = line.rstrip("\n")
            print(f"{number}: {line}")
        choice = get_input("Enter an option from the above list", numOnly=True, numMin=0, numMax=number+1)
        delete_line(choice, file=ENQUIRY_FILENAME)
        print("Enquiry answered")


def disp_options():
    print("Selection an option from the list below:")
    print("0) Exit\n1) Add POI\n2) Search POI\n3) List all POIs\n4) Search POI name\n5) Delete POI\n6) Make enquiry\n7) Answer enquiry")
    choice = get_input("Enter option", numOnly=True, numMin=0, numMax=8)
    return choice

def run():
    print("POI application")
    choice = None
    while True:
        choice = disp_options()
        print()
        match choice:
            case 0:
                return
            case 1:
                add_poi()
            case 2:
                user_search_poi()
            case 3:
                list_poi()
            case 4:
                user_search_poi_name()
            case 5:
                user_delete_poi()
            case 6:
                make_enquiry()
            case 7:
                answer_enquiry()
            case _:
                print("ERROR: option not found")
        print()

run()
