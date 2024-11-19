from django import forms
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone
from .models import Passenger



class CustomSignupForm(SignupForm):
    IDENTITY_DOC_CHOICES = [
        ('National Identity Card', 'National Identity Card'),
        ('Passport', 'Passport'),
        ('Resident Card', 'Resident Card'),
    ]

    phone = forms.CharField(max_length=15, required=False)
    identity_document = forms.ChoiceField(choices=IDENTITY_DOC_CHOICES, required=True)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    part_no = forms.CharField(max_length=30, required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Passenger
        fields = [ 'email', 'password1', 'password2', 'phone', 'identity_document', 'dob', 'part_no', 'profile_pic']

    def save(self, request):
        user = super().save(request)
        user.phone = self.cleaned_data['phone']
        user.identity_document = self.cleaned_data['identity_document']
        user.dob = self.cleaned_data['dob']
        user.part_no = self.cleaned_data['part_no']
        user.profile_pic = self.cleaned_data['profile_pic']
        user.save()
        return user



class CustomSignupUpdateForm(forms.ModelForm):
    IDENTITY_DOC_CHOICES = [
        ('National Identity Card', 'National Identity Card'),
        ('Passport', 'Passport'),
        ('Resident Card', 'Resident Card'),
    ]

    phone = forms.CharField(max_length=15, required=False)
    identity_document = forms.ChoiceField(choices=IDENTITY_DOC_CHOICES, required=True)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    part_no = forms.CharField(max_length=30, required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Passenger
        fields = [ 'first_name','last_name','email', 'phone', 'identity_document', 'dob', 'part_no', 'profile_pic']

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob is None:
            raise forms.ValidationError("Date of birth is required.")
        return dob

    def clean_part_no(self):
        part_no = self.cleaned_data.get('part_no')
        if not part_no:
            raise forms.ValidationError("Part number is required.")
        return part_no