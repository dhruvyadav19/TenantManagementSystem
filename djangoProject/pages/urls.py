from django.urls import path
from .views import home_view, about_view, search_view
from django.conf.urls.static import static
urlpatterns = [
    path('',home_view, name = 'home-view'),
    path('about/',about_view, name = 'about-view'),
    path('search/',search_view,name = 'search-view'),
]
