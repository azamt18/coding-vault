import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TZ = "Asia/Tashkent"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, "token.json")

UPDATES = [
    (date(2026, 8, 19), "🎓 EPAM .NET Mentoring Course (Learn Portal)", "11:30", "12:15", "🎓 Module 1: Help Module"),
    (date(2026, 8, 20), "🎓 EPAM .NET Mentoring Course (Learn Portal)", "13:00", "13:45", "🎓 Module 2: Multithreading in .NET"),
    (date(2026, 8, 21), "🎓 EPAM .NET Mentoring Course (Learn Portal)", "12:00", "12:45", "🎓 Module 2: Multithreading in .NET (cont.)"),
]

def make_datetime(day: date, time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    return datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(TZ)).isoformat()

def get_credentials():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

service = build("calendar", "v3", credentials=get_credentials())

for day, old_title, start_str, end_str, new_title in UPDATES:
    result = service.events().list(
        calendarId="primary",
        timeMin=make_datetime(day, "00:00"),
        timeMax=make_datetime(day, "23:59"),
        q=old_title,
        singleEvents=True,
    ).execute()
    events = [e for e in result.get("items", []) if e.get("summary") == old_title]
    if not events:
        print(f"  NOT FOUND  {day} {old_title}")
        continue
    event = events[0]
    event["summary"] = new_title
    event["start"] = {"dateTime": make_datetime(day, start_str), "timeZone": TZ}
    event["end"]   = {"dateTime": make_datetime(day, end_str),   "timeZone": TZ}
    service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()
    print(f"  UPDATED  {day.strftime('%a %b %d')}  {start_str}–{end_str}  {new_title}")
