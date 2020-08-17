from song_player import Song_Player
from utilities import Network_Utilities

utility = Network_Utilities()        
song_master = Song_Player(utility)
    
song_master._run() 