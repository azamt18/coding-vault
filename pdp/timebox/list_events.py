import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TZ = "Asia/Tashkent"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, "token.json")

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            CREDS_PATH = os.path.join(SCRIPT_DIR, "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds

def make_datetime(day: date, time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    dt = datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(TZ))
    return dt.isoformat()

service = build("calendar", "v3", credentials=get_credentials())

# Fetch all calendars
calendars = service.calendarList().list().execute().get("items", [])
print(f"Calendars found: {[c.get('summary') for c in calendars]}\n")

DAYS = [date(2026, 8, 19), date(2026, 8, 20), date(2026, 8, 21)]

# Collect all events across all calendars per day
for day in DAYS:
    all_events = []
    for cal in calendars:
        cal_id = cal["id"]
        cal_name = cal.get("summary", cal_id)
        try:
            result = service.events().list(
                calendarId=cal_id,
                timeMin=make_datetime(day, "00:00"),
                timeMax=make_datetime(day, "23:59"),
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            for e in result.get("items", []):
                s = e.get("start", {}).get("dateTime", e.get("start", {}).get("date", ""))
                en = e.get("end", {}).get("dateTime", e.get("end", {}).get("date", ""))
                st = s[11:16] if len(s) > 10 else "allday"
                et = en[11:16] if len(en) > 10 else ""
                all_events.append((st, et, e.get("summary", "(no title)"), cal_name))
        except Exception:
            pass

    all_events.sort()
    print(f"── {day.strftime('%A %b %d')} ({len(all_events)} events) ──")
    for st, et, title, cal_name in all_events:
        print(f"  {st}-{et}  {title}  [{cal_name}]")
    print()
