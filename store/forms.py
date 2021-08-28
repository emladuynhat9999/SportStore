from django import forms
from django.forms import fields
from django.forms.widgets import Textarea
from . import models


class FormSearch(forms.ModelForm):
    name = forms.CharField()
    name_no_bind = forms.CharField()
    subcategory_id = forms.IntegerField()

    class Meta:
        model = models.Product
        fields = ('name', 'subcategory_id', 'name_no_bind')


class FormCustumer(forms.ModelForm):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput())
    password = forms.CharField(
        max_length=150, widget=forms.PasswordInput())
    confirm = forms.CharField(
        max_length=150, label='confirm', widget=forms.PasswordInput())
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput())
    last_name = forms.CharField(
        max_length=150, widget=forms.TextInput())
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
                            'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))', 'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    email = forms.EmailField(widget=forms.TextInput())
    address = forms.CharField(
        max_length=500, widget=forms.TextInput())

    class Meta:
        model = models.Customer
        fields = '__all__'


class UserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=150, label='Password', widget=forms.PasswordInput())
    confirm = forms.CharField(
        max_length=150, label='Confirm', widget=forms.PasswordInput())

    class Meta():
        model = models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileInfoForm(forms.ModelForm):
    address = forms.CharField(max_length=500, widget=forms.TextInput())
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    image = forms.ImageField(required=False)

    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', )


class ContactForm(forms.ModelForm):
    fullname = forms.CharField(max_length=250, widget=forms.TextInput())
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
                            'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))', 'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    email = forms.EmailField(widget=forms.TextInput())
    subject = forms.CharField(max_length=250, widget=forms.TextInput())
    content = forms.CharField(max_length=500, widget=Textarea())

    class Meta():
        model = models.Contact
        fields = '__all__'
