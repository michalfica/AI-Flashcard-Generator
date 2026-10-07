import genanki

from translator import Translator
from flashcard import FlashCard

class Deck:

    def __init__(self, deck_id, deck_name = '', word_list=None, target_language='russian'):
        print("O chuj chodzi?")
        self.deck = genanki.Deck(deck_id=deck_id, name=deck_name)
        self.word_list = word_list if word_list is not None else []
        self.translation_agent = Translator(targetLanguage=target_language)

    def generateFlashcards(self):
        print(f"self.word_list = {self.word_list}")
        for word in self.word_list: 
            print(f"word = {word}")
            card = FlashCard(word)
            card.setTranslation(self.translation_agent.translate_word_with_retry(word))
            # card.setTranslation('ochujchodzi')
            self.deck.add_note(card.convertToGenankiNote())
    
    def saveDeckToFile(self, fileName):
        genanki.Package(self.deck).write_to_file(file=fileName)
    