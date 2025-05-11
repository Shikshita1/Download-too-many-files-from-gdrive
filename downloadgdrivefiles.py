import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# --- USER INPUTS ---
FOLDER_ID = "" # Get folder id from the link of gdrive folder
TARGET_FILENAMES = None         # add list of files if you want particular files, otherwise leave None.
DOWNLOAD_DIR = r""  # folder to save files



# --- SETUP ---
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- Authentication ---
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds= flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# --- Build service ---
service = build('drive', 'v3', credentials=creds)

# --- List all files in the folder ---
query = f"'{FOLDER_ID}' in parents and trashed = false"
files = []
page_token = None
print("Fetching file list...")
while True:
    response = service.files().list(
        q=query,
        spaces='drive',
        fields='nextPageToken, files(id, name)',
        pageToken=page_token
    ).execute()
    files.extend(response.get('files', []))
    page_token = response.get('nextPageToken', None)
    if not page_token:
        break

print(f"Found {len(files)} files in folder.")

# --- Download matching files ---
# --- Download all files (or just matching ones if TARGET_FILENAMES is defined) ---
for f in files:
    if TARGET_FILENAMES is None or f['name'] in TARGET_FILENAMES:
        print(f"Downloading: {f['name']}")
        request = service.files().get_media(fileId=f['id'])
        filepath = os.path.join(DOWNLOAD_DIR, f['name'])
        fh = io.FileIO(filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  {int(status.progress() * 100)}% downloaded")
