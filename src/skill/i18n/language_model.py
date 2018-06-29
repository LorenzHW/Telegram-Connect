from src.skill.i18n.generic_language_model import GenericLanguageModel


class LanguageModel(GenericLanguageModel):
    def __init__(self, locale):
        super().__init__(locale)

        if locale == "de-DE":
            self.set_german_language_model()
        else:
            self.set_english_language_model()

    def set_german_language_model(self):
        pass

    def set_english_language_model(self):
        pass
