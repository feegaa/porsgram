from django import forms
from user.models import UserModel, AvatarModel

class UserForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('female', 'مونث'),
        ('male', 'مذکر'),
        ('none', 'به تو چه'),
    )


    first_name = forms.CharField(label='Your name', max_length=30, required=True)
    last_name  = forms.CharField(label='last anme', max_length=30, required=True)
    username   = forms.CharField(label='useranme', max_length=30, required=False)
    email      = forms.EmailField(label_suffix='email', required=True)
    password   = forms.PasswordInput()
    gender     = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']


    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('please inter 10 digits...')
        return password


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            counter = UserModel.objects.all().count()
            return 'user'+str(counter)
        return username

class UserUpdateForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['password'].disabled = True


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model  = AvatarModel
        fields = ['avatar']



