def command(input_value):
    config = {
        "name": "mahiro",
        "description": "developer."
    }

    if input_value == "__config__":
        return config
    elif input_value.startswith(config['name'] + ' ') or input_value == config['name']:
    	return "DEVELOPED BY MAHIRO CHAN"
    else:
        return f"Default option in {config['name']}: {config['description']}"
