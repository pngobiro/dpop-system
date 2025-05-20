# This directory is a Python package
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Document

@login_required
def library(request):
    """Main document library view"""
    documents = Document.objects.all().order_by('-created_at')
    return render(request, 'document_management/library.html', {'documents': documents})

@login_required
def document_detail(request, pk):
    """Document detail view"""
    document = Document.objects.get(pk=pk)
    return render(request, 'document_management/detail.html', {'document': document})