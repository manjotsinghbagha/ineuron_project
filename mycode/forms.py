from django.forms import ModelForm
from .models import MyCode

class MyCodeForm(ModelForm):
    class Meta:
        model = MyCode
        fields = ['code_name', 'code', 'language']
