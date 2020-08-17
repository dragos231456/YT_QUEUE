import socket,time 
from threading import *
from EXCEPTIONS.custom_exceptions import QueueError
from CONSTANTS.global_variables import Global

class MultiThreaded_Server():
    song_master = None
    
    def __init__(self,service):
        self.__service = service
        self.TCP_IP = self.__get_ip()
        self.TCP_PORT = Global.my_port 
        self.tcpServer = None

# Multithreaded Python server : TCP Server Socket Thread Pool
    def __get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        s.close()
        print(IP)
        return IP
    
    def __create_server(self):
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.tcpServer.bind((self.TCP_IP, self.TCP_PORT)) 
        
    def _start(self):
        self.__create_server()
        while True: 
            self.tcpServer.listen() 
            (conn, (ip,self.port)) = self.tcpServer.accept() 
            newthread = self.__ClientThread(ip,self.port,conn,self.__service) 
            newthread.start() 


    class __ClientThread(Thread): 
     
        def __init__(self,ip,port,conn,service): 
            Thread.__init__(self) 
            self.__service = service
            self.__ip = ip 
            self.__port = port
            self.conn = conn
            self.MESSAGE = ''
            self.data = Global.empty_message
            self.__queue_size = 0
          
        def __wait(self,timer):
            start_time = time.time()
            while time.time() - start_time < timer:
                pass
            return  
     
        def __get_data_from_clients(self):
            try:
                self.data = self.conn.recv(Global.BUFFER_SIZE).decode()
            except: 
                self.data = Global.empty_message
                
        def __check_new_song_master(self):
            if self.data == Global.success_skipping_message:
                MultiThreaded_Server.song_master = self.conn
                return True
            
            if self.data == Global.play_next_song_message:
                    MultiThreaded_Server.song_master = self.conn
                    
        def __get_new_song(self):
            try:
                self.MESSAGE = self.__service._get_next_song()
            except QueueError as eq:
                self.MESSAGE = str(eq)    
            except Exception as ex:
                self.MESSAGE = str(ex)
     
        def __add_new_song(self):
            url = self.data
            try:
                self.__service._add_song_to_queue(url)
                self.MESSAGE = "Multithreaded Python server : "+Global.valid_url_message
            except ValueError as not_url:
                self.MESSAGE = "Multithreaded Python server : "+Global.not_valid_url_message
            except Exception as ex:
                self.MESSAGE = "Multithreaded Python server : "+str(ex)
                
        def __skip_song(self):
            try:
                skip_command,number_of_skips = self.data.split()
                number_of_skips = int(number_of_skips)
            except:
                self.MESSAGE = Global.invalid_command_message
                return
            
            self.__queue_size = self.__service._return_queue_size()
            
            if number_of_skips <= self.__queue_size:
                while number_of_skips != 0:
                    self.MESSAGE = self.__service._get_next_song()
                    number_of_skips -= 1
            else:
                self.MESSAGE = Global.small_queue_size_message
                
            if len(self.MESSAGE) == Global.song_id_length:
                MultiThreaded_Server.song_master.send(self.MESSAGE.encode())
                self.MESSAGE = Global.next_song_confirmation_message
                self.__wait(1.5)
            
        def __feedback(self):
            if self.data != Global.empty_message:
                
                if type(self.conn) == type(MultiThreaded_Server.song_master):
                    if self.conn != MultiThreaded_Server.song_master:
                        self.MESSAGE += Global.feedback_binding_char + self.__service._get_playlist()
                else:
                    self.MESSAGE += Global.feedback_binding_char + self.__service._get_playlist()
                    
                self.conn.send(self.MESSAGE.encode())
     
        def run(self):
            self.__get_data_from_clients()
                
            if self.data == Global.play_next_song_message:
                print (str(self.__port),'sent:', Global.play_next_song_message_print)
            else:
                print (str(self.__port),'sent:', self.data)
            
            if self.__check_new_song_master() == True:
                return
            
            if self.data[:4] == Global.skip_n_command:
                self.__skip_song()
                
            elif self.data == Global.play_next_song_message:
                self.__get_new_song()
            else:
                self.__add_new_song()
            
            self.__feedback()
            
            print('MESSAGE SENT BY SERVER:',self.MESSAGE)
# Multithreaded Python server : TCP Server Socket Program Stub  






