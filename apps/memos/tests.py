from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import Memo, MemoTemplate
from .forms import MemoForm
from apps.organization.models import Department

User = get_user_model()


class MemoCreationTestCase(TestCase):
    """Test cases for memo creation functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create test department
        self.department = Department.objects.create(
            name="Test Department",
            code="TD",
            description="Test Department for memo testing"
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Associate user with department (assuming this is how it works)
        self.user.departments.add(self.department)
        
        # Create test memo template
        self.memo_template = MemoTemplate.objects.create(
            name="Standard Internal Memo",
            description="Standard template for internal memos",
            content="This is a template content for {subject}",
            memo_type="internal",
            department=self.department,
            created_by=self.user
        )
        
        self.client = Client()
    
    def test_memo_creation_get_request(self):
        """Test accessing the memo creation page"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create')
        self.assertContains(response, 'form')
    
    def test_memo_creation_post_request_valid_data(self):
        """Test creating a memo with valid data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        
        # Prepare valid memo data
        memo_data = {
            'title': 'Test Memo Title',
            'memo_type': 'internal',
            'content': 'This is the content of the test memo. It contains important information.',
            'priority': 'medium',
            'due_date': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'recipient_external_name': '',
            'recipient_external_organization': '',
            'is_confidential': False,
            'tags': 'test, memo, internal',
            'file_number': 'TM/2025/001'
        }
        
        response = self.client.post(url, memo_data)
        
        # Check if memo was created successfully
        self.assertEqual(Memo.objects.count(), 1)
        memo = Memo.objects.first()
        
        # Verify memo attributes
        self.assertEqual(memo.title, 'Test Memo Title')
        self.assertEqual(memo.memo_type, 'internal')
        self.assertEqual(memo.content, 'This is the content of the test memo. It contains important information.')
        self.assertEqual(memo.priority, 'medium')
        self.assertEqual(memo.created_by, self.user)
        self.assertEqual(memo.department, self.department)
        self.assertEqual(memo.status, 'draft')  # Default status
        
        # Check redirect after successful creation
        self.assertRedirects(response, reverse('memos:memo_detail', kwargs={'pk': memo.pk}))
    
    def test_memo_creation_post_request_invalid_data(self):
        """Test creating a memo with invalid data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        
        # Prepare invalid memo data (missing required fields)
        memo_data = {
            'title': '',  # Empty title
            'memo_type': '',  # Empty memo type
            'content': '',  # Empty content
            'priority': 'medium',
        }
        
        response = self.client.post(url, memo_data)
        
        # Check that no memo was created
        self.assertEqual(Memo.objects.count(), 0)
        
        # Check that form errors are displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_memo_creation_with_file_attachment(self):
        """Test creating a memo with a file attachment"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        
        # Create a test file
        test_file = SimpleUploadedFile(
            "test_document.txt",
            b"This is a test document content",
            content_type="text/plain"
        )
        
        memo_data = {
            'title': 'Memo with Attachment',
            'memo_type': 'internal',
            'content': 'This memo has an attachment.',
            'priority': 'high',
            'document': test_file
        }
        
        response = self.client.post(url, memo_data)
        
        # Check if memo was created
        self.assertEqual(Memo.objects.count(), 1)
        memo = Memo.objects.first()
        self.assertEqual(memo.title, 'Memo with Attachment')
        
        # Note: Document creation testing would depend on your document management setup
    
    def test_memo_creation_ajax_request(self):
        """Test creating a memo via AJAX request (for modal submission)"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        
        memo_data = {
            'title': 'AJAX Test Memo',
            'memo_type': 'circular',
            'content': 'This memo was created via AJAX request.',
            'priority': 'urgent',
        }
        
        response = self.client.post(
            url, 
            memo_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check if memo was created
        self.assertEqual(Memo.objects.count(), 1)
        memo = Memo.objects.first()
        self.assertEqual(memo.title, 'AJAX Test Memo')
        
        # Check JSON response for AJAX
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
    
    def test_memo_creation_external_type(self):
        """Test creating an external memo with recipient information"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        
        memo_data = {
            'title': 'External Memo to Partner Organization',
            'memo_type': 'external',
            'content': 'This is an external memo to our partner organization.',
            'priority': 'high',
            'recipient_external_name': 'John Doe',
            'recipient_external_organization': 'Partner Organization Ltd',
            'due_date': (date.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
        }
        
        response = self.client.post(url, memo_data)
        
        # Check if memo was created
        self.assertEqual(Memo.objects.count(), 1)
        memo = Memo.objects.first()
        
        self.assertEqual(memo.memo_type, 'external')
        self.assertEqual(memo.recipient_external_name, 'John Doe')
        self.assertEqual(memo.recipient_external_organization, 'Partner Organization Ltd')
    
    def test_memo_creation_confidential(self):
        """Test creating a confidential memo"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('memos:memo_create')
        
        memo_data = {
            'title': 'Confidential Strategic Memo',
            'memo_type': 'internal',
            'content': 'This memo contains confidential strategic information.',
            'priority': 'urgent',
            'is_confidential': True,
        }
        
        response = self.client.post(url, memo_data)
        
        # Check if memo was created
        self.assertEqual(Memo.objects.count(), 1)
        memo = Memo.objects.first()
        
        self.assertEqual(memo.title, 'Confidential Strategic Memo')
        self.assertTrue(memo.is_confidential)
    
    def test_memo_creation_requires_authentication(self):
        """Test that memo creation requires user authentication"""
        url = reverse('memos:memo_create')
        
        memo_data = {
            'title': 'Unauthorized Memo',
            'memo_type': 'internal',
            'content': 'This should not be created.',
        }
        
        response = self.client.post(url, memo_data)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Memo.objects.count(), 0)
    
    def test_memo_form_validation(self):
        """Test memo form validation"""
        # Test with valid data
        form_data = {
            'title': 'Valid Memo Title',
            'memo_type': 'internal',
            'content': 'Valid memo content',
            'priority': 'medium',
        }
        form = MemoForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
        # Test with invalid data (missing required fields)
        invalid_form_data = {
            'title': '',
            'memo_type': '',
            'content': '',
        }
        invalid_form = MemoForm(data=invalid_form_data, user=self.user)
        self.assertFalse(invalid_form.is_valid())
        self.assertIn('title', invalid_form.errors)
        self.assertIn('memo_type', invalid_form.errors)
        self.assertIn('content', invalid_form.errors)


