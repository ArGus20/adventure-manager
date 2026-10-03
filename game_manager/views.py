from typing import Any

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views import generic

from game_manager.forms import AdventureCreateForm
from game_manager.models import User, Adventure, CharacterClass, Character


class HomePageView(TemplateView):
    template_name = "game_manager/home_page.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["players_num"] = User.objects.filter(is_dm=False).count()
        context["masters_num"] = User.objects.filter(is_dm=True).count()
        context["adventures_num"] = Adventure.objects.count()
        return context


class AdventureListView(generic.ListView):
    model = Adventure
    template_name = "game_manager/adventure_list.html"
    context_object_name = "adventure_list"


class AdventureDetailView(generic.DetailView):
    model = Adventure
    queryset = Adventure.objects.select_related(
        "adventure_setting",
        "master"
    ).prefetch_related(
        "players"
    )

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["all_users"] = User.objects.exclude(is_dm=True)
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     adventure = self.get_object()
    #
    #     if request.user == adventure.master:
    #         player_ids = request.POST.getlist("player_ids")
    #
    #         if player_ids:
    #             adventure.players.add(*player_ids)


class AdventureCreateView(generic.CreateView):
    model = Adventure
    form_class = AdventureCreateForm
    success_url = reverse_lazy("game_manager:adventure-list")
    template_name = "game_manager/adventure_form.html"

    def form_valid(self, form) -> HttpResponse:
        form.instance.master = self.request.user
        return super().form_valid(form)


class AdventureUpdateView(generic.UpdateView):
    model = Adventure
    form_class = AdventureCreateForm
    success_url = reverse_lazy("game_manager:adventure-list")
    template_name = "game_manager/adventure_form.html"


class AdventureDeleteView(generic.DeleteView):
    model = Adventure
    success_url = reverse_lazy("game_manager:adventure-list")
    template_name = "game_manager/adventure_contifm_delete.html"


class MasterListView(generic.ListView):
    model = User
    queryset = User.objects.filter(is_dm=True)
    template_name = "game_manager/master_list.html"
    context_object_name = "master_list"


class MasterDetailView(generic.DetailView):
    model = User
    template_name = "game_manager/master_detail.html"
    context_object_name = "master"


class PlayerListView(generic.ListView):
    model = User
    queryset = User.objects.filter(is_dm=False)
    template_name = "game_manager/player_list.html"
    context_object_name = "player_list"


class PlayerDetailView(generic.DetailView):
    model = User
    template_name = "game_manager/player_detail.html"
    context_object_name = "player"

class CharacterDetailView(generic.DetailView):
    model = Character
    queryset = Character.objects.select_related(
        "user",
        "race",
        "character_class"
    )
    template_name = "game_manager/character_detail.html"
    context_object_name = "character"

