# Python TCP Client A
import socket
import time
from CONSTANTS.global_variables import Global

class Basic_Client():
    def __init__(self):
        self.host = input('IP:')
        self.tcpClient = None
        self.MESSAGE = ''
        
    def __wait(self,timer):
        start_time = time.time()
        while time.time() - start_time < timer:
            pass
        return 

    def __connect(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcpClient.connect((self.host, Global.my_port))
        
    def __disconnect(self):
        self.tcpClient.close() 
        
    def __send_new_song(self):
        self.tcpClient.send(self.MESSAGE.encode())
        
    def __feedback(self):
        data = self.tcpClient.recv(Global.BUFFER_SIZE).decode()
        print (" Client1 received data:", data)
        
    def __get_new_song(self):
        self.MESSAGE = input("tcpClientA: Enter message/ Enter exit:")
        self.MESSAGE = self.MESSAGE.replace('https://www.youtube.com/watch?v=','')
        return self.MESSAGE

    def _run(self):
        while True:
            self.__wait(3) #dont overload the pipe
            
            self.__connect()
            if self.__get_new_song() == 'exit':
                return
            
            self.__send_new_song()
            self.__feedback()
            self.__disconnect()
        
client = Basic_Client()
client._run()