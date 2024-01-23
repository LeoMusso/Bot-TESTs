from email import message
import telebot, json, os
from api import InformatiAPI
from set_up import Sistema
from path_manager import PathManager
from answer_bot_test import InformatiBOT
from error_bot import ErrorBot

sys = Sistema()

# giusto per il commit

main_bot = telebot.TeleBot(sys.token_bot_test, parse_mode=None)
error_bot = telebot.TeleBot(sys.token_bot_errori, parse_mode=None)
answerBot = InformatiBOT()
errBot = ErrorBot()

######################################################################################
# TODO: Implementazione blocco per fase di test                                      #
######################################################################################

# COMANDO [/start, /hello, /ciao]
@main_bot.message_handler(commands=["start", "hello", "ciao"], func=lambda message: True)
def send_welcome(message):
    sys = Sistema()
    
    path_manager = PathManager()
    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)
    
    moderatore = False

    if message.chat.id in sys.ids_moderatori.values():
        moderatore = True

    if sys.json_impostazioni["block"] == "on":
        response = errBot.closed()
        sys.set_last_message_user(message)
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["beta_test_test_bot"] == 'on':
            response = errBot.no_tester()
            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        try:
            if not message.from_user.username:
                value = message.from_user.first_name
            else:
                value = message.from_user.username

            if sys.crea_aggiorna_user(message.from_user.id, value, "True"):
                try:
                    response = answerBot.Welcome(message)
                    sys.set_last_message_user(message)
                    main_bot.send_message(message.chat.id, response)
                except Exception as e:
                    sys.set_last_message_user(message)
                    errBot.sendErrors(main_bot, error_bot, e, message)
        except Exception as e:
            sys.set_last_message_user(message)
            errBot.sendErrors(main_bot, error_bot, e, message)
        
# COMANDO PER I FUMAGAZZERS [/fumagazzi]
@main_bot.message_handler(commands=["fumagazzi"], func=lambda message: True)
def send_fumagazzi(message):
    sys = Sistema()

    path_manager = PathManager()
    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)

    moderatore = False

    if message.chat.id in sys.ids_moderatori.values():
        moderatore = True

    if sys.json_impostazioni["block"] == "on":
        response = errBot.closed()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["beta_test_test_bot"] == 'on':
        response = errBot.no_tester()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        try:
            response = answerBot.Fumagazzi()
            sys.set_last_message_user(message)
            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            sys.set_last_message_user(message)
            errBot.sendErrors(main_bot, error_bot, e, message)

@main_bot.message_handler(commands=["signup", "registrati"], func=lambda message: True)
def sign_up(message):
    sys = Sistema()
    
    path_manager = PathManager()
    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)
    
    value = ""
    moderatore = False

    if message.chat.id in sys.ids_moderatori.values():
        moderatore = True

    if sys.json_impostazioni["block"] == "on":
        response = errBot.closed()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["beta_test_test_bot"] == 'on':
        response = errBot.no_tester()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["signup"] == 'off':
        main_bot.send_message(message.chat.id, f'Mi dispiace ma in questo momento le iscrizioni sono chiuse!😣\nNon appena torneranno online ti avvertirò con un messaggio!🤗', parse_mode='Markdown')
    else:
        if not message.from_user.username:
            value = message.from_user.first_name
        else:
            value = "@" + message.from_user.username

        block = True
        if block:
            try:
                if sys.crea_aggiorna_user(message.from_user.id, value, "True"):
                    main_bot.send_message(message.chat.id, answerBot.SignUp(value, message.from_user.id), parse_mode='Markdown')
                else:
                    main_bot.send_message(message.chat.id, f"Mi spiace {value} risulti già essere resgitrato, se pensi possa essere un errore contatta @justL3lL0!", parse_mode='Markdown')

            except Exception as e:
                errBot.sendErrors(main_bot, error_bot, e, message)
        else:
            main_bot.send_message(message.chat.id, errBot.not_implemented(), parse_mode='Markdown')
            errBot.sendErrors(main_bot, error_bot, value, message, "error_command", True)

