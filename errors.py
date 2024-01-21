import telebot, json
from set_up import Sistema, TimerThread
from error_bot import ErrorBot
from path_manager import PathManager
from api import InformatiAPI, UrlEndpoint, ThreaDownloadJson

sys = Sistema()

errBot = ErrorBot()
main_bot = telebot.TeleBot(sys.token_bot_principale, parse_mode=None)
error_bot = telebot.TeleBot(sys.token_bot_errori, parse_mode=None)

@error_bot.message_handler(commands=["setblockon", "setblockoff", "getstatusblock"] , func=lambda message: message.from_user.id in sys.ids_moderatori.values())
def set_block_bot(message):
    sys = Sistema()
    
    path_manager = PathManager()

    block = 'on'
    response = 'Hai attivato il blocco su informati.\nPer il momento il bot non risponderà più agli utenti!\nPer disattvarlo inviare il comando /setblockoff.'
    
    if message.text != "/setblockoff" and message.text != "/setblockon":
            # TODO: Ottenere lo stato delle modifiche
            
            if sys.json_impostazioni["block"] == 'on':
                response = "Il blocco è attivo!\nNessun utente può chattare con il bot fino a che esso sarà acceso!\nRimuovilo con /setblockoff"
            else:
                response = "Il blocco non è attivo!\nTutti gli utenti possono chattare con il bot fino a che esso sarà spento!\nAttivalo con /setblockon"
            
            error_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    if message.text == '/setblockoff':
        block = 'off'
        response = 'Hai disattivato il blocco su informati.\nPer il momento il bot risponderà agli utenti!\nPer attvarlo inviare il comando /setblockon.'

    if sys.json_impostazioni["block"] != block:
        sys.json_impostazioni["block"] = block
        try:
            if path_manager.salva_json(path_manager.path_impostazioni_bot, sys.json_impostazioni):
                if block == 'on':
                    for user in sys.json_utenti:
                        main_bot.send_message(int(user), errBot.closed(), parse_mode='Markdown')
                else:
                    for user in sys.json_utenti:
                        main_bot.send_message(int(user), errBot.opened(), parse_mode='Markdown')
                error_bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            error_bot.send_message(message.chat.id, f"< *ERRORE* > C'è stato un problema nel salvataggio del file\n*ERRORE*: {e}", parse_mode='Markdown')
    else:
        if sys.json_impostazioni["block"] == 'off':
            error_bot.send_message(message.chat.id, "Il bot è già online!", parse_mode='Markdown')
        else:
           error_bot.send_message(message.chat.id, "Il bot è già offline!", parse_mode='Markdown')

@error_bot.message_handler(commands=["setsignupon", "setsignupoff"] , func=lambda message: message.from_user.id in sys.ids_moderatori.values())
def set_signup_block_bot(message):
    sys = Sistema()
    
    path_manager = PathManager()

    block = 'on'
    response = 'Hai attivato il blocco della registrazione su informati.\nPer il momento il bot non iscriverà più gli utenti!\nPer disattvarlo inviare il comando /setsignupoff.'
    
    if message.text != "/setsignupoff" and message.text != "/setsignupon":
        # TODO: Ottenere lo stato delle modifiche
        
        if sys.json_impostazioni["block"] == 'on':
            response = "Il blocco è attivo!\nNessun utente può chattare con il bot fino a che esso sarà acceso!\nRimuovilo con /setblockoff"
        else:
            response = "Il blocco non è attivo!\nTutti gli utenti possono chattare con il bot fino a che esso sarà spento!\nAttivalo con /setblockon"
        
        error_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    if message.text == '/setsignupoff':
        block = 'off'
        response = 'Hai disattivato il blocco su informati.\nPer il momento il bot iscriverà gli utenti!\nPer attivarlo inviare il comando /setsignupon.'

    if sys.json_impostazioni["block_signup"] != block:
        sys.json_impostazioni["block_signup"] = block
        try:
            if sys.json_impostazioni["block"] == 'off':
                if path_manager.salva_json(path_manager.path_impostazioni_bot, sys.json_impostazioni):
                    if block == 'on':
                        for user in sys.json_utenti:
                            main_bot.send_message(int(user), errBot.signup_closed(), parse_mode='Markdown')
                    else:
                        for user in sys.json_utenti:
                            main_bot.send_message(int(user), errBot.signup_opened(), parse_mode='Markdown')
                    error_bot.send_message(message.chat.id, response, parse_mode='Markdown')
            else:
                error_bot.send_message(message.chat.id, f"Il blocco è attivo, per (dis)attivare il sistema di iscrizioni devi prima disattivarlo!\nMandami il comando /setblockoff!", parse_mode='Markdown')
        except Exception as e:
            error_bot.send_message(message.chat.id, f"< *ERRORE* > C'è stato un problema nel salvataggio del file\n*ERRORE*: {e}", parse_mode='Markdown')
    else:
        if sys.json_impostazioni["block"] == 'off':
            error_bot.send_message(message.chat.id, "Il bot è già online!", parse_mode='Markdown')
        else:
           error_bot.send_message(message.chat.id, "Il bot è già offline!", parse_mode='Markdown')

@error_bot.message_handler(commands=["getuseronline"] , func=lambda message: message.from_user.id in sys.ids_moderatori.values())
def set_block_bot(message):
    sys = Sistema()
    
    path_manager = PathManager()

    sys.json_utenti = path_manager.get_json(path_manager.path_impostazioni_utenti)
    
    try:
        count = 0
        for key, users in sys.json_utenti.items():
            for user in users:
                if user["status"] == "online":
                    count += 1
        error_bot.send_message(message.chat.id, f"In questo momento ci sono {count} account attivi sul bot!", parse_mode='Markdown')
    
    except Exception as e:
        error_bot.send_message(message.chat.id, f"< *ERRORE* > C'è stato un problema nel conteggio degli utenti\n*ERRORE*: {e}", parse_mode='Markdown')
    


