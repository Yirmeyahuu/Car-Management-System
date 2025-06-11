from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('Cars/', include('CarsApp.urls')),  # Include the URLs from CrudApp
    path('admin/', admin.site.urls),
]