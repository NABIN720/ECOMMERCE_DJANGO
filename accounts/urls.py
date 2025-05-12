from django.urls import path
from . import views


urlpatterns = [
    path('signup/',views.signup_view, name='signup_view'),
    path('login/',views.login_view, name='login_view'),
    path('logout/',views.logout_view, name='logout'),   
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('index/',views.index, name='index'),
    path('pass_reset/',views.password_reset,name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

]