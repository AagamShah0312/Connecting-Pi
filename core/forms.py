from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ChatMessage, HireRequest, Skill, User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=User.Role.choices, widget=forms.RadioSelect)
    degree = forms.CharField(max_length=160, required=False)
    business_name = forms.CharField(max_length=160, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "role", "degree", "business_name", "password1", "password2")


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ("name", "category", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class HireRequestForm(forms.ModelForm):
    class Meta:
        model = HireRequest
        fields = ("message",)
        widgets = {"message": forms.Textarea(attrs={"rows": 5, "placeholder": "Tell the provider what you want to learn..."})}


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ("body",)
        labels = {"body": "Message"}
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Discuss the scope, timing, and a fair price..."})}
