import genanki

from translator import Translator
from flashcard import FlashCard

class Deck:

    def __init__(self, deck_id, name = '', word_list=None, target_language='russian'):
        self.deck = genanki.Deck(deck_id=deck_id, name=name)
        self.word_list = word_list if word_list is not None else []
        self.translation_agent = Translator(target_language=target_language)

    def generateFlashcards(self):
        words_translation = self.translation_agent.translate_list(self.word_list)
        for word, translation in words_translation.items(): 
            card = FlashCard(word=word, model=FlashCard.BASIC_MODEL, translation=translation)
            self.deck.add_note(card.convertToGenankiNote())

    def generateFlashcards_with_examples(self):
        words_entries = self.translation_agent.translate_words_with_examples(self.word_list)
        for word, entry in words_entries.items():
            card = FlashCard(word=word, model=FlashCard.EXAMPLE_SENTENCE_MODEL, translation=entry.translation, exampleSentence=entry.example)
            self.deck.add_note(card.convertToGenankiNote())
    
    def saveDeckToFile(self, fileName):
        genanki.Package(self.deck).write_to_file(file=fileName)
    