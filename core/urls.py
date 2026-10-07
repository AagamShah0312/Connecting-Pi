from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("providers/", views.provider_directory, name="provider_directory"),
    path("providers/<str:username>/", views.profile, name="profile"),
    path("skills/new/", views.create_skill, name="create_skill"),
    path("skills/<int:skill_id>/hire/", views.hire_skill, name="hire_skill"),
    path("requests/<int:request_id>/chat/", views.chat, name="chat"),
    path("requests/<int:request_id>/<str:action>/", views.update_request, name="update_request"),
]
