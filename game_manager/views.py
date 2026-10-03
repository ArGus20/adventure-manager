from typing import Any

from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views import generic

from game_manager.models import User, Adventure, CharacterClass


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
    fields = "__all__"
    success_url = reverse_lazy("game_manager:adventure_list")
    template_name = "game_manager/adventure_form.html"


class AdventureUpdateView(generic.UpdateView):
    model = Adventure
    fields = "__all__"
    success_url = reverse_lazy("game_manager:adventure_list")
    template_name = "game_manager/adventure_form.html"


class AdventureDeleteView(generic.DeleteView):
    model = Adventure
    success_url = reverse_lazy("game_manager:adventure_list")
    template_name = "game_manager/adventure_contifm_delete.html"





