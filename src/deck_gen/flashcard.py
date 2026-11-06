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

    EXAMPLE_SENTENCE_MODEL = genanki.Model(
                    1607392317,
                    'Simple Model',
                    fields=[
                        {'name': 'Word'},
                        {'name': 'Translation'},
                        {'name': 'ExampleSentence'},
                    ],
                    templates=[
                        {
                        'name': 'Word -> Translation',
                        'qfmt': '<div class="word">{{Word}}</div>',
                        'afmt': '{{FrontSide}}<hr id="answer"><div class="translation">{{Translation}}</div><div class="example">{{ExampleSentence}}</div>',
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
                        .example {
                            font-size: 32px;
                            color: #555;
                        }
                    """)
    
    def __init__(self, word: str, model=None, translation: str='', exampleSentence: str=''):
        self.model = model if model is not None else FlashCard.BASIC_MODEL
        self.word = word
        self.translation = translation
        self.exampleSentence = exampleSentence

    def setTranslation(self, translation):
        self.translation = translation

    def setExampleSentence(self, exampleSentence):
        self.exampleSentence = exampleSentence

    def convertToGenankiNote(self):
        if self.model == FlashCard.BASIC_MODEL:
            return genanki.Note(model=self.model, fields=[self.word, self.translation])
        elif self.model == FlashCard.EXAMPLE_SENTENCE_MODEL:
            return genanki.Note(model=self.model, fields=[self.word, self.translation, self.exampleSentence])