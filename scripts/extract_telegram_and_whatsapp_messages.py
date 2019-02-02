from random import shuffle
import json
import re

def extract_whats_messages_from_chat(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = lines[2:]

    messages = []
    for l in lines:
        current_line = l
        if ":" in l:
            splitted = l.split(":")
            if len(splitted) == 3:
                text = splitted[2].strip()
                if  text not in "<Media omitted>" and len(text) < 140:
                    text = remove_emojis(text)
                    if text:
                        messages.append(text)
        else:
            text = l.strip()
            if text not in "<Media omitted>" and len(text) < 140:
                text = remove_emojis(text)
                if text:
                    messages.append(text)

    shuffle(messages)
    return messages

def remove_emojis(text):
    # RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    # text = RE_EMOJI.sub(r'', text)
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U00010000-\U0010ffff"
                           "]+", flags=re.UNICODE)
    text =  emoji_pattern.sub(r'', text)
    return text.strip()


def extract_telegram_messages():
    dont_extract = ['Telegram', 'Michael', 'TriviaBot', 'Android Themes Channel', 'Amazon Test', 'alexatesting']

    with open('telegram.json') as file:
        data = json.load(file)
        chats = data.get('chats').get('list')
        
        extracted = []
        for chat in chats:
            if chat.get('type') == 'saved_messages':
                continue
            if chat.get('name') in dont_extract:
                continue
            messages = chat.get('messages')


            for m in messages:
                if isinstance(m, dict):
                    text = m.get('text')
                    if text and isinstance(text, str) and len(text) < 140:
                        text = remove_emojis(text)
                        if text:
                            extracted.append(text)

    file.close()
    shuffle(extracted)
    return extracted

def construct_alexa_slot_type(messages):
    res = {
        "name": "message",
        "values": [construct_value(message) for message in messages]
    }

    return res

def construct_value(message):
    res = {
        "name" : {
            "value": message
        }
    }

    return res

if __name__ == "__main__":
    res1 = extract_whats_messages_from_chat('data/whatsapp_grace.txt')
    res2 = extract_whats_messages_from_chat('data/whatsapp_stevens.txt')
    # res2 = extract_telegram_messages()
    res = res1 + res2
    shuffle(res)
    res = list(set(res))
    len_res = len(res)
    # len_res = int(len_res / 2)
    res = res[:len_res]
    # got like 18 000 values now --> not too big for alexa skill model
    res = construct_alexa_slot_type(res)
    with open('result.json', 'w') as fp:
        json.dump(res, fp, indent=4, ensure_ascii=False)



