"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView,SpectacularSwaggerView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('accounts/',include('accounts_app.urls', namespace='accounts_app')),
    path('projects/',include('projects.urls', namespace='project')),
    path('message/',include('massages.urls', namespace='massage')),
    path('meta/',include('meta.urls', namespace='meta')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('schema/',SpectacularAPIView.as_view(),name='schema'),
    path('schema/ui/',SpectacularRedocView.as_view(url_name='schema'),name='swagger-iu'),
    path('schema/redoc/',SpectacularSwaggerView.as_view(url_name='schema'),name='redoc'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)