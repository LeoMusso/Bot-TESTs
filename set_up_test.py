from path_manager_test import PathManager
from dotenv import load_dotenv
import os, json, threading
from api import InformatiAPI
from datetime import datetime

load_dotenv()

class TimerThread():
    def __init__(self, interval, bot_errori):
        super().__init__()
        self.interval = interval
        self.sys = Sistema()
        self.api = self.sys.api_url
        self.bot_errori = bot_errori
        self.stopped = threading.Event()

    def run(self):
        while not self.stopped.wait(self.interval):
            self.invia_richiesta_api()

    def stop(self):
        self.stopped.set()

    def invia_richiesta_api(self):
        response_web = self.api.set_user_online()

        if response_web.status_code != 200:
            self.stop()


class Sistema():
    json_impostazioni = {}
    json_utenti = {}
    json_traduzioni = {}
    json_comandi = {}
    json_domande = {}
    ids = {}

    token_bot_principale = ""
    token_bot_errori = ""
    token_bot_test = ""

    def __init__(self):
        
        path_manager = PathManager()
        
        # estraggo le impostazioni
        self.json_impostazioni = path_manager.get_json(path_manager.path_impostazioni_bot)
        
        self.token_bot_principale = os.environ.get("TOKEN_BOT_INFORMATI")
        self.token_bot_errori = os.environ.get("TOKEN_BOT_ERRORI")
        self.token_bot_test = os.environ.get("TOKEN_BOT_TEST")

        # estraggo le traduzioni
        self.json_traduzioni = path_manager.get_json(path_manager.path_traduzioni_genere)

        # ottengo gli id
        self.ids = path_manager.get_json(path_manager.path_id_sviluppatori)
        self.ids_moderatori = self.getIdsModeratori()

        # estraggo gli utenti
        self.json_utenti = path_manager.get_json(path_manager.path_impostazioni_utenti)

        # estraggo i comandi del bot
        self.json_comandi = path_manager.get_json(path_manager.path_file_comandi)

        # estraggo i comandi del bot
        self.json_comandi = path_manager.get_json(path_manager.path_file_comandi)

        self.api = InformatiAPI()

    def getIdsSviluppatori(self):
        return self.ids["ids_sviluppatori"]
    
    def getIdsModeratori(self):
        return self.ids["ids_moderatori"]
    
    def getIdsTester(self):
        return self.ids["ids_tester"]
    
    def crea_aggiorna_user(self, chiave, valore, notify = ""):
        try:
            path_manager = PathManager()

            if str(chiave) not in self.json_utenti:
                if notify != "":
                    self.json_utenti[chiave] = [
                        {
                            "user": valore,
                            "notifiche": notify,
                            "sesso": "maschile",
                            "status": "online",
                            "ultimo_messaggio": "",
                            "bot": "Astro",
                            "operazioni":
                                        {
                                            "True":
                                            {
                                                "OPERAZIONE" :"attivato",
                                                "INVERSA":"disattivarle",
                                                "COMANDO": "/setnotifyoff"
                                            },
                                            "False":
                                            {
                                                "OPERAZIONE" :"disattivato",
                                                "INVERSA":"attivarle",
                                                "COMANDO": "/setnotifyon"
                                            }
                                        }
                        }
                    ]
                else:
                    self.json_utenti[chiave] = [
                        {
                            "user": valore,
                            "notifiche": "True",
                            "sesso": "maschile",
                            "status": "online",
                            "ultimo_messaggio": "",
                            "bot": "Astro",
                            "operazioni":
                                        {
                                            "True":
                                            {
                                                "OPERAZIONE" :"attivato",
                                                "INVERSA":"disattivarle",
                                                "COMANDO": "/setnotifyoff"
                                            },
                                            "False":
                                            {
                                                "OPERAZIONE" :"disattivato",
                                                "INVERSA":"attivarle",
                                                "COMANDO": "/setnotifyon"
                                            }
                                        }
            
                        }
                    ]
            elif notify != "":
                for indice, (key, value)  in enumerate(self.json_utenti.items()):
                    self.json_utenti[str(chiave)] = [
                            {
                                "user": valore,
                                "notifiche": notify,
                                "sesso": self.json_utenti[str(chiave)][0]["sesso"],
                                "status": self.json_utenti[str(chiave)][0]["status"],
                                "ultimo_messaggio": self.json_utenti[str(chiave)][0]["ultimo_messaggio"],
                                "bot": self.json_utenti[str(chiave)][0]["bot"],
                                "operazioni":
                                            {
                                                "True":
                                                {
                                                    "OPERAZIONE" :"attivato",
                                                    "INVERSA":"disattivarle",
                                                    "COMANDO": "/setnotifyoff"
                                                },
                                                "False":
                                                {
                                                    "OPERAZIONE" :"disattivato",
                                                    "INVERSA":"attivarle",
                                                    "COMANDO": "/setnotifyon"
                                                }
                                            }
                            }
                        ] 
            else:   
                # Salvataggio del dizionario aggiornato su un file JSON
                with open(self.path_manager.path_impostazioni_utenti, 'w') as file_json:
                    json.dump(self.json_utenti, file_json, indent=4)
                self.json_utenti = path_manager.get_json(path_manager.path_impostazioni_utenti)
                return False

            # Salvataggio del dizionario aggiornato su un file JSON
            with open(path_manager.path_impostazioni_utenti, 'w') as file_json:
                json.dump(self.json_utenti, file_json, indent=4)
            self.json_utenti = path_manager.get_json(path_manager.path_impostazioni_utenti)
            return True
        except FileNotFoundError:
            print(f"Il file {path_manager.path_impostazioni_utenti} non esiste.")
            return False
    
    def set_last_message_user(self, message):
        
        data = str(datetime.now())
        
        path_manager = PathManager()
         
        self.json_utenti = path_manager.get_json(path_manager.path_impostazioni_utenti)

        self.json_utenti[str(message.from_user.id)][0]["ultimo_messaggio"] = data

        path_manager.salva_json(path_manager.path_impostazioni_utenti, self.json_utenti)
