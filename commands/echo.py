def command(input_value):
    config = {
        "name": "echo",
        "description": "make what you say."
    }
    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name']):
        argument = input_value[len(config['name']):].strip()
        return argument if argument else f"Default option in {config['name']}: {config['description']}"
    else:
        return f"Default option in {config['name']}: {config['description']}"
