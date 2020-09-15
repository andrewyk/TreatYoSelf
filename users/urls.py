from django.urls import path, include
from . import views
from .api import RegistrationAPI, LoginAPI, UserAPI, CreateProfileAPI, ProfileAPI
from knox import views as knox_views

urlpatterns = [
    # path("api/users/", views.ProfileListCreate.as_view()),
    path('auth', include('knox.urls')),
    path('auth/register', RegistrationAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/user/update', UserAPI.as_view()),
    # clears the token, so users have to log back in
    path('auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('total', CreateProfileAPI.as_view()),
    path('total/get', ProfileAPI.as_view()),

]

# Register, Login, Logout post requests
# User get request
