from django import forms


class ContentForm(forms.Form):
    subject = forms.CharField(label='subject', max_length=30)
    content = forms.CharField(label='content')
    email = forms.CharField(label='email')

class CommentForm(forms.Form):

    comment= forms.CharField(label='comment')
    idx1 = forms.CharField(label='idx1')

class LoginForm(forms.Form):
    id = forms.CharField(label='id', max_length=20)
    pw = forms.CharField(label='pw', max_length=20)