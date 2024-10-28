from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-page"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('delete-task/<str:name>', views.deleteTask, name="delete"),
    path('update-task/<str:name>', views.update, name="update"),
]