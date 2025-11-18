from django.contrib.auth.forms import UserCreationForm
from .models import User






class InstructorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name"]
