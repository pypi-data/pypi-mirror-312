from googletrans import Translator

class Nlator:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, from_lang, to_lang):
        translated = self.translator.translate(text, src=from_lang, dest=to_lang)
        return translated.text

    def findlanguage(self, text):
        detected = self.translator.detect(text)
        return detected.lang