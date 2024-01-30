from fbchat.models import *

def command(input_value, thread_id=None, thread_type=None, author_id=None, thread_prefix=None, thread_global=None, thread_user=None, thread_messageid=None, message_object=None, mid=None, bot=None):
    import re
    config = {
        "name": "count",
        "version": "1.0.0",
        "description": "Count words, sentences, paragraphs, and characters",
        "credits": "Miko Mempin",
        "usages": "<paragraph/word/sentence>",
        "cooldown": "2"
    }

    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        argument = input_value[len(config['name']):].strip()
        if argument != '':
            words_count = len(re.findall(r'\b\w+\b', argument))
            sentences_count = len(re.findall(r'[.!?]+', argument))
            paragraphs_count = len(re.findall(r'\n\s*\n', argument)) + 1
            characters_count = len(argument)

            reply = f'📊 Count Results: 📊\n\nWords: {words_count}\nSentences: {sentences_count}\nParagraphs: {paragraphs_count}\nCharacters: {characters_count}'
            bot.sendmessage(author_id, thread_id, thread_type, str(reply))
        else:
            bot.sendmessage(author_id, thread_id, thread_type, f"Please provide text to count using the '{config['name']}' command.")
    else:
        bot.sendmessage(author_id, thread_id, thread_type, f"Default option in {config['name']}: {config['description']}")