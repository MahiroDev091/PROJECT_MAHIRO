def command(input_value):
    import requests
    config = {
        "name": "arched",
        "description": "ask anything developed by Liane"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
        	ask = input_value[len(config['name']):].strip()
        	liane = requests.get('https://lianeapi.onrender.com/ask/arched?query=' + ask).json()['message']
        	return liane
        except:
        	return "❌𝚂𝙾𝚁𝚁𝚈, 𝚆𝙴 𝙰𝚁𝙴 𝙷𝙰𝚅𝙸𝙽𝙶 𝙴𝚁𝚁𝙾𝚁 𝙵𝙴𝚃𝙲𝙷𝙸𝙽𝙶 𝚁𝙴𝚂𝙿𝙾𝙽𝙳."
    else:
        return f"Default option in {config['name']}: {config['description']}"
