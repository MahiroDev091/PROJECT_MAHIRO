def command(input_value, thread_userid=None):
    import re
    config = {
        "name": "count",
        "version": "1.0.0",
        "description": "Count words, sentences, paragraphs, and characters",
        "credits": "Miko Mempin",
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
            return {'messages': [str(reply)]}
        else:
            return {'messages': [f"Please provide text to count using the '{config['name']}' command."]}
    else:
        return {'messages': [f"Default option in {config['name']}: {config['description']}"]}
