from django.contrib import admin
from app import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('verify/', views.verify_otp, name = "verify_otp")
]
