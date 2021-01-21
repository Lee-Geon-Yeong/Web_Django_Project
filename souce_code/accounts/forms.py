from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from allauth.account.forms import SignupForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from .models import Account

SEX_CHOICES = ((0, 'female'), (1, 'male'))

class SocialUserUpdateForm(forms.ModelForm):
    age = forms.IntegerField(max_value=130, min_value=18, required=True)
    sex = forms.ChoiceField(choices=SEX_CHOICES,required=True)
    class Meta:
        model = get_user_model()
        fields = ['sex', 'age']


class UserChangeForm_2(UserChangeForm):
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    age = forms.IntegerField(max_value=130)


class UserCreationForm_2(UserCreationForm):
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    age = forms.IntegerField(max_value=130, required=True)



class CustomSignupForm(SignupForm):
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=True)
    age = forms.IntegerField(max_value=120, min_value=18, required=True)

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        user.age = self.cleaned_data['age']
        user.sex = self.cleaned_data['sex']
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
