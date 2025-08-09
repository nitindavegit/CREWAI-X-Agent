from crewai.tools import BaseTool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
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
    name: str = "Google Docs Archive Manager"
    description: str = "Professionally archives tweet threads in Google Docs with metadata, formatting, and engagement predictions"
    
    FIXED_DOC_ID: str = os.getenv("GOOGLE_DOC_ID")
    FIXED_DOC_TITLE: str = "ByteBrief - Viral Tech Thread Archive"

    def __init__(self):
        super().__init__()
        
    def _authenticate(self):
        """ authentication with better error handling"""
        SCOPES = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = None

        try:
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

            service = build('docs', 'v1', credentials=creds)
            return service, None
            
        except Exception as e:
            return None, f"❌ Authentication failed: {str(e)}"

    def _find_or_create_document(self, service):
        """ document management with better error handling"""
        try:
            
            if self.FIXED_DOC_ID:
                try:
                    service.documents().get(documentId=self.FIXED_DOC_ID).execute()
                    print(f"📄 Using existing archive document (ID: {self.FIXED_DOC_ID[:8]}...)")
                    return self.FIXED_DOC_ID
                except HttpError:
                    print(f"⚠️ Document with ID {self.FIXED_DOC_ID} not accessible")

            
            drive_service = build('drive', 'v3', credentials=service._http.credentials)
            
            results = drive_service.files().list(
                q=f"name='{self.FIXED_DOC_TITLE}' and mimeType='application/vnd.google-apps.document'",
                spaces='drive'
            ).execute()

            files = results.get('files', [])
            if files:
                doc_id = files[0]['id']
                print(f"📄 Found existing archive: {self.FIXED_DOC_TITLE}")
                return doc_id
            else:
                # Create new document with enhanced header
                doc = service.documents().create(body={'title': self.FIXED_DOC_TITLE}).execute()
                doc_id = doc['documentId']
                print(f"📄 Created new archive: {self.FIXED_DOC_TITLE}")

                header_text = f"""# ByteBrief - Viral Tech Thread Archive

🎯 **Mission**: Create viral tech content for maximum X impressions
📱 **Platform**: X (Twitter) 
👥 **Audience**: Developers & tech enthusiasts
🤖 **Powered by**: CrewAI Multi-Agent System

**Archive Started**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{"="*80}

"""
                requests = [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': header_text
                    }
                }]
                service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
                return doc_id

        except Exception as e:
            print(f"❌ Error with document management: {str(e)}")
            return None

    def _get_document_length(self, service, doc_id):
        """Get document length with error handling"""
        try:
            doc = service.documents().get(documentId=doc_id).execute()
            content = doc.get('body', {}).get('content', [])
            if content:
                return content[-1].get('endIndex', 1)
            return 1
        except Exception as e:
            print(f"⚠️ Error getting document length: {str(e)}")
            return 1

    def _run(self, tweet_text: str, doc_title: str = None) -> str:
        """Enhanced main execution with professional formatting"""
        try:
            print("💾 Archiving thread to Google Docs...")
            
            # Sanitize and process tweet text
            tweet_text = tweet_text.encode("utf-8").decode("utf-8")
            
            # Format tweets properly
            tweets = []
            lines = tweet_text.strip().split('\n')
            current_tweet = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('Tweet '):
                    if current_tweet:
                        tweets.append(current_tweet.strip())
                    current_tweet = line + '\n'
            
            if current_tweet:
                tweets.append(current_tweet.strip())
            
            # Create formatted thread block
            thread_content = '\n\n'.join(tweets) if tweets else tweet_text.strip()
            
            # Authenticate and get service
            service, error = self._authenticate()
            if error:
                return error

            # Find or create document
            doc_id = self._find_or_create_document(service)
            if not doc_id:
                return "❌ Failed to access or create archive document"

            # Get document length for appending
            end_index = self._get_document_length(service, doc_id)

            # Create timestamp and content (simplified)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            separator = "\n" + "─" * 60 + "\n"
            content = f"""{separator}📅 {timestamp}

{thread_content}

🤖 Generated by ByteBrief CrewAI
"""

            # Insert content into document
            requests = [{
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': content
                }
            }]

            service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

            # Create response URL
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            
            # Professional success message (simplified)
            success_message = f"""✅ Thread saved to Google Docs
📅 {timestamp}
🔗 {doc_url}"""
            
            print("✅ Archive complete!")
            return success_message

        except Exception as e:
            error_message = f"❌ Archive failed: {str(e)}"
            print(error_message)
            return error_message

    def get_setup_instructions(self) -> str:
        """Enhanced setup instructions"""
        return """
🔧 **ByteBrief Google Docs Setup Instructions**

**Step 1: Google Cloud Console Setup**
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable these APIs:
   - Google Docs API
   - Google Drive API

**Step 2: Create Credentials**
1. Go to "Credentials" in the left sidebar
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop Application"
4. Download the credentials file
5. Rename it to 'credentials.json'
6. Place it in your ByteBrief project folder

**Step 3: Optional - Use Specific Document**
1. Create a Google Doc manually (optional)
2. Copy the document ID from URL (between /d/ and /edit)
3. Add to .env file: GOOGLE_DOC_ID=your_document_id_here

**Step 4: First Run**
- Run ByteBrief - it will open browser for authentication
- Grant permissions to access Google Docs/Drive
- Future runs will be automatic!

🎯 **Perfect for CrewAI demos and real-world use!**
"""