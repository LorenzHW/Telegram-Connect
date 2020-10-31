import unittest

from skill.i18n.language_model_abc import LanguageModelABC
from skill.i18n.util import get_i18n


class LanguageModelTest(unittest.TestCase):
    def test_language_model(self):
        german = get_i18n("de-DE", "Europe/Vienna")
        us = get_i18n("en-US", "America/Los_Angeles")
        us_attrs = dir(us)
        german_attrs = dir(german)
        abc_annotations = LanguageModelABC.__annotations__

        self.assertTrue(len(us_attrs) == len(german_attrs))
        for attr in abc_annotations.keys():
            self.assertTrue(attr in us_attrs, '{} not in us_attrs'.format(attr))

        # same_attrs = all([True if attr_en == german_attrs[i] else False for i, attr_en in enumerate(us_attrs)])
        # self.assertTrue(same_attrs is True)
        print('HELLO WORLD')
