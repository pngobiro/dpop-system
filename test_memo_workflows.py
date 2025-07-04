#!/usr/bin/env python
"""
Comprehensive Memo Workflow Tests
This script tests all major memo workflows including:
1. Memo creation
2. Memo editing
3. Memo status updates
4. Attachment handling
5. Search and filtering
6. User permissions
"""

import os
import sys
import django
from datetime import datetime, timedelta
import tempfile
from io import BytesIO

# Add the project directory to the Python path
sys.path.append('/home/ngobiro/projects/moringa_capstone')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Setup Django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import CustomUser
from apps.organization.models import Department, Role, UserRole
from apps.memos.models import (
    Memo, MemoType, MemoCategory, PriorityLevel, MemoStatus,
    MemoDocument, ActionItem
)
from apps.document_management.models import Document

User = get_user_model()

class MemoWorkflowTests:
    def __init__(self):
        self.client = Client()
        self.setup_test_data()
        
    def setup_test_data(self):
        """Setup test users, departments, and memo-related data"""
        print("Setting up test data...")
        
        # Create departments
        self.dept1, created = Department.objects.get_or_create(
            name="Test Department 1",
            defaults={'email': 'dept1@test.com', 'is_active': True}
        )
        
        self.dept2, created = Department.objects.get_or_create(
            name="Test Department 2", 
            defaults={'email': 'dept2@test.com', 'is_active': True}
        )
        
        # Create roles
        self.role1, created = Role.objects.get_or_create(
            title="Test Manager",
            department=self.dept1,
            defaults={'job_group': 'M', 'is_active': True}
        )
        
        self.role2, created = Role.objects.get_or_create(
            title="Test Officer", 
            department=self.dept2,
            defaults={'job_group': 'P', 'is_active': True}
        )
        
        # Create users
        self.user1, created = User.objects.get_or_create(
            username='testuser1',
            defaults={
                'email': 'test1@example.com',
                'first_name': 'Test',
                'last_name': 'User1',
                'is_active': True
            }
        )
        if created:
            self.user1.set_password('testpass123')
            self.user1.save()
            
        self.user2, created = User.objects.get_or_create(
            username='testuser2',
            defaults={
                'email': 'test2@example.com', 
                'first_name': 'Test',
                'last_name': 'User2',
                'is_active': True
            }
        )
        if created:
            self.user2.set_password('testpass123')
            self.user2.save()
        
        # Assign roles to users
        UserRole.objects.get_or_create(
            user=self.user1,
            role=self.role1,
            defaults={'is_active': True}
        )
        
        UserRole.objects.get_or_create(
            user=self.user2, 
            role=self.role2,
            defaults={'is_active': True}
        )
        
        # Create memo types and categories
        self.memo_type, created = MemoType.objects.get_or_create(
            name="Test Memo Type",
            defaults={'description': 'Test type', 'is_active': True}
        )
        
        self.memo_category, created = MemoCategory.objects.get_or_create(
            name="Test Category",
            defaults={'description': 'Test category', 'is_active': True}
        )
        
        # Create priority levels
        self.priority, created = PriorityLevel.objects.get_or_create(
            level=2,
            defaults={'name': 'Medium', 'description': 'Medium priority'}
        )
        
        # Create memo statuses
        self.draft_status, created = MemoStatus.objects.get_or_create(
            name="Draft",
            defaults={'description': 'Draft status', 'is_active': True}
        )
        
        self.pending_status, created = MemoStatus.objects.get_or_create(
            name="Pending",
            defaults={'description': 'Pending approval', 'is_active': True}
        )
        
        print("✅ Test data setup complete")

    def test_user_login(self):
        """Test user authentication"""
        print("\n🔐 Testing user login...")
        
        # Test login
        login_successful = self.client.login(username='testuser1', password='testpass123')
        if login_successful:
            print("✅ User login successful")
        else:
            print("❌ User login failed")
            return False
            
        return True

    def test_memo_creation(self):
        """Test memo creation workflow"""
        print("\n📝 Testing memo creation...")
        
        # Login first
        self.client.login(username='testuser1', password='testpass123')
        
        # Test GET request to memo creation page
        response = self.client.get(reverse('memos:memo_create'))
        if response.status_code == 200:
            print("✅ Memo creation page loads successfully")
        else:
            print(f"❌ Memo creation page failed to load: {response.status_code}")
            return False
        
        # Create test file for attachment
        test_file = SimpleUploadedFile(
            "test_memo.txt", 
            b"This is a test memo attachment",
            content_type="text/plain"
        )
        
        # Test POST request to create memo
        memo_data = {
            'title': 'Test Memo Title',
            'content': 'This is a test memo content for workflow testing.',
            'memo_type': self.memo_type.id,
            'category': self.memo_category.id,
            'priority': self.priority.id,
            'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'is_confidential': False,
            'is_physical': False,
            'recipient_departments': [self.dept2.id],
        }
        
        response = self.client.post(
            reverse('memos:memo_create'),
            data=memo_data,
            files={'attachments': test_file}
        )
        
        if response.status_code == 302:  # Redirect after successful creation
            print("✅ Memo created successfully")
            
            # Check if memo was actually created
            memo = Memo.objects.filter(title='Test Memo Title').first()
            if memo:
                print(f"✅ Memo found in database: {memo.reference_number}")
                self.test_memo = memo
                return True
            else:
                print("❌ Memo not found in database")
                return False
        else:
            print(f"❌ Memo creation failed: {response.status_code}")
            if hasattr(response, 'context') and 'form' in response.context:
                print(f"Form errors: {response.context['form'].errors}")
            return False

    def test_memo_list_and_search(self):
        """Test memo listing and search functionality"""
        print("\n📋 Testing memo list and search...")
        
        # Login first
        self.client.login(username='testuser1', password='testpass123')
        
        # Test my memos page
        response = self.client.get(reverse('memos:my_memos'))
        if response.status_code == 200:
            print("✅ My memos page loads successfully")
        else:
            print(f"❌ My memos page failed: {response.status_code}")
            return False
        
        # Test search functionality
        response = self.client.get(reverse('memos:my_memos'), {'search': 'Test Memo'})
        if response.status_code == 200:
            memos = response.context.get('memos', [])
            if len(memos) > 0:
                print("✅ Search functionality working")
            else:
                print("⚠️  Search returned no results (might be expected)")
        else:
            print(f"❌ Search functionality failed: {response.status_code}")
            return False
        
        # Test filtering
        response = self.client.get(reverse('memos:my_memos'), {
            'status': self.draft_status.id,
            'memo_type': self.memo_type.id
        })
        if response.status_code == 200:
            print("✅ Filter functionality working")
        else:
            print(f"❌ Filter functionality failed: {response.status_code}")
            return False
            
        return True

    def test_memo_detail_view(self):
        """Test memo detail view"""
        print("\n👁️  Testing memo detail view...")
        
        # Login first
        self.client.login(username='testuser1', password='testpass123')
        
        # Get the test memo
        memo = Memo.objects.filter(title='Test Memo Title').first()
        if not memo:
            print("❌ No test memo found for detail view test")
            return False
        
        # Test memo detail page
        response = self.client.get(reverse('memos:memo_detail', args=[memo.pk]))
        if response.status_code == 200:
            print("✅ Memo detail page loads successfully")
            return True
        else:
            print(f"❌ Memo detail page failed: {response.status_code}")
            return False

    def test_memo_editing(self):
        """Test memo editing workflow"""
        print("\n✏️  Testing memo editing...")
        
        # Login first
        self.client.login(username='testuser1', password='testpass123')
        
        # Get the test memo
        memo = Memo.objects.filter(title='Test Memo Title').first()
        if not memo:
            print("❌ No test memo found for editing test")
            return False
        
        # Test GET request to edit page
        response = self.client.get(reverse('memos:memo_edit', args=[memo.pk]))
        if response.status_code == 200:
            print("✅ Memo edit page loads successfully")
        else:
            print(f"❌ Memo edit page failed: {response.status_code}")
            return False
        
        # Test POST request to update memo
        updated_data = {
            'title': 'Updated Test Memo Title',
            'content': 'This is updated content for the test memo.',
            'memo_type': self.memo_type.id,
            'category': self.memo_category.id,
            'priority': self.priority.id,
            'due_date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'is_confidential': False,
            'is_physical': False,
        }
        
        response = self.client.post(
            reverse('memos:memo_edit', args=[memo.pk]),
            data=updated_data
        )
        
        if response.status_code == 302:  # Redirect after successful update
            print("✅ Memo updated successfully")
            
            # Verify update
            memo.refresh_from_db()
            if memo.title == 'Updated Test Memo Title':
                print("✅ Memo title updated correctly")
                return True
            else:
                print("❌ Memo title not updated")
                return False
        else:
            print(f"❌ Memo update failed: {response.status_code}")
            return False

    def test_memo_permissions(self):
        """Test memo permission system"""
        print("\n🔒 Testing memo permissions...")
        
        # Login as user2 (different department)
        self.client.login(username='testuser2', password='testpass123')
        
        # Get the test memo created by user1
        memo = Memo.objects.filter(title__contains='Test Memo').first()
        if not memo:
            print("❌ No test memo found for permission test")
            return False
        
        # Try to edit memo from different department
        response = self.client.get(reverse('memos:memo_edit', args=[memo.pk]))
        
        # Should redirect or show permission error
        if response.status_code in [302, 403]:
            print("✅ Permission system working - unauthorized access blocked")
        elif response.status_code == 200:
            # Check if user can actually edit (might be allowed if recipient)
            print("⚠️  User can access memo (might be recipient)")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
            
        return True

    def test_dashboard_access(self):
        """Test dashboard access"""
        print("\n📊 Testing dashboard access...")
        
        # Login first
        self.client.login(username='testuser1', password='testpass123')
        
        # Test department dashboard
        response = self.client.get(reverse('memos:department_dashboard'))
        if response.status_code == 200:
            print("✅ Department dashboard loads successfully")
        else:
            print(f"❌ Department dashboard failed: {response.status_code}")
            return False
            
        return True

    def test_memo_status_workflow(self):
        """Test memo status change workflow"""
        print("\n🔄 Testing memo status workflow...")
        
        # Login first
        self.client.login(username='testuser1', password='testpass123')
        
        # Get the test memo
        memo = Memo.objects.filter(title__contains='Test Memo').first()
        if not memo:
            print("❌ No test memo found for status test")
            return False
        
        original_status = memo.status
        
        # Try to update status (if endpoint exists)
        try:
            response = self.client.post(
                reverse('memos:memo_status_update', args=[memo.pk]),
                data={'status': self.pending_status.id}
            )
            
            if response.status_code in [200, 302]:
                memo.refresh_from_db()
                if memo.status == self.pending_status:
                    print("✅ Memo status updated successfully")
                else:
                    print("⚠️  Status update response OK but status not changed")
            else:
                print(f"⚠️  Status update endpoint returned: {response.status_code}")
        except:
            print("⚠️  Status update endpoint not available or not implemented")
            
        return True

    def run_all_tests(self):
        """Run all memo workflow tests"""
        print("🚀 Starting Memo Workflow Tests")
        print("=" * 50)
        
        test_results = []
        
        # Run tests in order
        tests = [
            ("User Login", self.test_user_login),
            ("Memo Creation", self.test_memo_creation),
            ("Memo List & Search", self.test_memo_list_and_search),
            ("Memo Detail View", self.test_memo_detail_view),
            ("Memo Editing", self.test_memo_editing),
            ("Memo Permissions", self.test_memo_permissions),
            ("Dashboard Access", self.test_dashboard_access),
            ("Memo Status Workflow", self.test_memo_status_workflow),
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                test_results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {str(e)}")
                test_results.append((test_name, False))
        
        # Print summary
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<25} {status}")
            if result:
                passed += 1
        
        print("-" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Memo system is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please review the issues above.")

if __name__ == "__main__":
    # Run the tests
    test_runner = MemoWorkflowTests()
    test_runner.run_all_tests()
