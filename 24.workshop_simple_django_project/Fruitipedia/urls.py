from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Fruitipedia.fruits.urls')),  # Route root URL to fruits app
]
