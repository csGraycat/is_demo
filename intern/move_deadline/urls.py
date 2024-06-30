from django.urls import path, include
from .views.move_deadline_view import move_deadline_js, move_deadline

urlpatterns = [
    path('', move_deadline_js, name='move_deadline_js'),
    path('move_deadline/', move_deadline, name='move_deadline'),
]
