from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    def post_login(self, request, user, **kwargs):
        """
        Called just before the login process.
        Here we can block unverified users and redirect them.
        """
        if user and not user.is_verified:
            return redirect("user:account_not_verified")  # 👈 works here!
        return super().post_login(request, user, **kwargs)

        pass