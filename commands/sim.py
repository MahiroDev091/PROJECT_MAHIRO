def command(input_value, thread_userid=None):
    import requests
    import json
    config = {
        "name": "sim",
        "version": "1.0.1",
        "description": "Talk to sim. (PH)",
        "credits": "Kenlie Jugarap",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        try:
            talk = input_value[len(config['name']):].strip()
            if talk != '':
                talk2 = requests.get('https://simsimi.fun/api/v2/?mode=talk&lang=ph&message={}&filter=true'.format(talk))
                decoded_response = json.loads(talk2.content.decode('utf-8-sig'))
                return {"messages": [str(decoded_response['success'])]}
            else:
                return {"messages": ["❌Missing parameter."]}
        except Exception as e:
            return {"messages": ["❌Error fetching response."]}
    else:
        return {'messages': [f"Default option in {config['name']}: {config['description']}"]}
