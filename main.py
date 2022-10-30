FILENAME = "POIs.txt"


def get_input(query: str = "",
              acceptBlank: bool = False,
              numOnly: bool = False,
              rawStr: bool = False):
    if rawStr == False:
        query += ": "
    while True:
        try:
            inp = input(query)
            if acceptBlank == False and len(inp) == 0:
                raise IndexError
            if numOnly == True and len(inp) > 0:
                inp = int(inp)
        except ValueError:
            print("Please enter a number")
        except IndexError:
            pass
        else:
            return inp


def parse(string: str) -> dict:
    # 0: id, 1: name, 2: type, 3: description
    names = ("id", "name", "type", "description")
    lst = string.split(",")

    dict = {}
    dict["id"] = lst[0]
    for i in range(4):
        dict[names[i]] = lst[i]

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
            id = "\n" + str(prevId + 1)
    with open(FILENAME, "a") as file:
        file.write(f"{id}, {name}, {type}, {desc}")


def search_poi(id: int):
    with open(FILENAME, "r") as file:
        for line in file.readlines():
            if id == parse(line)["id"]:
                return line
        return -1


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


def list_sort(e):
    return parse(e)["name"].lower()


def list_poi() -> None:
    with open(FILENAME, "r") as file:
        lines = file.readlines()
        lines.sort(key=list_sort)

        for line in lines:
            line = line.rstrip("\n")
            print(line)


def delete_poi(id: int):
    with open(FILENAME, "rw") as file:
        lines = file.readlines()


user_search_poi()
# add_poi()
# list_poi()
