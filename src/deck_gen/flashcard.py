import genanki 

class FlashCard:

    BASIC_MODEL = genanki.Model(
                    1607392319,
                    'Simple Model',
                    fields=[
                        {'name': 'Word'},
                        {'name': 'Translation'},
                    ],
                    templates=[
                        {
                        'name': 'Word -> Translation',
                        'qfmt': '<div class="word">{{Word}}</div>',
                        'afmt': '{{FrontSide}}<hr id="answer"><div class="translation">{{Translation}}</div>',
                        },
                    ],
                      css="""
                        .card {
                            font-family: Arial, sans-serif;
                            text-align: center;
                            background-color: #fafafa;
                        }
                        .word {
                            font-size: 50px;
                            color: #1a5fb4;
                            font-weight: bold;
                        }
                        .translation {
                            font-size: 40px;
                            color: #26a269;
                        }
                    """)
    
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