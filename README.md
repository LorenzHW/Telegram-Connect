# Telegram Connect
[Telegram Connect](https://github.com/LorenzHW/Telegram-connect) is an open source  Alexa Skill that connects Alexa with the [Telegram Messenger](https://telegram.org/).

### High Level Overview
<p align="center">
  <img src="https://raw.githubusercontent.com/LorenzHW/My-Telegrams/telegram-connect/skill-package/assets/highlevel-overview.png"/>
</p>


### Supported Features
- Listening to new telegrams you received on Alexa
- Languages: English

### Desired Features (contributions welcome!)
- Support more languages: German, Spanish, Italian
- Add [Voice Profiles](https://developer.amazon.com/blogs/alexa/post/1ad16e9b-4f52-4e68-9187-ec2e93faae55/recognize-voices-and-personalize-your-skills)
for people who use the same Alexa device but different telegram accounts.

### Getting started  
If you want to play around with the skill in your own Alexa Developer Console, follow these steps:

**Prerequisites**  
- [ASK cli](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html) (Version 2.19 or higher)

Clone the repository
```
git clone https://github.com/LorenzHW/Telegram-Connect.git
cd Telegram-Connect
touch lambda/secrets.py
```
We now want to deploy the skill to your Alexa developer console. In order to do that, we need to do a couple of things first.


Head over to [Telegram](https://core.telegram.org/api/obtaining_api_id) and create an `api_id` and `api_hash`.
Then update secrets.py
```
API_ID = YOUR_API_ID (type: integer)
API_HASH = YOUR_API_HASH (type: string)
```

Go to .ask/ask-states.json and change the file to
```
{
  "askcliStatesVersion": "2020-03-31",
  "profiles": {
    "default": {
      "skillInfrastructure": {
        "@ask-cli/lambda-deployer": {
          "deployState": {}
        }
      }
    }
  }
}
```

Then head over to skill-package/skill.json and set the `custom` key to:
```
.
.
    "custom": {}
.
.

``` 

Deploy the skill to AWS:
```
ask deploy
```
This will create a new skill in your Alexa Developer Console, an AWS Lambda function and DynamoDB database.

You need to grant your lambda function access to your DynamoDB database. 
1. Head over to [AWS](https://aws.amazon.com/de/console/)
2. IAM -> Roles. Find the role that is associated with your lambda function (something like: ask-lambda-telegram-connect)
3. Attach policy: AmazonDynamoDBFullAccess

At last you need to increase the timeout and the memory of your lambda function.
1. Inside the AWS console go to lambda and find you lambda function.
2. After you clicked on it, edit Basic Settings->Timeout to 20 seconds.
3. Increase the memory of the function as well.


Feel free to create PR's!

