from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('CarsApp.urls')),  # Include the URLs from CrudApp
    path('admin/', admin.site.urls),
]