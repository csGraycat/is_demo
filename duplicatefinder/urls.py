from django.urls import path

from crmfields.views.reload import reload_start
from duplicatefinder.views.find_duplicate import find_entity_duplicates

urlpatterns = [
    path('find_entity_duplicates/', find_entity_duplicates, name='find_entity_duplicates'),
    path('', reload_start, name='reload_start'),
]
