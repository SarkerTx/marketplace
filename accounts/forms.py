from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, VendorProfile

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.CUSTOMER
        if commit:
            user.save()
        return user

class VendorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    store_name = forms.CharField(max_length=255)
    store_description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.VENDOR
        if commit:
            user.save()
            VendorProfile.objects.create(
                user=user,
                store_name=self.cleaned_data['store_name'],
                store_description=self.cleaned_data['store_description']
            )
        return user