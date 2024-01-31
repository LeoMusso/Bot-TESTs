from threading import Thread
from path_manager import PathManager
from set_up import Sistema
import signal, subprocess
 
class ThreadUpdateBot():
    path = PathManager()
    sys = Sistema()
    
    def __init__(self, user_id, update):
        self.id_user = user_id
        self.update = update

    def autorizza_bot(self):
        json_id_sviluppatori = self.sys.get_json(self.path_id_sviluppatori)