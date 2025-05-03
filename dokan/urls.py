from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="dokanhome"),
    path('about/',views.about, name="AboutUs"),
    path('contact/',views.contact, name="ContactUs"),
    path('tracker/',views.tracker, name="TrackingStatus"),
    path('productview/<int:pid>',views.prodview, name="ProductView"),
    path('checkout/',views.checkout, name="Checkout"),
    # path('search/',views.search, name="Search")
]