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

TH  = date(2026, 8, 20)
F   = date(2026, 8, 21)
SA  = date(2026, 8, 22)
SU  = date(2026, 8, 23)
M   = date(2026, 8, 24)
TU  = date(2026, 8, 25)
W   = date(2026, 8, 26)
TH2 = date(2026, 8, 27)
F2  = date(2026, 8, 28)
SA2 = date(2026, 8, 29)
SU2 = date(2026, 8, 30)

def make_dt(day: date, time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    return datetime(day.year, day.month, day.day, h, m, tzinfo=ZoneInfo(TZ)).isoformat()

def get_credentials():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

service = build("calendar", "v3", credentials=get_credentials())

# ── UPDATE EXISTING EVENTS (Thu Aug 20 + Fri Aug 21) ────────────────────────
UPDATES = {
    # Thu: start fresh from 14:30 (drop Book/LeetCode morning, reschedule rest)
    "🎯 Yandex Prep: C#/.NET Questionnaire":         {TH: ("14:30", "15:15")},
    "💻 LeetCode — Yandex prep":                     {TH: ("15:35", "16:35"), F: ("13:35", "14:35")},
    "🤖 AIST Program tasks":                         {TH: ("16:35", "17:05")},
    "🚀 Gemini AI Hackathon":                        {TH: ("17:05", "17:35")},
    # Fri: shift Module 2 cont. earlier to 10:00, LeetCode after Asr
    "🎓 Module 2: Multithreading in .NET (cont.)":   {F:  ("10:00", "11:00")},
}

print("── UPDATES ─────────────────────────────────────────")
for title, day_map in UPDATES.items():
    for day, (start_str, end_str) in day_map.items():
        result = service.events().list(
            calendarId="primary",
            timeMin=make_dt(day, "00:00"),
            timeMax=make_dt(day, "23:59"),
            q=title,
            singleEvents=True,
        ).execute()
        events = [e for e in result.get("items", []) if e.get("summary") == title]
        if not events:
            print(f"  NOT FOUND  {day} {title}")
            continue
        event = events[0]
        event["start"] = {"dateTime": make_dt(day, start_str), "timeZone": TZ}
        event["end"]   = {"dateTime": make_dt(day, end_str),   "timeZone": TZ}
        service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()
        print(f"  UPDATED  {day.strftime('%a %b %d')}  {start_str}–{end_str}  {title}")

# ── CREATE NEW EVENTS (Aug 22–30) ───────────────────────────────────────────
# Prayer windows (Asr ~13:10–13:32, Maghrib ~15:15–15:33) — blocks start after each ends
NEW_EVENTS = [
    # Sat Aug 22
    ("📖 Book: Beyond Cracking the Coding Interview", SA,  "09:00", "09:45"),
    ("🎓 M3: Async Programming",                      SA,  "10:00", "11:30"),
    ("🎯 Yandex Prep: Async/await & Coroutines",      SA,  "11:30", "12:30"),
    ("💻 LeetCode — Yandex prep",                     SA,  "13:35", "14:35"),
    ("🤖 AIST Program tasks",                         SA,  "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                        SA,  "16:15", "16:45"),
    # Sun Aug 23
    ("📖 Book: Beyond Cracking the Coding Interview", SU,  "09:00", "09:45"),
    ("🎓 M4: Message queues",                         SU,  "10:00", "11:30"),
    ("🎯 Yandex Prep: EF Core / Databases",           SU,  "11:30", "12:30"),
    ("💻 LeetCode — Yandex prep",                     SU,  "13:35", "14:35"),
    ("🤖 AIST Program tasks",                         SU,  "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                        SU,  "16:15", "16:45"),
    # Mon Aug 24
    ("📖 Book: Beyond Cracking the Coding Interview",  M,  "09:00", "09:45"),
    ("🎓 M5: Analyzing and profiling tools",           M,  "10:00", "11:00"),
    ("🎯 Yandex Prep: Code review tasks",              M,  "11:00", "12:00"),
    ("💻 LeetCode — Yandex prep",                      M,  "13:35", "14:35"),
    ("🤖 AIST Program tasks",                          M,  "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                         M,  "16:15", "16:45"),
    # Tue Aug 25
    ("📖 Book: Beyond Cracking the Coding Interview", TU,  "09:00", "09:45"),
    ("🎓 M6: LINQ, IQueryable",                       TU,  "10:00", "11:30"),
    ("🎯 Yandex Prep: C#/.NET Questionnaire (review)", TU, "11:30", "12:30"),
    ("💻 LeetCode — Yandex prep",                     TU,  "13:35", "14:35"),
    ("🤖 AIST Program tasks",                         TU,  "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                        TU,  "16:15", "16:45"),
    # Wed Aug 26
    ("📖 Book: Beyond Cracking the Coding Interview",  W,  "09:00", "09:45"),
    ("🎓 M7: Expressions",                             W,  "10:00", "11:30"),
    ("🎯 Yandex Prep: Async & WPF Review",             W,  "11:30", "12:30"),
    ("💻 LeetCode — Yandex prep",                      W,  "13:35", "14:35"),
    ("🤖 AIST Program tasks",                          W,  "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                         W,  "16:15", "16:45"),
    # Thu Aug 27
    ("📖 Book: Beyond Cracking the Coding Interview", TH2, "09:00", "09:45"),
    ("🎓 M8: REST architecture",                      TH2, "10:00", "11:00"),
    ("🎓 M9: Hosting and Deployment",                 TH2, "11:00", "12:00"),
    ("💻 LeetCode — Yandex prep",                     TH2, "13:35", "14:35"),
    ("🎯 Yandex Prep: EF Core & Code Review (recap)", TH2, "14:35", "15:10"),
    ("🤖 AIST Program tasks",                         TH2, "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                        TH2, "16:15", "16:45"),
    # Fri Aug 28
    ("📖 Book: Beyond Cracking the Coding Interview", F2,  "09:00", "09:45"),
    ("🎓 M10: GOF Overview",                          F2,  "10:00", "11:00"),
    ("🎓 M11: GOF: Cutting shape",                    F2,  "11:00", "12:00"),
    ("💻 LeetCode — Yandex prep",                     F2,  "13:35", "14:35"),
    ("🎯 Yandex Prep: Weak spots",                    F2,  "14:35", "15:10"),
    ("🤖 AIST Program tasks",                         F2,  "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                        F2,  "16:15", "16:45"),
    # Sat Aug 29
    ("📖 Book: Beyond Cracking the Coding Interview", SA2, "09:00", "09:45"),
    ("🎓 M12: GOF: Managing State",                   SA2, "10:00", "11:00"),
    ("🎓 M13: GOF: Altering behavior",                SA2, "11:00", "12:00"),
    ("💻 LeetCode — Yandex prep",                     SA2, "13:35", "14:35"),
    ("🎯 Yandex Prep: Mock interview",                SA2, "14:35", "15:10"),
    ("🤖 AIST Program tasks",                         SA2, "15:35", "16:05"),
    ("🚀 Gemini AI Hackathon",                        SA2, "16:15", "16:45"),
    # Sun Aug 30 — pre-interview, light day (no AIST/Hackathon)
    ("📖 Book: Beyond Cracking the Coding Interview", SU2, "09:00", "09:45"),
    ("🎓 M14: GOF: Reducing coupling",                SU2, "10:00", "11:00"),
    ("🎯 Yandex Prep: Final review",                  SU2, "11:00", "12:00"),
    ("💻 LeetCode — Yandex prep",                     SU2, "13:35", "14:35"),
]

print("\n── CREATES ─────────────────────────────────────────")
for title, day, start_str, end_str in NEW_EVENTS:
    body = {
        "summary": title,
        "start": {"dateTime": make_dt(day, start_str), "timeZone": TZ},
        "end":   {"dateTime": make_dt(day, end_str),   "timeZone": TZ},
    }
    service.events().insert(calendarId="primary", body=body).execute()
    print(f"  CREATED  {day.strftime('%a %b %d')}  {start_str}–{end_str}  {title}")
