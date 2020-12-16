from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class OrderForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите Ваше имя'}))
    phone_number = forms.CharField(max_length=16, label='НОМЕР ТЕЛЕФОНА', widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона в международном формате'}))
    email = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Ввведите Email'}))
    post_code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'placeholder': 'Введите свой почтовый индекс'}), required=False)
    city = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Введите свой город'}), required=False)
    street = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Введите вашу улицу'}), required=False)
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Дополнительная информация'}), required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class SubscribeForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True)