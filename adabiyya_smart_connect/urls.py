"""
URL configuration for adabiyya_smart_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Public website & dashboards
    path("", include("core.urls")),

    # ERP modules
    path("accounts/", include("accounts.urls")),
    path("admissions/", include("admissions.urls")),
    path("academics/", include("academics.urls")),
    path("payments/", include("payments.urls")),
    path("sponsorship/", include("sponsorship.urls")),
    path("committee/", include("committee.urls")),

    # API endpoints (versioned for future mobile apps)
    path("api/v1/accounts/", include("accounts.api_urls")),
    path("api/v1/admissions/", include("admissions.api_urls")),
    path("api/v1/academics/", include("academics.api_urls")),
    path("api/v1/payments/", include("payments.api_urls")),
    path("api/v1/sponsorship/", include("sponsorship.api_urls")),
    path("api/v1/committee/", include("committee.api_urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Force reload for Admission Letter URL

