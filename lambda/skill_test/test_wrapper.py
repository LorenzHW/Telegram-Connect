import unittest
import sys

from skill_test.launch_intent.test_launch import LaunchIntentTest
from skill_test.message_intent.test_message import MessageIntentTest
from skill_test.setup_intent.test_setup import SetupIntentTest
from skill_test.test_language_model import LanguageModelTest

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(LanguageModelTest("test_language_model"))
    # suite.addTest(LaunchIntentTest("test_launch"))
    # suite.addTest(SetupIntentTest("test_setup"))
    # suite.addTest(MessageIntentTest("test_message"))

    runner = unittest.TextTestRunner()
    res = not runner.run(suite).wasSuccessful()
    sys.exit(res)
