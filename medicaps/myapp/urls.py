from django.urls import path
from . import views

urlpatterns = [
    # path("",views.home),
    path("register",views.register_view),
     path('users', views.get_all_users, name='get_all_users'),

]