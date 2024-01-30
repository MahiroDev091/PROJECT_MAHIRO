from fbchat.models import *

def command(input_value, thread_id=None, thread_type=None, author_id=None, thread_prefix=None, thread_global=None, thread_user=None, thread_messageid=None, message_object=None, mid=None, bot=None):
    config = {
        "name": "mahiro",
        "version": "1.0.0",
        "description": "Developer.",
        "credits": "Mahiro chan",
        "usages": "N/A",
        "cooldown": "2"
    }

    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name'] + ' ') or input_value == config['name']:
        bot.sendmessage(author_id, thread_id, thread_type, "DEVELOPED BY MAHIRO CHAN")
        bot.reactToMessage(thread_messageid, MessageReaction.LOVE)
    else:
        bot.sendmessage(author_id, thread_id, thread_type, f"Default option in {config['name']}: {config['description']}")
        