from django.test import SimpleTestCase, TestCase
from game_manager.models import (
    Adventure,
    AdventureSettings,
    Character,
    CharacterClass,
    Race,
    User,
)


class ModelStrTests(SimpleTestCase):
    def test_character_class_str(self):
        char_class = CharacterClass(name="Wizard")
        self.assertEqual(str(char_class), "Wizard")

    def test_user_str(self):
        user = User(username="dungeon_master")
        self.assertEqual(str(user), "dungeon_master")

    def test_race_str(self):
        race = Race(name="Elf")
        self.assertEqual(str(race), "Elf")

    def test_character_str(self):
        character = Character(character_name="Legolas")
        self.assertEqual(str(character), "Legolas")

    def test_adventure_settings_str(self):
        setting = AdventureSettings(type="Dark Fantasy")
        self.assertEqual(str(setting), "Dark Fantasy")

    def test_adventure_str(self):
        adventure = Adventure(name="Curse of Strahd")
        self.assertEqual(str(adventure), "Curse of Strahd")


class UserModelTests(TestCase):
    def test_user_is_dm_default_false(self):
        user = User.objects.create_user(
            username="player_one",
            password="securepassword123"
        )
        self.assertFalse(user.is_dm)