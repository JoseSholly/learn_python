from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(email_confirmed)
def update_user_verified_status(request, email_address, **kwargs):
    """
    When a user confirms their email via allauth, update is_verified=True
    """
    try:
        user = User.objects.get(email=email_address.email)
        user.is_verified = True
        user.save()
    except User.DoesNotExist:
        pass
