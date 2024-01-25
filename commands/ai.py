def command(input_value, thread_userid=None):
    import requests
    config = {
        "name": "ai",
        "version": "1.0.2",
        "description": "ask anything",
        "credits": "Kenlie Jugarap",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
            ask = input_value[len(config['name']):].strip()
            ask2 = requests.get('https://api.kenliejugarap.com/ai/?text=' + ask).json()['response']
            return {"messages": [f"𝙰𝙸 𝚁𝙴𝚂𝙿𝙾𝙽𝙳: \n{ask2}"]}
        except:
            return {"messages": ["❌𝚂𝙾𝚁𝚁𝚈, 𝚆𝙴 𝙰𝚁𝙴 𝙷𝙰𝚅𝙸𝙽𝙶 𝙴𝚁𝚁𝙾𝚁 𝙵𝙴𝚃𝙲𝙷𝙸𝙽𝙶 𝚁𝙴𝚂𝙿𝙾𝙽𝙳."]}
    else:
        return {'messages': [f"Default option in {config['name']}: {config['description']}"]}