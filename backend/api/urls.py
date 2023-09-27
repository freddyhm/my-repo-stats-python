from django.urls import path

from .views import api_home

urlpatterns = [
    path('stats/username/<str:username>/repo/<str:repo>/', api_home) # localhost 
]
