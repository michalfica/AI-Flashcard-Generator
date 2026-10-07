import time 

from google import genai 
from google.genai import types
from google.genai import errors

class Translator:

    def __init__(self, model="gemini-3.6-flash", baseLanguage='polish', targetLanguage='english'):
        self.model = model
        self.baseLanguage = baseLanguage
        self.targetLanguage = targetLanguage 
        self.client = genai.Client()
        self.config = types.GenerateContentConfig(
            system_instruction= (
                f"You are a translator agent. Translate each word in the user's input "
                f"from {baseLanguage} into {targetLanguage}. "
                f"Respond with only the translation, no explanations or extra text."
            ),
            temperature=0,
        )
    def translate_word_with_retry(self, word, max_retries=3):
        delay = 1 
        for attempt in range(max_retries):
            try: 
                print(f"probuje tlumaczyc {word}")
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=word, 
                    config=self.config
                )
                print(f"udalo sie")
                return response.text
            except errors.ServerError as e: 
                if attempt == max_retries - 1:
                    raise e 
                print(f"Server busy (attempt {attempt+1}/{max_retries}), retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2 
    
    def translate_list_of_words_with_retry(self, words, max_retries=3):
        delay = 1 
        for attempt in range(max_retries):
            try: 
                print(f"probuje tlumaczyc liste {words}")
                response = self.client.models.generate_content(
                    model=self.model, 
                    contents=" ".join(words), 
                    config=self.config
                )
                print(f"Udało sie")
                return response.text
            except errors.ServerError as e: 
                if attempt == max_retries - 1:
                    raise e 
                print(f"Server busy (attempt {attempt+1}/{max_retries}), retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2 