import json
import os

FILE = "config/guild_config.json"

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_guild(guild_id):
    data = load_data()
    return data.get(str(guild_id), {
        "welcome_message": "Welcome to {server}",
        "link": ""
    })

def update_guild(guild_id, key, value):
    data = load_data()
    gid = str(guild_id)

    if gid not in data:
        data[gid] = {}

    data[gid][key] = value
    save_data(data)