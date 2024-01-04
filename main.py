from flask import Flask, render_template, url_for, request
import requests
from fbchat import Client
from fbchat.models import *
import os
import json
import sys
import time
import importlib.util
import platform
import threading

try:
    with open('configuration.json') as f:
        configuration = json.load(f)
except FileNotFoundError:
    print(
        "\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE FINDING 'configuration.json'.\033[0m")
    sys.exit()
except json.decoder.JSONDecodeError:
    print(
        "\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE READING THE JSON FILE.\033[0m")
    sys.exit()


def import_command_option(file_path):
    try:
        spec = importlib.util.spec_from_file_location("module_name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'command') and callable(module.command):
            return module.command
        else:
            return None
    except Exception as e:
        print(f"Error loading module from '{file_path}': {e}")
        return None


def import_command_option(file_path):
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, 'command') and callable(module.command):
        return module.command
    else:
        return None


def get_available_commands(folder_path):
    available_commands = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)
            command_option = import_command_option(file_path)
            if command_option:
                config = command_option("__config__")
                if isinstance(config, dict) and 'name' in config and 'description' in config:
                    command_name = config['name']
                    command_description = config['description']
                    available_commands.append(
                        (command_name, command_description))
    return available_commands


def run_selected_command(selected_command, folder_path):
    for command_name, command_description in get_available_commands(folder_path):
        if selected_command.startswith(command_name):
            command_option = import_command_option(
                os.path.join(folder_path, f"{command_name}.py"))
            if command_option:
                argument = selected_command[len(command_name):].strip()
                result = command_option(f"{command_name} {argument}")
                print(result)
                return
            else:
                print(f"Error loading command '{selected_command}'. Ignoring.")
                return
    print(f"Command '{selected_command}' not found")


class MessBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_commands = get_available_commands("commands")

    def sendmessage(self, author_id, thread_id, thread_type, reply):
        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            global cooldown_flag
            with open('configuration.json') as f:
                configuration = json.load(f)

            msg = message_object.text.lower()
            rainbow_light_text_print("[ [ MESSAGE ] ] " + msg)
            prefix = str(configuration['CONFIG']['BOT_INFO']['PREFIX'])
            prefix = str(configuration['CONFIG']['BOT_INFO']['PREFIX'])
            prefixs = ("prefix", "PREFIX", "Mahiro", "MAHIRO", "Prefix")
            if any(msg.startswith(prefix) for prefix in prefixs):
                reply = f"𝚃𝚢𝚙𝚎 '{prefix}𝚕𝚒𝚜𝚝' 𝚝𝚘 𝚜𝚑𝚘𝚠 𝚊𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜."
                self.sendmessage(author_id, thread_id, thread_type, reply)
            file_path = "commands"

            for loop_command_name, command_description in self.available_commands:
                if msg.startswith(str(prefix) + loop_command_name):
                    command_option = import_command_option(
                        os.path.join(file_path, f"{loop_command_name}.py"))
                    if command_option:
                        argument = msg[len(
                            str(prefix) + loop_command_name):].strip()
                        result = command_option(
                            f"{loop_command_name} {argument}")
                        self.sendmessage(author_id, thread_id,
                                         thread_type, result)
                        return
                    else:
                        reply = f"Error loading command '{loop_command_name}'. Ignoring."
                        self.sendmessage(author_id, thread_id,
                                         thread_type, reply)
            if msg.startswith(f"{prefix}list"):
                commands_per_page = 3
                page_number = 1

                try:
                    page_number = int(msg[len(prefix) + len("list "):])
                except ValueError:
                    pass
                start_index = (page_number - 1) * commands_per_page
                end_index = start_index + commands_per_page
                current_page_commands = self.available_commands[start_index:end_index]

                if current_page_commands:
                    reply = f"𝙿𝚁𝙾𝙹𝙴𝙲𝚃 𝙼𝙰𝙷𝙸𝚁𝙾 - 𝙿𝙰𝙶𝙴 {page_number}\n" + "\n".join([f"╭─❍\n➠ {prefix}{name}: {description}\n╰───────────⟡" for name, description in current_page_commands] + [
                                                                                 f"""╭─❍\n➠{prefix}setprefix: Change the prefix of the bot[ADMIN ONLY].\n╰───────────⟡"""])
                    if end_index < len(self.available_commands):
                        reply += f"\nUse `{prefix}list {page_number + 1}` to view the next page."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
                    image_path = "commands/images/mahiro.jpeg"
                    self.sendLocalImage(
                        image_path, message=Message(text=""), thread_id=thread_id, thread_type=thread_type)
                else:
                    reply = "𝙽𝚘 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚏𝚘𝚞𝚗𝚍 𝚘𝚗 𝚝𝚑𝚎 𝚜𝚙𝚎𝚌𝚒𝚏𝚒𝚎𝚍 𝚙𝚊𝚐𝚎."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
            greetings = ("hi", "Hi", "hello", "Hello",
                         "hi!", "Hi!", "hello!", "Hello!")
            if cooldown_flag:
                if any(msg.startswith(greeting) for greeting in greetings):
                    cooldown_flag = False
                    sender_name = self.fetchUserInfo(author_id)[author_id].name
                    reply = f"Hello, {sender_name}!"
                    self.sendmessage(author_id, thread_id, thread_type, reply)

                    def reset_cooldown():
                        global cooldown_flag
                        cooldown_flag = True
                    threading.Timer(3, reset_cooldown).start()
            else:
                reply = "Too fast, please wait for a bit."
                self.sendmessage(author_id, thread_id, thread_type, reply)
            if msg.startswith(f"{prefix}setprefix"):
                if author_id in configuration['CONFIG']['BOT_INFO']['ADMIN_ID']:
                    new = msg[len(prefix)+10:]
                    if new == "" or " " in new or len(new) != 1:
                        reply = "❌𝙿𝚁𝙴𝙵𝙸𝚇 𝙼𝚄𝚂𝚃 𝙷𝙰𝚅𝙴 𝚅𝙰𝙻𝚄𝙴 𝙰𝙽𝙳 𝙳𝙾𝙴𝚂𝙽'𝚃 𝙷𝙰𝚅𝙴 𝚂𝙿𝙰𝙲𝙴 𝙰𝙽𝙳 𝙾𝙽𝙻𝚈 𝙾𝙽𝙴 𝚂𝚈𝙼𝙱𝙾𝙻/𝙻𝙴𝚃𝚃𝙴𝚁."
                        self.sendmessage(author_id, thread_id,
                                         thread_type, reply)
                    else:
                        with open("configuration.json", "r") as jsonFile:
                            data = json.load(jsonFile)
                        data['CONFIG']['BOT_INFO']['PREFIX'] = str(new)
                        with open("configuration.json", "w") as jsonFile:
                            json.dump(data, jsonFile, indent=3)
                        reply = f"✅𝙿𝚁𝙴𝙵𝙸𝚇 𝚆𝙰𝚂 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳.\n𝙽𝙴𝚆 𝙿𝚁𝙴𝙵𝙸𝚇: {new}"
                        self.sendmessage(author_id, thread_id,
                                         thread_type, reply)
                else:
                    reply = "❌𝙾𝙽𝙻𝚈 𝙰𝙳𝙼𝙸𝙽 𝙲𝙰𝙽 𝙰𝙲𝙲𝙴𝚂𝚂 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
        except Exception as e:
            print(f"Error: {e}")


def rainbow_light_text_print(text, end='\n'):
    colors = [
        "\033[91m",
        "\033[93m",
        "\033[92m",
        "\033[96m",
        "\033[94m",
        "\033[95m",
    ]

    num_steps = len(colors)

    for i, char in enumerate(text):
        color_index = i % num_steps
        print(f"{colors[color_index]}{char}", end="")

    print("\033[0m", end=end)


