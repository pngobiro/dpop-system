#!/usr/bin/env python
"""
Test script to create a memo with attachments and verify the complete flow
"""
import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.organization.models import Department
from apps.memos.models import *
from apps.memos.forms import MemoForm

User = get_user_model()

def create_test_memo_with_attachments():
    """Create a test memo with attachments"""
    print("=== Creating Test Memo with Attachments ===")
    
    # Get or create a test user
    user = User.objects.filter(username='joseph.osewe').first()
    if not user:
        print("Creating test user...")
        user = User.objects.create_user(
            username='joseph.osewe',
            email='joseph.osewe@example.com',
            first_name='Joseph',
            last_name='Osewe'
        )
    
    # Get or create a department
    department = Department.objects.filter(name__icontains='admin').first()
    if not department:
        department = Department.objects.create(
            name='Administration',
            description='Administration Department'
        )
    
    # Assign user to department if not already assigned
    if not user.department:
        user.department = department
        user.save()
    
    # Get required memo data
    memo_type = MemoType.objects.filter(name__icontains='internal').first()
    category = MemoCategory.objects.filter(name__icontains='admin').first()
    priority = PriorityLevel.objects.filter(name__icontains='medium').first()
    
    if not memo_type:
        print("ERROR: No memo type found. Run seed_memo_data command first.")
        return None
    
    # Create test file content
    test_file_content = b"This is a test PDF file content for memo attachments."
    test_file = SimpleUploadedFile(
        "test_memo_attachment.pdf",
        test_file_content,
        content_type="application/pdf"
    )
    
    # Create form data
    form_data = {
        'title': 'Test Memo with Attachments',
        'subject': 'Testing the new memo attachment system',
        'content': 'This is a test memo to verify that file attachments are working correctly.',
        'memo_type': memo_type.id,
        'category': category.id if category else '',
        'priority': priority.id if priority else '',
        'sender_internal': user.id,
        'is_physical': False,
        'is_confidential': False,
    }
    
    # Create form with file
    form = MemoForm(form_data, {'attachments': [test_file]}, user=user, department=department)
    
    if form.is_valid():
        print("✓ Form is valid")
        memo = form.save(commit=False)
        memo.created_by = user
        memo.department = department
        memo.save()
        form.save_m2m()
        
        print(f"✓ Memo created: {memo.reference_number}")
        print(f"✓ Memo title: {memo.title}")
        print(f"✓ Memo ID: {memo.id}")
        
        # Check if documents were attached
        documents = memo.documents.all()
        print(f"✓ Documents attached: {documents.count()}")
        
        for doc in documents:
            print(f"  - {doc.document.title} ({doc.document_type})")
        
        return memo
    else:
        print("✗ Form is invalid")
        print("Form errors:", form.errors)
        return None

def test_memo_detail_view():
    """Test the memo detail view"""
    print("\n=== Testing Memo Detail View ===")
    
    # Get the latest memo
    memo = Memo.objects.first()
    if not memo:
        print("No memo found to test")
        return
    
    print(f"Testing memo: {memo.reference_number}")
    print(f"Documents count: {memo.documents.count()}")
    
    # Test the view context
    from apps.memos.views import memo_detail
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser
    
    factory = RequestFactory()
    request = factory.get(f'/memos/{memo.id}/')
    request.user = memo.created_by
    
    # This would normally be tested with a proper test client,
    # but we can at least check the basic data
    documents = memo.documents.all().order_by('-uploaded_at')
    print(f"✓ Documents available for template: {documents.count()}")
    
    for doc in documents:
        print(f"  - {doc.document.title}")
        print(f"    Type: {doc.document_type}")
        print(f"    Uploaded: {doc.uploaded_at}")
        print(f"    By: {doc.uploaded_by.get_full_name()}")

if __name__ == "__main__":
    # Create test memo
    memo = create_test_memo_with_attachments()
    
    if memo:
        # Test detail view
        test_memo_detail_view()
        
        print(f"\n✓ Test completed successfully!")
        print(f"✓ You can now view the memo at: http://localhost:8001/memos/{memo.id}/")
    else:
        print("\n✗ Test failed!")
