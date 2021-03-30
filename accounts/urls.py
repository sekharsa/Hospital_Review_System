from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('userReg', views.userReg, name="UserRegisteration"),
    path('docReg', views.docReg, name="DoctorRegisteration"),
    path('hospReg', views.hospReg, name="HospitalRegisteration"),
    path('forgPass', views.forgPass, name="ForgotPassword"), 
]
