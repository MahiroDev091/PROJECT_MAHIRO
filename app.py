from main import rainbow_light_text_print
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
        rainbow_light_text_print("[ RESTARTING ] PLEASE WAIT FOR A MOMENT..")

if __name__ == "__main__":
    server = Thread(target=app.run, kwargs={'host': "0.0.0.0", 'port': 8000})
    server.start()
    run() 
    server.join()