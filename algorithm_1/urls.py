from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/<uuid:id>/', views.dashboard, name="dashboard"),
    path('delete_password/<uuid:id>/', views.delete_password, name="delete_password"),
    path('edit_password/<uuid:id>/', views.edit_password, name="edit_password"),
    path('view_password/<uuid:id>/', views.view_password, name='view_password'),
    path('settings/<uuid:id>/', views.settings, name='settings'),
    path('account/delete/<uuid:id>/', views.delete_account, name='delete_account'),
    path('feedback/<uuid:id>/', views.feedback, name='feedback'),
    path('delete_login_history/<uuid:id>', views.delete_login_history, name='delete_login_history'),
    # path("admins/reset_password/", auth_views.PasswordResetView.as_view()),
    # path("admins/reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path("admins/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path("admins/reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    

]