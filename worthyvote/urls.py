from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.RegisterFormView.as_view(), name='signup'),
    path('signup_successful', views.registration_success, name='signup_success'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('email_confirmed/', views.email_confirmed, name='email_confirmed')
]
