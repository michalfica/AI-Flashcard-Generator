import genanki

from translator import Translator
from flashcard import FlashCard

class Deck:

    def __init__(self, deck_id, name = '', word_list=None, target_language='russian'):
        self.deck = genanki.Deck(deck_id=deck_id, name=name)
        self.word_list = word_list if word_list is not None else []
        self.translation_agent = Translator(targetLanguage=target_language)

    def generateFlashcards(self):
        words_translation = self.translation_agent.translate_words(self.word_list).split()  
        for i, word in enumerate(self.word_list): 
            card = FlashCard(word=word, translation=words_translation[i])
            self.deck.add_note(card.convertToGenankiNote())
    
    def saveDeckToFile(self, fileName):
        genanki.Package(self.deck).write_to_file(file=fileName)
    