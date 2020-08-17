import json
import urllib.request
from CONSTANTS.global_variables import Global

class Network_Utilities():

    def __get_video_id(self,url):
        url=url.replace('https://www.youtube.com/watch?v=','') #the root structure is eleiminated
        return url
    
    def __get_duration_in_seconds(self,duration): #PT<mins>M<sec>S is the format of the get_video_length function
        t=0
        seconds=0
        for char in duration:
            if char=='P' or char=='T':
                pass
            elif char=='M':
                minutes=t
                t=0
            elif char=='S':
                seconds=t
            else:
                t=t*10+int(char)
        return minutes*60+seconds
                
    
    def _get_video_length(self,url):
        try:
        #video_id="XCVAgd4G3qY" model
            video_id=self.__get_video_id(url)
            api_key="AIzaSyC0G-ZtQWEGDPSN0ckOnzmKXnm3tM1Lffo"
            searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails"
            response = urllib.request.urlopen(searchUrl).read()
            data = json.loads(response)
            all_data=data['items']
            contentDetails=all_data[0]['contentDetails']
            duration=contentDetails['duration']
            duration=self.__get_duration_in_seconds(duration)
            return duration
        except:
            raise Exception(Global.not_valid_url_message)