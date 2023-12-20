from django import forms
from main.models import Comment, Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class SubscriptionForm(forms.ModelForm):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    email = forms.EmailField()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']