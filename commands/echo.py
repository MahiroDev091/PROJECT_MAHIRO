def command(input_value, thread_userid=None):
    config = {
        "name": "echo",
        "version": "1.0.0",
        "description": "make what you say.",
        "credits": "Mahiro chan",
        "cooldown": "2"
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        argument = input_value[len(config['name']):].strip()
        return {'messages': [argument if argument else f"Default option in {config['name']}: {config['description']}"]}
    else:
        return {'messages': [f"Default option in {config['name']}: {config['description']}"]}