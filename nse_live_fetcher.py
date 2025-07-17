import requests
import time

def get_all_indices(retries=3, delay=2):
    url = "https://www.nseindia.com/api/allIndices"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com",
    }

    for attempt in range(retries):
        try:
            session = requests.Session()
            session.get("https://www.nseindia.com", headers=headers, timeout=5)
            response = session.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                print(f"[Attempt {attempt+1}] NSE responded with {response.status_code}")
        except Exception as e:
            print(f"[Attempt {attempt+1}] Exception occurred: {e}")
        time.sleep(delay)
    print("❌ Failed to fetch indices after retries.")
    return []

def get_nifty_ltp():
    indices = get_all_indices()
    for idx in indices:
        if idx.get("index") == "NIFTY 50":
            return float(idx.get("last", 0))
    return None

def get_bank_nifty_ltp():
    indices = get_all_indices()
    for idx in indices:
        if idx.get("index") == "NIFTY BANK":
            return float(idx.get("last", 0))
    return None
