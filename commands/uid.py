from fbchat.models import *

def command(input_value, thread_id=None, thread_type=None, author_id=None, thread_prefix=None, thread_global=None, thread_user=None, thread_messageid=None, message_object=None, mid=None, bot=None):
    config = {
        "name": "uid",
        "version": "1.0.0",
        "description": "Get your uid.",
        "credits": "Mahiro chan",
        "usages": "N/A",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        argument = input_value[len(config['name']):].strip()
        bot.sendmessage(author_id, thread_id, thread_type, f"Hi, {thread_user.name}\nYOUR UID: {thread_user.uid}")
    else:
        bot.sendmessage(author_id, thread_id, thread_type, f"Default option in {config['name']}: {config['description']}")