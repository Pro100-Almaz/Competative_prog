from django.forms import ModelForm
from .models import UsersList


class CreateAcc(ModelForm):
    class Meta:
        model = UsersList
        fields = ['name', 'email']