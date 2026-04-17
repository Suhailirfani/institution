from django.urls import path
from django.contrib.auth import views as auth_views

app_name = "accounts"

from . import views

urlpatterns = [
    # Auth
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),

    # User Management (Admin Only)
    path("manage/", views.UserListView.as_view(), name="user_list"),
    path("manage/add/", views.UserCreateView.as_view(), name="user_create"),
    path("manage/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_update"),
    path("manage/<int:pk>/toggle-status/", views.UserSoftDeleteView.as_view(), name="user_toggle_status"),
]



