def command(input_value, thread_userid=None):
    import requests
    config = {
        "name": "catfacts",
        "version": "1.0.2",
        "description": "get random catfacts everyday.",
        "credits": "Mahiro chan",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
        	ask = input_value[len(config['name']):].strip()
        	facts = requests.get('https://catfact.ninja/fact').json()['fact']
        	return {'messages': [f"𝙲𝙰𝚃𝙵𝙰𝙲𝚃 𝚁𝙴𝚂𝙿𝙾𝙽𝙳: \n{facts}"], 'images': ['commands/images/cat.jpeg']} 
        except:
        	return {"messages": ["❌𝚂𝙾𝚁𝚁𝚈, 𝚆𝙴 𝙰𝚁𝙴 𝙷𝙰𝚅𝙸𝙽𝙶 𝙴𝚁𝚁𝙾𝚁 𝙵𝙴𝚃𝙲𝙷𝙸𝙽𝙶 𝚁𝙴𝚂𝙿𝙾𝙽𝙳."]}
    else:
        return {"messages": [f"Default option in {config['name']}: {config['description']}"]} 
