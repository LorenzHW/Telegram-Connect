import unittest

from src.tests.yes_no_intent.yes_requests import *
from src.tests.yes_no_intent.no_requests import *
from src.tests.secret import VALID_TOKEN
from src.skill.i18n.language_model import LanguageModel
from lambda_function import sb



class AlexaParticleTests(unittest.TestCase):
    def if_user_wants_to_authorize_yes_intent(self):
        i18n = LanguageModel('en-US')
        handler = sb.lambda_handler()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("if_user_wants_to_authorize_yes_intent"))
    runner = unittest.TextTestRunner()
    runner.run(suite)