import unittest

from src.main import sb
from src.tests.can_ful_fill import can_ful_fill_request


class AlexaParticleTests(unittest.TestCase):
    def test_launch_request(self):
        pass
        # event = handler()
        # self.assertEqual(event["response"]["card"]["title"], "Willkommen")

    def test_send_intent(self):
        ##############################
        # Send Intent
        ##############################
        request = can_ful_fill_request
        handler = sb.lambda_handler()
        handler(can_ful_fill_request, None)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AlexaParticleTests("test_send_intent"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
