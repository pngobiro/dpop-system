from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from ..utils.google_drive_manager import GoogleDriveManager
from ..models import Document, DocumentActivity
import os
import openai

# Initialize OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

@login_required
def summarize_document(request, file_id):
    """Generate an AI summary of a Google Drive document"""
    try:
        drive_manager = GoogleDriveManager()
        file_info = drive_manager.get_file_info(file_id)
        
        if not file_info or file_info['mimeType'] != 'application/pdf':
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid file or file type. Only PDFs are supported.'
            })

        # Extract text from PDF (you'll need to implement this in GoogleDriveManager)
        text = drive_manager.extract_text(file_id)
        
        if not text:
            return JsonResponse({
                'status': 'error',
                'message': 'Could not extract text from PDF'
            })
        
        # Get summary from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes legal and judiciary documents. Be concise but comprehensive."},
                {"role": "user", "content": f"Please summarize this document:\n\n{text[:4000]}"}  # First 4000 chars
            ],
            max_tokens=500
        )
        
        summary = response.choices[0].message['content']
        
        return JsonResponse({
            'status': 'success',
            'summary': summary
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
def google_drive_files(request, folder_id=None):
    """List files from Google Drive"""
    try:
        drive_manager = GoogleDriveManager()
        search_query = request.GET.get('q', '')
        files = drive_manager.list_files(folder_id=folder_id, search_query=search_query)
        
        context = {
            'files': files,
            'current_folder': folder_id,
            'search_query': search_query,
        }
        return render(request, 'document_management/drive_files.html', context)
        
    except Exception as e:
        messages.error(request, f"Error accessing Google Drive: {str(e)}")
        return redirect('document_management:library')

@login_required
def import_drive_file(request, file_id):
    """Import a file from Google Drive into the document management system"""
    try:
        drive_manager = GoogleDriveManager()
        file_info = drive_manager.get_file_info(file_id)
        
        if file_info:
            # Create document record
            document = Document.objects.create(
                title=file_info['name'],
                file_type=file_info['mimeType'],
                file_size=int(file_info.get('size', 0)),
                storage_type='google_drive',
                drive_file_id=file_info['id'],
                drive_view_link=file_info['webViewLink'],
                uploaded_by=request.user,
                source_module='google_drive'
            )
            
            # Record activity
            DocumentActivity.objects.create(
                document=document,
                user=request.user,
                action='upload',
                action_details='Imported from Google Drive',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, f"Successfully imported '{file_info['name']}' from Google Drive")
            return redirect('document_management:document_detail', pk=document.pk)
            
        messages.error(request, "Unable to import file from Google Drive")
        return redirect('document_management:drive_files')
        
    except Exception as e:
        messages.error(request, f"Error importing file: {str(e)}")
        return redirect('document_management:drive_files')

@login_required
def share_drive_file(request, document_id):
    """Share a Google Drive file with another user"""
    try:
        document = Document.objects.get(pk=document_id)
        if not document.drive_file_id:
            messages.error(request, "This document is not stored in Google Drive")
            return redirect('document_management:document_detail', pk=document_id)
        
        if request.method == 'POST':
            email = request.POST.get('email')
            role = request.POST.get('role', 'reader')
            
            drive_manager = GoogleDriveManager()
            if drive_manager.share_file(document.drive_file_id, email, role):
                messages.success(request, f"Successfully shared document with {email}")
                
                # Record activity
                DocumentActivity.objects.create(
                    document=document,
                    user=request.user,
                    action='share',
                    action_details=f"Shared with {email} (role: {role})",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
            else:
                messages.error(request, "Unable to share document")
                
        return redirect('document_management:document_detail', pk=document_id)
        
    except Document.DoesNotExist:
        messages.error(request, "Document not found")
        return redirect('document_management:library')
    except Exception as e:
        messages.error(request, f"Error sharing document: {str(e)}")
        return redirect('document_management:document_detail', pk=document_id)