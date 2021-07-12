import json

class JSON:
    def __init__(self, path = "users.json"):
        self.path = path
        with open(self.path, "w+", encoding="utf-8") as json_file:
            if json_file.read():
                self.database = json.load(json_file)
            else:
                self.database = {'users': []}
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)

    def user_is_find(self,user_id):
        for item in self.database["users"]:
            if item["id"] == user_id:
                return True
        return False
        
    def init_user(self,user_id):
        if not self.user_is_find(user_id):
            with open(self.path, "w", encoding="utf-8") as json_file:
                item = {
                    "id": int(user_id),
                    "geolocation": None
                }
                self.database["users"].append(item)
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)
        else: pass

    def set_geolocation(self,user_id,geolocation):
        self.init_user(user_id)
        with open(self.path, "w", encoding="utf-8") as json_file:
            for item in self.database["users"]:
                if item["id"] == int(user_id):
                    item["geolocation"] = geolocation
                    json.dump(self.database,json_file,indent=4, ensure_ascii=False)
                    break
                else: pass

    def get_geolocation(self,user_id):
        self.init_user(user_id)
        for item in self.database["users"]:
            if item["id"] == int(user_id):
                return item["geolocation"] if item["geolocation"] != None else "Город не задан"

    def update_database(self):
        with open(self.path, "r+", encoding="utf-8") as json_file:
            if self.database != json.load(json_file):
                json.dump(self.database,json_file,indent=4, ensure_ascii=False)
            else: pass
