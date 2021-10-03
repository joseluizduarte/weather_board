"""weather_board URL Configuration"""

from django.contrib import admin
from django.urls import path

from board.views import HomeView, BoardView, NewBoardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('board/<str:uniqueCode>', BoardView.as_view(), name='board'),
    path('newBoard', NewBoardView.as_view(), name='new_board'),
    path('admin/', admin.site.urls, name='admin'),
]
