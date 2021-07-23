import json

CSV_FILE_HEADER = "id","geolocation"
DEFAULT_GEOLOCATION = "Город не задан" 

class Database:
    def __init__(self, path):
        self._path = path
        self._database = self._read()

    def _read(self):
        pass

    def _append(self,item):
        pass

    def _write_all(self):
        pass

    def _user_is_find(self,user_id):
        for item in self._database["users"]:
            if item["id"] == user_id:
                return item
        return None

    def init_user(self,user_id):
        if self.user_is_find(user_id) == None:
            self._append({"id": int(user_id), "geolocation": None })
        else: pass

    def set_geolocation(self,user_id,geolocation):
        item = self._user_is_find(user_id)
        if item:
            item["geolocation"] = geolocation
            self._write_all()
        else:
            self._append({"id": int(user_id), "geolocation": geolocation})

    def get_geolocation(self,user_id):
        item = self._user_is_find(user_id)
        if item:
            return item["geolocation"] if item["geolocation"] != None else DEFAULT_GEOLOCATION
        else:
            self._append({"id": int(user_id), "geolocation": None })
            return DEFAULT_GEOLOCATION 

    def update_database(self):
        if self._database != self._read():
            self._write_all()
        else: pass

class JSON(Database):
    def __init__(self, path = "users.json", indent = 4):
        self.__indent = indent
        Database.__init__(self, path)

    def _read(self):
        database = {'users': []}
        try:
            with open(self._path, "r", encoding="utf-8") as file:
                database = json.load(file)
        except:
                with open(self._path, "w", encoding="utf-8") as file:
                    json.dump(database, file, indent=self.__indent, ensure_ascii=False)
        return database

    def _append(self,item):
        self._database["users"].append(item)
        with open(self._path, "w", encoding="utf-8") as file:
            json.dump(self._database, file, indent=self.__indent, ensure_ascii=False)

    def _write_all(self):
        with open(self._path, "w", encoding="utf-8") as file:
            json.dump(self._database, file, indent=self.__indent, ensure_ascii=False)

class CSV(Database):
    def __init__(self, path = "users.csv", delimiter = ";"):
        self.__delimiter = delimiter
        Database.__init__(self, path)

    def _read(self):
        database = []
        try:
            with open(self._path, "r+", encoding="utf-8") as file:
                for user in file.readlines()[1:]:
                    item = user.split(self.__delimiter)
                    database.append({"id": int(item[0]), "geolocation": item[1]})
        except:
            with open(self._path, "w+", encoding="utf-8") as file:
                file.write(CSV_FILE_HEADER[0]+self.__delimiter+CSV_FILE_HEADER[1]+"\n")
        return database

    def _append(self, item):
        with open(self._path, "a", encoding="utf-8") as file:
            file.write(str(item["id"])+self.__delimiter+str(item["geolocation"])+"\n")
        self._database.append(item)

    def _write_all(self):
        with open(self._path, "w+", encoding="utf-8") as file:
            file.write(CSV_FILE_HEADER[0]+self.__delimiter+CSV_FILE_HEADER[1]+"\n")
            for item in self._database:
                file.write(str(item["id"])+self.__delimiter+str(item["geolocation"])+"\n")

class YAML:
    def __init__(self, path = "users.yaml", indent = 2):
        self.path = path
        self.indent = indent
        self.database = self._yaml_read()

    def __write_user_to_str(self, item):
        user_data = f'-{" " * (self.indent-1)}id: {item["id"]}\n'
        user_data += f'{" " * self.indent}geolocation: {item["geolocation"] if item["geolocation"] != None else "null"}\n'
        return user_data

    def _yaml_read(self):
        database = {'users': []}
        try:
            with open(self.path, "r+", encoding="utf-8") as file:
                text = file.readlines()
                for count in range(1,len(text),2):
                    id = int(text[count][self.indent:].split(" ")[1])
                    geolocation = text[count+1][self.indent:].split(" ")[1]
                    database["users"].append({"id": id, "geolocation": geolocation if geolocation != "null\n" else None})
        except:
            with open(self.path, "w+", encoding="utf-8") as file:
                file.write("users:\n")
        return database

    def _yaml_append(self, item):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(self.__write_user_to_str(item))
        self.database["users"].append(item)

    def _yaml_write_all(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            file.write("users:\n")
            for item in self.database["users"]:
                file.write(self.__write_user_to_str(item))

    def user_is_find(self,user_id):
        for item in self.database["users"]:
            if item["id"] == user_id:
                return item
        return None

    def init_user(self,user_id):
        if self.user_is_find(user_id) == None:
            self._yaml_append({"id": int(user_id), "geolocation": None})
        else: pass

    def set_geolocation(self,user_id,geolocation):
        item = self.user_is_find(user_id)
        if item:
                item["geolocation"] = geolocation
                self._yaml_write_all()
        else:
            self._yaml_append({"id": int(user_id), "geolocation": geolocation})

    def get_geolocation(self,user_id):
        item = self.user_is_find(user_id)
        if item:
            return item["geolocation"] if item["geolocation"] != None else DEFAULT_GEOLOCATION
        else:
            self._yaml_append({"id": int(user_id), "geolocation": None})
            return DEFAULT_GEOLOCATION 

    def update_database(self):
        if self.database != self._yaml_read():
            self._yaml_write_all()
        else: pass
