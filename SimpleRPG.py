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
    def __init__(self):
        pass

    def generate(self,p_xy):#プレイヤーの座標
        map_data = [["+" for i in range(20)] for i in range(10)]
        map_data[p_xy[1]][p_xy[0]] = "p"
        
        return map_data
    
    def printm(self,map_data):
        
        for i in map_data:
            print("".join(i))
    
    def xy_generator(self,x,y): #x,yの上限
        xy = [random.randrange(x),random.randrange(y)]

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
                    "map_data":["new"]
            })
            print("以下の名前でセーブデータを作成しました\n→",self.p_name)

    def run(self):
        
        while(1):
            selector = input("\nSIMPLE RPG\n\na:START\nb:DATACLEAR\nc:END\n→")
            
            if selector == "a":
                Main()

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

class Main:
        def __init__(self):
            Map = Map_Control()
            j = Json("setting.json").load()
            self.map_data = j["map_data"][0]

            if self.map_data == "new":
                p_xy = Map.xy_generator(20,10)
                input(p_xy)
                self.map_data = Map.generate(p_xy)
            
            print(Map.xy_searcher("p",self.map_data),p_xy)
            Map.printm(self.map_data)
            

if __name__ == "__main__":
    Game = Game()
    Game.run()