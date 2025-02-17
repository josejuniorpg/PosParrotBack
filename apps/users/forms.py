from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Custom User Creation Form"""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'profile_image')


class CustomUserChangeForm(UserChangeForm):
    """Custom User Change Form"""

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'profile_image')
