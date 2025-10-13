"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from post import views as post_views
from django.conf import settings # we added this to be able to access the media files in the browser
from django.conf.urls.static import static # we added this to be able to access the media files in the browser

from django.contrib.auth import views as auth_views

from django.shortcuts import redirect

from BlogApi.views import PostViewSet

from .views import signup # we added this to be able to use the built-in login and logout views

from post.views import about

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions, routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="API for blog posts"
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
    path('admin/', admin.site.urls),

    # Home Page (food blog landing)
    path('', post_views.home, name='home'),

    # Posts URLs
    path('', include('post.urls')),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', signup, name='signup'),

    path('about/', about, name='about'),

    path('api/', include(router.urls)),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    re_path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# we added the above code to be able to access the media files in the browser. Note that this is only for development purposes. In production, you will need to configure your web server to serve media files.