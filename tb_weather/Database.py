import re

CSV_FILE_HEADER = "id","geolocation"
DEFAULT_GEOLOCATION = "Город не задан" 

JSON_READ_PATTERN = r'\s*\"id\": (?P<id>\d*),\s*\"geolocation\": (?:(?:\"(?P<geolocation>.*)\")|(?:null))\s'
CSV_READ_PATTERN = r'(?P<id>\d+).(?:(?:\"(?P<geolocation>.*)\"\s)|\s)'
YAML_READ_PATTERN = r'-\s*id: (?P<id>\d+)\s*geolocation: (?:(?:null)|(?P<geolocation>.*))\s'

class Database:
    def __init__(self, path: str, read_pattern: str):
        self._path = path
        self._read_pattern = re.compile(read_pattern)

    def _read(self) -> list:
        database = []
        with open(self._path, "r", encoding="utf-8") as file:
            for match in self._read_pattern.finditer(file.read()): 
                id = int(match.group("id"))
                geolocation = match.group("geolocation")
                database.append({"id": id, "geolocation": geolocation })
        return database

    def _append(self, item: dict[int,str]) -> None:
        raise NotImplementedError("Method _append() is`n implemented in child class")

    def _write_all(self) -> None:
        raise NotImplementedError("Method _write_all() is`n implemented in child class")

    def _write_user_to_str(self, item: dict[int,str]) -> str:
        raise NotImplementedError("Method _write_user_to_str() is`n implemented in child class")

    def _user_is_find(self, user_id: int) -> dict[int,str] or None:
        for item in self._database:
            if item["id"] == user_id:
                return item
        return None

    def init_user(self, user_id: int) -> None:
        if self._user_is_find(user_id) == None:
            self._append({"id": int(user_id), "geolocation": None })
        else: pass

    def set_geolocation(self, user_id: int, geolocation: str) -> None:
        item = self._user_is_find(user_id)
        if item:
            item["geolocation"] = geolocation
            self._write_all()
        else:
            self._append({"id": int(user_id), "geolocation": geolocation})

    def get_geolocation(self, user_id: int) -> str:
        item = self._user_is_find(user_id)
        if item:
            return item["geolocation"] if item["geolocation"] else DEFAULT_GEOLOCATION
        else:
            self._append({"id": int(user_id), "geolocation": None })
            return DEFAULT_GEOLOCATION 

    def update_database(self) -> None:
        if self._database != self._read():
            self._write_all()
        else: pass

class JSON(Database):
    def __init__(self, path: str = "users.json", indent: int = 4):
        self.__indent = indent
        Database.__init__(self, path, JSON_READ_PATTERN)
        try:
            self._database = self._read()
        except:
            with open(self._path, "w+", encoding="utf-8") as file:
                file.write(f'{{\n{" "*self.__indent}"users": [\n{" "*self.__indent}]\n}}\n')

    def _write_user_to_str(self, item: dict[int,str]) -> str:
        geolocation = f'"{item["geolocation"]}"' if item["geolocation"] else "null"
        user_data  = f'{" "*(self.__indent*2)}{{\n'
        user_data += f'{" "*(self.__indent*3)}"id": {item["id"]},\n'
        user_data += f'{" "*(self.__indent*3)}"geolocation": {geolocation}\n'
        user_data += f'{" "*(self.__indent*2)}}}'
        return user_data

    def _append(self, item: dict[int,str]):
        with open(self._path, "a", encoding="utf-8") as file:
            file.truncate(file.tell()-(8+self.__indent))
            file.write(f',\n{self._write_user_to_str(item)}\n{" "*self.__indent}]\n}}\n')
        self._database.append(item)

    def _write_all(self) -> None:
        with open(self._path, "w+", encoding="utf-8") as file:
            file.write(f'{{\n{" "*self.__indent}"users": [\n{self._write_user_to_str(self._database[0])}')
            for item in self._database[1:]:
                file.write(f',\n{self._write_user_to_str(item)}')
            file.write(f'\n{" "*self.__indent}]\n}}\n')

class CSV(Database):
    def __init__(self, path: str = "users.csv", delimiter: str = ";"):
        self.__delimiter = delimiter
        Database.__init__(self, path, CSV_READ_PATTERN)
        try:
            self._database = self._read()
        except:
            with open(self._path, "w+", encoding="utf-8") as file:
                file.write(f'{CSV_FILE_HEADER[0]}{self.__delimiter}{CSV_FILE_HEADER[1]}\n')

    def _write_user_to_str(self, item: dict[int,str]) -> str:
        geolocation = f'"{item["geolocation"]}"\n' if item["geolocation"] else "\n"
        return f'{item["id"]}{self.__delimiter}{geolocation}'

    def _append(self, item: dict[int,str]) -> None:
        with open(self._path, "a", encoding="utf-8") as file:
            file.write(self._write_user_to_str(item))
        self._database.append(item)

    def _write_all(self) -> None:
        with open(self._path, "w+", encoding="utf-8") as file:
            file.write(f'{CSV_FILE_HEADER[0]}{self.__delimiter}{CSV_FILE_HEADER[1]}\n')
            for item in self._database:
                file.write(self._write_user_to_str(item))

class YAML(Database):
    def __init__(self, path: str = "users.yaml", indent: int = 2):
        self.__indent = indent
        Database.__init__(self, path, YAML_READ_PATTERN)
        try:
            self._database = self._read()
        except:
            with open(self._path, "w+", encoding="utf-8") as file:
                file.write("users:\n")

    def _write_user_to_str(self, item: dict[int,str]) -> str:
        user_data = f'-{" " * (self.__indent-1)}id: {item["id"]}\n'
        user_data += f'{" " * self.__indent}geolocation: {item["geolocation"] if item["geolocation"] else "null"}\n'
        return user_data

    def _append(self, item: dict[int,str]) -> list:
        with open(self._path, "a", encoding="utf-8") as file:
            file.write(self._write_user_to_str(item))
        self._database.append(item)

    def _write_all(self) -> None:
        with open(self._path, "w+", encoding="utf-8") as file:
            file.write("users:\n")
            for item in self._database:
                file.write(self._write_user_to_str(item))
