# core/urls.py
from django.contrib import admin
from django.urls import path, include
from authentication import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('authentication.urls')),  # <--- Ensure THIS line is here
    path('permissions/', include('apps.permissions.urls', namespace='permissions')), # ADD THIS
    path("statistics/", include("apps.statistics.urls", namespace="statistics")),
    path('login/', views.login_view, name='login'),
    path('budget/', include('apps.budget.urls', namespace='budget')),
    path('meetings/', include('apps.meetings.urls', namespace='meetings')),
    path('memos/', include('apps.memos.urls', namespace='memos')),
    path('mail/', include('apps.mail.urls', namespace='mail')),
    path("unicorn/", include("django_unicorn.urls")),
    path("", include("apps.home.urls")),
    path('react/', TemplateView.as_view(template_name='react.html'), name='react'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
