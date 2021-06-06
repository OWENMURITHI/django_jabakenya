"""jabakenya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import Settings, settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from jaba.views import jaba, sellers



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jaba.urls')),
    path('search', include('jaba.urls')),
    path('aoth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile', sellers.ProfileView.as_view(), name="profile"),
    path('accounts/password/', sellers.change_password , name='change_password'),
    path('accounts/profile/update/<int:pk>/', sellers.ProfileUpdate.as_view(), name='update_user'),
    path('accounts/signup/', jaba.SignUpView.as_view(), name='signup'),
    path('accounts/signup/seller/', sellers.register, name='seller_signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

