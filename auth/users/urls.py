from django.urls import path
from .views import RegisterView, LoginView, UserView, Logaut

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logaut', Logaut.as_view()),

]
