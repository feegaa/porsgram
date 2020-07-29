from django.urls import path
from django.contrib.auth import views as auth_views
from user import views

app_name = 'user'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),


    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),

    path('users/', views.users, name='users'),
]

