import json
from pathlib import Path

# مسار ملف الـ JSON المحلي
CONFIG_FILE = Path.home() / ".VibeCap" / "config.json"

def save_api_key(api_key: str):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"GROQ_API_KEY": api_key}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_api_key():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("GROQ_API_KEY")
        except Exception:
            pass
    return None

def get_api_key(cli_key=None):
    if cli_key:
        save_api_key(cli_key)
        return cli_key
    
    return load_api_key()