class MemoModelTestCase(TestCase):
    """Test cases for Memo model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.department = Department.objects.create(
            name="Model Test Department",
            code="MTD",
            description="Department for model testing"
        )
        
        self.user = User.objects.create_user(
            username='modeluser',
            email='model@example.com',
            password='testpass123'
        )
        self.user.departments.add(self.department)
    
    def test_memo_string_representation(self):
        """Test the string representation of a memo"""
        memo = Memo.objects.create(
            title="Test Memo for String Representation",
            memo_type="internal",
            content="Test content",
            department=self.department,
            created_by=self.user,
            reference_number="TEST/2025/001"
        )
        
        expected_string = "Test Memo for String Representation"
        self.assertEqual(str(memo), expected_string)
    
    def test_memo_default_values(self):
        """Test that memo has correct default values"""
        memo = Memo.objects.create(
            title="Default Values Test",
            memo_type="internal",
            content="Test content",
            department=self.department,
            created_by=self.user,
            reference_number="DEFAULT/2025/001"
        )
        
        self.assertEqual(memo.status, 'draft')
        self.assertEqual(memo.priority, 'medium')
        self.assertEqual(memo.version_number, 1)
        self.assertFalse(memo.is_confidential)
        self.assertIsNotNone(memo.created_at)
        self.assertIsNotNone(memo.updated_at)


# Create your tests here.
