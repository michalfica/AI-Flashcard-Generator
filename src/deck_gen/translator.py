import time 
import json 

from google import genai 
from google.genai import types
from google.genai import errors

from pydantic import BaseModel

import logging

logger = logging.getLogger()
logging.basicConfig(filename='logging_info.txt', encoding='utf-8', level=logging.WARNING)

class TranslationPair(BaseModel):
    word: str
    translation: str

class Translator:

    """Translate words or phrases from one language to another using Gemini model"""
    # RETRYABLE_CODES = {429, 500, 502, 503, 504}

    def __init__(
            self,
            model : str ="gemini-3.6-flash", 
            base_language : str ='polish', 
            target_language : str ='english',
            client = None,
            max_retries: int = 3 
        ):
        self.model = model
        self.base_language = base_language
        self.target_language = target_language 
        self.client = client or genai.Client()
        self.max_retries = max_retries
        self._single_config = types.GenerateContentConfig(
            system_instruction= (
                f"You are a translator agent. Translate each word or phrase in the user's input "
                f"from {base_language} into {target_language}. "
                f"Respond with only the translation, no explanations or extra text."
            ),
            temperature=0,
        ) 
        self._batch_config = types.GenerateContentConfig(
            system_instruction= (
               f"You are a translator agent. The user sends a JSON array of "
               f"{base_language} words or phrases. Return a JSON array with one object "
               f"per input, in the same order, where 'word' is the input excatly as given "
               f"and 'translation' is its {target_language} translation." 
            ),
            temperature=0, 
            response_mime_type='application/json', 
            response_schema=list[TranslationPair],
            # max_output_tokens=10,
            # thinking_config=types.ThinkingConfig(thinking_budget=0)
        )

    def translate_word(self, word : str) -> str:
        response = self._generate(word, self._single_config)
        return response.text.strip()

    def translate_list(self, words : list[str]) -> dict[str, str]:
        logger.info('translate_list evoked for %s', words)

        response = self._generate(json.dumps(words, ensure_ascii=False), self._batch_config)
        logger.info('model response %s', response)
        
        pairs = response.parsed
        logger.info('model response parsed %s', pairs) 

        if pairs is None:
            raise ValueError(f"Could not parse model response: {response.text}")
        translations = {pair.word: pair.translation for pair in pairs}
        missing = [w for w in words if w not in translations]
        if missing:
            raise ValueError(f"Model response is missing translations for: {missing}")
        return translations

    def _generate(self, contents, config : types.GenerateContentConfig):
        logger.info('_generate evoked')

        delay = 1 
        for attempt in range(1, self.max_retries+1):
            try:
                logger.info('attempt nr %d', attempt)
                response = self.client.models.generate_content(
                    model=self.model, contents=contents, config=config
                )
                return response
            except errors.APIError as e:
                if attempt==self.max_retries:
                    raise e
                logger.info('Server busy (attempt %d/%s), retrying in %ds...', attempt, self.max_retries, delay)
                time.sleep(delay)
                delay *= 2
