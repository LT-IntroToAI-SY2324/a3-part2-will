from googletrans import Translator

translator = Translator()

translated = translator.translate("Hello World", dest="fr")

print(translated)