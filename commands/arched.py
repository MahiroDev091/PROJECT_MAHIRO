def command(input_value, thread_userid=None):
    import requests
    config = {
        "name": "arched",
        "version": "1.0.0",
        "description": "ask anything developed by Liane",
        "credits": "Liane",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
            ask = input_value[len(config['name']):].strip()
            liane = requests.get('https://lianeapi.onrender.com/ask/arched?query=' + ask).json()['message']
            reply = liane
            if reply:
                return {'messages': [str(reply)]}
            else:
                return {'messages': ['No response from the API']}
        except Exception as e:
            reply = "❌𝚂𝙾𝚁𝚁𝚈, 𝚆𝙴 𝙰𝚁𝙴 𝙷𝙰𝚅𝙸𝙽𝙶 𝙴𝚁𝚁𝙾𝚁 𝙵𝙴𝚃𝙲𝙷𝙸𝙽𝙶 𝚁𝙴𝚂𝙿𝙾𝙽𝙳."
            return {'messages': [str(reply)]}
    else:
        reply = f"Default option in {config['name']}: {config['description']}"
        return {'messages': [str(reply)]}
