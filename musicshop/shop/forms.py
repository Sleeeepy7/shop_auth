from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе')
        if not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['address'].label = 'Адрес'
        self.fields['email'].label = 'Почта'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net', 'xyu']:
            raise forms.ValidationError(f'Регистрация для домена {domain} невозможна')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Данный почтовый адресс уже зарегистрирован')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Имя {username} уже занято. Попробуйте другое')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']



