import os, json
from path_manager import PathManager
from set_up import Sistema

class ErrorBot():  

    def Error(self, message, errore):

        user = message.from_user

        if user.username:
            user = f"@{user.username}"
        else:
            user = user.first_name

        return f"<*ERRORE*>  il bot ha generato un errore alla domanda: [{message.text}] da user: [{user}]\nERRORE: [{errore}]"
    
    def no_answ(self, message):

        user = message.from_user

        if user.username:
            user = f"@{user.username}"
        else:
            user = user.first_name

        response = f"<*SENZA RISPOSTA*>  il bot non sapeva rispondere alla domanda: [{message.text}] da user: [{user}]"

        return response
    
    def no_commands(self):
        response = '''
            Hey, non ho capito cosa volevi chiedermi... 😕, oppure non posso darti la risposta a questa domanda!🤭 Se hai bisogno di qualsiasi altra cosa chiedi pure, altrimenti usa i comandi nel menu! ✌️'''
        return response
    
    def beta_on(self):
        response = '''
            Hey, da questo momento la beta è attiva!✌️'''
        return response
    
    def beta_off(self):
        response = '''
            Hey, da questo momento il bot è accessibile a tutti!✌️'''
        return response
    
    def not_implemented(self):
        response = '''
            Hey, questa parte è ancora in fase di sviluppo... 😕, se hai bisogno di qualsiasi cosa chiedi pure, altrimenti usa i comandi nel menu! ✌️'''
        return response
    
    def signup_closed(self):
        response = '''
            Hey, purtroppo il bot non è in grado di iscriverti al momento.😕\nTi aggiorneremo non appena sarà possibile!🤗 \n\n\n\r_Team Fumagazzers_! ✌️'''
        return response

    def closed(self):
        response = '''
            Hey, purtroppo il bot non è in grado di risponderti.😕\nTi aggiorneremo non appena tornerà online \n\n\n\r_Team Fumagazzers_! ✌️'''
        return response
    
    def not_authorized(self):
        response = '''
            Hey, mi dispiace ma non sei autorizzato ad usare questo bot!😕\nPer provare ad iscriverti alla beta puoi inviare il comando /vogliopartecipare, altrimenti dovrai aspettare l'uscita del bot per tutti!😉  \n\n\n\t_Team Fumagazzers_! ✌️'''
        return response
    
    def no_tester(self):
        response = '''
            Hey, Mi dispiace ma la beta è già al completo.😣\nCi vedremo non appena uscirà per tutti!!🤗 \n\n\r_Team Fumagazzers_! ✌️'''
        return response
    
    def signup_opened(self):
        response = '''
            Hey, ora è possibile iscriversi!🤩\nScusa l'assenza ma hanno dovuto fare dei lavoretti di manutezione, ma ora sono più forte che mai, mandami il comando /signup e il gioco sarà fatto!😎\n\n\r il _Team Fumagazzers_ si scusa per l'attesa! ✌️'''
        return response

    def opened(self):
        response = '''
            Hey, Sono tornato online!🤩\nScusa l'assenza ma hanno dovuto fare dei lavoretti di manutezione, ma ora sono più forte che mai!😎\n\n\r il _Team Fumagazzers_ si scusa per l'attesa! ✌️'''
        return response
    
    def che_fol(self, message):
        if message.from_user.username:
            user = f'@{message.from_user.username}'
        else:
            user = message.from_user.first_name
            if message.from_user.last_name:
                user += f" {message.from_user.last_name}"
        
        response = f'''
            Hey, ma lo sai che il simpaticone di {user} ha tentato di modificare il bot con il comando {message.text}!! Ci sta, provare non costa nulla🤣'''
        return response

    def sendErrors(self, main_bot, error_bot, e, message, function = "error", error_just_sended = False):
        
        sys = Sistema()
        path_manager = PathManager()
        
        ids_sviluppatori = sys.getIdsSviluppatori()
        ids_moderatori = sys.getIdsModeratori()

        if not error_just_sended:
            main_bot.send_message(message.chat.id, self.no_commands(), parse_mode='markdown')

        if function == 'error':
            for id, value in ids_sviluppatori.items():
                if value != "000000":
                    error_bot.send_message(value, self.Error(message, e), parse_mode='markdown')
        elif function == 'no_error':
            json_domande = path_manager.get_json(path_manager.path_file_domande_no_risposta)
            json_domande[len(json_domande) + 1] = message
            if(path_manager.salva_json(path_manager.path_file_domande_no_risposta, json_domande)):
                for id, value in ids_moderatori.items():
                    if value != "000000":
                        error_bot.send_message(value, self.no_answ(message), parse_mode='markdown')
        elif function == 'block_on':
            for id, value in ids_moderatori.items():
                if value != "000000":
                    error_bot.send_message(value, self.closed(), parse_mode='markdown')
        elif function == 'error_command':
            for id, value in ids_moderatori.items():
                if value != "000000":
                    error_bot.send_message(value, f"L'utente {e} ha selezionato il comando {message.text} non ancora implementato", parse_mode='markdown')
        elif function == "not_authorized":
            error_bot.send_message(message.chat.id, self.not_authorized(), parse_mode='markdown')
        elif function == "che_fol":
            error_bot.send_message(message.chat.id, e, parse_mode='Markdown')
            for id, value in ids_moderatori.items():
                if value != "000000":
                    error_bot.send_message(value, self.che_fol(message), parse_mode='markdown')
        elif function == 'tester':
            for id, value in ids_moderatori.items():
                if value != "000000":
                    error_bot.send_message(value, e, parse_mode='markdown')
        elif function == 'saving':
            for id, value in ids_moderatori.items():
                if value != "000000":
                    error_bot.send_message(value, e, parse_mode='markdown')
        else:
            for id, value in ids_sviluppatori.items():
                if value != "000000":
                    error_bot.send_message(value, "il Bot di inFORMATI si sta avviando", parse_mode='markdown')