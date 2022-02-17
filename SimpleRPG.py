import json
import os
import sys
import random
import copy

class Json:
    def __init__(self,file_name):
        self.Path = os.path.join(os.path.dirname(__file__),"data",file_name)

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

    def generate(self,player_state):
        """map_data_structure
        map_data = [(y↓)
            [floor_element,...(x→)],
            [floor_element,...],
            ...
        ]
        """ 
        #y軸は下が正の方向、x軸は右が正の方向
        map_data = self.add_entity([["+" for i in range(self.MAP_SIZE[0])] for raw in range(self.MAP_SIZE[1])],"p",player_state)
        
        return map_data
    
    def save(self,data,state_mode=False): #state_modeにTrueを渡すとdataをstate_dataとして扱い、記録を行う
        j =  Json("setting.json")
        Dict = j.load()

        if state_mode:
            Dict["state_data"] = data
        else:
            Dict["state_data"] = self.state_data_picker(data)
        
        j.dump(Dict)

    def draw(self,map_data):
        
        for i in map_data:
            print("".join(i)) #列は連結していない

    def add_entity(self,map_data,entity,xy):
        map_data[xy[1]][xy[0]] = entity #座標の探索はy軸、x軸の順

        return map_data
    
    def load(self,state_data=None): #新規作成ならstate_dataには引数を渡さない

        if state_data == None:
            state_data = self.create_new_states()
            self.save(state_data,True)
        
        map_data = self.generate(state_data[0])
    
        for xy in state_data[1]:
            map_data = self.add_entity(map_data,"e",xy)
        
        for xy in state_data[2]:
            map_data = self.add_entity(map_data,"i",xy)
        
        for xy in state_data[3]:
            map_data = self.add_entity(map_data,"s",xy)        
        
        return map_data

    def xy_generator(self):
        xy = [random.randrange(self.MAP_SIZE[0]),random.randrange(self.MAP_SIZE[1])]
        
        return xy
    
    def state_data_picker(self,map_data):

        state_data = [
            self.xy_searcher("p",map_data)[0],
            self.xy_searcher("e",map_data),
            self.xy_searcher("i",map_data),
            self.xy_searcher("s",map_data)
        ]

        return state_data

    def create_new_states(self):
        """state_data_structure
        state_element = [y,x]
        state_data = [
            player_state,
            [enemy_states],
            [item_states],
            [stairs_state(only one)]
        ]
        """
        
        while (1):
            l = []
            states = [self.xy_generator() for i in range(7)]
            another = [x for x in states if x not in l and not l.append(x)]

            if  len(states) == len(another):
                break

        states = [
            states[0],
            [x for x in states if states.index(x) > 0 and states.index(x) < 4],
            [x for x in states if states.index(x) > 3 and states.index(x) < 6],
            [states[6]]
        ]

        return states
    
    def xy_searcher(self,entity,map_data):
        y = 0
        xy_list = []
        copied_map_data = copy.deepcopy(map_data)
            
        for i in copied_map_data:
        
            while(1):
                
                try:
                    xy = [i.index(entity),y]
                    i[xy[0]] = "nodata"
                    xy_list.append(xy)
                except ValueError:
                    break

            y += 1
        
        return xy_list

    def judge_state(self,state):
        if state[0] < self.MAP_SIZE[0] and state[1] < self.MAP_SIZE[1]:

            if state[0] >= 0 and state[1] >= 0:
                
                return True
        return False

class Controller(Map_Control):
    def __init__(self,map_data,state_data,MAP_SIZE):
        super().__init__(MAP_SIZE)
        self.map_data = map_data
        self.state_data = state_data

    def menu(self):

        while (1):
            
            selector = input("w:上\ns:下\na:左\nd:右\nq:セーブしてタイトルに戻る\n→")
            
            if selector in ["w","a","s","d"]:
                self.player_move(selector).enemy_move().draw(self.load(self.state_data))
                event = Event_handler()
                event.on_encount(self.state_data)
            elif selector == "q":
                self.save(self.map_data)
                input("セーブしました")

                break

            else:
                input("無効な操作")        

    def player_move(self,direction):
        while(1):
            
            while(1):

                try:
                    direction = self.change_direction(direction)
                    break
                except Exception:
                    direction = input("無効な操作です。もう一度移動可能な方向の中から選択してください。\n→")

            next_state = [self.state_data[0][0]+direction[0],self.state_data[0][1]+direction[1]]
            if self.judge_state(next_state):
                self.state_data[0] = next_state
                break
            else:
                direction = input("その方向には移動できません。もう一度移動可能な方向の中から選択してください。\n→")

        return self
        
    def enemy_move(self):
        bad_states = list(self.state_data[2]+self.state_data[3])
        new_states = []

        for xy in self.state_data[1]:

            #移動方向の候補はwasdの順に記述している
            expect_direction = [x for x in [[xy[0],xy[1]-1],[xy[0]-1,xy[1]],[xy[0],xy[1]+1],[xy[0]+1,xy[1]]] if ((x not in bad_states) and self.judge_state(x))]
            
            try:
                next_state = random.choice(expect_direction)
                bad_states.append(next_state)
                new_states.append(next_state)
            except Exception:
                new_states.append(xy)

        self.state_data[1] = new_states

        return self

    def change_direction(self,direction):

        if direction == "w":
            direction = [0,-1]
        
        elif direction == "a":
            direction = [-1,0]
        
        elif direction == "s":
            direction = [0,1]
        
        elif direction == "d":
            direction = [1,0]
        
        return direction

class Event_handler:
    def on_encount(self,state_data):
        if state_data[0] in (state_data[1]+state_data[2]+state_data[3]):
            input("何かに接触しています")

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
        
        self.MAP_SIZE = [20,10] #[x,y]
        
        self.Map = Map_Control(self.MAP_SIZE)
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
        controller = Controller(self.map_data,self.state_data,self.MAP_SIZE)
        controller.menu()

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
    game = Game()
    game.run()