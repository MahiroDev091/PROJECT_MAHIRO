from fbchat.models import *

def command(input_value, thread_id=None, thread_type=None, author_id=None, thread_prefix=None, thread_global=None, thread_user=None, thread_messageid=None, message_object=None, mid=None, bot=None):
    import requests
    config = {
        "name": "ai",
        "version": "1.0.2",
        "description": "ask anything",
        "credits": "Kenlie Jugarap",
        "usages": "<ask anything>",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
            ask = input_value[len(config['name']):].strip()
            if ask != '':
            	ask2 = requests.get('https://api.kenliejugarap.com/ai/?text=' + ask).json()['response']
            	bot.sendmessage(author_id, thread_id, thread_type, f"𝙰𝙸 𝚁𝙴𝚂𝙿𝙾𝙽𝙳: \n{ask2}")
            else:
            	bot.sendmessage(author_id, thread_id, thread_type, f"❌𝚆𝚁𝙾𝙽𝙶 𝙵𝙾𝚁𝙼𝙰𝚃!\n{thread_prefix}{config['name']} <your question>")
        except:
            bot.sendmessage(author_id, thread_id, thread_type, "❌𝚂𝙾𝚁𝚁𝚈, 𝚆𝙴 𝙰𝚁𝙴 𝙷𝙰𝚅𝙸𝙽𝙶 𝙴𝚁𝚁𝙾𝚁 𝙵𝙴𝚃𝙲𝙷𝙸𝙽𝙶 𝚁𝙴𝚂𝙿𝙾𝙽𝙳.")
    else:
        bot.sendmessage(author_id, thread_id, thread_type, f"Default option in {config['name']}: {config['description']}")