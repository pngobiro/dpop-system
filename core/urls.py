from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


app_name = "apps.core"

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("statistics/", include("apps.statistics.urls", namespace="statistics")),
    path('budget/', include('apps.budget.urls', namespace='budget')),
    path("unicorn/", include("django_unicorn.urls")),
    path("", include("apps.home.urls")), # UI Kits Html files

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns


