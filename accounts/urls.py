from django.urls import path
from django.contrib.auth import views as auth_views

app_name = "accounts"

from . import views

app_name = "accounts"

urlpatterns = [
    # Auth
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]



