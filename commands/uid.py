def command(input_value, thread_userid=None):
    config = {
        "name": "uid",
        "version": "1.0.0",
        "description": "Get your uid.",
        "credits": "Mahiro chan",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        argument = input_value[len(config['name']):].strip()
        
        return {'messages': [f"Hi, {thread_userid.name}\nYOUR UID: {thread_userid.uid}"]}
    else:
        return {'messages': [f"Default option in {config['name']}: {config['description']}"]}