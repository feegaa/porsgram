from django import forms
from user.models import UserModel, AvatarModel
from ckeditor.fields import RichTextFormField

class UserForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('female', 'مونث'),
        ('male', 'مذکر'),
        ('none', 'به تو چه'),
    )

    first_name = forms.CharField(label='نام', max_length=30, required=True)
    last_name  = forms.CharField(label='نام خانوادگی', max_length=30, required=True)
    username   = forms.CharField(label='نام کاربری', max_length=30, required=False)
    email      = forms.EmailField(label='ایمیل', required=True)
    password   = forms.PasswordInput()
    gender     = forms.ChoiceField(choices=STATUS_CHOICES, label="جنسیت", widget=forms.RadioSelect)
    

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']


    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError('حداقل ۸ کاراکتر لازمه...')

        # check for digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(('حداقل ۱ عدد باید داشته باشه...'))

        # check for letter
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError(('...حداقل ۱ حرف باید داشته باشه'))

        return password


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            counter = UserModel.objects.all().count()
            return 'user'+str(counter)
        return username

class UserUpdateForm(UserForm):
    about_me = RichTextFormField(max_length=700)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        # self.fields.pop('password')

    class Meta(UserForm.Meta):
        fields = ['about_me', 'first_name', 'last_name', 'username', 'email', 'gender']

class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model  = AvatarModel
        fields = ['avatar']


class ResetPasswordForm(forms.Form):
    password       = forms.CharField(widget=forms.PasswordInput())
    password_check = forms.CharField(widget=forms.PasswordInput())


    def clean(self):
        cleaned_data   = super().clean()
        password       = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if len(password) < 8:
            raise forms.ValidationError('حداقل ۸ کاراکتر لازمه...')


        if password != password_check:
            raise forms.ValidationError('گذرواژه ها با هم همخوان نیست...')


        # check for digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(('حداقل ۱ عدد باید داشته باشه...'))

        # check for letter
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError(('...حداقل ۱ حرف باید داشته باشه'))

        return password

        


class GetEmailForm(forms.Form):
    email = forms.EmailField(required=True)