from django.urls import path

from .views import (
    HomePageView,
    AdventureListView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),
    path("adventures/", AdventureListView.as_view(), name="adventure-list")
]

app_name = "game_manager"