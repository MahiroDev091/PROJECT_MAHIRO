from fbchat.models import *

def command(input_value, thread_id=None, thread_type=None, author_id=None, thread_prefix=None, thread_global=None, thread_user=None, thread_messageid=None, message_object=None, mid=None, bot=None):
    import requests
    import json
    config = {
        "name": "sim",
        "version": "1.0.1",
        "description": "Talk to sim. (PH)",
        "credits": "Kenlie Jugarap",
        "usages": "<ask anything>",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
            talk = input_value[len(config['name']):].strip()
            if talk != '':
                talk2 = requests.get('https://simsimi.fun/api/v2/?mode=talk&lang=ph&message={}&filter=true'.format(talk))
                decoded_response = json.loads(talk2.content.decode('utf-8-sig'))
                bot.sendmessage(author_id, thread_id, thread_type, str(decoded_response['success']))
            else:
                bot.sendmessage(author_id, thread_id, thread_type, f"❌𝚆𝚁𝙾𝙽𝙶 𝙵𝙾𝚁𝙼𝙰𝚃!\n{thread_prefix}{config['name']} <your question>")
        except Exception as e:
            bot.sendmessage(author_id, thread_id, thread_type, "❌Error fetching response.")
    else:
        bot.sendmessage(author_id, thread_id, thread_type, f"Default option in {config['name']}: {config['description']}")