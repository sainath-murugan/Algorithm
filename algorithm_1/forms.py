from django.forms.widgets import Textarea
from .models import Vault, FeedBack
from django.forms import ModelForm, TextInput 


class VaultForm(ModelForm):
    
    class Meta:
        model = Vault
        fields = [
            'key',
            'value'
        ]
        widgets = {
            'key': TextInput(attrs={'placeholder': 'key',}),
            'value': TextInput(attrs={'placeholder': 'value',}),
        }

class FeedBackForm(ModelForm):
    
    class Meta:
        model = FeedBack
        fields = [
            'feedback'
        ]
        widgets = {
            'feedback': Textarea(attrs={'placeholder': 'Enter your feedback or tell us know what you want...',}),
        }
        
