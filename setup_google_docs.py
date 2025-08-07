#!/usr/bin/env python3
"""
ByteBrief Google Docs Setup Script
This script helps you set up Google Docs integration for ByteBrief
"""

import os
import json
from google_docs_tool import GoogleDocsTool

def check_credentials():
    """Check if credentials.json exists"""
    if os.path.exists('credentials.json'):
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
            print("✅ credentials.json found and valid")
            return True
        except json.JSONDecodeError:
            print("❌ credentials.json exists but is not valid JSON")
            return False
    else:
        print("❌ credentials.json not found")
        return False

def setup_instructions():
    """Print detailed setup instructions"""
    print("\n🔧 GOOGLE DOCS SETUP INSTRUCTIONS")
    print("="*50)
    
    print("\n1. Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    
    print("\n2. Create a new project or select existing one")
    
    print("\n3. Enable APIs:")
    print("   - Google Docs API")
    print("   - Google Drive API")
    print("   (Search for them in the API Library and click Enable)")
    
    print("\n4. Create Credentials:")
    print("   - Go to 'Credentials' in the left sidebar")
    print("   - Click '+ CREATE CREDENTIALS'")
    print("   - Select 'OAuth 2.0 Client IDs'")
    print("   - Choose 'Desktop application'")
    print("   - Name it 'ByteBrief' (or any name you prefer)")
    print("   - Click 'Create'")
    
    print("\n5. Download credentials:")
    print("   - Click the download icon next to your new credential")
    print("   - Save the file as 'credentials.json' in this folder:")
    print(f"   {os.getcwd()}")
    
    print("\n6. Run this script again to test the setup")
    
    print("\n💡 OPTIONAL - Use a specific document:")
    print("   - Create a Google Doc manually")
    print("   - Copy the document ID from URL (between /d/ and /edit)")
    print("   - Update FIXED_DOC_ID in google_docs_tool.py")

def test_connection():
    """Test Google Docs connection"""
    print("\n🧪 Testing Google Docs connection...")
    
    try:
        docs_tool = GoogleDocsTool()
        
        # Try to authenticate
        service, error = docs_tool._authenticate()
        
        if error:
            print(f"❌ Authentication failed: {error}")
            return False
            
        print("✅ Authentication successful!")
        
        # Try to find/create document
        doc_id = docs_tool._find_or_create_document(service)
        
        if doc_id:
            print(f"✅ Document ready: https://docs.google.com/document/d/{doc_id}/edit")
            
            # Test saving a sample tweet
            test_result = docs_tool._run("🧪 TEST TWEET: This is a test message from ByteBrief setup!")
            print(f"✅ Test save result: {test_result}")
            return True
        else:
            print("❌ Failed to create/find document")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 ByteBrief Google Docs Setup")
    print("="*40)
    
    # Check if credentials exist
    if not check_credentials():
        setup_instructions()
        return
    
    # Test the connection
    if test_connection():
        print("\n🎉 SUCCESS! Google Docs is ready for ByteBrief")
        print("You can now run: python bytebrief_crew.py")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")
        setup_instructions()

if __name__ == "__main__":
    main()