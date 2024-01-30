import os
import json

with open('configuration.json') as f:
	required_libraries = json.load(f)['CONFIG']['BOT_INFO']['PACKAGE']
	
def install_library(library_name):
    os.system(f'pip3 install {library_name}')

for library in required_libraries:
    try:
        exec(f'import {library}')
    except ImportError:
        print(f"{library} is not installed. Installing...")
        install_library(library)

from pystyle import Colors, Colorate
from flask import Flask, render_template
from threading import Thread
import subprocess
import time

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("mahiro.html", status="Bot is active!")

def run():
    while True:
        script_path = 'main.py'
        process = subprocess.Popen(["python3", script_path])
        process.wait()
        time.sleep(1)
        print(Colorate.Horizontal(Colors.rainbow, "[ RESTARTING ] PLEASE WAIT FOR A MOMENT..", 1))

if __name__ == "__main__":
    server = Thread(target=app.run, kwargs={'host': "0.0.0.0", 'port': 8000})
    server.start()
    run() 
    server.join()