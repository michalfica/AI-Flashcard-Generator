import genanki 

class FlashCard:

    BASIC_MODEL = genanki.Model(
                    1607392319,
                    'Simple Model',
                    fields=[
                        {'name': 'Question'},
                        {'name': 'Answer'},
                    ],
                    templates=[
                        {
                        'name': 'Card 1',
                        'qfmt': '{{Question}}',
                        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                        },
                    ])
    
    def __init__(self, word, model=None, translation='', exampleSentence=''):
        self.model = model if model is not None else FlashCard.BASIC_MODEL
        self.word = word
        self.translation = translation
        self.exampleSentence = exampleSentence

    def setTranslation(self, translation):
        self.translation = translation

    def setExampleSentence(self, exampleSentence):
        self.exampleSentence = exampleSentence

    def convertToGenankiNote(self):
        return genanki.Note(model=self.model, fields=[self.word, self.translation])