import json

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
            return item["geolocation"] if item["geolocation"] != None else "Город не задан"
        else:
            with open(self.path, "w", encoding="utf-8") as json_file:
                self.database["users"].append({"id": int(user_id), "geolocation": None})
                json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)
            return "Город не задан"

    def update_database(self):
        with open(self.path, "r+", encoding="utf-8") as json_file:
            if self.database != json.load(json_file):
                json.dump(self.database, json_file, indent=self.indent, ensure_ascii=False)
            else: pass

class CSV:
    def __init__(self, path, delimiter):
        self.path = path
        self.delimiter = delimiter
        self._csv_read()

    def _csv_read(self):
        with open(self.path, "r+", encoding="utf-8") as file:
            for user in file.readlines()[1:]:
                    item = user.split(self.delimiter)
                    self.database.append({"id": int(item[0]), "geolocation": item[1]})

    def _csv_append(self, item):
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(str(item["id"])+self.delimiter+str(item["geolocation"])+"\n")
        self.database.append(item)

    def _csv_write_all(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            file.write("id;geolocation\n")
            for item in self.database:
                file.write(str(item["id"])+self.delimiter+str(item["geolocation"])+"\n")

    def user_is_find(self,user_id):
        for item in self.database:
            if item["id"] == user_id:
                return item
        return None
        
    def init_user(self,user_id):
        if self.user_is_find(user_id) == None:
            self._csv_append({"id": int(user_id), "geolocation": "Город не задан"})
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
            self._csv_append({"id": int(user_id), "geolocation": "Город не задан"})
            return "Город не задан"