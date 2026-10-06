from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views import View, generic

from game_manager.forms import AdventureCreateForm, AdventureNameSearchForm, UserUsernameSearchForm
from game_manager.models import User, Adventure, Character


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
    paginate_by = 5

    def get_context_data(
            self,
            *,
            object_list=None,
            **kwargs
    ) -> dict:
        context = super(AdventureListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = AdventureNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Adventure.objects.all()
        form = AdventureNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class AdventureDetailView(generic.DetailView):
    model = Adventure
    queryset = Adventure.objects.select_related(
        "adventure_setting",
        "master"
    ).prefetch_related(
        "players"
    )


class AdventureCreateView(LoginRequiredMixin, generic.CreateView):
    model = Adventure
    form_class = AdventureCreateForm
    success_url = reverse_lazy("game_manager:adventure-list")
    template_name = "game_manager/adventure_form.html"

    def form_valid(self, form) -> HttpResponse:
        form.instance.master = self.request.user
        return super().form_valid(form)


class AdventureUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Adventure
    form_class = AdventureCreateForm
    success_url = reverse_lazy("game_manager:adventure-list")
    template_name = "game_manager/adventure_form.html"


class AdventureDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Adventure
    success_url = reverse_lazy("game_manager:adventure-list")
    template_name = "game_manager/adventure_contifm_delete.html"


class MasterListView(generic.ListView):
    model = User
    template_name = "game_manager/master_list.html"
    context_object_name = "master_list"
    paginate_by = 5

    def get_context_data(
            self,
            *,
            object_list=None,
            **kwargs
    ) -> dict:
        context = super(MasterListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = UserUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = User.objects.filter(is_dm=True)
        form = UserUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class MasterDetailView(generic.DetailView):
    model = User
    template_name = "game_manager/master_detail.html"
    context_object_name = "master"


class PlayerListView(generic.ListView):
    model = User
    template_name = "game_manager/player_list.html"
    context_object_name = "player_list"
    paginate_by = 5

    def get_context_data(
            self,
            *,
            object_list=None,
            **kwargs
    ) -> dict:
        context = super(PlayerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = UserUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = User.objects.filter(is_dm=False, is_superuser=False)
        form = UserUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


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


class CharacterCreateView(LoginRequiredMixin, generic.CreateView):
  model = Character
  fields = ["name", "race", "character_class", "bio"]
  template_name = "game_manager/character_form.html"

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_success_url(self):
    return reverse(
        "game_manager:player-detail", kwargs={"pk": self.request.user.pk}
    )


class CharacterUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
  model = Character
  fields = ["name", "race", "character_class", "bio"]
  template_name = "game_manager/character_form.html"

  def test_func(self):
    return self.get_object().user == self.request.user

  def get_success_url(self):
    return reverse(
        "game_manager:player-detail", kwargs={"pk": self.request.user.pk}
    )


class CharacterDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView
):
  model = Character
  template_name = "game_manager/character_confirm_delete.html"

  def test_func(self):
    return self.get_object().user == self.request.user

  def get_success_url(self):
      return reverse(
          "game_manager:player-detail", kwargs={"pk": self.request.user.pk}
      )


class ManagePlayerAdventuresView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any) -> HttpResponse:
        player = get_object_or_404(User, pk=pk)
        adventures = Adventure.objects.filter(master=request.user)
        context = {
            "player": player,
            "adventures": adventures
        }

        return render(request, "game_manager/manage_player_adventures.html", context=context)

    def post(self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any) -> HttpResponse:
        player = get_object_or_404(User, pk=pk)
        selected_ids = request.POST.getlist("adventures_ids")
        master_adventures = Adventure.objects.filter(master=request.user)

        for adventure in master_adventures:
            adventure.players.remove(player)

        for adventure in master_adventures.filter(id__in=selected_ids):
            adventure.players.add(player)

        return redirect("game_manager:player-list")


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = "game_manager/user_confirm_delete.html"

    def get_success_url(self) -> str:
        if self.object.is_dm:
            return reverse("game_manager:master-list")
        return reverse("game_manager:player-list")
