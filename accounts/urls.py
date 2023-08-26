from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path("login/", views.loginView.as_view() , name="login"),
    path('register/',views.registrationView.as_view(), name='register'),
    path('logout/', views.logoutView.as_view(), name='logout')
]
