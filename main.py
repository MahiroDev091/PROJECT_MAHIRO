#HI! THIS BOT WAS MADE BY ME(MAHIRO) AND WITH HELP OF MY FRIEND (KENLIE) - DO NOT STEAL MY CODE :l
from flask import Flask, render_template, url_for, request
from pystyle import Colors, Colorate
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
import sqlite3

filename2 = 'configuration.json'

try:
				with open(filename2, 'r') as f:
					configuration = json.load(f)
except FileNotFoundError:
			print("\033[1m\033[91mSORRY, AN ERROR ENCOUNTERED WHILE FINDING {}.\033[0m".format(filename2.upper()))
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
                if isinstance(config, dict) and 'name' in config and 'description' in config  and 'cooldown' in config and 'version' in config and 'credits' in config and 'usages' in config:
                    command_name = config['name'].lower()
                    command_description = config['description'].title()
                    command_cooldown = int(config['cooldown'])
                    command_version = config['version']
                    command_credits = config['credits'].title()
                    command_usages = config['usages'].lower()
                    available_commands.append((command_name, command_description, command_cooldown, command_version, command_credits, command_usages))
    return available_commands

class MessBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_commands = get_available_commands("commands")
        self.cooldowns = {} 
        self.cooldown_dict = {}

    def sendmessage(self, author_id, thread_id, thread_type, reply):
        if author_id != self.uid:
            with open(filename2, 'r') as f:
                configuration = json.load(f)
            if str(configuration['CONFIG']['BOT_INFO']['SET_TYPING']).upper() != "FALSE":
                self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
                time.sleep(0.3)
                self.setTypingStatus(TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
            else:
                self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                
    def CurrenciesUserData(self, user_id):
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM currencies WHERE uid=?', (user_id,))
        found_command = cursor.fetchone()
        if found_command is not None:
            amount = found_command[1]
        else:
            cursor.execute('''INSERT INTO currencies (uid, amount) VALUES (?, ?)''', (user_id, 0))
            amount = 0
        conn.commit()
        conn.close()
        return amount

    def update_currency(self, user_id, new_amount):
        try:
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM currencies WHERE uid=?', (user_id,))
            found_amount = cursor.fetchone()
            
            if found_amount is not None:
                cursor.execute('''UPDATE currencies SET amount = ? WHERE uid = ?''', (new_amount, user_id))
                result = "SUCCESS"
                conn.commit()
                conn.close()
            else:
                result = "CANNOT FIND UID!"
                
        except Exception as e:
            result = str(e)

        return result

    def CurrenciesDecreaseMoney(self, user_id, amount):
        current_amount = self.CurrenciesUserData(user_id)
        deducted = int(max(current_amount - amount, 0))
        return self.update_currency(user_id, deducted)

    def CurrenciesIncreaseMoney(self, user_id, amount):
        current_amount = self.CurrenciesUserData(user_id)
        increase = int(current_amount + amount)
        return self.update_currency(user_id, increase)

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            with open(filename2, 'r') as f:
                configuration = json.load(f)

            msg = message_object.text.lower()
            print(Colorate.Horizontal(Colors.rainbow, "[ [ MESSAGE ] ] " + msg, 1))
            
            prefix = str(configuration['CONFIG']['BOT_INFO']['PREFIX'])
            prefixs = ("prefix", "PREFIX", "Mahiro", "MAHIRO", "Prefix")
            if any(msg.startswith(prefix) for prefix in prefixs):
                reply = f"𝚃𝚢𝚙𝚎 '{prefix}𝚕𝚒𝚜𝚝' 𝚝𝚘 𝚜𝚑𝚘𝚠 𝚊𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜."
                self.sendmessage(author_id, thread_id, thread_type, reply)

            file_path = "commands"
            current_time = time.time()
            key = thread_id
            for loop_command_name, command_description, cooldown_count, _, _, _ in self.available_commands:
                        cooldown_duration = cooldown_count
                        if msg.startswith(str(prefix) + loop_command_name):
                            if key not in self.cooldown_dict or current_time - self.cooldown_dict[key] > cooldown_duration:
                            	self.cooldown_dict[key] = current_time
                            	command_option = import_command_option(os.path.join(file_path, f"{loop_command_name}.py"))
                            	if command_option:
                            		argument = msg[len(str(prefix) + loop_command_name):].strip()
                            		sender_name = self.fetchUserInfo(author_id)[author_id]
                            		message_id = mid
                            		sender_id = author_id
                            		print(Colorate.Horizontal(Colors.rainbow, f"Message ID: {message_id}\nSender ID: {sender_id}", 1))
                            		command_option(f"{loop_command_name} {argument}", thread_id=thread_id, thread_type=thread_type, author_id=author_id, thread_prefix=configuration['CONFIG']['BOT_INFO']['PREFIX'], thread_global=configuration,  thread_user=sender_name, thread_messageid=message_id, message_object=message_object, mid=mid, bot=self)
                            	else:
                            		reply = f"Error loading command '{loop_command_name}'. Ignoring."
                            		self.sendmessage(author_id, thread_id, thread_type, reply)
                            		return
                            else:
                            	reply = "Too fast, please wait for a bit."
                            	self.sendmessage(author_id, thread_id, thread_type, reply)
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
⇒ Usages: {prefix + command[0] + ' ' +command[5] if command[5] else "No data!"}
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
                    reply = f"𝙿𝚁𝙾𝙹𝙴𝙲𝚃 𝙼𝙰𝙷𝙸𝚁𝙾 - 𝙿𝙰𝙶𝙴 {page_number}\n" + "\n".join([f"╭─❍\n➠ {prefix}{name}: {description if description else 'No data!'}\n╰───────────⟡" for name, description, _, _, _, _ in current_page_commands] + [f"""╭─❍\n➠{prefix}setprefix: Change the prefix of the bot[ADMIN ONLY].\n╰───────────⟡"""])
                    if end_index < len(self.available_commands):
                        reply += f"\nUse `{prefix}list {page_number + 1}` to view the next page."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
                    image_path = "commands/images/mahiro.jpeg"
                    self.sendLocalImage(
    image_path,message=Message(text="All available commands."),thread_id=thread_id,thread_type=thread_type)
                else:
                    reply = "𝙽𝚘 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚏𝚘𝚞𝚗𝚍 𝚘𝚗 𝚝𝚑𝚎 𝚜𝚙𝚎𝚌𝚒𝚏𝚒𝚎𝚍 𝚙𝚊𝚐𝚎."
                    self.sendmessage(author_id, thread_id, thread_type, reply)
            current_time = time.time()
            cooldown_duration = 3
            greetings = ("hi", "Hi", "hello", "Hello", "hi!", "Hi!", "hello!", "Hello!")
            key = thread_id
            if any(msg.startswith(greeting) for greeting in greetings):
                		if key not in self.cooldown_dict or current_time - self.cooldown_dict[key] > cooldown_duration:
                			self.cooldown_dict[key] = current_time
                			sender_name = self.fetchUserInfo(author_id)[author_id].name
                			reply = f"Hello, {sender_name}!"
                			self.sendmessage(author_id, thread_id, thread_type, reply)
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
            			with open(filename2, "r") as jsonFile:
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
    with open(filename2, 'r') as f:
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
            print(Colorate.Horizontal(Colors.rainbow, "[ [ NAME ] ] PROJECT MAHIRO V1", 1))
            print(Colorate.Horizontal(Colors.rainbow, "[ [ VERSION ] ] Version: 1.1.3", 1))
            time.sleep(0.5)
            print(Colorate.Horizontal(Colors.rainbow, "[ [ PLATFORM VERSION ] ] {}".format(platform.version()), 1))
            print(Colorate.Horizontal(Colors.rainbow, "[ [ DESCRIPTION ] ] A Facebook Messenger Bot developed by Mahiro chan", 1))
            print(f"\033[93m\033[1m━━━━━━━━━━━━ LOAD COMMANDS ━━━━━━━━━━━━       \033[0m")
            folder_path = 'commands'
            for filename in os.listdir(folder_path):
            	if filename.endswith('.py'):
            		file_path = os.path.join(folder_path, filename)
            		try:
            			with open(file_path, 'r') as file:
            				content = file.read()
            				config_start = content.find('config = {')
            				if config_start != -1:
            					config_end = content.find('}', config_start) + 1
            					config_str = content[config_start:config_end]
            					config_lines = config_str.split('\n')
            					for line in config_lines:
            						if 'name' in line:
            							name_value = line.split(':')[-1].strip().strip('"')
            							print(Colorate.Horizontal(Colors.rainbow, f"[ [ COMMAND ] ] LOADED {name_value.lower()} SUCCESS", 1))
            		except SyntaxError as e:
            			print(f"\033[91m[ [ COMMAND ] ] LOADED {name_value.lower()} ERROR {e}\033[0m")
            		except Exception as e:
            			print(f"\033[91m[ [ COMMAND ] ] LOADED {name_value.lower()} ERROR {e}\033[0m")
        if str(configuration['CONFIG']['BOT_INFO']['PREFIX']) == "" or " " in configuration['CONFIG']['BOT_INFO']['PREFIX'] or len(configuration['CONFIG']['BOT_INFO']['PREFIX']) != 1:
            sys.exit("\033[91m[ [ ERROR ] ] PLEASE CHECK THE PREFIX, PREFIX MUST HAVE VALUE AND DOESN'T HAVE SPACE AND ONLY ONE SYMBOL/LETTER. \033[0m")
        else:
            try:
                print(f"\033[93m\033[1m━━━━━━━━━━━━ DATABASE ━━━━━━━━━━━━       \033[0m")
                print(Colorate.Horizontal(Colors.rainbow, "[ [ DATABASE ] ] Start connecting to database.", 1))
                conn = sqlite3.connect('database/database.db')
                cursor = conn.cursor()
                cursor.execute('''
   				 CREATE TABLE IF NOT EXISTS currencies (
     			   uid INT,
   			     amount INT
				    )
				''')
                conn.commit()
                conn.close()
                print(Colorate.Horizontal(Colors.rainbow, "[ [ SUCCESS ] ] Auto generate database if the database cannot find, JUST IGNORE THIS.", 1))
                time.sleep(1)
                print(f"\033[93m\033[1m━━━━━━━━━━━━ LOGIN PROCESS ━━━━━━━━━━━━       \033[0m")
                user_agent = str(configuration['CONFIG']['BOT_INFO']['USER-AGENT'])
                bot = MessBot(' ', ' ', user_agent=user_agent if user_agent else None, max_tries=1, session_cookies=session_cookies)
                print(Colorate.Horizontal(Colors.rainbow, "[ [ CONNECTING ] ] {}".format(str(bot.isLoggedIn()).upper()), 1))
                print(Colorate.Horizontal(Colors.rainbow, "[ [ CONNECTING ] ] BOT ID: {}".format(bot.uid), 1))
            except Exception as e:
                print("\033[91m[ [ ERROR ] ]   {} \033[0m".format(e))
            try:
                listener_thread = threading.Thread(target=bot.listen)
                listener_thread.start()
                print(Colorate.Horizontal(Colors.rainbow, "[ [ SUCCESS ] ] BOT IS  SUCCESSFULLY ACTIVATED!", 1))
            except:
                listener_thread = threading.Thread(target=bot.listen)
                listener_thread.start()

    except Exception as e:
        print("\033[91m[ [ ERROR ] ]   {} \033[0m".format(e))
        
if __name__ == "__main__":
	login_and_start_listener()