from bs4 import BeautifulSoup
import ssl
from urllib.request import Request, urlopen
from CONSTANTS.global_variables import Global

#soup = BeautifulSoup('https://www.youtube.com/watch?v=cGW70Hc0W4M', 'html.parser')

class Network_Extractor():
    def __init__(self):   
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.filename = 'song_names.txt'
        self.song_titles = {}
        self.__read_all_from_file()
    
    
    def __read_all_from_file(self):
        with open(self.filename,'r') as file:
            lines = file.readlines()
            for line in lines:
                if line != '':
                    line = line.strip('\n')
                    key,name = line.split(':')
                    self.song_titles[key]=name
            file.close()
            
    def __write_to_file(self,id,name):
        with open(self.filename,'a') as file:
            line = id+':'+name+'\n'
            file.write(line)
            file.close()
            
    # Input from user
    def __get_name_from_url(self,id):
        try:
            url = Global.url_prefix + id
            # Making the website believe that you are accessing it using a mozilla browser
            
            req = Request(url, headers={'User-Agent': 'Chrome/79.0.3945.130'})
            webpage = urlopen(req).read()
            # Creating a BeautifulSoup object of the html page for easy extraction of data.
            
            soup = BeautifulSoup(webpage, 'html.parser')
            html = soup.prettify('utf-8')
            video_details = {}
            
            for span in soup.findAll('span',attrs={'class': 'watch-title'}):
                video_details['TITLE'] = span.text.strip()
                
            self.song_titles[id]=video_details['TITLE']
            self.__write_to_file(id,self.song_titles[id])
            
            return video_details['TITLE']
        except:
            return id
    
    def _decode_id_string(self,ids_string):
        playlist = []
        number_of_ids = len(ids_string)//Global.song_id_length
        index = 0
        for id_index in range(number_of_ids):
            id = ''
            for id_char in range(Global.song_id_length):
                id += ids_string[index]
                index += 1
            if id in self.song_titles.keys():
                playlist.append(self.song_titles[id])
            else:
                playlist.append(self.__get_name_from_url(id))
        return playlist
            
        
        
        
        
        
