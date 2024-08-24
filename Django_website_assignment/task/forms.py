from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Questionnaire, Question

# Form for creating or updating a Question instance
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'option_1', 'option_2', 'option_3', 'option_4', 'option_5', 'answer']

# Formset for managing multiple Question forms
QuestionFormSet = forms.modelformset_factory(
    Question, form=QuestionForm, extra=1, can_delete=True
)

# Form for creating or updating a Questionnaire instance
class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['title']

# Custom form for user registration that includes an email field
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Custom form for user login with username and password fields
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=250)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
