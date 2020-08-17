import queue,copy
from EXCEPTIONS.custom_exceptions import QueueError
from CONSTANTS.global_variables import Global

class Repo():
    __song_list=queue.Queue()
    def __init__(self):
        pass
    
    def _append_to_queue(self,song):
        self.__song_list.put(song)
        print('Queue size:',self.__song_list.qsize())
    
    def _get_size_of_queue(self):
        return self.__song_list.qsize()
        
    def _get_new_song(self):
        if self.__song_list.qsize() == 0:
            raise QueueError(Global.empty_queue_message)
        return self.__song_list.get()
    
    def _get_queue(self):
        return self.__song_list