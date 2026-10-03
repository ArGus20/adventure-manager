from django.contrib.auth.models import AbstractUser
from django.db import models


class CharacterClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    is_dm = models.BooleanField(default=False)

    class Meta:
        ordering = ("username", )

    def __str__(self) -> str:
        return self.username


class Race(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Character(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="characters",
    )
    character_name = models.CharField(max_length=255)
    race = models.ForeignKey(
        Race,
        on_delete=models.PROTECT,
        related_name="characters"
    )
    gender = models.CharField(max_length=6, choices=Gender.choices)
    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.PROTECT,
        related_name="characters"
    )

    class Meta:
        ordering = ("character_name", )

    def __str__(self) -> str:
        return self.character_name


class AdventureSettings(models.Model):
    type = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ("type",)

    def __str__(self) -> str:
        return self.type


class Adventure(models.Model):
    class Difficulty(models.TextChoices):
        LOW = "low", "Low"
        MODERATE = "moderate", "Moderate"
        HIGH = "high", "High"

    name = models.CharField(max_length=255)
    description = models.TextField()
    added_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    difficulty = models.CharField(
        max_length=8,
        choices=Difficulty.choices
    )
    adventure_setting = models.ForeignKey(
        AdventureSettings,
        on_delete=models.PROTECT,
        related_name="adventures"
    )
    master = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="mastered_adventures"
    )
    players = models.ManyToManyField(
        User,
        related_name="joined_adventures"
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
