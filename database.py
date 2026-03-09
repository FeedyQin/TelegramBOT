import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "db.json")

def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_warns(chat_id, user_id):
    db = load_db()
    return db.get("warns", {}).get(f"{chat_id}_{user_id}", [])

def add_warn(chat_id, user_id, reason, by):
    db = load_db()
    if "warns" not in db:
        db["warns"] = {}
    key = f"{chat_id}_{user_id}"
    if key not in db["warns"]:
        db["warns"][key] = []
    db["warns"][key].append({"reason": reason, "by": by, "date": datetime.now().isoformat()})
    save_db(db)
    return len(db["warns"][key])

def remove_warn(chat_id, user_id):
    db = load_db()
    key = f"{chat_id}_{user_id}"
    warns = db.get("warns", {}).get(key, [])
    if warns:
        db["warns"][key] = warns[:-1]
        save_db(db)
    return len(db.get("warns", {}).get(key, []))

def clear_warns(chat_id, user_id):
    db = load_db()
    key = f"{chat_id}_{user_id}"
    if "warns" in db and key in db["warns"]:
        db["warns"][key] = []
        save_db(db)

def get_flood_data(chat_id, user_id):
    db = load_db()
    return db.get("flood", {}).get(f"flood_{chat_id}_{user_id}", {"count": 0, "last_time": None})

def update_flood(chat_id, user_id, count, last_time):
    db = load_db()
    if "flood" not in db:
        db["flood"] = {}
    db["flood"][f"flood_{chat_id}_{user_id}"] = {"count": count, "last_time": last_time}
    save_db(db)

def get_welcome(chat_id):
    db = load_db()
    return db.get("welcome", {}).get(str(chat_id), "🔥 {name} ENTERED THE TEMPLE. GOD SEES ALL. WELCOME TO {chat}.")

def set_welcome(chat_id, text):
    db = load_db()
    if "welcome" not in db:
        db["welcome"] = {}
    db["welcome"][str(chat_id)] = text
    save_db(db)

def get_notes(chat_id):
    db = load_db()
    return db.get("notes", {}).get(str(chat_id), {})

def set_note(chat_id, name, text):
    db = load_db()
    if "notes" not in db:
        db["notes"] = {}
    if str(chat_id) not in db["notes"]:
        db["notes"][str(chat_id)] = {}
    db["notes"][str(chat_id)][name.lower()] = text
    save_db(db)

def del_note(chat_id, name):
    db = load_db()
    notes = db.get("notes", {}).get(str(chat_id), {})
    if name.lower() in notes:
        del notes[name.lower()]
        db["notes"][str(chat_id)] = notes
        save_db(db)
        return True
    return False

def get_stats(chat_id, user_id):
    db = load_db()
    return db.get("stats", {}).get(f"{chat_id}_{user_id}", {"messages": 0, "commands": 0, "joined": None})

def increment_stats(chat_id, user_id, field="messages"):
    db = load_db()
    if "stats" not in db:
        db["stats"] = {}
    key = f"{chat_id}_{user_id}"
    if key not in db["stats"]:
        db["stats"][key] = {"messages": 0, "commands": 0, "joined": datetime.now().isoformat()}
    db["stats"][key][field] = db["stats"][key].get(field, 0) + 1
    save_db(db)
