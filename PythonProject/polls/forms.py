from django import forms
from .models import Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['option', 'email', 'name']

    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll', None)
        super().__init__(*args, **kwargs)

        if self.poll:
            self.fields['option'].queryset = self.poll.options.all()
            if not self.poll.voting_security_email:
                self.fields.pop('email')
            if not self.poll.display_names:
                self.fields.pop('name')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if self.poll and self.poll.voting_security_email and email:
            if Vote.objects.filter(poll=self.poll, email=email).exists():
                raise forms.ValidationError("You have already voted in this poll.")

        return cleaned_data
