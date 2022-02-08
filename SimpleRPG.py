from hashlib import new
import json
import os
import sys
import random

class Json:
    def __init__(self,Path):
        self.Path = os.path.join(os.path.dirname(__file__),"data",Path)

    def load(self):
        
        with open(self.Path,"r",encoding="utf-8") as f:
            Dict = json.load(f)
        
        return Dict
        
    def dump(self,Dict):
        
        with open(self.Path,"w",encoding="utf-8") as f:
            json.dump(Dict,f,indent=2)

class Map_Control:
    def __init__(self,MAP_SIZE):
        self.MAP_SIZE = MAP_SIZE

    def generate(self,MAP_SIZE,p_xy):#プレイヤーの座標
        map_data = [["+" for i in range(MAP_SIZE[0])] for i in range(MAP_SIZE)[1]]
        map_data = self.add_entity(map_data,"p",p_xy)
        
        return map_data
    
    def save(self,map_data,state_data):
        j =  Json("setting.json")
        Dict = j.load()
        Dict["map_data"] = map_data
        Dict["state_data"] = state_data
        Json("setting.json").dump(Dict)

    def draw(self,map_data):
        
        for i in map_data:
            print("".join(i))

    def add_entity(self,map_data,entity,xy):
        map_data[xy[1]][xy[0]] = entity

        return map_data
    
    def load(self,state_data,map_data=None):

        if state_data == "new":
            state_data = [
                self.xy_generator(self.MAP_SIZE),
                [self.xy_generator(self.MAP_SIZE) for i in range(3)],
                [self.xy_generator(self.MAP_SIZE) for i in range(3)]
            ]
        
        map_data = self.generate(self.MAP_SIZE,state_data[0])
        
        for xy in state_data[1]:
            self.add_entity(map_data,"e",xy)
            

    def xy_generator(self,map_size): #x,yの上限
        xy = [random.randrange(map_size[0]),random.randrange(map_size[1])]

        return xy
    
    def xy_searcher(self,entity,map_data):
        y = 0

        for i in map_data:
            
            try:
                xy = [i.index(entity),y]
                break
            except ValueError:
                pass

            y += 1
        
        return xy

class Game:    
    def __init__(self):
        self.j = Json("setting.json")

        try:
            self.p_name = self.j.load()['name']
            print("以下の名前のセーブデータを読み込みました\n→",self.p_name)
        except:
            self.p_name = input("君の名前を教えて!\n→")
            self.j.dump({
                    "name":self.p_name,
                    "state_data":["new"]
            })
            print("以下の名前でセーブデータを作成しました\n→",self.p_name)

    def preparation(self):
        MAP_SIZE = [20,10]
        Map = Map_Control(MAP_SIZE)
        j = Json("setting.json").load()
        self.state_data = j["state_data"][0]

        self.map_data = Map.load(self.state_data)
        entity_state = j["entity_state"]
        print("以下のマップをロードしました")
        Map.draw(self.map_data)

    def main(self):
        self.preparation()
        

    def run(self):
        
        while(1):
            selector = input("\nSIMPLE RPG\n\na:START\nb:DATACLEAR\nc:END\n→")
            
            if selector == "a":
                self.main()

            if selector == "b":
                input_name = input("二重確認:現在の名前を入力してください\n→")
            
                if input_name == self.p_name:
                    Json("setting.json").dump({})
                    input("データを削除しました。再起動してください。")
                    sys.exit()
                
                input("確認に失敗しました\nタイトルに戻ります。")
            
            if selector == "c":
                input("終了します")
                sys.exit()

            continue

if __name__ == "__main__":
    Game = Game()
    Game.run()