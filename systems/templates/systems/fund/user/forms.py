

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['language',]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email_address', 'first_name', 'last_name']
