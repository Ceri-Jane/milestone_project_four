from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    """
    Form for creating and editing entries.
    Used for server-side validation and clean saving.
    """

    class Meta:
        model = Entry

        # Mood is derived from the hue slider in the view
        fields = ["hue", "notes"]

        widgets = {
            # Hue value is set via the slider in the template
            "hue": forms.TextInput(attrs={"type": "hidden"}),

            # Optional free-text notes
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_hue(self):
        """Ensure hue stays within a valid range."""
        hue = self.cleaned_data.get("hue")

        if not hue:
            return ""

        try:
            hue = int(hue)
        except (TypeError, ValueError):
            return ""

        return str(max(0, min(100, hue)))
