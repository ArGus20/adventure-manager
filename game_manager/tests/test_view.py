import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from game_manager.models import (
    Adventure,
    AdventureSettings,
    Character,
    CharacterClass,
    Race,
)

User = get_user_model()


class EssentialViewTests(TestCase):
    def setUp(self):
        self.dm = User.objects.create_user(username="dm_user", password="123", is_dm=True)
        self.player = User.objects.create_user(username="player_user", password="123", is_dm=False)
        self.setting = AdventureSettings.objects.create(type="Fantasy")

    def test_home_page_counts(self):
        Adventure.objects.create(
            name="Quest",
            start_date=datetime.date.today(),
            difficulty="low",
            adventure_setting=self.setting,
            master=self.dm,
        )
        res = self.client.get(reverse("game_manager:home-page"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["players_num"], 1)
        self.assertEqual(res.context["masters_num"], 1)
        self.assertEqual(res.context["adventures_num"], 1)

    def test_adventure_search(self):
        adv = Adventure.objects.create(
            name="Dragon Lair",
            start_date=datetime.date.today(),
            difficulty="high",
            adventure_setting=self.setting,
            master=self.dm,
        )
        res = self.client.get(reverse("game_manager:adventure-list"), {"name": "Dragon"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(adv, res.context["adventure_list"])

    def test_character_update_permission_only_owner(self):
        race = Race.objects.create(name="Elf")
        c_class = CharacterClass.objects.create(name="Mage")
        char = Character.objects.create(
            user=self.player,
            character_name="Hero",
            race=race,
            character_class=c_class,
            gender="male",
        )
        url = reverse(
            "game_manager:character-update",
            kwargs={"player_pk": self.player.pk, "pk": char.pk},
        )

        self.client.force_login(self.dm)
        self.assertEqual(self.client.get(url).status_code, 403)

        # Власник має доступ
        self.client.force_login(self.player)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_manage_player_adventures_sync(self):
        adv = Adventure.objects.create(
            name="Quest 1",
            start_date=datetime.date.today(),
            difficulty="low",
            adventure_setting=self.setting,
            master=self.dm,
        )
        self.client.force_login(self.dm)
        url = reverse("game_manager:manage-player-adventures", kwargs={"pk": self.player.pk})

        self.client.post(url, {"adventures_ids": [adv.id]})
        self.assertIn(self.player, adv.players.all())

    def test_user_delete_redirects_by_role(self):
        self.client.force_login(self.dm)

        res_dm = self.client.post(reverse("game_manager:master-delete", kwargs={"pk": self.dm.pk}))
        self.assertRedirects(res_dm, reverse("game_manager:master-list"))

        self.client.force_login(self.player)
        res_player = self.client.post(reverse("game_manager:player-delete", kwargs={"pk": self.player.pk}))
        self.assertRedirects(res_player, reverse("game_manager:player-list"))