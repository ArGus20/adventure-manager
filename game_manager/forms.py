from xml.dom import ValidationErr

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Adventure


class AdventureCreateForm(forms.ModelForm):
    class Meta:
        model = Adventure
        fields = ("name", "description", "start_date", "difficulty", "adventure_setting")
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type":"date"}
            )
        }

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]

        if start_date <= timezone.localdate():
            raise ValidationError("It must be future date!")

        return start_date