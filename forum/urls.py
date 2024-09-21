from django.urls import path
from .views import registerUser,loginUser,checkUser,question

urlpatterns = [
    path('users/register/', registerUser),
    path('users/login/', loginUser),
    path('users/check/',checkUser),
    path('users/abene/',question),
]