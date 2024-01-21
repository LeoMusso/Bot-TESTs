from error_bot import ErrorBot
from set_up import Sistema, TimerThread
import telebot


sys = Sistema()

main_bot = telebot.TeleBot(sys.token_bot_principale, parse_mode=None)
error_bot = telebot.TeleBot(sys.token_bot_errori, parse_mode=None)
errBot = ErrorBot()

thread_set_utenti = TimerThread(3, errBot, main_bot, error_bot)
thread_set_utenti.run()