# COMANDI PER LE NOTIFICHE [/setnotifyon, /setnotifyoff]
@main_bot.message_handler(commands=["setnotifyon", "setnotifyoff", "statusnotify"], func=lambda message: True)
def set_notify(message):
    sys = Sistema()

    path_manager = PathManager()
    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)

    moderatore = False

    if message.chat.id in sys.ids_moderatori.values():
        moderatore = True

    if sys.json_impostazioni["block"] == "on":
        response = errBot.closed()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["beta_test_test_bot"] == 'on':
        response = errBot.no_tester()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    else:
        response = 'Hai OPERAZIONE le notifiche correttamente! Per INVERSA basta inviare il comando COMANDO'
        notify = "True"
        if message.text != "/setnotifyoff" and message.text != "/setnotifyon":            
            if sys.json_utenti[str(message.from_user.id)][0]["notifiche"] == "True":
                response = "Hey, le tue notifiche sono attive!\nNon appena arriverà il momento ti aggiornerò con tutti i bellissimi eventi di inFORMATI!🤩\nNel mentre che aspetti potresti seguire [la mia pagina instagram](https://www.instagram.com/informati.perbene/)!😎"
            else:
                response = "Hey, le tue notifiche non sono attive!\nRimedia subito mandando il comando /setnotifyon, oppure puoi seguire [la mia pagina instagram](https://www.instagram.com/informati.perbene/) per rimanere sempre aggiornato!😎"
            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
        else:
            if message.text == "/setnotifyoff":
                notify = "False"
            try:
                if not message.from_user.username:
                    value = message.from_user.first_name
                else:
                    value = message.from_user.username
                if sys.crea_aggiorna_user(message.from_user.id, value, notify):
                    try:
                        if notify in sys.json_utenti[str(message.from_user.id)][0]["operazioni"]:
                            
                            '''
                            PER IL MOMENTO L'API AL SERVER LA LASCIAMO COMMENTATA
                                api = InformatiAPI()
                                response_web = api.set_notify(message.from_user.id, notify)
                            '''
                            for key, rep in sys.json_utenti[str(message.from_user.id)][0]["operazioni"][notify].items():
                                response = response.replace(key,rep)
                            sys.set_last_message_user(message)
                            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
                    except Exception as e:
                        sys.set_last_message_user(message)
                        errBot.sendErrors(main_bot, error_bot, e, message)   
                else:
                    sys.set_last_message_user(message)
                    main_bot.send_message(message.chat.id, f"Mi spiace @{value} risulti già essere resgitrato, se pensi possa essere un errore contatta @justL3lL0!", parse_mode='Markdown')
            except Exception as e:
                sys.set_last_message_user(message)
                errBot.sendErrors(main_bot, error_bot, e, message)
    
# COMANDO PER SETTARE IL NOME DEL BOT [/setnebula /setastro]
@main_bot.message_handler(commands=["setnebula", "setastro"], func=lambda message: True)
def set_name_bot(message):
    sys = Sistema()

    path_manager = PathManager()
    sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)

    moderatore = False

    if message.chat.id in sys.ids_moderatori.values():
        moderatore = True

    if sys.json_impostazioni["block"] == "on":
        response = errBot.closed()
        sys.set_last_message_user(message)
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["beta_test_test_bot"] == 'on':
        response = errBot.no_tester()
        main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    else:
        try:
            response = answerBot.set_name_bot(message)
            sys.set_last_message_user(message)
            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            errBot.sendErrors(main_bot, error_bot, e, message)

# FUNZIONE PER CERCARE LA RISPOSTA NON PRESENTE TRA I COMANDI BASE
@main_bot.message_handler(func=lambda message: True)
def send_response(message):
    try:
        sys = Sistema()

        path_manager = PathManager()
        sys.ids = path_manager.get_json(path_manager.path_id_sviluppatori)

        moderatore = False

        if message.chat.id in sys.ids_moderatori.values():
            moderatore = True

        if sys.json_impostazioni["block"] == "on":
            response = errBot.closed()
            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
        elif message.from_user.id not in sys.ids["ids_tester"].values() and moderatore == False and sys.json_impostazioni["beta_test_test_bot"] == 'on':
            response = errBot.no_tester()
            main_bot.send_message(message.chat.id, response, parse_mode='Markdown')
        else:
            response = ""
            e = ""
            error_just_sended = False

            try:
                response = answerBot.cerca_risposta(message)
            
            except Exception as e:
                function = "error"
                if e != "":
                    function = "no_error" 
                    errBot.sendErrors(main_bot, error_bot, e, message, function, error_just_sended)
                    error_just_sended = True
                    
            try:
                if response[1] != 404:
                    if not response[0].strip() or response[0] == None:
                        sys.set_last_message_user(message)
                        main_bot.send_message(message.chat.id, errBot.no_commands(), parse_mode='markdown')
                        for id, value in sys.ids_moderatori.items():
                            if value != 000000:
                                error_bot.send_message(value, errBot.no_answ(message), parse_mode='markdown')
                    else:
                        sys.set_last_message_user(message)
                        main_bot.send_message(message.chat.id, response, parse_mode='markdown')
                else:
                    sys.set_last_message_user(message)
                    main_bot.send_message(message.chat.id, errBot.no_commands(), parse_mode='markdown')
                    if e == "" or e == None:
                        e = "no_exeception"
                    errBot.sendErrors(main_bot, error_bot, e, message, "no_error", True)

            except Exception as e:
                if not error_just_sended: 
                    error_just_sended = True
                
                errBot.sendErrors(main_bot, error_bot, e, message, "error", error_just_sended)
    except Exception as e:
        errBot.sendErrors(main_bot, error_bot, e, message)

#### TODO: Thread per api


# Segnalazione avviamento bot
errBot.sendErrors(main_bot, error_bot, e = "", message = "", function="start", error_just_sended = True)

# start del bot all'infinito
main_bot.infinity_polling()