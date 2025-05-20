# Google Drive Service Account Setup

## 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one

## 2. Enable the Google Drive API
1. Navigate to APIs & Services > Library
2. Search for "Google Drive API"
3. Click Enable

## 3. Create Service Account
1. Go to APIs & Services > Credentials
2. Click "Create Credentials" and select "Service Account"
3. Fill in the service account details:
   - Name: `judiciary-docs-service`
   - ID: will be auto-generated
   - Description: "Service account for Judiciary documents management"
4. Click "Create and Continue"
5. For "Role", select "Editor" under "Basic"
6. Click "Continue" and then "Done"

## 4. Generate Key File
1. In the Service Accounts list, click on your newly created service account
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Click "Create"
6. The key file will be downloaded automatically

## 5. Configure the Application
1. Rename the downloaded JSON file to `client_secrets.json`
2. Place it in your project root directory (same level as manage.py)
3. Update your .env file with:
```
GOOGLE_DRIVE_CREDENTIALS_FILE=client_secrets.json
```

## 6. Share Google Drive Folders
1. Create a folder in Google Drive that will be used for document storage
2. Share this folder with the service account email (found in client_secrets.json)
3. Copy the folder ID from the URL and add it to your .env file:
```
GOOGLE_DRIVE_DOCUMENT_ROOT=<folder_id>
```

## Security Notes
- Keep the client_secrets.json file secure and never commit it to version control
- Restrict the service account's access to only the necessary folders
- Regularly audit the service account's activity
- Consider using environment variables for sensitive values in production

## Troubleshooting
If you encounter permission issues:
1. Verify the service account email has access to the folder
2. Check that the Google Drive API is enabled
3. Ensure the client_secrets.json file is in the correct location
4. Verify the GOOGLE_DRIVE_CREDENTIALS_FILE path in settings.py