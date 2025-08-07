from crewai.tools import BaseTool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json
import sys
import locale
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Force UTF-8 encoding to handle emojis safely on Windows
if sys.platform == "win32":
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

class GoogleDocsTool(BaseTool):
    name: str = "Google Docs Saver"
    description: str = "Creates or appends a tweet thread into a Google Doc grouped by date"
    
    FIXED_DOC_ID: str = os.getenv("GOOGLE_DOC_ID")
    FIXED_DOC_TITLE: str = "ByteBrief- Thread Saver"

    def __init__(self):
        super().__init__()
    def _authenticate(self):
        SCOPES = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    return None, "❌ credentials.json file not found. Please download it from Google Cloud Console."

                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('docs', 'v1', credentials=creds), None

    def _find_or_create_document(self, service):
        try:
            if self.FIXED_DOC_ID:
                try:
                    service.documents().get(documentId=self.FIXED_DOC_ID).execute()
                    return self.FIXED_DOC_ID
                except HttpError:
                    print(f"❌ Document with ID {self.FIXED_DOC_ID} not found")

            drive_service = build('drive', 'v3', credentials=service._http.credentials)

            results = drive_service.files().list(
                q=f"name='{self.FIXED_DOC_TITLE}' and mimeType='application/vnd.google-apps.document'",
                spaces='drive'
            ).execute()

            files = results.get('files', [])
            if files:
                doc_id = files[0]['id']
                print(f"✅ Found existing document: {self.FIXED_DOC_TITLE}")
                return doc_id
            else:
                doc = service.documents().create(body={'title': self.FIXED_DOC_TITLE}).execute()
                doc_id = doc['documentId']
                print(f"✅ Created new document: {self.FIXED_DOC_TITLE}")

                header_text = "# ByteBrief Tweet Archive\n\nStarted: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n" + "="*50 + "\n\n"
                requests = [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': header_text
                    }
                }]
                service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
                return doc_id

        except Exception as e:
            print(f"❌ Error finding/creating document: {str(e)}")
            return None

    def _get_document_length(self, service, doc_id):
        try:
            doc = service.documents().get(documentId=doc_id).execute()
            content = doc.get('body', {}).get('content', [])
            if content:
                return content[-1].get('endIndex', 1)
            return 1
        except Exception as e:
            print(f"❌ Error getting document length: {str(e)}")
            return 1

    def _run(self, tweet_text: str, doc_title: str = None) -> str:
        try:
            # Sanitize tweet text to avoid emoji-related encoding issues
            tweet_text = tweet_text.encode("utf-8").decode("utf-8")
            # Add Tweet 1 / Tweet 2 if not present
            tweets = tweet_text.strip().split("\n\n")
            if len(tweets) >= 2 and not tweets[0].lower().startswith("tweet"):
                tweet_1 = f"Tweet 1:\n{tweets[0].strip()}\n\n"
                tweet_2 = f"Tweet 2:\n{tweets[1].strip()}\n\n"
                tweet_block = tweet_1 + tweet_2
            else:
                tweet_block = tweet_text.strip()
    
            # Authenticate
            service, error = self._authenticate()
            if error:
                return error

            doc_id = self._find_or_create_document(service)
            if not doc_id:
                return "❌ Failed to find or create document"

            end_index = self._get_document_length(service, doc_id)

            today = datetime.now().strftime("[Date] %Y-%m-%d %H:%M:%S")
            separator = "\n" + "─" * 60 + "\n"
            content = f"{separator}{today}\n\n{tweet_block}\n"

            requests = [{
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': content
                }
            }]

            service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            return f"✅ Tweet saved to Google Docs: {doc_url}"

        except Exception as e:
            return f"❌ Error saving to Google Docs: {str(e)}"

    def get_setup_instructions(self) -> str:
        return """
🔧 Google Docs Tool Setup Instructions:

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Docs API and Google Drive API
4. Create credentials (OAuth 2.0 Client IDs) for a desktop application
5. Download the credentials file and save it as 'credentials.json' in your project folder
6. Run the script - it will open a browser for authentication on first use

Optional: If you want to use a specific document:
- Create a Google Doc manually
- Copy the document ID from the URL (between /d/ and /edit)
- Set GOOGLE_DOC_ID in your .env file
"""

