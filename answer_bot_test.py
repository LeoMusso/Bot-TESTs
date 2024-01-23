import spacy, json, os
from set_up import Sistema
from path_manager import PathManager


class InformatiBOT():

    ### DOWNLOAD MODELLO DI APPRENDIMENTO
    spacy.cli.download("it_core_news_sm")
    nlp = spacy.load("it_core_news_sm")

    caratteri_da_rimuovere = ["=", "?", "!", "^"]
    
    domande_risposte = {}

    def rimuovi_duplicate_vicine(self, stringa):
        nuova_stringa = ''
        
        for i in range(len(stringa)):
            # Aggiungi la lettera corrente solo se è diversa dalla precedente
            if i == 0 or (stringa[i] != stringa[i - 1] or stringa[i] not in ["a", "e", "i", "o", "u"]):
                nuova_stringa += stringa[i]
        
        return nuova_stringa

    def Welcome(self, message):
        user = message.from_user
        sys = Sistema()
        
        if user.username:
            response = f"Ciao, @{user.username}! Sono [NOME_ROBOT], il bot ufficiale di inFORMATI! 😎\nSono qui per soddisfare tutte le tue richieste, quindi se hai domande chiedi pure!!"
        else:
            response = f"Ciao, {user.first_name}! Sono [NOME_ROBOT], il bot ufficiale di inFORMATI!\nSono qui per soddisfare tutte le tue richieste, quindi se hai domande chiedi pure!!"
        try:
            response = response.replace("[NOME_ROBOT]", sys.json_utenti[str(message.from_user.id)][0]["bot"])
        except Exception as e:
            response = response.replace("[NOME_ROBOT]", "Astro")
        return response
    
    def Fumagazzi(self):
        response = '''
            Hey, sai che i miei creatori prima di me hanno creato un sito di orologi molto carini?\nVai a dare un\'occhiata a [questo link](https://jackiso2006.github.io/Fumagazzers/)! 👀'''
        return response
    
    def set_name_bot(self, message):
        sys = Sistema()
        path_manager = PathManager()
        
        if(message.text == "/setastro"):
            sys.json_utenti[str(message.from_user.id)][0]["bot"] = "Astro"
        else:
            sys.json_utenti[str(message.from_user.id)][0]["bot"] = "Nebula"
        
        try:
            if path_manager.salva_json(path_manager.path_impostazioni_utenti, sys.json_utenti):
                response = f'''
                    D'ora in poi potrai chiamarmi {sys.json_utenti[str(message.from_user.id)][0]["bot"]}!\nChiedi pure quello che vuoi!😊'''
            else:
                response = f'''
                    Qualcosa è andato storto😕\nRiprova più tardi👀'''
        except Exception as e:
            response = f'''
                Qualcosa è andato storto😕\nRiprova più tardi👀'''
        return response
    
    def SignUp(self, user, user_id):
        return f"Ciao @{user}, completa la registrazione [cliccando qui](https://informiamoci.netsons.org/signup.php?id_telegram={user_id})"
        
    def cerca_risposta(self, message):
        path_manager = PathManager()
        sys = Sistema()
        
        testo_modificato = str(message.text.lower())
        
        testo_modificato = self.rimuovi_duplicate_vicine(testo_modificato)
        try:
            for carattere in self.caratteri_da_rimuovere:
                testo_modificato = testo_modificato.replace(carattere, '')

            message.text = testo_modificato
            for root, directories, files in os.walk(path_manager.path_cartella_domande):
                for filename in files:
                    #if '_noexe' not in filename and 'commands' not in filename:
                        with open(os.path.join(path_manager.path_cartella_domande, filename), 'r', encoding='utf-8') as file:
                            self.domande_risposte.update(json.load(file))
        
        except UnicodeDecodeError as e:
            print(f"Errore durante la decodifica del carattere: {e}")

        doc_domanda = self.nlp(message.text)
        migliore_corrispondenza = ["", 404]
        punteggio_migliore = 0.0

        for domanda_confronto, risposta in self.domande_risposte.items():
            doc_domanda_confronto = self.nlp(domanda_confronto)
            similarita = doc_domanda.similarity(doc_domanda_confronto)

            if similarita > punteggio_migliore and similarita > 0.56:
                
                if "ID-TELEGRAM" in risposta:
                    risposta = risposta.replace("ID-TELEGRAM", str(message.from_user.id))

                punteggio_migliore = similarita
                migliore_corrispondenza = [risposta, 200]

                if migliore_corrispondenza[0] == "Welcome":
                    return [self.Welcome(message), 200]
               
            migliore_corrispondenza = [migliore_corrispondenza[0].replace("[NOME_ROBOT]", sys.json_utenti[str(message.from_user.id)][0]["bot"]), 200]

        return migliore_corrispondenza
    
    def Response(self, value, message = ""):
        if value == 0:
            return self.Welcome(message)
        elif value == 1:
            return self.Fumagazzi()
        else:
            return self.cerca_risposta(message)
            