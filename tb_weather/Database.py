import json

CSV_FILE_HEADER = "id","geolocation"
DEFAULT_GEOLOCATION = "Город не задан" 

class Database:
    pass

class JSON:
    def __init__(self, path = "users.json", indent = 4):
        self.path = path
        self.indent = indent
        with open(self.path, "r+", encoding="utf-8") as json_file:
            try:
                self.database = json.load(json_file)
            except:
                self.database = {'users': []}
                json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)

    def user_is_find(self,user_id):
        for item in self.database["users"]:
            if item["id"] == user_id:
                return item
        return None
        
    def init_user(self,user_id):
        if self.user_is_find(user_id) == None:
            with open(self.path, "w", encoding="utf-8") as json_file:
                self.database["users"].append({"id": int(user_id), "geolocation": None})
                json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)
        else: pass

    def set_geolocation(self,user_id,geolocation):
        item = self.user_is_find(user_id)
        with open(self.path, "w", encoding="utf-8") as json_file:
            if item:
                item["geolocation"] = geolocation
            else:
                self.database["users"].append({"id": int(user_id), "geolocation": geolocation})
            json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)

    def get_geolocation(self,user_id):
        item = self.user_is_find(user_id)
        if item:
            return item["geolocation"] if item["geolocation"] != None else DEFAULT_GEOLOCATION 
        else:
            with open(self.path, "w", encoding="utf-8") as json_file:
                self.database["users"].append({"id": int(user_id), "geolocation": None})
                json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)
            return DEFAULT_GEOLOCATION 

    def update_database(self):
        with open(self.path, "r+", encoding="utf-8") as json_file:
            if self.database != json.load(json_file):
                json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)
            else: pass

class CSV:
    def __init__(self, path = "users.csv", delimiter = ";"):
        self.path = path
        self.delimiter = delimiter
        self.database = self._csv_read()

    def _csv_read(self):
        database = []
        try:
            with open(self.path, "r+", encoding="utf-8") as file:
                for user in file.readlines()[1:]:
                    item = user.split(self.delimiter)
                    database.append({"id": int(item[0]), "geolocation": item[1]})
        except:
            with open(self.path, "w+", encoding="utf-8") as file:
                file.write(CSV_FILE_HEADER[0]+self.delimiter+CSV_FILE_HEADER[1]+"\n")
        return database

    def _csv_append(self, item):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(str(item["id"])+self.delimiter+str(item["geolocation"])+"\n")
        self.database.append(item)

    def _csv_write_all(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            file.write(CSV_FILE_HEADER[0]+self.delimiter+CSV_FILE_HEADER[1]+"\n")
            for item in self.database:
                file.write(str(item["id"])+self.delimiter+str(item["geolocation"])+"\n")

    def user_is_find(self,user_id):
        for item in self.database:
            if item["id"] == user_id:
                return item
        return None
        
    def init_user(self,user_id):
        if self.user_is_find(user_id) == None:
            self._csv_append({"id": int(user_id), "geolocation": DEFAULT_GEOLOCATION })
        else: pass

    def set_geolocation(self,user_id,geolocation):
        item = self.user_is_find(user_id)
        if item:
            item["geolocation"] = geolocation
            self._csv_write_all()
        else:
            self._csv_append({"id": int(user_id), "geolocation": geolocation})

    def get_geolocation(self,user_id):
        item = self.user_is_find(user_id)
        if item:
            return item["geolocation"]
        else:
            self._csv_append({"id": int(user_id), "geolocation": DEFAULT_GEOLOCATION })
            return DEFAULT_GEOLOCATION 

    def update_database(self):
        if self.database != self._csv_read():
            self._csv_write_all()
        else: pass

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
