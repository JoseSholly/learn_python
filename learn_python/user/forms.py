from django import forms

class CustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name", required=True)
    last_name = forms.CharField(max_length=30, label="Last name", required=True)

    def signup(self, request, user):
        """
        Called by django-allauth after the user object is created.
        Attach extra fields to the user and save them.
        """
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.save()
        return user
