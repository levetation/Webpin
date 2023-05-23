from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('delete_user', views.delete_user, name='delete_user'),

    # Submit email form
    path('reset_password/', views.auth_views.PasswordResetView.as_view(), name="reset_password"),

    # Email sent success message
    path('reset_password_sent/', views.auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    # Link to password reset form in email
    path('reset/<uidb64>/<token>/', views.auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # Password successfully changed message
    path('reset_password_complete', views.auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]