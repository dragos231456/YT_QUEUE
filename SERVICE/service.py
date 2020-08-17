import queue
from CONSTANTS.global_variables import Global

class Service():
    def __init__(self,repo,validator):
        self.__validator = validator
        self.__repo=repo
    
    def _add_song_to_queue(self,url):
        song=url
        self.__validator._is_url_valid(song)
        self.__repo._append_to_queue(song)
        
    def _get_next_song(self):
        return self.__repo._get_new_song()
    
    def _return_queue_size(self):
        return self.__repo._get_size_of_queue()
    
    def _get_playlist(self):
        que = self.__repo._get_queue()
        queuesize = que.qsize()
        playlist = ''
        for i in range(queuesize):
            id = que.get()
            playlist += id
            que.put(id)
        if playlist == '':
            playlist = Global.empty_queue_message
        
        return playlist
                
        
        