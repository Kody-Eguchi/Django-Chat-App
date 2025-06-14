from django.urls import path
from a_users.views import *

urlpatterns = [
    path('', profile_view, name="profile"),
]
