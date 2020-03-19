"""clintwin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path

"""clintwin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

# New additions.
from api import views
from django.conf.urls import url
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views


# End of new additions
# path('accounts/login/', views.login, name='login'),

urlpatterns = [
    path('admin/', admin.site.urls),
	path('accounts/', include('django.contrib.auth.urls')),
	path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('register/', TemplateView.as_view(template_name='register.html'), name='signup'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('', TemplateView.as_view(template_name='index.html'), name='index'),
	path('about', views.AboutPageView.as_view(), name='about'),
	path('how_works', views.HowWorksPageView.as_view(), name='how_works'),
	path('contact', views.ContactPageView.as_view(), name='contact'),
	path('directions', views.DirectionsPageView.as_view(), name='directions'),
	path('contactform', views.contact, name='contactform'),

]
