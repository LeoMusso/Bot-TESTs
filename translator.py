from googletrans import Translator
from set_up import Sistema

class GenderTranslator():

    sesso = "maschile"

    def __init__(self, sesso):
        self.sesso = sesso

    def traduci_al_femminile(self, testo):
        translator = Translator()
        
        sys = Sistema()
        sys.json_traduzioni()

        # Traduci il testo nella lingua target
        testo_tradotto = translator.translate(testo, dest='it').text

        # Sostituisci le forme maschili con quelle femminili se il genere è femminile
        if self.sesso.lower() == 'femminile':
            for key, traduzione in sys.json_traduzioni:
                testo_tradotto = testo_tradotto.replace(key, traduzione)

        return testo_tradotto