from typing import Any
from django.views.generic.base import TemplateView
from django.views import generic

from game_manager.models import User, Adventure


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

