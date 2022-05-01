from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserLoginForm, PassResetForm, PassResetConfirmForm
from apps.core.views import frontpage



app_name="account_"
urlpatterns = [
    path('check-registration/', views.registration_check, name="registration_check"),
    path('delete_confirmation/', auth_views.TemplateView.as_view(
        template_name='account/user/delete_confirmation.html'), name="delete_confirmation"),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/user/password_reset_form.html',
        success_url='password_reset_email_confirm',
        email_template_name='account/user/password_reset_email.html',
        form_class=PassResetForm),
        name="password_reset"),

    path('edit_login/', auth_views.PasswordResetView.as_view(
            template_name='account/user/password_reset_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='account/user/password_reset_email.html',
            form_class=PassResetForm),
            name="edit_login"),
    path('password_reset/password_reset_email_confirm/', auth_views.TemplateView.as_view(
        template_name='account/user/reset_status.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/user/password_reset_confirm.html',
        success_url='/account/password_reset_complete/',
        form_class=PassResetConfirmForm),
        name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.TemplateView.as_view(
        template_name='account/user/reset_status.html'), name="password_reset_complete"),
    path('register/', views.account_registration, name="register"),
    path('activate/<uidb64>/<token>/', views.account_activation,  name="activate_"),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',form_class=UserLoginForm), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name="logout"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/set_default/", views.set_default, name="set_default"),
]
