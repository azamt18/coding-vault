import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_PATH = os.path.expanduser("~/Library/CloudStorage/OneDrive-EPAM/pdp/timebox/token.json")

creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

service = build("calendar", "v3", credentials=creds)
calendars = service.calendarList().list().execute().get("items", [])

for c in calendars:
    print(f"{c.get('summary'):40s}  id={c.get('id')}  access={c.get('accessRole')}")
