from django import forms


class UserForm(forms.Form):
    source = forms.CharField(required=True, label="Книга/фильм")
    text = forms.CharField(required=True, label="Цитата", widget=forms.Textarea)
    weight = forms.IntegerField(required=True, min_value=1, label="Вес цитаты")