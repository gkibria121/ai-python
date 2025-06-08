from typing import List, Tuple, Optional
import copy

StateType = List[List[Optional[str]]]
ActionType = Tuple[int, int]

class TicTacToe:
    def __init__(self, players=["o", "x"], factor=3):
        self.players = players
        self.initial_state: StateType = [[None for _ in range(factor)] for _ in range(factor)]
 
 
    def actions(self, state: StateType) -> List[ActionType]:
        return [(i, j) for i in range(3) for j in range(3) if state[i][j] is None]

    def result(self, state: StateType, action: ActionType) -> StateType:
        i, j = action
        if state[i][j] is not None:
            raise ValueError("Cannot mark this position")

        new_state = copy.deepcopy(state)
        new_state[i][j] = self.current_player(state)
        return new_state

    def mark(self, state: StateType, i: int, j: int) -> StateType:
        return self.result(state, (i, j))

    def current_player(self, state: StateType) -> str:
        flat = [cell for row in state for cell in row]
        o_count = flat.count(self.players[0])
        x_count = flat.count(self.players[1])
        return self.players[1] if x_count <= o_count else self.players[0]

    def is_terminal(self, state: StateType) -> bool:
        return self.winner(state) is not None or all(cell is not None for row in state for cell in row)

    def winner(self, state: StateType) -> Optional[str]:
        lines = []

        # Rows and columns
        for i in range(3):
            lines.append(state[i])  # row
            lines.append([state[0][i], state[1][i], state[2][i]])  # column

        # Diagonals
        lines.append([state[0][0], state[1][1], state[2][2]])
        lines.append([state[0][2], state[1][1], state[2][0]])

        for line in lines:
            if line[0] is not None and all(cell == line[0] for cell in line):
                return line[0]

        return None

    def utility(self, state: StateType) -> int:
        win = self.winner(state)
        if win == self.players[0]:
            return -1
        elif win == self.players[1]:
            return 1
        return 0

    def display(self, state: StateType):
        for row in state:
            print([" " if cell is None else cell for cell in row])
        print()

class TicTacToeAI:
    
    def __init__(self,tic_tac_toe:TicTacToe):
        self.tic_tac_toe = tic_tac_toe

    def get_action(self,state:StateType):
        
        actions = self.tic_tac_toe.actions(state)  
       
        best_action = None
        player = self.tic_tac_toe.current_player(state)
        best_value = -float('inf') if player=='x' else float('inf')
        for action in actions:
            new_state = self.tic_tac_toe.result(copy.deepcopy(state), action)
            value = self.minMax(new_state)
            if player =='x':
                 
                if value>  best_value:
                    best_value= value
                    best_action = action
            else:
                 
                if value<  best_value:
                    best_value= value
                    best_action = action
        
        return best_action
    
    def minMax(self,state:StateType)->int:
        
        if self.tic_tac_toe.is_terminal(state):
            return self.tic_tac_toe.utility(state)
        
        actions = self.tic_tac_toe.actions(state)
        player = self.tic_tac_toe.current_player(state)
        best_value = -float('inf') if player=='x' else float('inf')
        
        for action in actions:
            
            new_state = self.tic_tac_toe.result(state,action)
            value = self.minMax(new_state) 
            
            
            if player =='x':
                 
                if value> best_value:
                    best_value = value
            else:
                 
                if value< best_value:
                    best_value = value
            
        
        return best_value
    
    
        
    

class TicTacToeEngine:
    def __init__(self, game: TicTacToe,ai_player:TicTacToeAI):
        self.game = game
        self.ai_player= ai_player

    def play(self):
        state = self.game.initial_state

        while not self.game.is_terminal(state):
            self.game.display(state)
            current = self.game.current_player(state)
            print(f"Current Player: {current}")

            if current == "x":
                try:
                    move_input = input("Enter your move (row,col): ")
                    i, j = map(int, move_input.strip().split(","))
                    state = self.game.mark(state, i, j)
                except Exception as e:
                    print(f"Invalid move: {e}")
            else:
                # Let 'o' (AI or placeholder) make the first available move
                action = self.ai_player.get_action(state)
                print(f"AI ({current}) moves at: {action}")
                state = self.game.result(state, action)

        # Game over
        self.game.display(state)
        result = self.game.utility(state)
        if result == -1:
            print("O won!")
        elif result == 1:
            print("X won!")
        else:
            print("Match draw!")


if __name__ == "__main__":
    game = TicTacToe()
    ai_player = TicTacToeAI(game)
    engine = TicTacToeEngine(game,ai_player)
    
    engine.play()
