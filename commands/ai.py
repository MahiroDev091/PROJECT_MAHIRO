def command(input_value):
    import requests
    config = {
        "name": "ai",
        "description": "ask anything"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
        	ask = input_value[len(config['name']):].strip()
        	ask2 = requests.get('https://api.kenliejugarap.com/ai/?text=' + ask).json()['response']
        	return f"𝙰𝙸 𝚁𝙴𝚂𝙿𝙾𝙽𝙳: \n{ask2}" 
        except:
        	return "❌𝚂𝙾𝚁𝚁𝚈, 𝚆𝙴 𝙰𝚁𝙴 𝙷𝙰𝚅𝙸𝙽𝙶 𝙴𝚁𝚁𝙾𝚁 𝙵𝙴𝚃𝙲𝙷𝙸𝙽𝙶 𝚁𝙴𝚂𝙿𝙾𝙽𝙳."
    else:
        return f"Default option in {config['name']}: {config['description']}"
