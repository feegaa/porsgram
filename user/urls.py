from django.urls import path, include
# from django.contrib.auth import views as auth_views

from user import views

# from django_email_verification import urls as mail_urls

app_name = 'user'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('confirm-email/<str:email>/<str:email_token>', views.confirmEmail, name='confirmation'),
    path('what-is-email/', views.getEmailForResetPassword, name='getEmailForResetPassword'),
    path('reset-password/<str:username>/<str:email>/<str:email_token>', views.ResetPasswordView.as_view(), name='resetPasswordVerifyToken'),

    # path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),


    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),

    path('users/', views.users, name='users'),
    path('user/<int:id>', views.user, name='user'),
]

