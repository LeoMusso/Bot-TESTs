import os, json

class PathManager():
    # percorsi possibili dove potrebbero trovarsi i file 😅
    cartelle_finali = ["\\_bot","\\applicazione\\bot", "\\inFORMATI\\bot", "\\bot","\\_bot\\bot"]

    # variabile di errore
    error = ""
    
    # ottengo il percorso dell'applicazione
    percorso = os.getcwd()

    # percorsi dell'applicazione
    path_id_sviluppatori = f"[PERCORSO]\\conf\\impostazioni_sviluppatore.json"
    path_impostazioni_utenti = f"[PERCORSO]\\conf\\impostazioni_utenti.json"
    path_impostazioni_bot = f"[PERCORSO]\\conf\\impostazioni_bot.json"
    path_cartella_domande = f"[PERCORSO]\\domande"
    path_file_comandi = f"[PERCORSO]\\conf\\commands.json"
    path_traduzioni_genere = f"[PERCORSO]\\traduzioni_rimpiazi\\traduzioni.json"
    path_rimpiazi_parole = f"[PERCORSO]\\traduzioni_rimpiazi\\rimpiazi.json"

    
    def __init__(self):
        percorso = self.percorso
        
        percorso_cartella_domande = self.path_file_comandi.replace("[PERCORSO]", percorso)

        for cartella in self.cartelle_finali:
            try:
                
                result = self.get_json(percorso_cartella_domande)

                if(len(result) != 0):
                    self.path_cartella_domande = self.path_cartella_domande.replace("[PERCORSO]", percorso)
                    self.path_id_sviluppatori = self.path_id_sviluppatori.replace("[PERCORSO]", percorso)
                    self.path_impostazioni_bot = self.path_impostazioni_bot.replace("[PERCORSO]", percorso)
                    self.path_traduzioni_genere = self.path_traduzioni_genere.replace("[PERCORSO]", percorso)
                    self.path_rimpiazi_parole = self.path_rimpiazi_parole.replace("[PERCORSO]", percorso)
                    self.path_impostazioni_utenti = self.path_impostazioni_utenti.replace("[PERCORSO]", percorso)
                    self.path_file_comandi = percorso_cartella_domande
                    break
                else:
                    percorso = self.percorso + cartella
                    percorso_cartella_domande = self.path_file_comandi.replace("[PERCORSO]", percorso)

            except Exception as e:
                self.error = e

    def get_json(self, path):
        try:
            with open(path, 'r') as file_json:
                dictionary = json.load(file_json)
         
        except FileNotFoundError:
            dictionary = {}
    
        return dictionary
    
    def salva_json(self, nomefile, jsonContent):
        try:
            with open(nomefile, 'w') as file_json:
                json.dump(jsonContent, file_json, indent=4)
                return True
        except Exception as e:
            return False