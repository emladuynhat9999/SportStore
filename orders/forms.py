from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    class Meta:
        model = Order
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone']