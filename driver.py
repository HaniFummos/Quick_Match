import Quick_Match
import menu
import joinLobby
import gameState
import join
import create
import lobby
import YouAreRed
import YouAreBlue

class Driver:
    def __init__(self):
        self.gameStateRun = True

        self.stateManager = gameState.State('start') # initial state
      
        self.quickMatch = Quick_Match.Game(self.stateManager)
        self.menu = menu.Menu(self.stateManager)
        self.joinLobby = joinLobby.Menu(self.stateManager)
        self.lobby = lobby.Menu(self.stateManager)
        self.join = join.Menu(self.stateManager)
        self.create = create.Menu(self.stateManager)
        self.YouAreRed = YouAreRed.Game(self.stateManager)
        self.YouAreBlue = YouAreBlue.Game(self.stateManager)



        self.scenes = {
            'start': self.menu, 
            'quickMatch': self.quickMatch,
            'joinLobby': self.joinLobby,
            'lobby' : self.lobby,
            'join' : self.join,
            'create' : self.create,
            'YouAreRed' : self.YouAreRed,
            'YouAreBlue' : self.YouAreBlue
        }
        
    def run(self):
        while self.gameStateRun:
            if self.stateManager.getState() == 'join' or self.stateManager.getState() == 'create' or 'You' in self.stateManager.getState():
                self.scenes[self.stateManager.getState()].run(self.stateManager.ip, self.stateManager.port)    
            else:
                self.scenes[self.stateManager.getState()].run()          

if __name__ == "__main__":
    game = Driver()
    game.run()
