from django.urls import path

from users.views import UserRegister, CustomAuthToken, Logout

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

]
