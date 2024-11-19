
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('bus-list/<int:id>/', views.bus_list, name="bus-list"),
    path('bus-single/<slug:slug>/', views.bus_single, name="bus-single"),
    path('book-seat/<int:bus_id>/<int:route_id>/', views.book_seat, name='book_seat'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment_view'),
    # path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('add-suggestion', views.suggestions, name='suggestions'),
    path('contact-us', views.contact_us, name='contact_us'),
    path('services', views.services_list, name='services'),
    path('blog', views.post_list, name='post_list'),
    path('blog/single/<slug>', views.post_single, name='post_single'),
    path('services/single/<slug>', views.services_single, name='services_single'),
    path('blog/category/<str:name>', views.post_by_category, name='post_by_category'),
    path('blog/tags/<str:name>', views.post_by_tag, name='post_by_tag'),
    path('faqs/', views.faqs, name='faqs'),


    #user Dashboard Views
    path('panel', views.dashboard, name="dashboard"),
    path('panel/settings', views.profile_settings, name="profile_settings"),
    path('panel/my-bookings', views.my_booking, name="my_booking"),
    path('panel/ratings', views.user_ratings, name="user_ratings"),
]
