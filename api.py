import requests, threading
from path_manager import PathManager

class UrlEndpoint():
    # url di base
    base_url = "https://informiamoci.netsons.org"

    # endpoint bot
    set_notify_endpoint  = "/api/set_notify.php"
    delete_account_endpoint = "/api/delete_account.php"
    get_events_endpoint = "/api/get_events.php"
    get_user_online_endpoint = "/api/get_user_online.php"
    signup_users_endpoint = "/api/signup_users.php"

    # endpoint thread per ottenere i documenti
    set_user_online_endpoint = "/api/set_user_online.php"
    get_domande_aggiornate_endpoint = "/api/get_domande.php"
    get_traduzioni_aggiornate_endpoint = "/api/traduzioni.php"
    get_utenti_registrati_endpoint = "/api/get_users_signed.php"

    # endpoint per info sugli eventi
    get_utenti_totali_evento_endpoint = "/api/get_total_subscribers_event.php"

class InformatiAPI():
    
    api = UrlEndpoint()

    def set_notify(self, id_telegram, notify):
        # costruisco l'URL dell'api
        api_url = self.api.base_url + self.api.set_notify_endpoint
        
        # inserisco i parametri
        params = {"id_telegram":str(id_telegram), "notify":notify.upper()}

        response = requests.get(api_url, params)

        return response

    def get_user_online(self, id_telegram):
        
        # costruisco l'URL dell'api
        api_url = self.api.base_url + self.api.get_user_online_endpoint

        params = {"id_telegram":str(id_telegram)}

        response = requests.get(api_url, params)

        return response
    
    def set_user_online(self, id_telegram):
        
        path_manager = PathManager()
        
        json_utenti = path_manager.get_json(path_manager.path_impostazioni_utenti)

        # costruisco l'URL dell'api
        api_url = self.api.base_url + self.api.get_user_online_endpoint

        params = {"users":json_utenti}

        response = requests.post(api_url, params)

        return response

    def download_json(self, endpiont, id_telegram):
        
        url_api = self.api.base_url + endpiont

        params = {
            "id_telegram":id_telegram,
            "download": "TRUE"
        }

        response = requests.post(url_api, params)

        if response.status_code == 200:
    # La risposta è in formato JSON, puoi accedere ai dati come dizionario Python
            json_response = response.json()
            return json_response
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return response.text

    def get_count_user(self, id_telegram):

        url_api = self.api.base_url + self.api.get_utenti_totali_evento_endpoint

        params = {
            "id_telegram":id_telegram
        }

        response = requests.post(url_api, params)

        if response.status_code != 200:
            return "error"
class ThreaDownloadJson(threading.Thread):

    def __init__(self, api, endpoint):
        self.api = api
        self.endpoint = endpoint

    def run(self, id_telegram):
        response = self.api.download_json(self.endpoint, id_telegram)
    

