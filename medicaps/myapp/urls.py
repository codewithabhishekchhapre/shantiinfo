from django.urls import path
from . import views

urlpatterns = [
    path("",views.home),
    path("abc/",views.members),
    path("student/",views.student),
    path("signup-page/",views.signup_page),
    path("htmlpage/",views.htmlpage),
    path("logindata/",views.logindata),
    path("signupdata/",views.signupdata)
]