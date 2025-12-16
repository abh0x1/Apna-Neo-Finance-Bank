from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core app (Home, About, Contact)
    path("", include("core.urls")),

    # Accounts app (signup, login, dashboard etc.)
    path("accounts/", include("accounts.urls")),

    # Support app
    path("support/", include("support.urls")),

    path("banking/", include(("banking.urls", "banking"), namespace="banking")),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)