from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.api_core import retry
from googleapiclient.http import HttpRequest, MediaIoBaseDownload
from django.conf import settings
import os
import socket
import httplib2
import io
import PyPDF2

class GoogleDriveManager:
    """Handles all Google Drive operations"""
    SCOPES = ['https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive.readonly',
              'https://www.googleapis.com/auth/drive']

    def __init__(self):
        self.creds = None
        self.service = None
        self.initialize_service()

    def initialize_service(self):
        """Initialize Google Drive API service using service account"""
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_DRIVE_CREDENTIALS_FILE,
                scopes=self.SCOPES
            )
            
            self.service = build(
                'drive',
                'v3',
                credentials=self.creds,
                cache_discovery=False
            )
            
            if not self.service:
                raise Exception("Failed to initialize Google Drive service")
                
            print("Successfully initialized Google Drive service")
                
        except Exception as e:
            print(f"Error initializing Google Drive service: {str(e)}")
            self.service = None

    DEFAULT_FOLDER_ID = '1O-A9BfyVuoi3U-1MRMJBxHpzo-GEjAsK'  # The shared folder ID
    
    def _get_shared_files(self):
        """Get list of files shared with the service account"""
        try:
            print("\nListing shared files...")
            results = self.service.files().list(
                q="sharedWithMe = true and trashed = false",
                fields="files(id, name, mimeType, webViewLink, createdTime, modifiedTime, size, parents, capabilities)",
                orderBy="folder,name",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                corpora='allDrives',
                spaces='drive'
            ).execute()
            
            files = results.get('files', [])
            if files:
                print(f"Found {len(files)} shared files:")
                for file in files:
                    print(f"- {file.get('name')} ({file.get('id')})")
            else:
                print("No shared files found")
            return files
            
        except Exception as e:
            print(f"Error listing shared files: {str(e)}")
            return []
    
    @retry.Retry(predicate=retry.if_exception_type(Exception))
    def list_files(self, folder_id=None, page_size=100, search_query=None):
        """List files in Google Drive or specific folder"""
        if not self.service:
            raise Exception("Google Drive service not initialized")
            
        try:
            print("\n=== Starting Google Drive file listing ===")
            print("1. Checking service account permissions...")
            
            try:
                about = self.service.about().get(fields="user,storageQuota,maxImportSizes,canCreateDrives").execute()
                print("Service account details:")
                print(f"- Email: {about.get('user', {}).get('emailAddress')}")
                print(f"- Storage quota: {about.get('storageQuota', {})}")
                print(f"- Can create drives: {about.get('canCreateDrives')}")
            except Exception as about_error:
                print(f"Error getting account info: {str(about_error)}")
            
            # First, try to get files that are explicitly shared
            shared_files = self._get_shared_files()
            
            # If we found the target folder in shared files, use it
            target_folder = None
            if shared_files:
                for file in shared_files:
                    if file.get('id') == self.DEFAULT_FOLDER_ID:
                        target_folder = file
                        break
            
            if not target_folder:
                print(f"\nTarget folder {self.DEFAULT_FOLDER_ID} not found in shared files")
                return []
                
            print(f"\nFound target folder: {target_folder.get('name')}")
            
            # Build the query to list files in the target folder
            query = [
                f"'{self.DEFAULT_FOLDER_ID}' in parents",
                "trashed = false"
            ]
            
            # Add search query if provided
            if search_query:
                query.append(f"name contains '{search_query}'")
            query_string = " and ".join(query)
            
            # List files in the target folder
            print("\nListing files in target folder...")
            try:
                results = self.service.files().list(
                    pageSize=page_size,
                    q=query_string,
                    fields="nextPageToken, files(id, name, mimeType, webViewLink, createdTime, modifiedTime, size, parents, capabilities)",
                    orderBy="folder,name",
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    corpora='allDrives',
                    spaces='drive'
                ).execute()
                
                files = results.get('files', [])
                if files:
                    print(f"\nFound {len(files)} files in folder:")
                    for file in files:
                        print(f"- {file.get('name')} ({file.get('mimeType')})")
                        print(f"  Web link: {file.get('webViewLink')}")
                else:
                    print("\nNo files found in folder")
                
                return files
                
            except Exception as list_error:
                print(f"\nError listing files in folder: {str(list_error)}")
                return []
            
            files = results.get('files', [])
            if not files:
                print("No files found in Google Drive")
            else:
                print(f"Found {len(files)} files in Google Drive")
                for file in files:
                    print(f"- {file.get('name')} ({file.get('mimeType')})")
            return files
            
        except Exception as e:
            error_msg = f"Error listing files: {str(e)}"
            print(error_msg)
            raise  # Let the retry decorator handle retries

    def get_file_info(self, file_id):
        """Get detailed information about a specific file"""
        try:
            return self.service.files().get(
                fileId=file_id,
                fields='id, name, mimeType, webViewLink, createdTime, modifiedTime, size'
            ).execute()
        except Exception as e:
            print(f"Error getting file info: {str(e)}")
            return None

    def extract_text(self, file_id):
        """Extract text content from a PDF file in Google Drive"""
        try:
            # Get the file metadata
            file = self.service.files().get(
                fileId=file_id,
                supportsAllDrives=True
            ).execute()
            
            if file['mimeType'] != 'application/pdf':
                raise Exception("File is not a PDF")
            
            # Download the file content
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            # Extract text from PDF
            file_content.seek(0)
            pdf_reader = PyPDF2.PdfReader(file_content)
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return None

    def create_folder(self, name, parent_folder_id=None):
        """Create a new folder in Google Drive"""
        try:
            print(f"Creating folder '{name}' in parent: {parent_folder_id}")
            
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
                
            file = self.service.files().create(
                body=file_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()

            # Set folder permissions
            if file.get('id'):
                # Get service account email from credentials
                creds_info = service_account.Credentials.from_service_account_file(
                    settings.GOOGLE_DRIVE_CREDENTIALS_FILE
                ).service_account_email

                permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': creds_info
                }
                
                self.service.permissions().create(
                    fileId=file['id'],
                    body=permission,
                    fields='id',
                    supportsAllDrives=True
                ).execute()
                
                print(f"Created folder with ID: {file.get('id')}")
            
            return file.get('id')
        except Exception as e:
            print(f"Error creating folder: {str(e)}")
            return None

    def share_file(self, file_id, email, role='reader'):
        """Share a file with specific user"""
        try:
            batch = self.service.new_batch_http_request()
            
            user_permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            
            batch.add(self.service.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
                sendNotificationEmail=True
            ))
            
            batch.execute()
            return True
        except Exception as e:
            print(f"Error sharing file: {str(e)}")
            return False

    def upload_file(self, file_obj, filename, folder_id=None):
        """Upload a file to Google Drive"""
        try:
            print(f"Uploading file '{filename}' to folder: {folder_id}")
            folder_id = folder_id or self.DEFAULT_FOLDER_ID
            
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }

            from googleapiclient.http import MediaIoBaseUpload
            media = MediaIoBaseUpload(
                file_obj,
                mimetype=file_obj.content_type,
                resumable=True,
                chunksize=1024*1024
            )

            print("Creating file in Google Drive...")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink',
                supportsTeamDrives=True,
                supportsAllDrives=True
            ).execute()

            if file.get('id'):
                print(f"File created with ID: {file.get('id')}")
                
                # Set file permissions
                permission = {
                    'type': 'anyone',
                    'role': 'reader'
                }
                
                print("Setting file permissions...")
                self.service.permissions().create(
                    fileId=file['id'],
                    body=permission,
                    fields='id',
                    supportsAllDrives=True
                ).execute()
                
                return file.get('id'), file.get('webViewLink')
            else:
                print("Failed to create file - no ID returned")
                return None, None
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None, None