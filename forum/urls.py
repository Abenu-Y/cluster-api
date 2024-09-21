from django.urls import path
from .views import registerUser,loginUser

urlpatterns = [
    path('users/register/', registerUser),
    path('users/login/', loginUser),
]