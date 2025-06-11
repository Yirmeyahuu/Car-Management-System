from django.urls import path
from . import views
from .views import ImportCSV

urlpatterns = [
    path('', views.home, name='Home'),
    path('create/', views.Create, name='Create'),
    path('read/', views.Read, name='Read'),
    path('update/<int:uid>/', views.Update, name='Update'),
    path('delete/<int:uid>/', views.Delete, name='Delete'),
    path('archive/', views.Archive, name='Archive'),
    path('retrieve/<int:uid>/', views.Retrieve, name='Retrieve'),
    path('dashboard/', views.Dashboard, name='Dashboard'),
    path('hard_delete/<int:uid>/', views.HardDelete, name='HardDelete'),
    path('import-csv/', ImportCSV, name='ImportCSV'),
]