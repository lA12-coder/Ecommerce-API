from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class UserCreationForm(forms.ModelForm):  
    """A form for creating new users in the admin. Includes repeated password fields."""  
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)  
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)  
  
    class Meta:  
        model = User    
        fields = ("email", "first_name", "last_name")  
  
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_password2(self):  
        p1 = self.cleaned_data.get("password1")  
        p2 = self.cleaned_data.get("password2")  
        if p1 and p2 and p1 != p2:  
            raise forms.ValidationError("Passwords don't match")  
        return p2  
  
    def save(self, commit=True):  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data["password1"])  
        if commit:  
            user.save()  
        return user  
    
class UserChangeForm(forms.ModelForm):  
    """A form for updating users. Shows password as read-only hash."""  
    password = ReadOnlyPasswordHashField()  
  
    class Meta:  
        model = User  
        fields = ("email", "password", "first_name", "last_name", "is_active", "is_staff", 'is_superuser', 'role')
        
    