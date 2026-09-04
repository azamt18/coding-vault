import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TZ = "Asia/Tashkent"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, "token.json")
CREDS_PATH = os.path.join(SCRIPT_DIR, "credentials.json")

DAYS = [date(2026, 8, 19), date(2026, 8, 20), date(2026, 8, 21)]

BLOCKS = [
    ("09:00", "09:45", "📖 Book: Beyond Cracking the Coding Interview"),
    ("10:00", "11:00", "🎯 .NET Interview Prep (Yandex)"),
    ("11:15", "12:00", "🎓 EPAM .NET Mentoring Course (Learn Portal)"),
    ("13:00", "14:00", "💻 LeetCode — Yandex prep"),
    ("14:15", "14:45", "🤖 AIST Program tasks"),
    ("15:00", "15:30", "🚀 Gemini AI Hackathon"),
]


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


def make_datetime(day: date, time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    dt = datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(TZ))
    return dt.isoformat()


def event_exists(service, day: date, title: str) -> bool:
    start = make_datetime(day, "00:00")
    end = make_datetime(day, "23:59")
    result = service.events().list(
        calendarId="primary",
        timeMin=start,
        timeMax=end,
        q=title,
        singleEvents=True,
    ).execute()
    return any(e.get("summary") == title for e in result.get("items", []))


def create_event(service, day: date, start: str, end: str, title: str):
    body = {
        "summary": title,
        "start": {"dateTime": make_datetime(day, start), "timeZone": TZ},
        "end": {"dateTime": make_datetime(day, end), "timeZone": TZ},
        "status": "confirmed",
        "transparency": "opaque",
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 5}],
        },
    }
    return service.events().insert(calendarId="primary", body=body).execute()


def main():
    service = build("calendar", "v3", credentials=get_credentials())
    for day in DAYS:
        print(f"\n── {day.strftime('%A %b %d')} ──")
        for start, end, title in BLOCKS:
            if event_exists(service, day, title):
                print(f"  SKIP (exists)  {start} {title}")
                continue
            event = create_event(service, day, start, end, title)
            link = event.get("htmlLink", "")
            print(f"  CREATED  {start} {title}\n           {link}")


if __name__ == "__main__":
    main()
