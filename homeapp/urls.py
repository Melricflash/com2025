from django.urls import path
from . import views

app_name = "homeapp" # namespace for this app

urlpatterns = [
    #/signup
    path('signup', views.RegisterUser.as_view(), name='signup_user'),
    #/contact
    path('contact', views.contact, name = 'contact'),
    path('', views.home, name = 'home'),
]