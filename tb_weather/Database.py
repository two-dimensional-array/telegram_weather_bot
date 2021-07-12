import json

class JSON:
    def __init__(self, path = "users.json"):
        self.path = path
        with open(self.path, "r+", encoding="utf-8") as json_file:
            try:
                self.database = json.load(json_file)
            except:
                self.database = {'users': []}
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)

    def user_is_find(self,user_id):
        for item in self.database["users"]:
            if item["id"] == user_id:
                return item
        return None
        
    def init_user(self,user_id):
        if self.user_is_find(user_id) == None:
            with open(self.path, "w", encoding="utf-8") as json_file:
                self.database["users"].append({"id": int(user_id), "geolocation": None})
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)
        else: pass

    def set_geolocation(self,user_id,geolocation):
        item = self.user_is_find(user_id)
        with open(self.path, "w", encoding="utf-8") as json_file:
            if item:
                item["geolocation"] = geolocation
            else:
                self.database["users"].append({"id": int(user_id), "geolocation": geolocation})
            json.dump(self.database,json_file,indent=4, ensure_ascii=False)

    def get_geolocation(self,user_id):
        item = self.user_is_find(user_id)
        if item:
            return item["geolocation"] if item["geolocation"] != None else "Город не задан"
        else:
            with open(self.path, "w", encoding="utf-8") as json_file:
                self.database["users"].append({"id": int(user_id), "geolocation": None})
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)
            return "Город не задан"

    def update_database(self):
        with open(self.path, "r+", encoding="utf-8") as json_file:
            if self.database != json.load(json_file):
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)
            else: pass