@error_bot.message_handler(commands=["setbetateston", "setbetatestoff", "getstatusbeta"] , func=lambda message: message.from_user.id in sys.ids_moderatori.values())
def set_beta_test_bot(message):
    sys = Sistema()
    path_manager = PathManager()

    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)

    beta = 'on'
    response = 'Hai attivato la beta su informati.\nPer il momento il bot risponderà solo agli utenti inseriti nella lista di test!\nPer disattvarla inviare il comando /setbetatestoff.'
    
    if message.text != "/setbetatestoff" and message.text != "/setbetateston":
        # TODO: Ottenere lo stato delle modifiche
        
        if sys.json_impostazioni["beta_test"] == 'on':
            response = "La beta è attiva!\nSolo gli utenti registrati possono chattare con il bot fino a che essa sarà attiva!\nRimuovila con /setbetatestoff"
        else:
            response = "La beta non è attiva!\nTutti gli utenti possono chattare con il bot fino a che essa non sarà attiva!\nAttivala con /setbetateston"
        
        error_bot.send_message(message.chat.id, response, parse_mode='Markdown')

    if message.text == '/setbetatestoff':
        beta = 'off'
        response = 'Hai disattivato la beta su informati.\nIl bot risponderà a tutti gli utenti!\nPer attvarla inviare il comando /setbetateston.'
    if message.text == "/setbetatestoff" or message.text == "/setbetateston":
        if sys.json_impostazioni["beta_test"] != beta:
            sys.json_impostazioni["beta_test"] = beta
            try:
                if path_manager.salva_json(path_manager.path_impostazioni_bot, sys.json_impostazioni):
                    if beta == 'on':
                        error_bot.send_message(message.chat.id, response, parse_mode='Markdown')
                    else:
                        error_bot.send_message(message.chat.id, response, parse_mode='Markdown')
            except Exception as e:
                error_bot.send_message(message.chat.id, f"< *ERRORE* > C'è stato un problema nel salvataggio del file\n*ERRORE*: {e}", parse_mode='Markdown')
        else:
            if sys.json_impostazioni["beta_test"] == 'off':
                error_bot.send_message(message.chat.id, "Il bot è già accessibile a tutti!", parse_mode='Markdown')
            else:
                error_bot.send_message(message.chat.id, "Il bot è già in beta!", parse_mode='Markdown')

@error_bot.message_handler(commands=["vogliopartecipare"] , func=lambda message: message.from_user.id not in sys.ids_moderatori.values())
def closed_beta(message):
    path_manager = PathManager()

    sys = Sistema()
    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)
    sys.json_impostazioni = path_manager.get_json(path_manager.path_impostazioni_bot)   

    if not message.from_user.username:
        user = message.from_user.first_name
    else:
        user = f'@{message.from_user.username}' 

    if sys.json_impostazioni["beta_test"] == 'on' and sys.json_impostazioni["block"] == "off":
        if len(sys.ids["ids_tester"]) < 60:

            confirm_tester = f'{user} è entrato a far parte della beta'

            if message.from_user.id not in sys.ids["ids_tester"].values():
                sys.ids["ids_tester"][len(sys.ids["ids_tester"]) + 1 ] = message.from_user.id

                path_manager.salva_json(path_manager.path_id_sviluppatori, sys.ids)

                error_bot.send_message(message.from_user.id, f"Hey, Grande sei tra i fortunati che sono riusciti ad iscriversi, complimenti!!🤩\nOra non ti resta che [cliccare qui](https://t.me/inFORMIAMOCIbot) e cominciare subito a chattare con Astro!😎", parse_mode='Markdown')
                errBot.sendErrors(main_bot, error_bot, e = confirm_tester, message = message, function="tester", error_just_sended=True)
            else:
                error_bot.send_message(message.from_user.id, f"Hey, Sembra che tu sia stato tra i fortunati che sono riusciti ad iscriversi, complimenti!!🤩\nOra non ti resta che [cliccare qui](https://t.me/inFORMIAMOCIbot) e cominciare subito a chattare con Astro!😎", parse_mode='Markdown')
        else:
            error_bot.send_message(message.from_user.id, f"Hey, Mi dispiace ma la beta è già al completo.😣\nCi vedremo non appena uscirà per tutti!!🤗", parse_mode='Markdown')
    else:
       error_bot.send_message(message.from_user.id, f"Hey, Mi dispiace ma la beta non è attiva.😣\nPer rimanere aggiornato sul rilascio seguici su [instagram](https://www.instagram.com/informati.perbene/)!!", parse_mode='Markdown') 

@error_bot.message_handler(func=lambda message: True)
def rispondi(message):
    sys = Sistema()
    path_manager = PathManager()

    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)
    sys.json_comandi = path_manager.get_json(path_manager.path_file_comandi)

    if message.from_user.id not in sys.ids["ids_moderatori"].values():
        if message.text not in sys.json_comandi["error_bot"]:
            errBot.sendErrors(main_bot, error_bot, e = "", message = message, function="not_authorized", error_just_sended = True)
        else:
            errBot.sendErrors(main_bot, error_bot, e = sys.json_comandi["error_bot"][message.text], message = message, function="che_fol", error_just_sended = True) 
    elif message.text == "/vogliopartecipare":
        error_bot.send_message(message.from_user.id, f"Daii sei un moderatore lascia spazio agli altri!!\nLa beta puoi già usarla!", parse_mode='Markdown')

error_bot.infinity_polling()