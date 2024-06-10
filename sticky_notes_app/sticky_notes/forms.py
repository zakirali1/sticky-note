from django import forms
from .models import Sticky_Notes


class StickyForm(forms.ModelForm):

    class Meta:
        model = Sticky_Notes
        fields = ['title', 'things_to_do']