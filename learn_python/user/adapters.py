from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied


class CustomAccountAdapter(DefaultAccountAdapter):
    def authenticate(self, request, **credentials):
        """
        Override authenticate to block unverified users from logging in
        """
        user = super().authenticate(request, **credentials)
        if user and not user.is_verified:
            raise PermissionDenied("Please verify your email before logging in.")
        return user