app = Flask(__name__)
listener_started = False
listener_lock = threading.Lock()
listener_thread = None
cooldown_flag = True


def login_and_start_listener():
    global listener_started, listener_thread

    if listener_started:
        return render_template('mahiro.html', status="Bot is already active!")

    with listener_lock:
        if listener_started:
            return render_template('mahiro.html', status="Bot is already active!")

        listener_started = True
        with open('configuration.json') as f:
            configuration = json.load(f)

    try:
        os.system("clear")
        try:
            with open(configuration['CONFIG']['BOT_INFO']['APPSTATE'], 'r') as file:
                data = json.loads(file.read())
        except json.JSONDecodeError:
            print("\033[91m[ [ APPSTATE ] ] ERROR: Unable to decode JSON in '{}'.\033[0m".format(
                str(configuration['CONFIG']['BOT_INFO']['APPSTATE'])))
            sys.exit()
        except FileNotFoundError:
            print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE FINDING '{}'.\033[0m".format(
                configuration['CONFIG']['BOT_INFO']['APPSTATE']))
            sys.exit()

        if not data:
            sys.exit("\033[91m[ [ APPSTATE ] ] YOUR {} DOESN'T HAVE CONTENT. \033[0m".format(
                str(configuration['CONFIG']['BOT_INFO']['APPSTATE'])))
        else:
            cookie = '; '.join([f"{entry['key']}={entry['value']}" for entry in data if entry['key'] in {
                               'c_user', 'xs', 'fr', 'datr'}])
            key_value_pairs = [pair.strip() for pair in cookie.split(";")]
            session_cookies = {key: value for key, value in (
                pair.split("=") for pair in key_value_pairs)}
            rainbow_light_text_print("[ [ NAME ] ] PROJECT MAHIRO V1")
            rainbow_light_text_print("[ [ VERSION ] ] Version: 1.0.1")
            time.sleep(0.5)
            rainbow_light_text_print(
                "[ [ PLATFORM VERSION ] ] {}".format(platform.version()))
            full_url = url_for('index', _external=True, _scheme='https')
            rainbow_light_text_print("[ [ MAHIRO ] ] " + full_url)
            rainbow_light_text_print("[ [ UPTIME ] ] " + requests.get(
                'https://y7sj8t-2792.csb.app/ping?url='+full_url).json()['message'].upper())
            rainbow_light_text_print(
                "[ [ DESCRIPTION ] ] A Facebook Messenger Bot developed by Mahiro chan")

        if str(configuration['CONFIG']['BOT_INFO']['PREFIX']) == "" or " " in configuration['CONFIG']['BOT_INFO']['PREFIX'] or len(configuration['CONFIG']['BOT_INFO']['PREFIX']) != 1:
            sys.exit(
                "\033[91m[ [ ERROR ] ] PLEASE CHECK THE PREFIX, PREFIX MUST HAVE VALUE AND DOESN'T HAVE SPACE AND ONLY ONE SYMBOL/LETTER. \033[0m")
        else:
            try:
                bot = MessBot(' ', ' ', session_cookies=session_cookies)
                rainbow_light_text_print(
                    "[ [ CONNECTING ] ] {}".format(str(bot.isLoggedIn()).upper()))
            except Exception as e:
                listener_started = False
                return render_template('mahiro.html', status="An error encountered during login.")

        if not listener_thread:
            try:
                listener_thread = threading.Thread(target=bot.listen)
                listener_thread.start()
                return render_template('mahiro.html', status="Bot is successfully activated!")
            except:
                listener_thread = threading.Thread(target=bot.listen)
                listener_thread.start()

    except Exception as e:
        print(f"Error during login: {e}")
        return render_template('mahiro.html', status="Error during login.")


@app.route('/')
def index():
    return login_and_start_listener()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
