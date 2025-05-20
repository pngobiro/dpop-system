# apps/home/views.py
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse # Import reverse
from django.shortcuts import render
from apps.organization.models import Department
from apps.home.models import Module # Import Module model
from django.db.models import Q
from types import SimpleNamespace # Import SimpleNamespace to create mock objects

# Import the Project model from the tasks app
try:
    from apps.tasks.models import Project as TaskProject
except ImportError:
    TaskProject = None

# Check if document management app is installed (for library link)
try:
    from apps.document_management.models import Document
    document_app_exists = True
except ImportError:
    document_app_exists = False


def react_view(request):
    return render(request, 'home/react.html')

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

    # Fetch existing permitted modules based on home.Module permissions
    all_modules = Module.objects.filter(departments=department)
    permitted_modules = []
    for module in all_modules:
        permission_codename = f'home.{module.permission_codename}'
        if request.user.has_perm(permission_codename):
            permitted_modules.append(module)

    # --- Add Dynamic Task Projects Module ---
    if TaskProject:
        try:
            task_project_url = reverse('tasks:department_task_project_list', args=[department_id])
            task_projects_module = SimpleNamespace(
                name="Task Projects", url=task_project_url, url_name='dynamic_task_url',
                icon_class="fa fa-tasks", description="Track service delivery tasks and projects"
            )
            permitted_modules.append(task_projects_module)
        except Exception as e:
            print(f"Error creating Task Projects module link: {e}")

    # --- Add Dynamic Digital Library Module ---
    if document_app_exists:
         try:
            # Add query parameter to track originating department
            library_url = reverse('document_management:library') + f'?from_dept={department_id}'
            if request.user.has_perm('document_management.view_document'):
                library_module = SimpleNamespace(
                    name="Digital Library", url=library_url, url_name='dynamic_library_url',
                    icon_class="fa fa-book-open", description="Search and access documents"
                )
                permitted_modules.append(library_module)
         except Exception as e:
            print(f"Error creating Digital Library module link: {e}")


    context = {
        'department': department,
        'modules': permitted_modules,
    }
    return render(request, "home/department_modules.html", context)