#CLIENT 0, song player
import socket,time,webbrowser,os
from CONSTANTS.global_variables import Global

class Song_Player():
    def __init__(self,utility):
        self.utility = utility
        self.MESSAGE = Global.play_next_song_message
        self.host = self.__get_ip()
        self.song_length = Global.no_song_timer
        self.start_time = None
        self.tcpPlayerClient = None
        self.data = ''
    
    def __get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        s.close()
        return IP
    
    
    def __wait(self,timer):
        start_time = time.time()
        while time.time() - start_time < timer:
            pass
        return 
    
    def __reconnect(self):
        try:
            self.tcpPlayerClient.close()
        except:
            pass
        
        self.tcpPlayerClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcpPlayerClient.settimeout(10)
        self.tcpPlayerClient.connect((self.host, Global.my_port))
    
    def __play_song(self):
        if len(self.data)==Global.song_id_length: # got a new song
            url = Global.url_prefix + self.data
            try:
                self.song_length = self.utility._get_video_length(url) - 3#delay
                #browserExe = "chrome"
                os.system("taskkill /im chrome.exe /f")
            except Exception as ex:
                print(str(ex))
                
            os.startfile(url)
        else: #no song, reset stand_by timer
            self.song_length = Global.no_song_timer
            
    
    
    #waiting before we make a request to the server for a new song
    def __stand_by(self):#    10 seconds when no song is playing,waitinng time before asking again
                         #for a song to be played
                         #    <song_length> when a song is played, waiting for a skip command
        self.start_time = time.time()
        while time.time()-self.start_time < self.song_length:
            self.data = ''
            if self.tcpPlayerClient != None:
                try:
                    self.data = self.tcpPlayerClient.recv(Global.BUFFER_SIZE).decode()
                except:
                    pass
            
                if len(self.data)==Global.song_id_length:
                    self.song_length = Global.no_song_timer
    
    def __request_new_song(self):
        if len(self.data)!=Global.song_id_length: #need to ask for a song
            self.tcpPlayerClient.send(self.MESSAGE.encode())
            self.data = self.tcpPlayerClient.recv(Global.BUFFER_SIZE).decode()
        else: #we already got a new song, send a 'recieved' message to confirm and re-establish conn
            self.__confirm_recieving()
    
    def __confirm_recieving(self):
        self.tcpPlayerClient.send(Global.success_skipping_message.encode())
    
    def _run(self):
        while True:
            self.__stand_by()
            
            self.__reconnect()
            
            self.__request_new_song()
                
            self.__play_song()
        
