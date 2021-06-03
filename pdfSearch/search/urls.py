from django.urls import path
from .views import *

app_name = 'search'

urlpatterns = [
    path('', home,name='home'),
    path('det/', detail,name='detail'),
]