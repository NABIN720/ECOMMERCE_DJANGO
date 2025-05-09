from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup_view, name='signup_view'),
    path('login/',views.login_view, name='login_view'),
    path('logout/',views.logout_view, name='logout'),   
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('index/',views.index, name='index')
]