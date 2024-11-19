from django import forms
from contact.models import ContactForm, FAQs
from .models import SuggestionBox, Review


class SuggestionBoxForm(forms.ModelForm):
	class Meta:
		model = SuggestionBox
		fields = ['full_name','email','message']

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['title', 'message','rating']

class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactForm
		fields = '__all__'


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=[('USD', 'USD'),('XAF', 'XAF'), ('EUR', 'EUR')])  # Add more currencies as needed
    email = forms.EmailField()