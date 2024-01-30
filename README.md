# 🚀  PROJECT MAHIRO V1 BOTPACK
FACEBOOK MESSENGER BOTPACK DEVELOPED BY MAHIRO CHAN INSPIRED BY MIRAI NODEJS

- Webview added!
- Appstate method support now
- Now you can add your own commands.
- Version 1.1.3 [NEW VERSION]

NEW FEATURES ADDED:
- New configuration features added!
- New command format (Now you can use all features of __[fbchat](https://fbchat.readthedocs.io/en/stable/)__ without having any issues). 
- Cooldown issue fixed!
- Database for currencies added!
- New UI Added!

# 📷 SCREENSHOTS

<img src="screenshot/Screenshot_20240101_162318.jpg" style="height: 220px; width: 200px"></img>

# 📰 HOW TO SETUP CONFIG

```python
{
   "CONFIG": {
      "BOT_INFO": {
         "PREFIX": ".",
         "ADMIN_ID": [
            "100089164803882" - CHANGE THIS ID TO YOUR FACEBOOK ID OR JUST INSERT NEW ID.
         ],
         "USER-AGENT": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
         "SET_TYPING": "FALSE", - CHANGE THIS TO TRUE IF YOU WANT TO TURN ON TYPING INDICATOR (ANIMATION)
         "APPSTATE": "appstate.json",
         "PACKAGE": [ - IN THIS PACKAGE ARRAY THIS IS WHERE YOU WILL ADD ALL LIBRARY YOU WANT TO PIP INSTALL
 	        "flask",
           "fbchat",
           "pystyle",
     	     "requests"
         ]
      }
   }
}
```

# 💥 HOW TO USE

```python
𝙿𝚁𝙾𝙹𝙴𝙲𝚃 𝙼𝙰𝙷𝙸𝚁𝙾 - AVAILABLE COMMANDS
╭─❍
➠ .ai: ask anything
╰───────────⟡
╭─❍
➠ .echo: make what you say.
╰───────────⟡
╭─❍
➠ .mahiro: developer.
╰───────────⟡
╭─❍
➠ .arched: ask anything developed by Liane
╰───────────⟡
╭─❍
➠ .catfacts: get random catfacts everyday.
╰───────────⟡
╭─❍
➠.setprefix: Change the prefix of the bot[ADMIN ONLY].
╰───────────⟡
```
# ❤ HIGHLY CONTRIBUTE TO THIS PROJECT
```
Special Thanks to Kenlie Jugarap and Choru Tiktoker for helping me to this project!
```

# 📰 HOW TO SETUP

```python
git clone https://github.com/MahiroDev091/PROJECT_MAHIRO; cd PROJECT_MAHIRO; pip install -r requirements.txt; python3 app.py
