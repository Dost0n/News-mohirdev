from django.urls import path
from main.views import home, error, single, contact, ContactView, category, Homeview, NewsUpdateView, NewsDeleteView, NewsCreateView, SearchList


urlpatterns = [
    path('', Homeview.as_view(), name = 'home'),
    path('create/', NewsCreateView.as_view(), name = 'create'),
    path('<slug>/update/', NewsUpdateView.as_view(), name = 'update'),
    path('<slug>/delete/', NewsDeleteView.as_view(), name = 'delete'),
    path('error/', error, name = 'error'),
    path('contact/', contact, name = 'contact'),
    path('category/<int:pk>', category, name = 'category'),
    path('contactview/', ContactView.as_view(), name = 'contactview'),
    path('single/<slug:news>/', single, name = 'single'),
    path('search/', SearchList.as_view(), name = 'search'),
]