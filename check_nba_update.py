import requests
from datetime import datetime
from pathlib import Path

url = "https://cdn.nba.com/static/json/staticData/EliasGameStats/00/all_players_day.txt"
state_file = Path("nba_last_update.txt")

# Get last modification time from header
r = requests.head(url)
last_modified = r.headers.get("Last-Modified")

# If header missing, fallback to simple hash
if not last_modified:
    import hashlib
    r = requests.get(url)
    last_modified = hashlib.sha256(r.content).hexdigest()

# Load previous record (if any)
previous = state_file.read_text().strip() if state_file.exists() else ""

if previous != last_modified:
    print(f"✅ NBA file updated! ({datetime.now():%Y-%m-%d %H:%M})")
    state_file.write_text(last_modified)
else:
    print("🟢 No change detected.")
