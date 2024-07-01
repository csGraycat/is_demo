from django.urls import path

from crmfields.views.reload import reload_start
from .views.grid_view import show_grid

urlpatterns = [
    path('deal_grid/', show_grid, name='show_grid'),
    path('reload_start/', reload_start)
]