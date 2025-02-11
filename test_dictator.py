from unittest import TestCase
from dictator import Dictator
import string


class TestDictator(TestCase):

    def test_loads(self):
        dictator = Dictator()
        self.assertIsNotNone(dictator)

    def test_transcribe(self):
        lower_chars = f"{string.ascii_lowercase}{string.digits} "

        dictator = Dictator()
        dictator.TEMP_WAV_FILENAME = "test_news_headline.wav"

        transcription = dictator.transcribe()
        sanitised_transcription = "".join([x.lower() for x in transcription if x.lower() in lower_chars])

        self.assertEqual(
            sanitised_transcription,
            "today at one the bank of england cuts interest rates by a quarter of a percentage point",
            "Transcription does not match audio")

    def test_detect_language(self):
        dictator = Dictator()
        dictator.TEMP_WAV_FILENAME = "test_news_headline.wav"
        dictator.transcribe()

        self.assertEqual(
            dictator.detect_language(),
            "en",
            "Language not detected correctly"
        )
