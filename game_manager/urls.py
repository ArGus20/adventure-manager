from django.urls import path

from .views import (
    HomePageView,
    AdventureListView,
    AdventureDetailView,
    AdventureCreateView,
    AdventureUpdateView,
    AdventureDeleteView,
    MasterListView,
    PlayerListView,
    MasterDetailView,
    PlayerDetailView,
    CharacterDetailView,
    ManagePlayerAdventuresView,
    UserDeleteView,
    CharacterCreateView,
    CharacterUpdateView,
    CharacterDeleteView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),

    path("adventures/", AdventureListView.as_view(), name="adventure-list"),
    path("adventures/<int:pk>/", AdventureDetailView.as_view(), name="adventure-detail"),
    path("adventures/create/", AdventureCreateView.as_view(), name="adventure-create"),
    path("adventures/<int:pk>/update/", AdventureUpdateView.as_view(), name="adventure-update"),
    path("adventures/<int:pk>/delete/", AdventureDeleteView.as_view(), name="adventure-delete"),

    path("masters/", MasterListView.as_view(), name="master-list"),
    path("masters/<int:pk>/", MasterDetailView.as_view(), name="master-detail"),
    path("masters/<int:pk>/delete", UserDeleteView.as_view(), name="master-delete"),

    path("players/", PlayerListView.as_view(), name="player-list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("players/<int:pk>/delete", UserDeleteView.as_view(), name="player-delete"),
    path("players/<int:pk>/player-adventures", ManagePlayerAdventuresView.as_view(), name="manage-player-adventures"),

    path("players/<int:player_pk>/character/<int:pk>", CharacterDetailView.as_view(), name="character-detail"),
    path("players/<int:player_pk>/character/create/", CharacterCreateView.as_view(), name="character-create"),
    path("players/<int:player_pk>/character/<int:pk>/update/", CharacterUpdateView.as_view(), name="character-update"),
    path("players/<int:player_pk>/character/<int:pk>/delete/", CharacterDeleteView.as_view(), name="character-delete"),

]

app_name = "game_manager"