from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["placeholder"] = "Name"
        self.fields["description"].widget.attrs["placeholder"] = "About the Room"


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "username", "email", "bio"]
