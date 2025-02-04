# apps/home/views.py
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect # IMPORT IS HERE!
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from apps.organization.models import Department
from apps.home.models import Module # Import Module model

@login_required
def dashboard(request):
    departments = Department.objects.prefetch_related('roles').filter(is_active=True)
    return render(request, "home/dashboard.html", {'departments': departments})

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
            
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
        
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required
def department_modules(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    # all_modules = Module.objects.filter(department=department) # Get all modules for the department
    all_modules = Module.objects.all()
    permitted_modules = []

    for module in all_modules:
        permission_codename = f'home.{module.permission_codename}' # Construct full permission codename (app_label.codename)
        if request.user.has_perm(permission_codename): # Check if user has permission
            permitted_modules.append(module)

    context = {
        'department': department,
        'modules': permitted_modules, # Pass only permitted modules to the template
    }
    return render(request, "home/department_modules.html", context)