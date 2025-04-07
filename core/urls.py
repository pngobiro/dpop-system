# core/urls.py
from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('authentication.urls')),
    path('permissions/', include('apps.permissions.urls', namespace='permissions')),
    path("statistics/", include("apps.statistics.urls", namespace="statistics")),
    path('login/', auth_views.login_view, name='login'),
    path('budget/', include('apps.budget.urls', namespace='budget')),
    path('meetings/', include('apps.meetings.urls', namespace='meetings')),
    path('memos/', include('apps.memos.urls', namespace='memos')),
    path('mail/', include('apps.mail.urls', namespace='mail')),
    path('innovations/', include('apps.innovations.urls', namespace='innovations')),
    path('pmmus/', include('apps.pmmu.urls', namespace='pmmu')),
    path('tasks/', include('apps.tasks.urls', namespace='tasks')),
    path('documents/', include('apps.document_management.urls', namespace='document_management')), # Added document management URLs

    # The /departments/<id>/modules/ URL is handled within apps.home.urls

    # path("unicorn/", include("django_unicorn.urls")), # Removed as Unicorn is no longer used
    path("", include("apps.home.urls")), # This include handles the department modules URL
    path('react/', TemplateView.as_view(template_name='react.html'), name='react'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
