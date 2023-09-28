from django.urls import path

from .views import api_post, api_get

urlpatterns = [
    path('stats/username/<str:username>/repo/<str:repo>/', api_get, name='api_get'),
    path('stats/create', api_post, name='api_post')
]
