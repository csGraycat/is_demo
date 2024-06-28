from django.urls import path

from .views import company_to_db

urlpatterns = [
    path('', company_to_db, name='company_to_db'),
]
