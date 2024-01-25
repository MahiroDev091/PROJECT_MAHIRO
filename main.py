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
			print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE FINDING 'configuration.json'.\033[0m")
			sys.exit()
except json.decoder.JSONDecodeError:
			print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE READING THE JSON FILE.\033[0m")
			sys.exit()

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
                if isinstance(config, dict) and 'name' in config and 'description' in config  and 'cooldown' in config and 'version' in config and 'credits' in config:
                    command_name = config['name']
                    command_description = config['description']
                    command_cooldown = int(config['cooldown'])
                    command_version = config['version']
                    command_credits = config['credits']
                    available_commands.append((command_name, command_description, command_cooldown, command_version, command_credits))
    return available_commands

class MessBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_commands = get_available_commands("commands")
        self.cooldowns = {} 
        self.cooldown_flag = True
        self.cooldown_flag_2 = True

    def sendmessage(self, author_id, thread_id, thread_type, reply):
        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            with open('configuration.json') as f:
                configuration = json.load(f)

            msg = message_object.text.lower()
            rainbow_light_text_print("[ [ MESSAGE ] ] " + msg)
            prefix = str(configuration['CONFIG']['BOT_INFO']['PREFIX'])
            prefixs = ("prefix", "PREFIX", "Mahiro", "MAHIRO", "Prefix")
            if any(msg.startswith(prefix) for prefix in prefixs):
                reply = f"𝚃𝚢𝚙𝚎 '{prefix}𝚕𝚒𝚜𝚝' 𝚝𝚘 𝚜𝚑𝚘𝚠 𝚊𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜."
                self.sendmessage(author_id, thread_id, thread_type, reply)

            file_path = "commands"
            if self.cooldown_flag_2:
                for loop_command_name, command_description, cooldown_count, _, _ in self.available_commands:
                    if msg.startswith(str(prefix) + loop_command_name):
                        if loop_command_name in self.cooldowns and not self.cooldowns[loop_command_name]:
                            reply = "Too fast, please wait for a bit."
                            self.sendmessage(author_id, thread_id, thread_type, reply)
                            return

                        self.cooldowns.setdefault(loop_command_name, True)
                        self.cooldown_flag_2 = False
                        command_option = import_command_option(os.path.join(file_path, f"{loop_command_name}.py"))
                        if command_option:
                            argument = msg[len(str(prefix) + loop_command_name):].strip()
                            sender_name = self.fetchUserInfo(author_id)[author_id]
                            response = command_option(f"{loop_command_name} {argument}", thread_userid=sender_name)
                            if 'messages' in response:
                            	for text_message in response['messages']:
                            		self.sendmessage(author_id, thread_id, thread_type, str(text_message))
                            if 'sendfromurl' in response:
                            	for file_url in response['sendfromurl']:
                            		self.sendRemoteFiles(file_urls=file_url, message=None, thread_id=thread_id, thread_type=thread_type)
                            if 'images' in response:
                            	for image_path in response['images']:
                            		self.sendLocalImage(
    image_path,message=None,thread_id=thread_id,thread_type=thread_type)
                            def reset_cooldown2():
                                self.cooldowns.setdefault(loop_command_name, False)
                                self.cooldown_flag_2 = True 
                            threading.Timer(cooldown_count, reset_cooldown2).start()
                            return
                        else:
                            reply = f"Error loading command '{loop_command_name}'. Ignoring."
                            self.sendmessage(author_id, thread_id, thread_type, reply)
                            return
            if msg.startswith(f"{prefix}info"):
            	search = str(msg[len(prefix) + len("info "):])
            	found_command = None
            	for command in self.available_commands:
            		if command[0] == search:
            			found_command = command
            			break
            	if found_command:
            		reply = f"""⇒ Name: {command[0]}
⇒ Version: {command[3] if command[3] else "No data!"}
⇒ Description: {command[1] if command[1] else "No data!"}
⇒ Cooldown: {command[2]}s
⇒ Credits: {command[4] if command[4] else "No data!"}"""
            		self.sendmessage(author_id, thread_id, thread_type, reply)
            	else:
            		reply = "❌𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝙽𝙾𝚃 𝙵𝙾𝚄𝙽𝙳!"
            		self.sendmessage(author_id, thread_id, thread_type, reply)
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
                    reply = f"𝙿𝚁𝙾𝙹𝙴𝙲𝚃 𝙼𝙰𝙷𝙸𝚁𝙾 - 𝙿𝙰𝙶𝙴 {page_number}\n" + "\n".join([f"╭─❍\n➠ {prefix}{name}: {description if description else 'No data!'}\n╰───────────⟡" for name, description, _, _, _ in current_page_commands] + [f"""╭─❍\n➠{prefix}setprefix: Change the prefix of the bot[ADMIN ONLY].\n╰───────────⟡"""])
                    if end_index < len(self.available_commands):
                        reply += f"\nUse `{prefix}list {page_number + 1}` to view the next page."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
                    image_path = "commands/images/mahiro.jpeg"
                    self.sendLocalImage(
    image_path,message=Message(text="All available commands."),thread_id=thread_id,thread_type=thread_type)
                else:
                    reply = "𝙽𝚘 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚏𝚘𝚞𝚗𝚍 𝚘𝚗 𝚝𝚑𝚎 𝚜𝚙𝚎𝚌𝚒𝚏𝚒𝚎𝚍 𝚙𝚊𝚐𝚎."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
            greetings = ("hi", "Hi", "hello", "Hello", "hi!", "Hi!", "hello!", "Hello!")
            if self.cooldown_flag:
                if any(msg.startswith(greeting) for greeting in greetings):
                	self.cooldown_flag = False
                	sender_name = self.fetchUserInfo(author_id)[author_id].name
                	reply = f"Hello, {sender_name}!"
                	self.sendmessage(author_id, thread_id, thread_type, reply)
                	def reset_cooldown():
                	   self.cooldown_flag = True
                	try:
                		threading.Timer(3, reset_cooldown).start()
                	except:
                		self.cooldown_flag = True
            else:
                reply = "Too fast, please wait for a bit."
                self.sendmessage(author_id, thread_id, thread_type, reply)
            if msg.startswith(f"{prefix}setprefix"):
            	if author_id in configuration['CONFIG']['BOT_INFO']['ADMIN_ID']:
            		new = msg[len(prefix)+10:]
            		if new == "" or " " in new or len(new) != 1:
            			reply = "❌𝙿𝚁𝙴𝙵𝙸𝚇 𝙼𝚄𝚂𝚃 𝙷𝙰𝚅𝙴 𝚅𝙰𝙻𝚄𝙴 𝙰𝙽𝙳 𝙳𝙾𝙴𝚂𝙽'𝚃 𝙷𝙰𝚅𝙴 𝚂𝙿𝙰𝙲𝙴 𝙰𝙽𝙳 𝙾𝙽𝙻𝚈 𝙾𝙽𝙴 𝚂𝚈𝙼𝙱𝙾𝙻/𝙻𝙴𝚃𝚃𝙴𝚁."
            			self.sendmessage(author_id, thread_id, thread_type, reply)
            		else:
            			with open("configuration.json", "r") as jsonFile:
            				data = json.load(jsonFile)
            			data['CONFIG']['BOT_INFO']['PREFIX'] = str(new)
            			with open("configuration.json", "w") as jsonFile:
            				json.dump(data, jsonFile, indent=3)
            			reply = f"✅𝙿𝚁𝙴𝙵𝙸𝚇 𝚆𝙰𝚂 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳.\n𝙽𝙴𝚆 𝙿𝚁𝙴𝙵𝙸𝚇: {new}" 
            			self.sendmessage(author_id, thread_id, thread_type, reply)
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
    
def convert_bool(value):
    if isinstance(value, str) and value.lower() == 'false':
        return False
    elif isinstance(value, list):
        return [convert_bool(item) for item in value]
    elif isinstance(value, dict):
        return {key: convert_bool(val) for key, val in value.items()}
    else:
        return value

def login_and_start_listener():
    with open('configuration.json') as f:
        configuration = json.load(f)

    try:
        os.system("clear")
        try:
            with open(configuration['CONFIG']['BOT_INFO']['APPSTATE'], 'r') as file:
                data = json.loads(file.read())
        except json.JSONDecodeError:
            print("\033[91m[ [ APPSTATE ] ] ERROR: Unable to decode JSON in '{}'.\033[0m".format(str(configuration['CONFIG']['BOT_INFO']['APPSTATE'])))
            sys.exit()
        except FileNotFoundError:
            print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE FINDING '{}'.\033[0m".format(configuration['CONFIG']['BOT_INFO']['APPSTATE']))

        if not data:
            sys.exit("\033[91m[ [ APPSTATE ] ] YOUR {} DOESN'T HAVE CONTENT. \033[0m".format(str(configuration['CONFIG']['BOT_INFO']['APPSTATE'])))
        else:
            converted_data = convert_bool(data)
            session_cookies = {item["key"]: item["value"] for item in converted_data}
            rainbow_light_text_print("[ [ NAME ] ] PROJECT MAHIRO V1")
            rainbow_light_text_print("[ [ VERSION ] ] Version: 1.1.2")
            time.sleep(0.5)
            rainbow_light_text_print("[ [ PLATFORM VERSION ] ] {}".format(platform.version()))
            rainbow_light_text_print("[ [ DESCRIPTION ] ] A Facebook Messenger Bot developed by Mahiro chan")

        if str(configuration['CONFIG']['BOT_INFO']['PREFIX']) == "" or " " in configuration['CONFIG']['BOT_INFO']['PREFIX'] or len(configuration['CONFIG']['BOT_INFO']['PREFIX']) != 1:
            sys.exit("\033[91m[ [ ERROR ] ] PLEASE CHECK THE PREFIX, PREFIX MUST HAVE VALUE AND DOESN'T HAVE SPACE AND ONLY ONE SYMBOL/LETTER. \033[0m")
        else:
            try:
                bot = MessBot(' ', ' ', session_cookies=session_cookies)
                rainbow_light_text_print("[ [ CONNECTING ] ] {}".format(str(bot.isLoggedIn()).upper()))
            except Exception as e:
                print("\033[91m[ [ ERROR ] ]   {} \033[0m".format(e))
            try:
                listener_thread = threading.Thread(target=bot.listen)
                listener_thread.start()
                rainbow_light_text_print("[ [ SUCCESS ] ] BOT IS  SUCCESSFULLY ACTIVATED!")
            except:
                listener_thread = threading.Thread(target=bot.listen)
                listener_thread.start()

    except Exception as e:
        print("\033[91m[ [ ERROR ] ]   {} \033[0m".format(e))
        
if __name__ == "__main__":
	login_and_start_listener()
