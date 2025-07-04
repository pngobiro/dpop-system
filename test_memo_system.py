#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/home/ngobiro/projects/moringa_capstone')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Setup Django
django.setup()

from authentication.models import CustomUser
from apps.memos.models import Memo, MemoType, MemoCategory, PriorityLevel, MemoStatus
from apps.organization.models import Department

print('=== Testing Memo System ===')

# Test user access
user = CustomUser.objects.first()
print(f'User: {user.username}')
print(f'User department: {user.department}')

# Test memo creation
memo_type = MemoType.objects.first()
memo_category = MemoCategory.objects.first()
priority = PriorityLevel.objects.first()
status = MemoStatus.objects.first()

if user.department:
    try:
        memo = Memo.objects.create(
            title="Test Memo",
            subject="Testing memo system",
            content="This is a test memo to verify the system is working.",
            memo_type=memo_type,
            category=memo_category,
            priority=priority,
            status=status,
            department=user.department,
            created_by=user,
            is_physical=False,
            is_confidential=False
        )
        print(f'Successfully created memo: {memo.reference_number}')
        print(f'Memo ID: {memo.id}')
        print(f'Memo department: {memo.department}')
        
        # Test memo retrieval
        user_memos = Memo.objects.filter(created_by=user)
        print(f'User has {user_memos.count()} memos')
        
        # Clean up - delete the test memo
        memo.delete()
        print('Test memo deleted successfully')
        
    except Exception as e:
        print(f'Error creating memo: {e}')
else:
    print('User has no department - cannot create memo')

print('=== Test Complete ===')
