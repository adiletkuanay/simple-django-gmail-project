"""
URL configuration for gmail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from review import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name=''),
    path('compose/', views.compose_message, name='compose'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('register/', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path("logout_user", views.logout_user, name="logout"),
    path('profile', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search', views.item_search, name='item_search'),
    path('create/', views.create_message_request, name='create_message_request'),
    path('list/', views.message_request_list, name='message_request_list'),
    path('approve/<int:message_request_id>/', views.approve_message_request, name='approve_message_request'),
    path('reject/<int:message_request_id>/', views.reject_message_request, name='reject_message_request'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
