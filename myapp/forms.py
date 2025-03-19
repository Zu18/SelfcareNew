from django import forms
from .models import DailyActivity, PersonalGoals, Journal

class DailyActivityForm(forms.ModelForm):
    class Meta:
        model = DailyActivity
        fields = ['date', 'water_intake', 'sleep_hours','meditation']
        labels = {
            'date': 'Date',
            'water_intake': 'Water Intake',
            'sleep_hours': 'Sleep Hours ',
            'meditation': 'Meditation',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'water_intake': forms.NumberInput(attrs={'placeholder': 'Liters of water', 'min': '0', 'class':'form-control'}),
            'sleep_hours': forms.NumberInput(attrs={'placeholder': 'Hours of sleep', 'min': '0', 'class':'form-control'}),
            'meditation': forms.NumberInput(attrs={'placeholder': 'Minutes of meditation', 'min': '0', 'class':'form-control'}),
        }


class PersonalGoalsForm(forms.ModelForm):
    class Meta:
        model = PersonalGoals
        fields = ['goal_title', 'target_date','status', 'goal_description']
        labels = {
            'goal_title': 'Goal',
            'goal_description': 'Description',
            'target_date': 'Target date ',
            'status': 'Status',
        }
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'placeholder': ''}),
            'goal_title': forms.my(attrs={'class':'form-control', 'placeholder': ''}),
            'goal_description': forms.Textarea(attrs={'class':'form-control', 'placeholder': '', 'rows': 5}),
            'status': forms.Select(attrs={'class':'form-control', 'placeholder': ''}),
        }


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['entry_date', 'entry_text']
        labels = {
            'entry_date': 'Date',
            'entry_text': 'What is on your mind?',
        }
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'entry_text': forms.Textarea(attrs={'class':'form-control'}),
        }