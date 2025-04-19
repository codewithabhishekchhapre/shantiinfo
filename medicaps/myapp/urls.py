from django.urls import path
from . import views

urlpatterns = [
    # path("",views.home),
    path("register",views.register_view),
     path('login/', views.login_user, name='login'),
     path('users', views.get_all_users, name='get_all_users'),
     path('send-otp',views.send_otp),
    path('employee-profile/create/', views.create_employee_profile, name='create_employee_profile'),
     path('employee-profile/<int:user_id>/', views.get_employee_profile, name='get_employee_profile'),

]