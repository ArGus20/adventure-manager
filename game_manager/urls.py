from django.urls import path

from .views import (
    HomePageView,
    AdventureListView,
    AdventureDetailView,
    AdventureCreateView,
    AdventureUpdateView,
    AdventureDeleteView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),

    path("adventures/", AdventureListView.as_view(), name="adventure-list"),
    path("adventures/<int:pk>/", AdventureDetailView.as_view(), name="adventure-detail"),
    path("adventures/create/", AdventureCreateView.as_view(), name="adventure-detail"),
    path("adventures/<int:pk>/update/", AdventureUpdateView.as_view(), name="adventure-update"),
    path("adventures/<int:pk>/delete/", AdventureDeleteView.as_view(), name="adventure-delete"),

]

app_name = "game_manager"

# path("classes/", CharacterClassListView.as_view(), name="character-class-list"),
#
#
# class CharacterClassListView(generic.ListView):
#     model = CharacterClass
#     template_name = "game_manager/character_class_list.html"
#     context_object_name = "character_class_list"