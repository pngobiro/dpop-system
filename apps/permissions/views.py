# apps/permissions/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.home.models import Module
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
from apps.organization.models import Department  # Import Department
from django.forms import modelformset_factory # Import

User = get_user_model()


@login_required
@permission_required('auth.change_permission', raise_exception=True)  # Require permission to change permissions
def manage_permissions(request):
    modules = Module.objects.all()
    selected_module_id = None
    selected_module = None
    permissions = []  # Initialize permissions
    users_with_permissions = []

    if request.method == 'POST':
        selected_module_id = request.POST.get('module')
    elif request.method == 'GET':
        selected_module_id = request.GET.get('module')

    if selected_module_id:
        selected_module = get_object_or_404(Module, pk=selected_module_id)
        content_type = ContentType.objects.get_for_model(selected_module)
        # --- CRUCIAL CHANGE: Filter permissions by content_type ---
        permissions = Permission.objects.filter(content_type=content_type)
        all_users = User.objects.all().prefetch_related('user_roles__role__permissions') # added permission to prefetch

        for user in all_users:
            user_permissions = {perm.codename: False for perm in permissions}
            for user_role in user.user_roles.filter(is_active=True): # Filter for active roles
                 for perm in user_role.role.permissions.all():
                    if perm.content_type == content_type:  # IMPORTANT: Only consider relevant permissions
                        user_permissions[perm.codename] = True

            users_with_permissions.append({
                'user': user,
                'permissions': user_permissions,
            })
    if request.method == 'POST':
        if not selected_module:
             return HttpResponse("No module selected.", status=400)

        for user_data in users_with_permissions:
            user = user_data['user']
            for perm_codename, has_perm in user_data['permissions'].items():
              permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
              user_roles = user.user_roles.filter(is_active=True) # get the user roles

              for user_role in user_roles:
                if request.POST.get(f'user_{user.id}_perm_{permission.id}') == 'on':
                  if permission not in user_role.role.permissions.all():
                    user_role.role.permissions.add(permission)
                elif permission in user_role.role.permissions.all():
                    user_role.role.permissions.remove(permission) # remove all permission if not selected.

        messages.success(request, 'Permissions updated successfully.')
        return redirect('permissions:manage_permissions')  # Redirect after POST


    context = {
        'modules': modules,
        'selected_module': selected_module,
        'users_with_permissions': users_with_permissions,
        'permissions': permissions,  # Pass the *filtered* permissions
    }
    return render(request, 'permissions/manage_permissions.html', context)

@login_required
@permission_required('home.change_module', raise_exception=True) # Require permission to change module
def assign_departments(request):
    ModuleFormSet = modelformset_factory(Module, fields=('departments',), extra=0)

    if request.method == 'POST':
        formset = ModuleFormSet(request.POST, queryset=Module.objects.all())
        if formset.is_valid():
            formset.save()
            messages.success(request, "Department assignments updated successfully.")
            return redirect('permissions:assign_departments')  # Redirect after saving
        else:
            messages.error(request, "There was a problem updating the assignments.")  # For debugging
            print(formset.errors)
    else:
        formset = ModuleFormSet(queryset=Module.objects.all())

    return render(request, 'permissions/assign_departments.html', {'formset': formset})