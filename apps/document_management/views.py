from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, HttpResponse
from .models import Document, DocumentCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def digital_library(request):
    """
    Displays a searchable and filterable list of documents,
    respecting confidentiality permissions, with pagination.
    """
    base_queryset = Document.objects.select_related('category', 'uploaded_by').order_by('-created_at')
    categories = DocumentCategory.objects.filter(is_active=True)

    # --- Filtering ---
    selected_category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('q')
    from_dept_id = request.GET.get('from_dept') # Get originating department ID

    filtered_queryset = base_queryset

    if selected_category_id:
        filtered_queryset = filtered_queryset.filter(category_id=selected_category_id)
    if start_date:
        filtered_queryset = filtered_queryset.filter(created_at__date__gte=start_date)
    if end_date:
        filtered_queryset = filtered_queryset.filter(created_at__date__lte=end_date)
    if search_query:
        filtered_queryset = filtered_queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    # --- Confidentiality Check ---
    can_view_confidential = request.user.has_perm('document_management.view_confidential_document')
    if not can_view_confidential:
        filtered_queryset = filtered_queryset.filter(is_confidential=False)

    # --- Pagination ---
    paginator = Paginator(filtered_queryset, 15)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
        'can_view_confidential': can_view_confidential,
        'from_dept_id': from_dept_id, # Pass originating department ID to template
    }
    return render(request, 'document_management/library.html', context)

@login_required
def document_detail(request, doc_id):
    """
    Displays details for a specific document and provides action buttons.
    """
    document = get_object_or_404(Document.objects.select_related('category', 'uploaded_by'), pk=doc_id)
    from_dept_id = request.GET.get('from_dept') # Pass through if present

    # --- Confidentiality Check ---
    can_view_confidential = request.user.has_perm('document_management.view_confidential_document')
    if document.is_confidential and not can_view_confidential:
        raise Http404("Document not found or you do not have permission to view it.")

    context = {
        'document': document,
        'can_view_confidential': can_view_confidential,
        'from_dept_id': from_dept_id, # Pass originating department ID to template
    }
    return render(request, 'document_management/detail.html', context)

# --- Placeholder Action Views ---
# (summarize, download, share views remain the same)
@login_required
def summarize_document(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id)
    can_view_confidential = request.user.has_perm('document_management.view_confidential_document')
    if document.is_confidential and not can_view_confidential: raise Http404
    level = request.GET.get('level', 'medium')
    summary = f"Placeholder summary ({level}) for document '{document.title}'. AI integration needed."
    return HttpResponse(summary)

@login_required
def download_document(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id)
    can_view_confidential = request.user.has_perm('document_management.view_confidential_document')
    if document.is_confidential and not can_view_confidential: raise Http404
    return HttpResponse(f"Placeholder for downloading document '{document.title}'. File serving logic needed.")

@login_required
def share_document(request, doc_id):
    document = get_object_or_404(Document, pk=doc_id)
    can_view_confidential = request.user.has_perm('document_management.view_confidential_document')
    if document.is_confidential and not can_view_confidential: raise Http404
    return HttpResponse(f"Placeholder for sharing document '{document.title}'. Sharing UI and logic needed.")
