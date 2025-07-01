from django import forms
from .models import Event, Participant, Category
from datetime import date

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean_date(self):
        event_date = self.cleaned_data.get('date')
        if event_date and event_date < date.today():
            raise forms.ValidationError("Event date can't be in the past.")
        return event_date

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
