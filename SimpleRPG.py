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

    def generate(self,p_xy):#プレイヤーの座標
        map_data = [["+" for i in range(self.MAP_SIZE[0])] for raw in range(self.MAP_SIZE[1])]
        map_data = self.add_entity(map_data,"p",p_xy)
        
        return map_data
    
    def save(self,map_data):
        j =  Json("setting.json")
        Dict = j.load()
        Dict["state_data"] = self.state_data_picker(map_data)
        Json("setting.json").dump(Dict)

    def draw(self,map_data):
        
        for i in map_data:
            print("".join(i))

    def add_entity(self,map_data,entity,xy):
        map_data[xy[1]][xy[0]] = entity

        return map_data
    
    def load(self,state_data=None): #新規作成ならstate_dataには引数を渡さない

        if state_data == None:
            state_data = self.create_new_states()
        
        map_data = self.generate(state_data[0])
        
        for xy in state_data[1]:
            map_data = self.add_entity(map_data,"e",xy)
        
        for xy in state_data[2]:
            map_data = self.add_entity(map_data,"i",xy)
        
        return map_data

    def xy_generator(self): #x,yの上限
        xy = [random.randrange(self.MAP_SIZE[0]),random.randrange(self.MAP_SIZE[1])]
        
        return xy
    
    def state_data_picker(self,map_data):

        state_data = [
            self.xy_searcher("p",map_data)[0],
            self.xy_searcher("e",map_data),
            self.xy_searcher("i",map_data)
        ]

        return state_data

    def create_new_states(self):
        
        while (1):
            l = []
            states = [self.xy_generator() for i in range(7)]
            another = [x for x in states if x not in l and not l.append(x)]

            if  len(states) == len(another):
                break

        states = [
            states[0],
            [x for x in states if states.index(x) > 0 and states.index(x) < 4],
            [x for x in states if states.index(x) > 3]
        ]

        return states
    
    def xy_searcher(self,entity,map_data):
        y = 0
        l = []
        for i in map_data:
            
            try:
                xy = [i.index(entity),y]
                l.append(xy)
            except ValueError:
                pass

            y += 1
        
        return l

class Controller:
    def __init__(self,map_data,MAP_CLASS):
        self.Map = MAP_CLASS

        while (1):
            selector = input("w:上\ns:下\na:左\nd:右\nq:セーブしてタイトルに戻る\n→")
            
            if selector in ["w","a","s","d"]:
                pass
            
            elif selector == "q":
                self.Map.save(map_data)
                input("セーブしました")
                break

            else:
                input("無効な操作")

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
                    "state_data":"new"
            })
            print("以下の名前でセーブデータを作成しました\n→",self.p_name)

    def preparation(self):

        MAP_SIZE = [20,10]
        
        self.Map = Map_Control(MAP_SIZE)
        data = Json("setting.json").load()
        self.state_data = data["state_data"]

        if self.state_data == "new":
            self.map_data = self.Map.load()
        else:
            self.map_data = self.Map.load(self.state_data)

        print("以下のマップをロードしました")
        self.Map.draw(self.map_data)

    def main(self):
        self.preparation()
        Controller(self.map_data,self.Map)

        

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

if __name__ == "__main__":
    Game = Game()
    Game.run()