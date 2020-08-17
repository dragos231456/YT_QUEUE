from CONSTANTS.global_variables import Global

class Validator():
    def _is_url_valid(self,url):
        if len(url)!=11:
            raise ValueError(Global.not_valid_url_message)