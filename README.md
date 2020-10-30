# Telegram Connect
Telegram Connect is an open source  Alexa Skill that connects Alexa with the [Telegram Messenger](https://telegram.org/).

### High Level Overview
<p align="center">
  <img src="https://raw.githubusercontent.com/LorenzHW/My-Telegrams/telegram-connect/icons/highlevel-overview.png"/>
</p>


### Supported Features
- Listening to new telegrams you received on Alexa
- Languages: English

### Desired Features (contributions welcome!)
- Support more languages: German, Spanish, Italian

### Getting started
If you don't want to play around with the Skill in the Alexa developer console, you can jump to step x  
**Prerequisites**  
[ASK cli](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html) (Version 2.19 or higher)

**First step:**  
Clone the repository
```
git clone https://github.com/LorenzHW/My-Telegrams
```


ask smapi get-interaction-model --skill-id amzn1.ask.skill.174177e4-dc9f-4411-82b3-0bf9bd7ce2d5 --stage development --locale en-US

ask smapi delete-skill --skill-id amzn1.ask.skill.174177e4-dc9f-4411-82b3-0bf9bd7ce2d5

TODO: Keep track of up to date interaction model in github repo
TODO: First finish skill in english, then do beta, then add german
TODO: Add typings to signatures, add codecov
TODO: Probably remove skill id
TODO: Send read acknowledgment
TODO: Unit Test for PyrogramManager

