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

W = date(2026, 8, 19)
TH = date(2026, 8, 20)
F = date(2026, 8, 21)

# Prayer-time-aware schedule (Asr ~13:15-13:32, Maghrib ~15:17-15:33)
SCHEDULE = {
    "📖 Book: Beyond Cracking the Coding Interview": {
        W:  ("09:00", "09:45"),
        TH: ("09:00", "09:45"),
        F:  ("09:00", "09:45"),
    },
    "🎯 Yandex Prep: Async/await & Coroutines": {
        W:  ("10:30", "11:30"),
    },
    "🎯 Yandex Prep: C#/.NET Questionnaire": {
        TH: ("10:00", "11:00"),
    },
    "🎯 Yandex Prep: WPF & Coding Tasks": {
        F:  ("11:00", "12:00"),
    },
    "🎓 Module 1: Help Module": {
        W:  ("11:30", "12:15"),
    },
    "🎓 Module 2: Multithreading in .NET": {
        TH: ("13:35", "14:20"),  # shifted: after Asr ends ~13:31
    },
    "🎓 Module 2: Multithreading in .NET (cont.)": {
        F:  ("12:00", "12:45"),
    },
    "💻 LeetCode — Yandex prep": {
        W:  ("13:35", "14:35"),  # shifted: after Asr ends ~13:32
        TH: ("14:25", "15:25"),  # cascade after mentoring shift
        F:  ("14:00", "15:00"),
    },
    "🤖 AIST Program tasks": {
        W:  ("14:45", "15:15"),  # cascade; ends before Maghrib ~15:20
        TH: ("15:35", "16:05"),  # shifted: after Maghrib ends ~15:33
        F:  ("15:35", "16:05"),  # shifted: after Maghrib ends ~15:32
    },
    "🚀 Gemini AI Hackathon": {
        W:  ("15:35", "16:05"),  # shifted: after Maghrib ends ~15:33
        TH: ("16:15", "16:45"),  # cascade
        F:  ("16:15", "16:45"),  # cascade
    },
}

def make_datetime(day: date, time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    return datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(TZ)).isoformat()

def get_credentials():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

service = build("calendar", "v3", credentials=get_credentials())

for title, day_map in SCHEDULE.items():
    for day, (start_str, end_str) in day_map.items():
        result = service.events().list(
            calendarId="primary",
            timeMin=make_datetime(day, "00:00"),
            timeMax=make_datetime(day, "23:59"),
            q=title,
            singleEvents=True,
        ).execute()
        events = [e for e in result.get("items", []) if e.get("summary") == title]
        if not events:
            print(f"  NOT FOUND  {day} {title}")
            continue
        event = events[0]
        event["start"] = {"dateTime": make_datetime(day, start_str), "timeZone": TZ}
        event["end"]   = {"dateTime": make_datetime(day, end_str),   "timeZone": TZ}
        service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()
        print(f"  UPDATED  {day.strftime('%a %b %d')}  {start_str}–{end_str}  {title}")
