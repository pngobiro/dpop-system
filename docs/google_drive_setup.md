# Google Drive Integration Setup

This document describes how to set up Google Drive integration for the document management system.

## 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API for your project

## 2. Create OAuth 2.0 Credentials

1. Go to APIs & Services > Credentials
2. Click "Create Credentials" and select "OAuth client ID"
3. Configure the OAuth consent screen:
   - Select "Internal" or "External" user type
   - Add required app information
   - Add scopes for Google Drive API
4. Create OAuth client ID:
   - Application type: "Web application"
   - Name: "DSPOP Document Management"
   - Authorized redirect URIs: Add `http://localhost:8005/documents/google-auth-callback/`
   - Click "Create"
5. Download the client secrets JSON file

## 3. Configure the Application

1. Rename the downloaded OAuth client secrets file to `client_secrets.json`
2. Place the file in the project root directory (same level as manage.py)
3. Add the following environment variables to your .env file:
```
GOOGLE_DRIVE_DOCUMENT_ROOT=<folder_id>  # Optional: ID of root folder for documents
```

## 4. First-time Setup

1. Start the application
2. Navigate to the document library
3. Click the "Google Drive" button
4. Complete the OAuth consent flow when prompted
5. The application will create a `token.pickle` file to store credentials

## 5. Security Notes

- Keep `client_secrets.json` and `token.pickle` secure and never commit them to version control
- Add both files to .gitignore
- In production, consider using environment variables or a secure key management service
- Regularly audit document sharing permissions
- Implement proper access controls for different user roles

## 6. Usage

### Importing Files
1. Click "Google Drive" in the document library
2. Browse your Google Drive files
3. Click "Import" on any file to add it to the document management system
4. The file remains in Google Drive but is now linked in the system

### Sharing Files
1. For imported Google Drive files, click the "Share" button
2. Enter the recipient's email address
3. Select the appropriate access level (View/Edit)
4. Click "Share" to grant access via Google Drive sharing

## 7. Troubleshooting

### Token Refresh Issues
If you encounter authentication errors:
1. Delete the `token.pickle` file
2. Restart the application
3. Re-authenticate through the OAuth flow

### Permission Issues
- Ensure the Google Drive API is enabled
- Check that the OAuth consent screen includes proper scopes
- Verify the application has permission to access the root folder

### API Quotas
- Monitor API usage in Google Cloud Console
- Implement caching if needed
- Consider upgrading quotas for production use