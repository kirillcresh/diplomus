from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='main'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('manager/', views.manage, name='manager'),
]