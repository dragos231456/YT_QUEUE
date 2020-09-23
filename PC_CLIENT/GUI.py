import socket,time,copy,tkinter
from CONSTANTS.global_variables import Global
from tkinter import *
#from PIL import Image

class GUI_Client():
    def __init__(self,extractor):
        self.__extractor = extractor
        self.host = self.__get_ip()
        self.tcpClient = None
        self.MESSAGE = ''
        self.playlist = []
        self.song_entry = 'plm'

    def __get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        s.close()
        return IP
    
    def __connect(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcpClient.connect((self.host, Global.my_port))
    
    def __disconnect(self):
        self.tcpClient.close() 
        
    def __send_new_song(self):
        self.tcpClient.send(self.MESSAGE.encode())
        
    def __feedback(self):
        data = self.tcpClient.recv(Global.BUFFER_SIZE).decode()
        confirmation,ids = data.split(Global.feedback_binding_char)
        print(ids)
        print (" Client1 received data:", confirmation)
        self.playlist = self.__extractor._decode_id_string(ids)
        print(self.playlist)
    
    def __interact_with_server(self):
        self.__connect()
        self.__send_new_song()
        self.__feedback()
        self.__disconnect()
        self.master.destroy()
        
        self._run()
    
    def __send_link(self):
        self.MESSAGE = self.song_entry.get()
        self.MESSAGE = self.MESSAGE.replace(Global.url_prefix,'')
        self.MESSAGE  = self.MESSAGE.replace(Global.phone_prefix,'')
        if len(self.MESSAGE) > 11:
            self.MESSAGE = self.MESSAGE[:11]
        self.__interact_with_server()
        
    def __refresh(self):
        self.MESSAGE = 'refresh'
        self.__interact_with_server()
        
    def __skip_n(self,event):
        item_from_list = self.playlist_listbox.curselection()
        self.MESSAGE = 'skip '+str(item_from_list[0]+1)
        
        print(self.MESSAGE)
        self.__interact_with_server()
        
    def _run(self):
        self.master = Tk()
        
        self.playlist_listbox = Listbox(self.master,width = 40,height = 20,font = 60)
        
        index = 0
        for song in self.playlist:
            index += 1
            print(song)
            self.playlist_listbox.insert(index,song)
        self.playlist_listbox.bind("<Double-Button-1>",self.__skip_n)
        
        
        canvas = Canvas(self.master, width = 340, height = 250)      
        canvas.grid(row = 0,column = 0)      
        img = PhotoImage(file="new-youtube-logo.pgm").subsample(2, 2)      
        canvas.create_image(20,20, anchor=NW, image=img) 
        
        
        search_frame = Frame(self.master)
        Label(search_frame,text='Song:',font = 80).grid(row = 0,column = 0,sticky = W)
        
        self.song_entry = Entry(search_frame,width = 50,font = 80)
        self.song_entry.grid(row = 0, column = 1,sticky = W)
        
        button_frame = Frame(search_frame)
        
        add_button = Button(button_frame, text='Add', command=lambda:self.__send_link()).grid(row=1, column=1, sticky=W, pady=4)
        refresh_button = Button(button_frame,text = 'Refresh',command = lambda:self.__refresh()).grid(row = 1,column = 3,sticky = W,pady = 4)
        
        button_frame.grid(row = 1,column = 1,sticky = W)
        
        search_frame.grid(row = 1,column = 0)
        self.playlist_listbox.grid(row = 0, column = 2,rowspan =200)
        
        self.master.mainloop()


