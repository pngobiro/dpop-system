from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import Document, DocumentCategory
from ..utils.google_drive_manager import GoogleDriveManager

# Number of documents per page
ITEMS_PER_PAGE = 10

# Hardcoded category mapping
CATEGORIES = {
    'policies': 'Policies',
    'procedures': 'Procedures',
    'reports': 'Reports',
    'forms': 'Forms',
    'templates': 'Templates',
    'other': 'Other Documents'
}

@login_required
def library(request):
    """Main document library view with search and pagination"""
    # Get search query
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    # Base queryset
    documents = Document.objects.all().order_by('-created_at')
    
    # Apply search if query exists
    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploaded_by__username__icontains=query) |
            Q(uploaded_by__first_name__icontains=query) |
            Q(uploaded_by__last_name__icontains=query)
        )
    
    # Apply category filter if selected
    if category:
        documents = documents.filter(category__name=CATEGORIES.get(category))
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(documents, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'documents': page_obj,
        'query': query,
        'selected_category': category,
        'categories': CATEGORIES,
        'total_documents': paginator.count,
    }
    
    return render(request, 'document_management/library.html', context)

@login_required
def document_detail(request, pk):
    """Document detail view"""
    document = Document.objects.get(pk=pk)
    return render(request, 'document_management/detail.html', {'document': document})

@login_required
def upload_document(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        title = request.POST.get('title') or file.name
        category_slug = request.POST.get('category')
        description = request.POST.get('description')

        if category_slug not in CATEGORIES:
            messages.error(request, 'Invalid category selected.')
            return redirect('document_management:library')

        drive_manager = GoogleDriveManager()

        try:
            # Get or create category in database
            try:
                category = DocumentCategory.objects.get(name=CATEGORIES[category_slug])
            except DocumentCategory.DoesNotExist:
                # Create folder in Google Drive
                folder_id = drive_manager.create_folder(CATEGORIES[category_slug])
                if not folder_id:
                    raise Exception("Failed to create category folder in Google Drive")
                
                # Create category in database
                category = DocumentCategory.objects.create(
                    name=CATEGORIES[category_slug],
                    drive_folder_id=folder_id
                )

            # Upload file to Google Drive in the category folder
            file_id, web_link = drive_manager.upload_file(
                file_obj=file,
                filename=title,
                folder_id=category.drive_folder_id
            )

            if file_id and web_link:
                # Create Document object
                content_type = ContentType.objects.get_for_model(Document)
                Document.objects.create(
                    title=title,
                    file_size=file.size,
                    file_type=file.content_type,
                    storage_type='google_drive',
                    drive_file_id=file_id,
                    drive_view_link=web_link,
                    file=None,  # Set to None for Google Drive files
                    uploaded_by=request.user,
                    source_module='document_management',
                    content_type=content_type,
                    object_id=1,  # Dummy object ID
                    description=description,
                    category=category
                )

                messages.success(request, 'Document uploaded successfully!')
            else:
                messages.error(request, 'Failed to upload document to Google Drive.')
        except Exception as e:
            messages.error(request, f'Error uploading document: {e}')

        return redirect('document_management:library')
    else:
        return redirect('document_management:library')  # Redirect if not POST