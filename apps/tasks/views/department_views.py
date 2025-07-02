"""
Department-related views for task management.
"""
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

try:
    from apps.organization.models import Department
except ImportError:
    Department = None


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'tasks/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        if not Department:
            # Handle case where Department model is not available
            return Department.objects.none() # Return an empty queryset
        return Department.objects.all().order_by('name')
