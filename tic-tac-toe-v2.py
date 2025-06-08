import copy
from typing import List,Tuple,Union


type StateType = List[List[3]]

class TicTacToeGame:
    def __init__(self):
        self.initial_state=[
            [None,None,None],
            [None,None,None],
            [None,None,None],
                        ]
        self.state = self.initial_state
        self.players = ["o","x"]
    
    def actions(self,state:StateType)->List[Tuple[int,int]]: 
        return [(row,col)  for row in range(3)  for col in range(3) if state[row][col] is None]
    
    def current_player(self,state:StateType): 
        
        flat = [ cell for row in state for cell in row if cell is not None]
        player_one = flat.count(self.players[0])
        player_two = flat.count(self.players[1])
        
        return self.players[1] if player_two<=player_one  else self.players[0]  
    
    def result(self,state:StateType,action:Tuple[int,int])->StateType:
        new_state = copy.deepcopy(state)
        player = self.current_player(state)
        row,column = action
        new_state[row][column]=player
        return new_state
    def winner(self,state:StateType):
        lines: List[List[3]] = []
        for i in range(3):
            lines.append(state[i])
            lines.append([state[0][i],state[1][i],state[2][i] ])

        lines.append([state[0][0], state[1][1], state[2][2]  ])
        lines.append([state[0][2], state[1][1], state[2][0]  ])
        
        for line in lines:
            if line[0] == line[1] and line[0] == line[2] and line[0] is not None:
                return 'x' if line[0] =='x' else 'o'
            
        return None

    def utility(self,state:StateType):  
        winner = self.winner(state)
        
        if winner=='o':
            return -1
        if winner=='x':
            return 1        
        return 0
     
    def is_terminate(self,state:StateType):
        if self.winner(state):
            return True
        cells = [cell for row in state for cell in row if cell ==None]
        return  not len(cells)
from abc import ABC,abstractmethod

class IPlayer(ABC):
    
    def __init__(self,name):
        super().__init__()
        self.name = name
    @abstractmethod
    def play()->StateType:
        pass
class TicTacToeEngine:
    
    def __init__(self,tic:TicTacToeGame,player_one:IPlayer,player_two:IPlayer ):
        self.game = tic
        self.state = self.game.state
        self.player_one = player_one
        self.player_two = player_two
    def is_terminate(self):
        return not self.game.is_terminate(self.state)
        
    def start(self):
        while self.is_terminate():
            
            self.display(self.state)
            player = self.game.current_player(self.state)
            action =None
            if player == self.player_one.name:
                action =  self.player_one.play(self.state)
            else: 
                action =    self.player_two.play(self.state)
            self.state =self.game.result(self.state,action)

    def display(self,state):
        print(f"\n")
        print("Current Game")
        print(f"\n")
        for row in state:
            print([ " " if cell ==None else cell  for cell in row  ])
        
        
class IOPlayer(IPlayer):
    def play(self,state):
        try: 
            print(f"\n")
            row,col = (int(item) for item in  input("Enter you move(a,b): ").split(","))
            return row,col
        except ValueError:
            print("Please enter valid input.")
            self.play(state)
class AIPlayer(IPlayer): 
    def __init__(self,name,game:TicTacToeGame):
        super().__init__(name)
        self.game = game
    def play(self,state):
        return self.game.actions(state)[0]
    
    
if __name__=="__main__":
    game = TicTacToeGame()
    player_one = IOPlayer("x")
    player_two = AIPlayer("o",game)
    engine =  TicTacToeEngine(game,player_one,player_two)
    engine.start()